"""Whole-ring statics and stability: the momentum-truss model against the
closed forms, and the numbers quoted in the effective-tension chapter."""
import math
import unittest

import numpy as np

from analysis import ladder, ring
from analysis.params import EARTH_500 as C


class Base(unittest.TestCase):
    def about(self, value, quoted, rel=0.03):
        self.assertTrue(math.isclose(value, quoted, rel_tol=rel), f"computed {value:.6g}, expected {quoted:.6g} (tolerance {rel:.1%})")


class RingEquilibrium(Base):
    def test_regular_polygon_is_in_equilibrium(self):
        truss, x0 = ring.ring_truss(n_nodes=180)
        weight = np.abs(truss.masses(x0)[:, None] * truss.gravity(x0)).max()
        self.assertLess(np.abs(truss.force(x0)).max() / weight, 1e-9)

    def test_effective_tension_equals_minus_weight_times_radius(self):
        truss, x0 = ring.ring_truss(n_nodes=180)
        mu = C.m_passive + C.lam_stream
        self.about(truss.effective_tension(x0).mean(), -mu * C.g_h * C.R, 1e-9)

    def test_analytic_stiffness_matches_finite_differences(self):
        truss, x0 = ring.ring_truss(n_nodes=24)
        K, K_fd = truss.stiffness(x0), truss.stiffness_fd(x0, h=1.0)
        self.assertLess(np.abs(K - K_fd).max() / np.abs(K).max(), 1e-8)


class RingModes(Base):
    def test_in_plane_growth_matches_closed_form(self):
        om2 = C.omega_orb**2
        for ea in (5e10, 5e12):
            truss, x0 = ring.ring_truss(n_nodes=360, ea=ea)
            got = ring.growth_rates_by_mode(truss, x0, "in")
            for n in (1, 2, 3, 4, 6):
                self.about(got[n] / om2, ring.growth_rate_in_plane(n, ea=ea) ** 2 / om2, 2e-3)

    def test_inextensible_limit(self):
        om2 = C.omega_orb**2
        for n in (1, 2, 5):
            self.about(ring.growth_rate_in_plane(n, ea=1e20) ** 2 / om2, n**4 / (n**2 + 1), 1e-6)

    def test_out_of_plane_growth(self):
        om2 = C.omega_orb**2
        truss, x0 = ring.ring_truss(n_nodes=180, ea=5e12, dim=3)
        got = ring.growth_rates_by_mode(truss, x0, "out")
        self.assertLess(abs(got[1]) / om2, 1e-6)          # a tilt of the whole ring is neutral
        for n in (2, 3, 4):
            self.about(got[n] / om2, n**2 - 1, 5e-3)

    def test_quoted_growth_times(self):
        """e-folding times quoted in the text, minutes."""
        minutes = lambda rate: 1.0 / rate / 60.0
        self.about(minutes(ring.growth_rate_in_plane(1)), 21, 0.03)
        self.about(minutes(ring.growth_rate_out_of_plane(2)), 8.7, 0.03)
        self.about(ring.growth_rate_local(100e3), 0.48, 0.02)
        self.about(ring.growth_rate_local(1000e3), 0.048, 0.02)


class SpeedRipple(Base):
    """A stationary speed ripple u = u0 (1 + eps cos p theta): where the tug goes."""

    def run_case(self, p, eps, shift_weight, ea=5e13, n=360):
        angles = ring.member_angles(n)
        truss, x0 = ring.ring_truss(n_nodes=n, ea=ea, speed_ratio=1 + eps * np.cos(p * angles), shift_weight=shift_weight)
        x, res = truss.equilibrium(x0)
        self.assertLess(res, 1e-6)
        W = ring.fourier_amplitude(ring.radial_displacement(x), p, np.arctan2(x[:, 1], x[:, 0]))
        N1 = ring.fourier_amplitude(truss.tension(x), p, angles)
        spread = np.ptp(truss.effective_tension(x)) / truss.thrust.mean()
        return W, N1 / (truss.thrust.mean() * eps), spread

    def test_effective_tension_stays_uniform(self):
        for p, eps in ((2, 1e-5), (8, 1e-4), (40, 1e-3)):
            _, _, spread = self.run_case(p, eps, True)
            self.assertLess(spread, 1e-5)

    def test_structure_tension_absorbs_the_tug(self):
        for p, eps in ((8, 1e-4), (40, 1e-3)):
            _, ratio, _ = self.run_case(p, eps, True)
            _, n1 = ring.speed_ripple_response(eps, p)
            self.about(ratio, n1 / (C.Pi_total * eps), 2e-3)
            self.assertGreater(ratio, 0.99)

    def test_shape_change_is_the_weight_shift_alone(self):
        for p, eps in ((2, 1e-5), (8, 1e-4), (40, 1e-3)):
            W, _, _ = self.run_case(p, eps, True)
            W_theory, _ = ring.speed_ripple_response(eps, p)
            self.about(W, W_theory, 0.03)        # 360 members: 9 per wavelength at p = 40
            W_no_shift, ratio, _ = self.run_case(p, eps, False)
            self.assertLess(abs(W_no_shift), 0.01 * abs(W))
            self.about(ratio, 1.0, 1e-3)


class ThrustLineShift(Base):
    """Opposed tug fields on a braced two-chord frame."""

    def centre_ratio(self, length, panels, ea_web):
        e0 = 0.05
        s_mid = (np.arange(panels) + 0.5) * length / panels
        truss, x0, fixed = ladder.ladder_truss(length=length, panels=panels, shift=e0 * np.sin(math.pi * s_mid / length) ** 2, ea_web=ea_web)
        x, _ = truss.equilibrium(x0, fixed=fixed, tol=1e-10)
        n_side = panels + 1
        y = 0.5 * (x[:n_side, 1] + x[n_side:, 1])
        tension = truss.tension(x)
        ripple = np.abs(0.5 * (tension[:panels] - tension[panels : 2 * panels])).max()
        return y[panels // 2] / e0, ripple / (C.Pi_total * e0 / (2 * C.a))

    def test_structure_moves_opposite_to_the_thrust_line(self):
        ratio, chord_share = self.centre_ratio(20e3, 200, 2.5e11)
        self.about(ratio, -1.0, 2e-3)
        self.assertLess(chord_share, 1e-3)

    def test_without_a_shear_path_each_chord_keeps_its_own_tug(self):
        ratio, chord_share = self.centre_ratio(20e3, 200, 2.5e5)
        self.assertLess(abs(ratio), 0.05)
        self.assertGreater(chord_share, 0.4)

    def test_crossover_wavelength(self):
        self.about(ladder.crossover_wavelength(), 174, 0.02)


if __name__ == "__main__":
    unittest.main()
