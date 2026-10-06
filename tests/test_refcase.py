"""Every number quoted in the paper that follows from the reference case.

If an input in analysis/params.py changes, the failures here list the
statements in the text that need updating. Tolerances match how the paper
rounds: "about 1,600" is checked to a few per cent, "0.79 degrees" to the
last digit shown.
"""
import math
import unittest

from analysis import lane_stability as ls
from analysis.params import EARTH_500 as C
from analysis.params import MOON_20, magnetic_pressure


class Base(unittest.TestCase):
    def about(self, value, quoted, rel=0.03):
        self.assertTrue(
            math.isclose(value, quoted, rel_tol=rel),
            f"computed {value:.6g}, paper quotes {quoted:.6g} (tolerance {rel:.0%})",
        )


class Introduction(Base):
    def test_ring_geometry(self):
        self.about(C.R, 6871e3, 1e-4)
        self.about(C.circumference, 43_000e3, 0.01)

    def test_inventory(self):
        self.about(C.total_passive_mass, 5e10, 0.05)
        self.about(C.lam_stream, 1640, 0.005)
        self.about(C.total_stream_mass, 7.1e10, 0.01)
        self.about(C.total_kinetic_energy, 3.5e18, 0.03)
        self.about(C.total_stream_mass / C.slug_mass, 7.1e9, 0.01)


class LaneGuide(Base):
    def test_magnetic_pressure_table(self):
        for b, mpa in [(0.5, 0.10), (1, 0.40), (2, 1.59), (3, 3.58)]:
            self.about(magnetic_pressure(b) / 1e6, mpa, 0.01)

    def test_representative_lane(self):
        self.about(C.lam_lane, 5.4, 0.02)
        self.about(C.mdot_lane, 5.4e4, 0.02)
        self.about(math.degrees(C.alpha), 0.79, 0.01)
        self.about(C.kappa_helix, 3.8e-6, 0.02)
        self.about(C.normal_load_lane, 2.1e3, 0.02)
        self.about(10e6 / C.n_lanes, 33e3, 0.02)
        self.about(10e6 / C.n_lanes / 100e3, 0.33, 0.02)

    def test_convective_times(self):
        for wavelength, t in [(100, 10e-3), (10, 1e-3), (1, 0.1e-3)]:
            self.about(wavelength / C.u, t, 1e-9)


class HelicalShell(Base):
    def test_crossover_angle_and_pitch(self):
        self.about(2 * math.pi * C.a, 314, 0.01)
        self.about(C.alpha, 0.014, 0.02)
        for gamma, deg, pitch_km in [(10, 0.79, 23), (30, 1.38, 13), (100, 2.51, 7)]:
            self.about(math.degrees(C.alpha_cross(gamma)), deg, 0.01)
            self.about(C.pitch(gamma) / 1e3, pitch_km, 0.03)

    def test_prestress(self):
        self.about(C.N_theta, 100e3, 1e-9)
        self.about(C.p_eq, 2e3, 1e-9)

    def test_stream_load_table(self):
        self.about(C.T_eq_lane, 5.4e8, 0.02)
        for wavelength, load in [(100, 2.1e3), (10, 210e3), (1, 21e6)]:
            self.about(ls.stream_stiffness(wavelength) * 1e-3, load, 0.03)


class FourLaneCell(Base):
    def test_momentum_flux_channels(self):
        self.about(C.mdot_lane * C.u, 5.4e8, 0.02)
        self.about(C.theta_flux_lane, 7.6e6, 0.02)
        for frac, s_res, th_res in [(1e-4, 54e3, 0.76e3), (1e-3, 0.54e6, 7.6e3), (1e-2, 5.4e6, 76e3)]:
            self.about(frac * C.mdot_lane * C.u, s_res, 0.02)
            self.about(frac * C.theta_flux_lane, th_res, 0.02)

    def test_slug_discreteness(self):
        self.about(C.slug_rate(), 5.4e3, 0.02)
        self.about(C.headway(), 0.185e-3, 0.02)
        for window, count, err in [(1e-3, 5.4, 0.185), (10e-3, 54, 0.0185), (0.1, 540, 0.00185), (1.0, 5400, 0.000185)]:
            self.about(window * C.slug_rate(), count, 0.02)
            self.about(1.0 / (window * C.slug_rate()), err, 0.02)
        self.about(0.01 * C.headway(), 1.8e-6, 0.03)
        self.about(0.001 * C.headway(), 0.18e-6, 0.03)


