"""Numbers quoted in the chapter on structures other than the orbital ring."""
import math
import unittest

from analysis import generalize as gen
from analysis.collective import CollectiveModel, MIRROR_GAIN
from analysis.params import EARTH_500, MOON_20
from analysis.plots import speed_ratio
from analysis.ring_modes import RingModes


class Base(unittest.TestCase):
    def about(self, value, expected, rel=0.02):
        self.assertLess(abs(value - expected), rel * abs(expected), f"{value} is not within {rel:.0%} of {expected}")


class ArchResults(Base):
    def test_ring_is_an_arch_with_no_ends(self):
        c = EARTH_500
        total = c.m_passive + c.lam_stream
        self.about(gen.arch_thrust(total, c.g_h, c.R), c.Pi_total, 1e-6)
        self.about(gen.threshold_speed(c.g_h, c.R), c.u_orb, 1e-9)

    def test_stream_mass_and_energy_follow_from_the_speed_ratio(self):
        c = EARTH_500
        nu = c.u / c.u_orb
        self.about(nu, 1.31, 0.005)
        self.about(gen.stream_per_passive(nu), c.lam_stream / c.m_passive, 1e-6)
        floor = gen.energy_floor(c.m_passive, c.g_h, c.R)
        self.about(floor, 34e9, 0.02)
        self.about(c.E_prime / floor, gen.energy_over_floor(nu), 1e-6)
        self.about(gen.energy_over_floor(nu), 2.4, 0.01)

    def test_growth_speed_is_the_threshold_speed_whatever_the_design(self):
        c = EARTH_500
        model = CollectiveModel.reference(c)
        k = 2.0 * math.pi / 1.0e5
        self.about(model.rigid_growth_rate(k), k * gen.growth_speed(c.g_h, c.R), 1e-3)
        self.about(c.u_orb / c.u, 0.76, 0.005)
        # a faster, thinner stream carrying the same weight grows at the same rate
        fast = c.with_(u=14.0e3)
        self.about(CollectiveModel.reference(fast).rigid_growth_rate(k), model.rigid_growth_rate(k), 1e-3)

    def test_steering_gain_limit(self):
        c = EARTH_500
        nu = c.u / c.u_orb
        self.about(gen.steering_gain_limit(nu), c.m_passive / c.lam_stream, 1e-6)
        self.about(gen.least_speed_ratio_for_gain(MIRROR_GAIN), 1.22, 0.005)

    def test_arch_at_the_launch_loop_speed_and_height(self):
        row = gen.arch_row(gen.LAUNCH_LOOP_LIKE)
        self.about(row["threshold"], 7.9e3, 0.01)
        self.about(row["speed_ratio"], 1.78, 0.005)
        self.about(row["passive_per_stream"], 2.2, 0.02)
        self.about(row["energy_over_floor"], 1.5, 0.03)
        self.about(row["efold_100km"], 2.0, 0.02)
        self.about(gen.arch_row(EARTH_500)["efold_100km"], 2.1, 0.02)

    def test_figure_curves_pass_through_the_reference_case(self):
        import numpy as np
        nu = EARTH_500.u / EARTH_500.u_orb
        _, stream, energy, limit = speed_ratio.curves(np.array([nu]))
        self.about(stream[0] * limit[0], 1.0, 1e-9)
        self.about(energy[0], 2.38, 0.005)


class Column(Base):
    def setUp(self):
        self.f = gen.FOUNTAIN_100

    def test_compression_is_the_weight_above_at_every_height(self):
        for z in (0.0, 2.0e4, 5.0e4, 9.0e4, self.f.height):
            self.about(-self.f.effective_tension(z), self.f.weight_above(z), 1e-6)

    def test_numbers_quoted(self):
        f = self.f
        self.about(f.base_speed, 1.7e3, 0.02)
        self.about(f.mdot, 5.4e3, 0.01)
        self.about(-f.effective_tension(0.0), 18.6e6, 0.005)
        in_flight = 2.0 * f.mdot * (f.base_speed - f.top_speed) / f.g
        self.about(in_flight, 800e3, 0.02)
        self.about(f.stored_energy, 0.75e12, 0.01)
        self.about(1.0 / (2.0 * math.pi / 1.0e4 * f.growth_speed(0.0)), 1.5, 0.02)
        self.assertLess(f.growth_speed(0.9 * f.height), f.growth_speed(0.0))

    def test_stored_energy_formula(self):
        f = self.f
        steps = 4000
        dz = f.height / steps
        direct = sum(0.5 * f.stream_per_length((i + 0.5) * dz) * f.speed((i + 0.5) * dz) ** 2 for i in range(steps)) * dz
        self.about(f.stored_energy, direct, 1e-5)


class OtherWorlds(Base):
    def test_table(self):
        rows = {name: gen.world_row(case) for name, case in (("earth", EARTH_500), ("mars", gen.MARS_200), ("moon", MOON_20))}
        expect = {
            "threshold": (7.6e3, 3.5e3, 1.7e3), "speed": (10.0e3, 4.5e3, 2.2e3), "circumference": (43.2e6, 22.6e6, 11.0e6),
            "thrust": (164e9, 34e9, 7.9e9), "energy_per_metre": (82e9, 17e9, 3.9e9), "energy_total": (3.5e18, 3.8e17, 4.3e16),
            "slug_energy": (500e6, 103e6, 24e6), "guide_load_lane": (2.1e3, 0.82e3, 0.39e3),
            "delay_budget_100m": (0.83e-3, 1.8e-3, 3.8e-3), "local_efold_100km": (2.1, 4.6, 9.5), "period": (95 * 60, 109 * 60, 110 * 60),
        }
        for key, values in expect.items():
            for name, want in zip(("earth", "mars", "moon"), values):
                self.about(rows[name][key], want, 0.03)

    def test_whole_ring_growth_times(self):
        for case, minutes in ((EARTH_500, 7.7), (gen.MARS_200, 9.6), (MOON_20, 10.1)):
            self.about(1.0 / RingModes(case, 50.0e9).growth_rate(2) / 60.0, minutes, 0.01)

    def test_ratios_quoted(self):
        self.about(EARTH_500.u_orb / MOON_20.u_orb, 4.6, 0.01)
        self.about(EARTH_500.E_prime / MOON_20.E_prime, 21.0, 0.02)
        self.about(EARTH_500.total_kinetic_energy / MOON_20.total_kinetic_energy, 80.0, 0.02)
        periods = [gen.world_row(c)["period"] for c in (EARTH_500, gen.MARS_200, MOON_20)]
        self.assertLess(max(periods) / min(periods), 1.2)


class Tabletop(Base):
    def test_numbers_quoted(self):
        t = gen.TabletopArch()
        self.about(t.threshold, 3.1, 0.02)
        self.about(t.carried_per_length, 0.15, 0.04)
        self.about(t.thrust, 2.5, 1e-9)
        self.about(t.efold_time(1.0), 0.065, 0.02)


if __name__ == "__main__":
    unittest.main()
