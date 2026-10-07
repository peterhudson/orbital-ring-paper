"""The closure loop as a number: figures quoted in the closure-screens chapter."""
import math
import unittest

from analysis import closure
from analysis.params import EARTH_500 as C


class Base(unittest.TestCase):
    def about(self, value, expected, rel=0.02):
        self.assertLess(abs(value - expected), rel * abs(expected), f"{value} is not within {rel:.0%} of {expected}")


class GuideForce(Base):
    def test_helix_prestress_is_paid_for_in_guide_force(self):
        self.about(closure.guide_force_ratio(10.0), 64.0, 0.01)
        self.about(closure.guide_force(), 638e3, 0.005)
        # the helix's normal load, lane by lane, is the 2 pi Gamma part
        self.about(C.n_lanes * C.normal_load_lane, 2.0 * math.pi * C.gamma * C.w_p, 1e-3)
        self.about(C.n_lanes * C.normal_load_lane, 2.0 * math.pi * C.N_theta, 1e-3)


class Loop(Base):
    def test_table(self):
        rows = {1e4: (640e3, 31e12, 4.5, math.inf), 1e5: (64e3, 3.1e12, 0.69, 3.2), 1e6: (6.4e3, 310e9, 0.31, 1.5), 1e7: (0.64e3, 31e9, 0.27, 1.4)}
        for ratio, (heat, power, gain, multiplier) in rows.items():
            a = closure.REFERENCE.with_(lift_to_drag=ratio)
            self.about(closure.drag_power(C, ratio), heat, 0.01)
            self.about(closure.ring_power(C, a), power, 0.02)
            self.about(closure.loop_gain(C, a), gain, 0.02)
            if math.isinf(multiplier):
                self.assertTrue(math.isinf(closure.mass_multiplier(C, a)))
            else:
                self.about(closure.mass_multiplier(C, a), multiplier, 0.04)

    def test_gain_is_a_geometric_series(self):
        a = closure.REFERENCE
        gain = closure.loop_gain(C, a)
        total, added = 1.0, 1.0
        for _ in range(200):
            added *= gain
            total += added
        self.about(total, closure.mass_multiplier(C, a), 1e-9)
        self.about(1.0 / (1.0 - 0.5), 2.0, 1e-12)
        self.about(1.0 / (1.0 - 0.9), 10.0, 1e-9)

    def test_where_the_loop_closes(self):
        self.about(closure.lift_to_drag_needed(1.0), 60e3, 0.05)
        self.about(closure.lift_to_drag_needed(0.5), 180e3, 0.02)
        self.assertGreater(closure.ring_power(C, closure.REFERENCE.with_(lift_to_drag=180e3)), 1.0e12)
        # without the helix
        self.assertLess(closure.lift_to_drag_needed(1.0, gamma=0.0), 1000.0)
        self.about(closure.lift_to_drag_needed(0.5, gamma=0.0), 1300.0, 0.03)
        self.about(closure.ring_power(C, closure.REFERENCE, gamma=0.0), 48e9, 0.01)

    def test_floor_is_the_guides_own_weight(self):
        floor = closure.guide_force_ratio(10.0) * C.g_h / closure.REFERENCE.guide_specific_force
        self.about(floor, 0.27, 0.01)
        self.about(closure.loop_gain(C, closure.REFERENCE.with_(lift_to_drag=1e12)), floor, 1e-6)
        self.about(closure.gain_terms(gamma=30.0)["guide"], 0.8, 0.01)

    def test_every_unit_of_prestress_adds_two_pi_of_guide_force(self):
        self.about(closure.guide_force_ratio(11.0) - closure.guide_force_ratio(10.0), 2.0 * math.pi, 1e-12)
        # with drag dominant the gain is proportional to phi
        a = closure.REFERENCE.with_(lift_to_drag=1e3)
        self.about(closure.loop_gain(C, a, 10.0) / closure.loop_gain(C, a, 0.0), 63.8, 0.01)


if __name__ == "__main__":
    unittest.main()
