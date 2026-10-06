"""Holding the whole ring: the structured law, the stators' part in it, and
runs of the controllers on the nonlinear particle simulation."""
import math
import unittest

import numpy as np
from scipy.linalg import expm

from analysis import ring_control as rc
from analysis.collective import CollectiveModel
from analysis.params import EARTH_500 as C
from analysis.ring_modes import ALONG_TRACK, FOLLOW, LATERAL, GuideLaw, RingModes
from analysis.ring_particles import RingParticleSim

MODEL = RingModes()
OM = MODEL.omega
LAW = rc.reference_law(MODEL)
SIM_GUIDE = 0.5        # rad/s: the guide bandwidth used in the particle simulation


class Base(unittest.TestCase):
    def about(self, value, quoted, rel=0.03):
        self.assertTrue(math.isclose(value, quoted, rel_tol=rel), f"computed {value:.6g}, expected {quoted:.6g} (tolerance {rel:.1%})")


class MirrorLawOnTheRing(Base):
    def test_coasting_slugs_bunch_when_the_wave_outruns_the_stream(self):
        """With no stator action the mirror law alone is neutral at short
        waves only while the structure's wave is slower than the stream,
        which is a gain below m / (2 lambda)."""
        limit = C.m_passive / (2 * C.lam_stream)
        self.about(limit, 0.36, 0.01)
        for n in (50, 200):
            self.assertLess(MODEL.growth_rate(n, GuideLaw(mirror=0.3)) / OM, 1e-6)
            self.assertGreater(MODEL.growth_rate(n, GuideLaw(mirror=0.4)) / OM, 0.5)
        wave_speed = lambda c0: math.sqrt(c0 * C.lam_stream / (C.m_passive - c0 * C.lam_stream)) * C.u
        self.about(wave_speed(limit), C.u, 1e-9)

    def test_lead_alone_pumps_the_bunching(self):
        for n in (10, 100):
            rate = MODEL.growth_rate(n, GuideLaw(mirror=0.2, lead=0.3)) / OM
            self.assertTrue(0.05 < rate < 0.2)

    def test_reference_law_holds_every_mode_from_two_up(self):
        for ea in (5e10, 5e11, 5e13):
            model = RingModes(ea=ea)
            law = rc.reference_law(model)
            for n in (2, 3, 4, 5, 6, 8, 12, 20, 50, 200, 1000, 10000):
                self.assertLess(model.growth_rate(n, law) / model.omega, -0.2, f"EA {ea:.0e}, n {n}")

    def test_reference_law_with_a_real_guide_and_set_point_adaptation(self):
        for n in (2, 3, 4, 6, 10, 30, 100, 300, 1000):
            plain = rc.baseline_gain(MODEL, n, LAW)
            self.assertLess(MODEL.closed_loop_eigenvalues(n, plain)[0].real / OM, -0.2)
            adaptive = rc.adaptive_closed_loop(MODEL, n, LAW)
            self.assertLess(np.linalg.eigvals(adaptive).real.max(), -0.2)

    def test_quoted_decay_times(self):
        minutes = lambda n: -1.0 / MODEL.growth_rate(n, LAW) / 60.0
        self.about(minutes(2), 33, 0.03)
        self.about(minutes(1000), 52, 0.03)

    def test_ring_and_local_models_agree_at_short_wavelength(self):
        """The structure's wave under the mirror law, far from ring scale."""
        n = 2000
        local = CollectiveModel.reference(c0=LAW.mirror, ff=1.0, lead=LAW.lead)
        want = local.ideal_roots(n / C.R)[0]
        ring = MODEL.eigenvalues(n, GuideLaw(mirror=LAW.mirror, lead=LAW.lead))
        got = min(ring, key=lambda z: abs(z - want))
        self.about(got.real, want.real, 0.01)
        self.about(abs(got.imag), abs(want.imag), 0.01)

    def test_uniform_mode_is_left_alone(self):
        self.assertIs(rc.law_for_mode(0, LAW), FOLLOW)
        self.assertGreater(MODEL.growth_rate(0, GuideLaw(mirror=0.5)) / OM, 1.0)      # mirrored, it runs away
        self.assertLess(MODEL.growth_rate(0, FOLLOW) / OM, 1e-9)


