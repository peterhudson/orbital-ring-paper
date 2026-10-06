"""Stream-plus-structure motion: eigenvalues, the particle simulation, and the
numbers quoted in the collective-stability chapter."""
import cmath
import math
import unittest

import numpy as np

from analysis.collective import CollectiveModel, funicular_deflection, load_capacity
from analysis.params import EARTH_500 as C
from analysis.particles import LocalParticleSim, envelope_rate, fitted_rate


class Base(unittest.TestCase):
    def about(self, value, quoted, rel=0.03):
        self.assertTrue(math.isclose(value, quoted, rel_tol=rel), f"computed {value:.6g}, expected {quoted:.6g} (tolerance {rel:.1%})")


def k_of(wavelength):
    return 2.0 * math.pi / wavelength


class FollowingGuides(Base):
    def test_stiff_following_grows_at_the_rigid_rate_at_every_wavelength(self):
        model = CollectiveModel.reference(zeta=0.3, ff=1.0)
        for wavelength in (300, 3e3, 1e5, 1e7):
            self.about(model.growth_rate(k_of(wavelength)), model.rigid_growth_rate(k_of(wavelength)), 0.03)

    def test_a_tube_as_tight_as_its_streams_push_is_neutral(self):
        """Birch's 1982 result: with structure tension equal to the momentum
        flux the tube neither straightens nor kinks. Less tension, and it grows."""
        model = CollectiveModel.reference(zeta=0.3, ff=1.0)
        for wavelength in (300, 3e3, 1e5):
            k = k_of(wavelength)
            rigid = model.rigid_growth_rate(k)
            self.assertLess(abs(model.with_(N=model.Pi).growth_rate(k)), 1e-3 * rigid)
            self.about(model.with_(N=0.5 * model.Pi).growth_rate(k), rigid * math.sqrt(0.5), 0.03)
            self.assertLess(model.with_(N=1.5 * model.Pi).growth_rate(k), 0.0)

    def test_rigid_rate_factors(self):
        model = CollectiveModel.reference()
        k = k_of(1e5)
        self.about(model.rigid_growth_rate(k) / (k * model.v), 0.76, 0.01)
        self.about(model.with_(counter=False).rigid_growth_rate(k) / (k * model.v), 0.49, 0.01)
        self.about(model.rigid_growth_rate(k), 0.48, 0.02)

    def test_spring_guide_decouples_short_waves_only(self):
        model = CollectiveModel.reference(zeta=0.2)
        for wavelength in (30, 100, 300):
            self.assertLess(model.growth_rate(k_of(wavelength)), 0.0)
        for wavelength in (3e3, 1e4, 1e5, 1e6):
            self.about(model.growth_rate(k_of(wavelength)), model.rigid_growth_rate(k_of(wavelength)), 0.12)

    def test_quoted_boundary_of_the_spring_guide(self):
        model = CollectiveModel.reference(zeta=0.2)
        wavelengths = np.geomspace(100, 1e4, 2000)
        rates = model.growth_curve(wavelengths)
        self.about(wavelengths[np.argmax(rates > 0)], 400, 0.05)
        self.about(model.guide_wavelength, 1000, 1e-9)

    def test_softer_guide_moves_the_unstable_band_to_longer_waves(self):
        self.about(CollectiveModel.reference(guide_hz=10).guide_wavelength, 1000, 1e-9)
        self.about(CollectiveModel.reference(guide_hz=1).guide_wavelength, 10000, 1e-9)
        soft = CollectiveModel.reference(guide_hz=1, zeta=0.2)
        self.assertLess(soft.growth_rate(k_of(3e3)), 0.0)
        self.assertGreater(soft.growth_rate(k_of(1e5)), 0.4)


