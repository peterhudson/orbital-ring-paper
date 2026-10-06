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


if __name__ == "__main__":
    unittest.main()