class LowestModes(Base):
    def test_no_mirror_gain_holds_the_ring_on_centre(self):
        rates = [MODEL.growth_rate(1, GuideLaw(mirror=c0)) / OM for c0 in np.arange(-1.0, 0.71, 0.05)]
        self.assertGreater(min(rates), 0.85)

    def test_steering_costs_more_than_twice_the_error_in_gap(self):
        cheap = rc.Scales(gap=0.02, speed=1e12, shape=2.0, floor=1.0, guide=C.g_h * 0.02 / C.R * 1e3)
        for n, quoted in ((1, 3.6), (2, 2.9), (3, 2.6), (10, 2.4)):
            K = rc.lqr_gain(MODEL, n, inputs=LATERAL, scales=cheap)
            self.assertLess(MODEL.closed_loop_eigenvalues(n, K)[0].real, 0.0)
            out = rc.recovery(MODEL, n, K, rc.unstable_direction(MODEL, n), duration=12.0 / MODEL.growth_rate(n))
            self.about(out["gap"], quoted, 0.03)

    def test_stators_hold_the_low_modes_with_small_speed_changes(self):
        """Peak speed change per metre of error on the growing mode."""
        nu = MODEL.nu
        for n, quoted in ((1, 0.009), (2, 0.016), (3, 0.027), (10, 0.28), (30, 2.8)):
            closed, K8, _ = rc.stator_lqr(MODEL, n, scales=rc.Scales(shape=10.0))
            self.assertLess(np.linalg.eigvals(closed).real.max(), -0.1)
            vals, vecs = np.linalg.eig(MODEL.tracking_matrix(n))
            x = vecs[:, np.argmax(vals.real)]
            x = x / x[0]
            times = np.linspace(0.0, 12.0 / vals.real.max(), 3000)
            step = expm(closed * (times[1] - times[0]))
            peak = 0.0
            for _ in times:
                peak = max(peak, abs(x[4] + nu * x[0]), abs(x[6] - nu * x[0]))
                x = step @ x
            self.about(peak * OM, quoted, 0.06)

    def test_off_centre_controller(self):
        closed, _, _ = rc.off_centre_controller(MODEL, LAW)
        self.about(np.linalg.eigvals(closed).real.max(), -0.13, 0.05)      # in units of the orbital rate
        self.about(100 * 0.009 / C.u, 9e-5, 0.02)                         # a 100 m offset, as a fraction of stream speed
        self.about(100 * 0.009 / C.u * C.Pi_total, 15e6, 0.03)             # and as tension in the structure


class SteadyLoads(Base):
    def test_set_point_adaptation_puts_the_ring_on_the_funicular(self):
        for n in (2, 3, 6, 30):
            w, gap = rc.static_response(MODEL, rc.adaptive_closed_loop(MODEL, n, LAW))
            self.about(w, -C.R**2 / (C.Pi_total * n * n), 0.02)
            self.assertLess(abs(gap), 1e-9 * abs(w))

    def test_without_it_the_gap_needed_is_hopeless(self):
        n = 2
        w, gap = rc.static_response(MODEL, rc.adaptive_closed_loop(MODEL, n, LAW, adapt=0.0)[:12, :12])
        self.assertGreater(w, 500.0)
        self.assertLess(gap, -800.0)

    def test_moon_tide(self):
        gm_moon, distance = 4.9028e12, 3.844e8
        accel = 1.5 * gm_moon * C.R / distance**3
        load = (C.m_passive + C.lam_stream) * accel
        self.about(load, 2.5e-3, 0.03)
        self.about(load * C.R**2 / (C.Pi_total * 4), 0.18, 0.03)
        self.about(load / (C.lam_stream * C.g_h) * C.u, 1.8e-3, 0.03)


class ParticleSimulation(Base):
    def test_perturbed_ring_returns_to_round_as_predicted(self):
        """Modes 1, 2 and 3 displaced by millimetres; mode 1 held by the
        stators, the others by the structured law."""
        _, _, K1 = rc.off_centre_controller(MODEL, LAW)
        sim = RingParticleSim(n_keep=4, law=LAW, feedback={1: K1}, dt=0.25, guide_bandwidth=SIM_GUIDE)
        sim.perturb(1, 0.010)
        sim.perturb(2, 0.005, phase=0.7)
        sim.perturb(3, 0.003, phase=1.9)
        start = {n: sim.modal_state(n) for n in (1, 2, 3)}
        t, a, gaps, speeds = sim.run(2400.0, record=(1, 2, 3), every=80)
        self.assertLess(gaps.max(), 0.012)
        self.assertLess(speeds.max(), 1e-4)
        for i, n in enumerate((1, 2, 3)):
            A, B = MODEL.plant(n)
            K = rc.baseline_gain(MODEL, n, LAW, guide_bandwidth=SIM_GUIDE) + (K1 if n == 1 else 0)
            closed = A - B @ K
            predicted = np.array([(expm(closed * ti * OM) @ start[n])[0] * C.R for ti in t])
            self.assertLess(np.abs(a[:, i] - predicted).max(), 0.01 * np.abs(predicted).max(), f"mode {n}")
            self.assertLess(abs(a[-1, i]), 0.5 * abs(predicted[0]))

    def test_sudden_load_is_taken_up_as_predicted(self):
        n, load = 3, 1.0e-4
        sim = RingParticleSim(n_keep=4, law=LAW, dt=0.25, adapt=rc.ADAPT, guide_bandwidth=SIM_GUIDE)
        sim.load = load * np.cos(n * sim.th0)
        t, a, _, _ = sim.run(2400.0, record=(n,), every=160)
        closed = rc.adaptive_closed_loop(MODEL, n, LAW, guide_bandwidth=SIM_GUIDE)
        b = np.zeros(closed.shape[0], complex)
        b[1] = load / (C.m_passive * C.g_h)
        forced = np.linalg.solve(closed, b)
        predicted = np.array([((expm(closed * ti * OM) - np.eye(len(b))) @ forced)[0] * C.R for ti in t])
        self.assertLess(np.abs(a[:, 0] - predicted).max(), 0.02 * np.abs(predicted).max())
        self.assertGreater(a[:, 0].real.max(), 0.004)                     # it first moves the way it is pushed


if __name__ == "__main__":
    unittest.main()