class MirrorLaw(Base):
    def test_reference_is_stable_at_every_wavelength(self):
        model = CollectiveModel.mirror_reference()
        wavelengths = np.concatenate([np.geomspace(3, 1e3, 200), np.geomspace(1e3, 1e7, 60)])
        self.assertLess(model.growth_curve(wavelengths).max(), 0.0)

    def test_stability_survives_changes_of_design(self):
        wavelengths = np.concatenate([np.geomspace(3, 1e3, 120), np.geomspace(1e3, 1e7, 40)])
        for change in (dict(f_filter=300.0), dict(guide_hz=3.0), dict(guide_hz=30.0, zeta=0.7), dict(c0=0.3), dict(c0=0.65),
                       dict(EI=1e12), dict(EI=1e14), dict(cutoff=1000.0), dict(loss_factor=1e-4)):
            self.assertLess(CollectiveModel.mirror_reference(**change).growth_curve(wavelengths).max(), 0.0, str(change))

    def test_short_waves_lean_on_structural_damping(self):
        model = CollectiveModel.mirror_reference(loss_factor=0.0)
        wavelengths = np.geomspace(3, 300, 400)
        rates = model.growth_curve(wavelengths)
        self.about(rates.max(), 0.005, 0.15)
        self.about(wavelengths[rates.argmax()], 20, 0.1)
        self.about(2 * math.pi * math.sqrt(model.EI / model.Pi), 120, 0.03)      # where bending stiffness takes over
        self.about(model.EI, 5e10 * C.a**2 / 2, 1e-9)

    def test_set_point(self):
        model = CollectiveModel.mirror_reference(adapt=0.03)
        wavelengths = np.concatenate([np.geomspace(3, 1e3, 200), np.geomspace(1e3, 1e7, 60)])
        self.assertLess(model.growth_curve(wavelengths).max(), 0.0)
        k = k_of(1e5)
        self.about(-1.0 / model.growth_rate(k), 55, 0.05)                            # settling time, s
        y, offset = model.static_response(k, 100.0)
        self.about(y, -funicular_deflection(100.0, k, model.Pi), 1e-3)
        self.assertLess(offset, 1e-9)                                                # every stream centered
        y, offset = CollectiveModel.mirror_reference().static_response(k, 100.0)
        self.assertGreater(y, 0.3)
        self.about(offset / y, abs(1 + 0.5 * cmath.exp(0.3j)), 0.01)                 # about 1 + c_m
        self.about(0.5 * math.sin(0.3), 0.15, 0.02)                                  # the part look-ahead adds, per stream
        # a 1% load mismatch uses 20 mm of room beyond this wavelength
        self.about(2 * math.pi / math.sqrt(100.0 / (model.Pi * 0.02 / 3)), 20e3, 0.05)

    def test_structure_behaves_as_a_damped_string_in_tension(self):
        model = CollectiveModel.mirror_reference()
        self.about(model.apparent_tension(), 0.5 * C.Pi_total, 1e-9)
        self.about(model.apparent_tension() / 1e9, 82, 0.01)
        self.about(model.apparent_mass(), 370, 0.02)
        self.about(math.sqrt(model.apparent_tension() / model.apparent_mass()), 15e3, 0.01)
        for wavelength in (1e3, 1e4, 1e5, 1e6):
            k = k_of(wavelength)
            self.about(model.ideal_damping_ratio(k), 0.43, 0.03 if wavelength < 5e3 else 0.005)
            least = max(model.eigenvalues(k), key=lambda z: z.real)
            if wavelength >= 1e4:
                self.about(least.real, model.ideal_roots(k)[0].real, 0.01)
                self.about(abs(least.imag), abs(model.ideal_roots(k)[0].imag), 0.01)

    def test_look_ahead_rule(self):
        model = CollectiveModel.mirror_reference()
        self.assertEqual(model.lookahead(k_of(100.0)), 20.0)
        self.about(model.lookahead(k_of(1e5)), 0.048 * 1e5, 0.01)
        self.about(2 * math.pi * 20.0 / 0.3, 420, 0.01)                   # wavelength where the rule changes over

    def test_look_ahead_must_outrun_the_delay(self):
        """d_a > u tau m / (2 (m - c_m lambda)), with tau the lag of the path command."""
        tau = 2 * 0.7 / (2 * math.pi * 1e3)
        for c0, quoted in ((0.2, 1.5), (0.5, 3.6), (0.65, 10.9)):
            model = CollectiveModel.reference(zeta=0.3, ff=1.0, c0=c0)
            floor = model.v * tau * model.m / (2 * (model.m - c0 * model.lam))
            self.about(floor, quoted, 0.03)
            k = k_of(1e4)
            self.assertGreater(model.with_(preview=0.9 * floor).growth_rate(k), 0.0)
            self.assertLess(model.with_(preview=1.1 * floor).growth_rate(k), 0.0)

    def test_heavy_guide_damping_makes_a_spring_guide_worse(self):
        short = np.geomspace(3, 200, 60)
        self.assertLess(CollectiveModel.reference(zeta=0.2).growth_curve(short).max(), 0.0)
        self.assertGreater(CollectiveModel.reference(zeta=0.5).growth_curve(short).max(), 1.0)
        self.assertGreater(CollectiveModel.reference(zeta=0.7).growth_curve(short).min(), 0.0)

    def test_needs_look_ahead_longer_than_the_control_delay(self):
        plain = dict(zeta=0.3, ff=1.0, c0=0.5)
        self.assertGreater(CollectiveModel.reference(**plain).growth_rate(k_of(1e3)), 0.0)                  # lag alone
        slow = CollectiveModel.reference(**plain, preview=100.0, f_filter=10.0)                             # 22 ms is 220 m
        self.assertGreater(slow.growth_rate(k_of(1e4)), 0.0)
        self.assertLess(slow.with_(preview=1000.0).growth_rate(k_of(1e5)), 0.0)

    def test_gain_limit(self):
        model = CollectiveModel.mirror_reference()
        self.about(model.m / model.lam, 0.72, 0.01)
        self.assertGreater(model.with_(c0=0.9).growth_rate(k_of(1e4)), 100.0)

    def test_load_capacity_numbers(self):
        pi = C.Pi_total
        self.about(funicular_deflection(100.0, k_of(100e3), pi), 0.155, 0.02)
        self.about(funicular_deflection(100.0, k_of(1000e3), pi), 15.5, 0.02)
        self.about(load_capacity(k_of(100e3), 0.02, pi, 0.5), 4.3, 0.02)
        self.about(load_capacity(k_of(1000e3), 0.02, pi, 0.5), 0.043, 0.02)
        self.about(load_capacity(k_of(10e3), 0.02, pi, 0.5), 430, 0.02)


