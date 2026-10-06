"""Longer simulation runs behind numbers quoted in the text. Skipped unless
RUN_SLOW=1 is set:  RUN_SLOW=1 python -m unittest tests.test_slow"""
import math
import os
import unittest

import numpy as np
from scipy.linalg import expm

from analysis import ring_control as rc
from analysis.params import EARTH_500 as C
from analysis.ring_modes import RingModes
from analysis.ring_particles import RingParticleSim, measured_growth_rate

MODEL = RingModes()
OM = MODEL.omega
LAW = rc.reference_law(MODEL)
SIM = dict(guide_bandwidth=0.5, filter_bandwidth=1.5)


@unittest.skipUnless(os.environ.get("RUN_SLOW"), "set RUN_SLOW=1 to run")
class SlowRuns(unittest.TestCase):
    def test_open_loop_growth_of_the_first_two_modes(self):
        for n in (1, 2):
            self.assertTrue(math.isclose(measured_growth_rate(n, dt=0.25), MODEL.growth_rate(n), rel_tol=2e-3))

    def test_thirty_modes_at_once(self):
        """Every mode from 1 to 30 displaced at random by 1 to 2 mm, on a
        mesh of 960 masses and 9,600 slugs each way."""
        top = 30
        _, _, K1 = rc.off_centre_controller(MODEL, LAW)
        sim = RingParticleSim(n_nodes=32 * top, slugs_per_direction=160 * top, n_keep=top, law=LAW, feedback={1: K1}, dt=0.25, **SIM)
        rng = np.random.default_rng(1)
        modes = range(1, top + 1)
        for n in modes:
            sim.perturb(n, 0.002 * rng.uniform(0.5, 1.0), phase=rng.uniform(0.0, 2.0 * math.pi))
        start = {n: sim.full_state(n) for n in modes}
        t, a, gaps, _ = sim.run(3600.0, record=tuple(modes), every=240)
        rms = lambda row: math.sqrt(0.5 * (np.abs(row) ** 2).sum())
        self.assertTrue(math.isclose(rms(a[0]), 2.9e-3, rel_tol=0.05))
        self.assertTrue(math.isclose(rms(a[-1]), 0.12e-3, rel_tol=0.1))
        self.assertLess(gaps.max(), 0.0095)
        worst = 0.0
        for i, n in enumerate(modes):
            matrix = rc.closed_loop(MODEL, n, LAW, extra=K1 if n == 1 else None, **SIM)
            predicted = np.array([(expm(matrix * ti * OM) @ start[n][:matrix.shape[0]])[0] for ti in t]) * C.R
            worst = max(worst, np.abs(a[:, i] - predicted).max() / np.abs(predicted).max())
        self.assertLess(worst, 0.035)
        self.assertTrue(math.isclose(2 * math.pi * C.R / top, 1.44e6, rel_tol=0.01))

    def test_slug_spacing_table(self):
        """Appendix C: decay rate under the mirror law against slug spacing, on a 10 m mesh."""
        from analysis.collective import CollectiveModel
        from analysis.particles import LocalParticleSim, envelope_rate

        model = CollectiveModel.mirror_reference(f_filter=200.0, preview=30.0)

        def rate(slugs, mode):
            sim = LocalParticleSim(model, length=5e3, n_nodes=500, slugs_per_direction=slugs, dt=5e-5)
            sim.y += 1e-3 * np.cos(2 * math.pi * mode * sim.s_nodes / 5e3)
            t, a = sim.run(1.0, record_modes=(mode,), every=20)
            return envelope_rate(t, a[:, 0])

        table = {12: (1.00, 0.97, 0.34, 0.24, 0.22), 4: (0.97, 0.93, 0.45, 0.18, 0.24), 2: (1.00, 1.00, 1.05, 0.51, 0.35), 1: (1.00, 1.00, 1.00, 1.04, 1.15)}
        for mode, row in table.items():
            fine = rate(500, mode)
            for spacing, want in zip((20.0, 31.25, 50.0, 250.0 / 3.0, 125.0), row):
                self.assertLess(abs(rate(int(round(5e3 / spacing)), mode) / fine - want), 0.03, (mode, spacing))

    def test_two_hours_under_a_sudden_load_with_the_stators_holding_three_modes(self):
        """The run drawn in the stator-held-load figure."""
        from analysis.plots import stator_held_load
        _, data = stator_held_load.run()
        sim, lin = data["sim"], data["linear"]
        self.assertLess(np.abs(sim[:, 0] - lin[:, 0]).max(), 0.005 * np.abs(lin[:, 0]).max())
        self.assertLess(np.abs(sim[:, 2] - lin[:, 2]).max(), 0.005 * np.abs(lin[:, 2]).max())
        self.assertLess(sim[:, 1].max(), 3.0e-6)
        self.assertTrue(math.isclose(sim[-1, 0], 1.9e-3, rel_tol=0.03))
        self.assertTrue(math.isclose(sim[-1, 2], 0.04e-3, rel_tol=0.03))


if __name__ == "__main__":
    unittest.main()
