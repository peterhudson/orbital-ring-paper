"""The numbers behind the explanatory figures, and the numbers quoted beside them."""
import math
import unittest

import numpy as np

from analysis.params import EARTH_500
from analysis.plots import cable_and_arch, control_bands, crossover_angle, fault_energy, slug_mass_trade, speed_ramp, unrolled_helix


class Base(unittest.TestCase):
    def about(self, value, expected, rel=0.02):
        self.assertLess(abs(value - expected), rel * abs(expected), f"{value} is not within {rel:.0%} of {expected}")


class CableAndArch(Base):
    def test_uniform_load_gives_a_parabola(self):
        s, y = cable_and_arch.shape(0.0)
        self.about(y.min(), -1.0 / 8.0, 0.01)                  # q L^2 / 8 T
        self.assertAlmostEqual(y[0], 0.0)
        self.assertAlmostEqual(y[-1], 0.0)

    def test_extra_weight_deepens_the_cable_most_where_it_is_added(self):
        s, base = cable_and_arch.shape(0.0)
        _, loaded = cable_and_arch.shape(cable_and_arch.EXTRA_SIZE)
        change = loaded - base
        self.assertTrue((change[1:-1] < 0.0).all())
        self.about(s[np.argmin(change)], 0.5, 0.01)


class Helix(Base):
    def test_numbers_quoted_in_the_helical_shell_chapter(self):
        num = unrolled_helix.helix_numbers()
        self.about(num["alpha_deg"], 0.79, 0.01)
        self.about(num["pitch_km"], 23.0, 0.02)
        self.about(num["girth"], 314.0, 0.005)
        self.about(num["v_round"], 139.0, 0.005)
        self.about(num["accel"], 384.0, 0.005)
        self.about(num["accel"] / 9.80665, 39.0, 0.01)
        self.about(num["load"], 2100.0, 0.01)

    def test_lane_table_matches_the_four_lane_chapter(self):
        # lane: (right-handed, travels toward +s); theta-momentum is positive when the two agree
        theta = {lane: (right == forward) for lane, (right, forward) in unrolled_helix.LANES.items()}
        self.assertEqual(theta, {1: True, 2: False, 3: False, 4: True})

    def test_wrap_evens_out_path_length_and_lift_ripple_is_small(self):
        case = EARTH_500
        self.about(2.0 * math.pi * 2.0 * case.a, 628.0, 0.002)
        lift_per_lane = case.w_p / 300.0
        self.about(lift_per_lane, 33.0, 0.02)
        self.about(lift_per_lane / case.normal_load_lane, 0.016, 0.02)


class CrossoverAngle(Base):
    def test_values_quoted_in_the_text(self):
        gammas, data = crossover_angle.curves(gammas=np.array([10.0, 30.0, 100.0]))
        alpha, pitch = data[10.0e3]
        for got, want in zip(alpha, (0.79, 1.38, 2.51)):
            self.about(got, want, 0.01)
        for got, want in zip(pitch, (23.0, 13.0, 7.0)):
            self.about(got, want, 0.04)

    def test_faster_streams_allow_a_steeper_helix(self):
        gammas, data = crossover_angle.curves(gammas=np.array([10.0]))
        angles = [data[u][0][0] for u in crossover_angle.SPEEDS]
        self.assertEqual(angles, sorted(angles))


class SpeedRamp(Base):
    def test_spacing_is_proportional_to_speed(self):
        s = speed_ramp.slug_positions()
        gaps = np.diff(s)
        mid = 0.5 * (s[1:] + s[:-1])
        slow = gaps[mid < speed_ramp.RAMP_A[0] - 0.02].mean()
        fast = gaps[(mid > speed_ramp.RAMP_A[1] + 0.02) & (mid < speed_ramp.RAMP_B[0] - 0.02)].mean()
        self.about(fast / slow, speed_ramp.FAST / speed_ramp.SLOW, 0.01)

    def test_speed_returns_to_where_it_started(self):
        self.assertEqual(float(speed_ramp.speed(0.0)), float(speed_ramp.speed(1.0)))


class ControlBands(Base):
    def test_growth_times_on_the_top_scale(self):
        times = control_bands.growth_times([1e3, 1e5, 1e6])
        self.about(times[0], 0.021, 0.02)
        self.about(times[1], 2.1, 0.02)
        self.about(times[2], 21.0, 0.02)

    def test_bands_cover_every_wavelength_from_a_metre_to_the_ring(self):
        rows = [r for r in control_bands.bands() if r[3] != "open"]
        reach = control_bands.SHORT
        for _, lo, hi, _ in sorted(rows, key=lambda r: r[1]):
            self.assertLessEqual(lo, reach * 1.0001)
            reach = max(reach, hi)
        self.about(reach, EARTH_500.circumference, 1e-6)


class SlugMass(Base):
    def test_reference_slug(self):
        masses, headway, energy = slug_mass_trade.curves(masses=np.array([0.1, 10.0, 100.0]))
        self.about(headway[1], 0.185e-3, 0.01)
        self.about(energy[1], 0.5e9, 0.01)
        self.about(headway[0], 1.8e-6, 0.03)
        self.about(energy[2], 5.0e9, 0.01)


class FaultEnergy(Base):
    def test_ladder_values(self):
        rows = {label: joules for label, joules, _ in fault_energy.ladder()}
        self.about(rows["One 10 kg slug"], 0.5e9, 0.01)
        self.about(rows["One lane for 10 ms"], 27e9, 0.02)
        self.about(rows["One metre of ring, all streams"], 82e9, 0.01)
        self.about(rows["One kilometre of ring"], 82e12, 0.01)
        self.about(rows["The whole ring"], 3.5e18, 0.02)
        self.about(rows["The whole ring"] / (1e6 * fault_energy.TNT_TONNE), 840.0, 0.02)

    def test_ladder_is_in_order(self):
        joules = [r[1] for r in fault_energy.ladder()]
        self.assertEqual(joules, sorted(joules))


if __name__ == "__main__":
    unittest.main()