class ParticleSimulation(Base):
    """Short runs of the time-domain model against the eigenvalues."""

    def make(self, model, **kw):
        return LocalParticleSim(model, length=5e3, n_nodes=250, slugs_per_direction=500, **kw)

    def test_spring_guide_growth_rate(self):
        model = CollectiveModel.reference(zeta=0.3, f_filter=200.0)
        sim = self.make(model)
        sim.y += 1e-6 * np.cos(2 * math.pi * sim.s_nodes / 5e3)
        t, a = sim.run(1.0, record_modes=(1,), every=25)
        self.about(fitted_rate(t, a[:, 0], (0.4, 1.0)), model.growth_rate(k_of(5e3)), 0.03)

    def test_mirror_law_decays_as_predicted(self):
        model = CollectiveModel.mirror_reference(f_filter=200.0, preview=30.0)
        sim = self.make(model)
        sim.y += 1e-3 * np.cos(2 * math.pi * 2 * sim.s_nodes / 5e3)
        t, a = sim.run(1.0, record_modes=(2,), every=10)
        self.about(envelope_rate(t, a[:, 0]), model.growth_rate(k_of(2500.0)), 0.15)
        self.assertLess(np.abs(sim.gap()).max(), 5e-3)

    def test_streams_act_as_continuous_until_the_slugs_are_far_apart(self):
        """Appendix C: decay rate of a 2.5 km wave under the mirror law against slug spacing."""
        model = CollectiveModel.mirror_reference(f_filter=200.0, preview=30.0)

        def rate(slugs):
            sim = LocalParticleSim(model, length=5e3, n_nodes=250, slugs_per_direction=slugs)
            sim.y += 1e-3 * np.cos(2 * math.pi * 2 * sim.s_nodes / 5e3)
            t, a = sim.run(1.0, record_modes=(2,), every=10)
            return envelope_rate(t, a[:, 0])

        fine = rate(1000)                                   # 5 m apart
        self.about(rate(500), fine, 1e-3)                   # 10 m
        self.about(rate(250), fine, 1e-3)                   # 20 m
        at_50 = rate(100) / fine
        self.assertTrue(1.015 < at_50 < 1.045)              # 2 to 4% faster
        self.assertTrue(0.4 < rate(60) / fine < 0.6)        # 83 m: about half
        self.assertTrue(0.2 < rate(40) / fine < 0.4)        # 125 m: a quarter to a third
        self.about(300.0 / 20.0, 15.0, 1e-9)                # slugs per cut-off wavelength where it is still exact
        self.about(C.spacing(100.0), 18.0, 0.03)            # 100 kg slugs

    def test_static_load_is_held_up_to_the_stroke_limit(self):
        model = CollectiveModel.mirror_reference(f_filter=200.0, preview=30.0)
        k = k_of(2500.0)
        stroke = 0.01
        capacity = load_capacity(k, stroke, model.Pi, model.c0)

        def final_amplitude(load):
            sim = self.make(model, stroke=stroke)
            shape = np.cos(k * sim.s_nodes)
            for _ in range(int(4.0 / sim.dt)):
                sim.load = load * min(1.0, sim.t / 2.0) * shape
                sim.step()
                if not np.isfinite(sim.y).all() or np.abs(sim.y).max() > 1.0:
                    return math.inf
            return (np.fft.rfft(sim.y)[2] * 2 / sim.n_nodes).real

        self.about(final_amplitude(0.5 * capacity), 0.5 * capacity / (-model.path_gain(k) * model.Pi * k**2), 0.1)
        self.assertEqual(final_amplitude(1.5 * capacity), math.inf)


if __name__ == "__main__":
    unittest.main()
