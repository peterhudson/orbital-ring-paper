"""Unequal streams: the table in the shape-control chapter."""
import unittest

from analysis import ring_balance as rb
from analysis.params import EARTH_500 as C
from analysis.ring_modes import RingModes

SAMPLE = [2, 3, 5, 10, 20, 22, 23, 26, 27, 50, 76, 77, 100, 148, 149, 170]
STEERED = [2, 3, 5, 10, 20, 21, 50, 100, 157, 300, 1000, 10000, 30000]


class Model(unittest.TestCase):
    def test_unequal_streams_still_carry_the_structure(self):
        for kw in (dict(flux_imbalance=0.1), dict(speed_imbalance=0.05), dict(flux_imbalance=0.03, speed_imbalance=-0.02)):
            lift = sum(l * (v * v - 1.0) for l, v in RingModes(**kw)._streams())
            self.assertAlmostEqual(lift, 1.0, places=12)

    def test_turning_with_the_earth_is_five_percent_in_speed(self):
        self.assertAlmostEqual(C.U_g / C.u, 0.05, delta=0.002)

    def test_open_loop_growth_hardly_changes(self):
        base = RingModes()
        for kw in (dict(flux_imbalance=0.05), dict(speed_imbalance=0.05)):
            for n in (1, 2, 3, 10):
                self.assertAlmostEqual(RingModes(**kw).growth_rate(n) / base.growth_rate(n), 1.0, delta=0.004)


class Table(unittest.TestCase):
    def first(self, modes):
        return modes[0] if modes else None

    def test_steered_modes(self):
        for kw in (dict(flux=0.003), dict(flux=0.01), dict(flux=0.1), dict(speed=0.003), dict(speed=0.01), dict(speed=0.04)):
            self.assertEqual(rb.steered_unstable(modes=STEERED, **kw), [])
        self.assertEqual(self.first(rb.steered_unstable(speed=0.05, modes=STEERED)), 21)
        # the mirror law itself still holds, and slower set points do too
        self.assertEqual(rb.steered_unstable(speed=0.05, adapt=0.0, modes=STEERED), [])
        self.assertEqual(rb.steered_unstable(speed=0.05, adapt=0.02, modes=STEERED), [])
        self.assertEqual(rb.steered_unstable(flux=0.1, adapt=0.0, modes=STEERED), [])

    def test_set_point_drift_takes_hours(self):
        from analysis import ring_control as rc
        model = RingModes(speed_imbalance=0.05)
        law = rc.reference_law(model)
        worst = max(rc.slowest_rate(model, rc.closed_loop(model, n, law, adapt=rc.ADAPT)) for n in STEERED)
        self.assertTrue(2.0 < 1.0 / worst / 3600.0 < 10.0)

    def test_stator_held_modes_with_feedback_designed_for_equal_streams(self):
        expect = {("flux", 0.003): None, ("flux", 0.01): 149, ("flux", 0.1): 27, ("speed", 0.003): None, ("speed", 0.01): 77, ("speed", 0.04): 27, ("speed", 0.05): 23}
        for (kind, value), first in expect.items():
            self.assertEqual(self.first(rb.stator_held_unstable(modes=SAMPLE, **{kind: value})), first, (kind, value))

    def test_stator_held_modes_with_feedback_designed_for_the_imbalance(self):
        for kw in (dict(flux=0.01), dict(flux=0.1), dict(speed=0.01), dict(speed=0.05)):
            self.assertEqual(rb.stator_held_unstable(redesign=True, modes=SAMPLE, **kw), [])

    def test_off_center_controller_is_indifferent(self):
        base = rb.off_centre_rate()
        for kw in (dict(flux=0.1), dict(speed=0.05), dict(flux=0.01), dict(speed=0.01)):
            self.assertLess(abs(rb.off_centre_rate(**kw) / base - 1.0), 0.1)


if __name__ == "__main__":
    unittest.main()