class TugFields(Base):
    def test_power_examples(self):
        self.about(1e6 * C.u, 10e9, 1e-9)
        self.about(10e6 * C.u, 100e9, 1e-9)
        self.about(10e6 / (3 * 9.80665), 340e3, 0.01)        # vehicle at 3 g
        self.about(C.Pi_total / 10e6, 16e3, 0.03)
        self.about(10e6 / C.n_lanes, 33e3, 0.02)

    def test_common_mode_tug(self):
        hoop = 1e-3 * C.Pi_total
        self.about(hoop, 164e6, 0.01)
        self.about(hoop / 1e9, 0.16, 0.03)                   # m^2 at 1 GPa
        self.about(hoop / 1e9 * 1600, 260, 0.02)             # kg/m at 1600 kg/m^3
        self.about(C.m_passive, 1200, 0.02)
        self.about(1e-3 * C.lam_stream * C.g_h, 14, 0.02)
        self.about(1e-3 * C.lam_stream * C.g_h / C.w_p, 1.4e-3, 0.02)

    def test_thrust_line_example(self):
        couple = 10e6 * 2 * C.a
        self.about(couple, 1e9, 1e-9)
        self.about(couple / C.Pi_total, 6e-3, 0.03)
        k = 2 * math.pi / 100e3
        self.about(couple * k, 60e3, 0.05)                   # shear force
        self.about(couple * k / (2 * C.a) * 10, 6e3, 0.05)   # one sector's tug on a 10 m bay

    def test_cost_of_sideways_load(self):
        per_newton = C.u * 100e3 / (2 * math.pi * C.a)
        self.about(per_newton, 3.2e6, 0.01)
        self.about(0.01 * C.w_p * per_newton, 320e6, 0.01)
        chi = C.weight_factor()
        self.about(chi, 3.4, 0.01)
        self.about(C.u**3 * (2 * math.pi / 1000e3) / (chi * C.g_h), 0.22e6, 0.01)
        # two waves round the ring: the hoop's give lowers the factor to 2.5 (tests/test_ring.py)
        self.about(C.u**3 * (2 / C.R) / (2.5 * C.g_h), 14e3, 0.03)

    def test_weight_coupling(self):
        self.about(C.weight_multiplier, 1.4, 0.02)           # streams alone, or a structure too stiff to stretch
        self.about(C.total_weight_multiplier(), 4.7, 0.02)
        self.about(C.weight_coupling(), 2.8e-7, 0.02)
        self.about(1 / C.weight_coupling(), 3.5e6, 0.01)
        self.about(C.weight_factor() * C.lam_stream * C.g_h * 1e-3, 47.0, 0.01)   # N/m per part in a thousand of speed
        self.about(C.lam_stream * C.g_h * 1e-3, 14.0, 0.02)
        # the stream-only sensitivity is larger by the curvature term that
        # tension in the structure cancels
        self.about(C.lift_multiplier - C.weight_multiplier, 1 / (1 - C.g_h * C.R / C.u**2), 1e-9)

    def test_speed_trim_example(self):
        du = 10e6 / (C.n_lanes * C.mdot_lane)
        self.about(du, 0.61, 0.01)
        self.about(du / C.u, 6e-5, 0.03)
        coupling = C.weight_coupling() * 100e3
        self.about(coupling, 0.03, 0.06)
        self.about(coupling * 10e6, 280e3, 0.02)
        side = coupling * 10e6 / 1000e3
        self.about(side, 0.3, 0.06)
        self.assertTrue(2e-5 < side / C.w_p < 4e-5)             # "a few hundred-thousandths"
        shift = side / (C.Pi_total * (2 * math.pi / 1000e3) ** 2)
        self.assertTrue(0.03 < shift < 0.06)                    # "a few centimetres"


class ClosureScreens(Base):
    def test_lift_and_energy(self):
        self.about(C.lift_accel, 6.1, 0.01)
        self.about(C.E_prime, 82e9, 0.01)
        for w, lam, e in [(10e3, 1640, 82e9), (30e3, 4900, 245e9), (100e3, 16000, 820e9)]:
            case = C.with_(w_p=w)
            self.about(case.lam_stream, lam, 0.03)
            self.about(case.E_prime, e, 0.01)
        self.about(C.E_prime * 1e3, 82e12, 0.01)

    def test_dump_speeds(self):
        self.about(C.U_g, 0.5e3, 0.01)
        self.about(C.u + C.U_g, 10.5e3, 0.01)
        self.about(C.u - C.U_g, 9.5e3, 0.01)
        self.about(C.v_esc, 10.8e3, 0.01)


