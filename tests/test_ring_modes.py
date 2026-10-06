"""Whole-ring modes with the streams as separate fields: the linear model
against closed forms, the truss model and the particle simulation, and the
numbers quoted in the effective-tension chapter."""
import math
import unittest

import numpy as np

from analysis import ring
from analysis.params import EARTH_500 as C
from analysis.ring_modes import FOLLOW, GuideLaw, RingModes, coasting_growth_rate, held_speed_growth_rate, out_of_plane_rate
from analysis.ring_particles import RingParticleSim, measured_growth_rate

OM = C.omega_orb
STIFF = RingModes(ea=5e14)
SOFT = RingModes(ea=5e10)
HELD = GuideLaw(speed_rate=1e4 * OM, reference="speed")


class Base(unittest.TestCase):
    def about(self, value, quoted, rel=0.03):
        self.assertTrue(math.isclose(value, quoted, rel_tol=rel), f"computed {value:.6g}, expected {quoted:.6g} (tolerance {rel:.1%})")


class OpenLoopGrowth(Base):
    def test_held_speed_matches_the_closed_form_and_the_truss(self):
        truss, x0 = ring.ring_truss(n_nodes=360, ea=5e14)
        from_truss = ring.growth_rates_by_mode(truss, x0, "in")
        for n in (1, 2, 3, 4, 6):
            closed = held_speed_growth_rate(n)
            self.about(STIFF.growth_rate(n, HELD), closed, 2e-3)
            self.about(math.sqrt(from_truss[n]), closed, 2e-3)
            self.about(closed, ring.growth_rate_in_plane(n), 1e-12)

    def test_coasting_matches_the_cubic(self):
        for n in (1, 2, 3, 4, 6, 10, 30):
            self.about(STIFF.growth_rate(n), coasting_growth_rate(n), 1e-4)

    def test_coasting_is_slower_than_held_speed(self):
        for n in (1, 2, 3, 10, 100):
            self.assertLess(coasting_growth_rate(n), held_speed_growth_rate(n))
        offset = lambda rate, n: (rate / OM) ** 2 - n * n
        self.about(offset(coasting_growth_rate(1000), 1000), -1.2, 0.03)
        self.about(offset(held_speed_growth_rate(1000), 1000), -1.0, 1e-3)

    def test_breathing_mode(self):
        """Uniform growth or shrinkage: stable if the slugs coast, not if their speed is held."""
        vals = SOFT.eigenvalues(0)
        self.assertLess(vals[0].real / OM, 1e-9)
        self.about(max(abs(z.imag) for z in vals) / OM, 1.14, 0.01)
        self.about(2 * math.pi / (1.1426 * OM) / 60, 83, 0.01)             # period, minutes
        self.assertGreater(SOFT.growth_rate(0, HELD) / OM, 0.5)

    def test_quoted_rates_and_times(self):
        minutes = lambda rate: 1.0 / rate / 60.0
        for n, rate, time in [(1, 0.0010, 17), (2, 0.0022, 7.7), (3, 0.0033, 5.1)]:
            self.about(SOFT.growth_rate(n), rate, 0.03)
            self.about(minutes(SOFT.growth_rate(n)), time, 0.02)
        self.about(minutes(coasting_growth_rate(1)), 26, 0.02)
        table = {
            "coast, 50 GN": ([SOFT.growth_rate(n) for n in (1, 2, 3, 4)], [0.90, 1.94, 2.96, 3.97]),
            "coast, stiff": ([coasting_growth_rate(n) for n in (1, 2, 3, 4)], [0.57, 1.72, 2.81, 3.85]),
            "held, stiff": ([held_speed_growth_rate(n) for n in (1, 2, 3, 4)], [0.71, 1.79, 2.85, 3.88]),
            "out of plane": ([out_of_plane_rate(n).real for n in (2, 3, 4)], [1.73, 2.83, 3.87]),
        }
        for rates, quoted in table.values():
            for rate, value in zip(rates, quoted):
                self.about(rate / OM, value, 0.01)
        self.about(minutes(held_speed_growth_rate(1)), 21, 0.02)
        self.about(SOFT.hoop, 0.73, 0.01)
        self.about(2 * math.pi * C.R / C.u / 60, 72, 0.01)                 # one circuit of the stream, minutes

    def test_out_of_plane(self):
        self.assertEqual(out_of_plane_rate(1), 0)
        for n in (2, 3, 5):
            self.about(out_of_plane_rate(n).real, ring.growth_rate_out_of_plane(n), 1e-12)
            self.assertEqual(out_of_plane_rate(n, mirror=0.3).real, 0.0)

    def test_plant_with_a_stiff_guide_matches_ideal_tracking(self):
        for law in (FOLLOW, GuideLaw(mirror=0.4, lead=0.3, speed_rate=OM, lock_rate=OM**2)):
            for n in (2, 3, 5):
                K = SOFT.tracking_gain(n, law, bandwidth=3000.0)
                self.about(SOFT.closed_loop_eigenvalues(n, K)[0].real, SOFT.eigenvalues(n, law)[0].real, 1e-3)


class ParticleSimulation(Base):
    def test_round_ring_stays_put(self):
        sim = RingParticleSim()
        for _ in range(200):
            sim.step()
        self.assertLess(np.abs(sim.structure_fields()[0]).max(), 1e-6)
        self.assertLess(np.abs(sim.gap()).max(), 1e-6)

    def test_growth_rate_matches_the_linear_model(self):
        """Three waves round the ring, coasting slugs, hoop stiffness 50 GN."""
        self.about(measured_growth_rate(3, dt=0.25), SOFT.growth_rate(3), 5e-3)


if __name__ == "__main__":
    unittest.main()