class AppendixA(Base):
    def test_stream_stiffness_table(self):
        rows = [(10, 2.1e8), (30, 2.4e7), (100, 2.1e6), (300, 2.4e5), (1e3, 2.1e4), (3e3, 2.4e3)]
        for wavelength, stiff in rows:
            self.about(ls.stream_stiffness(wavelength), stiff, 0.03)

    def test_bending_only_table(self):
        for wavelength, b in [(10, 1.4e9), (30, 1.2e10), (100, 1.4e11), (1e3, 1.4e13)]:
            self.about(ls.bending_stiffness_required(wavelength), b, 0.04)

    def test_delay_budget_table(self):
        for wavelength, budget in [(10, 0.083e-3), (30, 0.25e-3), (100, 0.83e-3), (300, 2.5e-3), (1e3, 8.3e-3)]:
            self.about(ls.delay_budget(wavelength, C.u), budget, 0.01)

    def test_eigenvalue_table(self):
        table = {
            10: (-3.0e2, +7.7e2, +9.9e2),
            30: (-2.2e2, +1.3e1, +1.9e2),
            100: (-7.4e1, -5.7e1, -3.0e1),
            300: (-2.6e1, -2.4e1, -2.2e1),
            1000: (-7.7, -7.6, -7.4),
        }
        for wavelength, row in table.items():
            for tau, quoted in zip((1e-4, 5e-4, 1e-3), row):
                got = ls.max_growth_rate(wavelength, tau)
                self.assertEqual(got > 0, quoted > 0, f"sign differs at L={wavelength}, tau={tau}")
                # The 30 m, 0.5 ms entry sits next to a zero crossing, so it is
                # sensitive to rounding of the inputs.
                tol = 0.15 if (wavelength, tau) == (30, 5e-4) else 0.03
                self.about(got, quoted, tol)

    def test_gain_examples(self):
        self.about(3 * ls.stream_stiffness(100) * 1e-3, 6.4e3, 0.02)
        self.about(3 * ls.stream_stiffness(10) * 1e-3, 640e3, 0.02)


class AppendixB(Base):
    def test_lane_wavenumber_table(self):
        rows = [
            (30, 0, 0.209, 2.4e7), (30, 64, 0.227, 2.8e7), (100, 0, 0.0628, 2.1e6), (100, 64, 0.0807, 3.5e6),
            (300, 0, 0.0209, 2.4e5), (300, 64, 0.0389, 8.2e5), (1e3, 0, 0.00628, 2.1e4), (1e3, 64, 0.0242, 3.2e5),
            (3e3, 0, 0.00209, 2.4e3), (3e3, 64, 0.0200, 2.2e5),
        ]
        for wavelength, n, k_par, stiff in rows:
            k = ls.lane_wavenumber(wavelength, n)
            self.about(k, k_par, 0.01)
            self.about(ls.stream_stiffness(wavelength, k_par=k), stiff, 0.03)

    def test_saturation_table(self):
        rows = [(30, 0, 71e3), (30, 64, 84e3), (100, 0, 6.4e3), (100, 64, 10.6e3),
                (300, 0, 0.71e3), (300, 64, 2.4e3), (1e3, 0, 64), (1e3, 64, 0.95e3)]
        for wavelength, n, load in rows:
            k = ls.lane_wavenumber(wavelength, n)
            self.about(3 * ls.stream_stiffness(wavelength, k_par=k) * 1e-3, load, 0.03)


class AppendixC(Base):
    def test_slug_mass_table(self):
        for mass, rate, spacing, headway, energy in [
            (0.1, 5.4e5, 0.018, 1.8e-6, 5e6), (1, 5.4e4, 0.18, 18e-6, 50e6),
            (10, 5.4e3, 1.8, 0.18e-3, 500e6), (100, 5.4e2, 18, 1.8e-3, 5e9),
        ]:
            self.about(C.slug_rate(mass), rate, 0.02)
            self.about(C.spacing(mass), spacing, 0.03)
            self.about(C.headway(mass), headway, 0.03)
            self.about(C.slug_energy(mass), energy, 1e-9)
        self.about(1.0 / (0.001 * C.slug_rate()), 0.19, 0.04)


class AppendixE(Base):
    def test_isolation_lengths(self):
        for allow, length in [(1e9, 0.012), (10e9, 0.12), (100e9, 1.2), (1e12, 12), (10e12, 120), (82e12, 1e3)]:
            self.about(allow / C.E_prime, length, 0.03)
            self.about(allow / C.E_prime / C.u, length / 1e4, 0.03)

    def test_ten_millisecond_fault(self):
        slugs = 0.010 * C.slug_rate()
        self.about(slugs, 54, 0.02)
        self.about(slugs * C.slug_mass, 540, 0.02)
        self.about(slugs * C.slug_energy(), 27e9, 0.02)
        self.about(0.010 * C.mdot_lane * C.u, 5.4e6, 0.02)


class AppendixF(Base):
    def test_corotation_correction(self):
        self.about((C.U_g / C.u) ** 2, 0.0025, 0.01)


class LunarCase(Base):
    """Numbers quoted for the lunar comparison case."""

    def test_same_speed_ratio(self):
        self.about(MOON_20.u / MOON_20.u_orb, C.u / C.u_orb, 1e-9)
        self.about(MOON_20.lam_stream, C.lam_stream, 1e-9)

    def test_energy_scale(self):
        self.about(MOON_20.u, 2.19e3, 0.01)
        self.about(MOON_20.E_prime, 3.9e9, 0.02)
        self.about(C.E_prime / MOON_20.E_prime, 21, 0.03)
        self.about(C.total_kinetic_energy / MOON_20.total_kinetic_energy, 80, 0.05)
        self.about(C.u / MOON_20.u, 4.6, 0.02)


if __name__ == "__main__":
    unittest.main()
