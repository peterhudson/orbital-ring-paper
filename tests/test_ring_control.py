"""Holding the whole ring: the structured law, the stators' part in it, and
runs of the controllers on the nonlinear particle simulation."""
import math
import unittest

import numpy as np
from scipy.linalg import expm

from analysis import ring_control as rc
from analysis.collective import CollectiveModel
from analysis.params import EARTH_500 as C
from analysis.ring_modes import FOLLOW, LATERAL, GuideLaw, RingModes, out_of_plane_rate
from analysis.ring_particles import RingParticleSim

MODEL = RingModes()
OM = MODEL.omega
LAW = rc.reference_law(MODEL)
SIM = dict(guide_bandwidth=0.5, filter_bandwidth=1.5)      # rad/s: the slow loops used in the particle simulation


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

    def test_gain_has_a_lower_limit_at_the_lowest_modes(self):
        """With the stators' soft hold, mode 2 needs a mirror gain above
        about 0.36, mode 3 above about 0.16."""
        rate = lambda n, c0: MODEL.growth_rate(n, LAW.with_(mirror=c0)) / OM
        self.assertGreater(rate(2, 0.3), 0.0)
        self.assertLess(rate(2, 0.4), 0.0)
        self.assertGreater(rate(3, 0.12), 0.0)
        self.assertLess(rate(3, 0.2), 0.0)
        self.assertLess(rate(2, 0.7), 0.0)

    def test_reference_law_with_a_real_guide_and_set_points(self):
        """Guide at 10 Hz, path command lagging at 1 kHz, with and without
        set-point adaptation. The look-ahead here is a pure phase, so the
        model stops being meaningful where that phase is shorter than the
        20 m floor of the local model."""
        for n in (2, 3, 4, 6, 10, 30, 100, 300, 1000, 3000, 10000, 30000):
            self.assertLess(rc.slowest_rate(MODEL, rc.closed_loop(MODEL, n, LAW)) / OM, -0.2, f"n {n}")
            self.assertLess(rc.slowest_rate(MODEL, rc.closed_loop(MODEL, n, LAW, adapt=rc.ADAPT)) / OM, -0.08, f"n {n}, adapting")
        self.about(LAW.lead * MODEL.case.R / 30000, 69, 0.01)             # look-ahead at n = 30,000, m

    def test_feedforward_is_what_makes_a_slow_guide_enough(self):
        """With the simulation's slow loops the closed loop still matches
        ideal tracking, because the guide is told what the path will ask."""
        for n in (2, 5, 20, 60):
            self.about(rc.slowest_rate(MODEL, rc.closed_loop(MODEL, n, LAW, **SIM)), MODEL.growth_rate(n, LAW), 0.02)

    def test_set_point_rate_has_a_margin_of_about_two(self):
        self.assertLess(rc.slowest_rate(MODEL, rc.closed_loop(MODEL, 2, LAW, adapt=0.05)), 0.0)
        self.assertGreater(rc.slowest_rate(MODEL, rc.closed_loop(MODEL, 2, LAW, adapt=0.08)), 0.0)

    def test_out_of_plane_modes_decay(self):
        for n in (1, 2, 3, 10, 100, 1000):
            self.assertLess(out_of_plane_rate(n, mirror=LAW.mirror, lead=LAW.lead).real, -0.5 * OM)
        self.about(out_of_plane_rate(2).real, math.sqrt(3) * OM, 1e-9)

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

    def test_steering_alone_needs_two_to_four_times_the_error_in_offset(self):
        for n, quoted in ((1, 3.6), (2, 2.7), (3, 2.4), (10, 2.0), (30, 1.8)):
            K = rc.lqr_gain(MODEL, n, inputs=LATERAL, scales=rc.steering_scales(MODEL))
            self.assertLess(MODEL.closed_loop_eigenvalues(n, K)[0].real, 0.0)
            self.about(rc.steering_gap_per_metre(MODEL, n), quoted, 0.03)
            out = rc.recovery(MODEL, n, K, rc.unstable_direction(MODEL, n), duration=120.0 / MODEL.growth_rate(n), samples=6000)
            self.assertLess(abs(out["w"][-1]), 0.02)                     # and the shape does come back

    def test_stators_hold_the_low_modes_with_small_speed_changes(self):
        """Peak speed change per metre of error on the growing mode, with the
        guide following and the stators' soft hold in place."""
        hold = LAW.with_(mirror=None, lead=0.0)
        for n, quoted in ((1, 0.010), (2, 0.017), (3, 0.028), (10, 0.29), (30, 2.9)):
            closed, _, _ = rc.stator_lqr(MODEL, n, hold, rc.Scales(shape=10.0))
            self.assertLess(np.linalg.eigvals(closed).real.max(), -0.1)
            self.about(rc.stator_speed_per_metre(MODEL, n, hold), quoted, 0.05)
        self.about(rc.stator_speed_per_metre(MODEL, 30, hold) / rc.stator_speed_per_metre(MODEL, 10, hold), 9.0, 0.15)     # roughly n squared

    def test_where_each_actuator_wins(self):
        hold = LAW.with_(mirror=None, lead=0.0)
        self.about(1.0 / rc.stator_speed_per_metre(MODEL, 1, hold), 100, 0.05)       # metres recovered with 1 m/s
        self.about(1.0 / rc.stator_speed_per_metre(MODEL, 30, hold), 0.35, 0.03)
        self.assertGreater(1.0 / rc.stator_speed_per_metre(MODEL, 160, hold), 0.01)  # 1 m/s still recovers 10 mm
        self.assertLess(1.0 / rc.stator_speed_per_metre(MODEL, 180, hold), 0.01)
        self.about(2 * math.pi * C.R / 170, 250e3, 0.02)
        self.assertTrue(0.005 < 0.02 / rc.steering_gap_per_metre(MODEL, 1) < 0.02 / rc.steering_gap_per_metre(MODEL, 30) < 0.012)
        self.about(1e-4 * C.lam_stream * C.g_h, 1.4, 0.02)                           # weight moved by 1e-4 of speed, N/m

    def test_off_centre_controller(self):
        closed, _, _ = rc.off_centre_controller(MODEL, LAW)
        self.about(np.linalg.eigvals(closed).real.max(), -0.13, 0.05)      # in units of the orbital rate
        self.about(-1.0 / (np.linalg.eigvals(closed).real.max() * OM) / 3600, 1.9, 0.03)      # hours
        self.about(1.0 / OM / 60, 15, 0.01)                                # the stators' soft hold, minutes
        per_metre = rc.stator_speed_per_metre(MODEL, 1, rc.law_for_mode(1, LAW))
        self.about(per_metre, 0.010, 0.05)
        self.about(100 * per_metre / C.u, 1e-4, 0.05)                      # a 100 m offset, as a fraction of stream speed
        self.about(MODEL.growth_rate(1, rc.law_for_mode(1, LAW)) / OM, 1.29, 0.01)             # what it has to overcome


class SteadyLoads(Base):
    def test_set_points_put_the_ring_on_the_funicular_with_no_offset(self):
        for n, per_newton in ((2, 66), (3, 31), (10, 2.9), (30, 0.32)):
            w, offset = rc.static_response(MODEL, rc.closed_loop(MODEL, n, LAW, adapt=rc.ADAPT))
            self.about(w, -per_newton, 0.02)
            self.about(w, -C.R**2 / (C.Pi_total * n * n), 0.1)
            self.assertLess(offset, 1e-4 * abs(w))

    def test_without_them_the_offset_needed_is_hopeless(self):
        w, offset = rc.static_response(MODEL, rc.closed_loop(MODEL, 2, LAW))
        self.about(w, 560, 0.01)
        self.about(offset, 830, 0.01)
        self.about(0.02 / offset * math.pi * C.R, 520, 0.02)        # the point load whose n = 2 part fills 20 mm, N

    def test_moon_tide_is_too_much_for_the_guide(self):
        gm_moon, distance = 4.9028e12, 3.844e8
        load = (C.m_passive + C.lam_stream) * 1.5 * gm_moon * C.R / distance**3       # radial part, two waves round the ring
        self.about(load, 2.5e-3, 0.03)
        self.about(load / (C.lam_stream * C.g_h) * C.u, 1.8e-3, 0.03)                 # the speed ripple that cancels it
        # forced response at the tide's period as seen from a ring turning with the Earth
        matrix = rc.closed_loop(MODEL, 2, LAW, adapt=rc.ADAPT)
        b = np.zeros(matrix.shape[0], complex)
        b[1] = load / (C.m_passive * C.g_h)
        forcing = 2 * math.pi / (12.42 * 3600) / OM
        x = np.linalg.solve(1j * forcing * np.eye(len(b)) - matrix, b) * C.R
        offset = max(abs(x[4] - x[0]), abs(x[8] - x[0]))
        self.assertTrue(0.2 < offset < 1.0)
        self.assertTrue(0.1 < abs(x[0]) < 0.6)


class ParticleSimulation(Base):
    def predicted(self, n, start, times, **kw):
        matrix = rc.closed_loop(MODEL, n, LAW, **SIM, **kw)
        return np.array([expm(matrix * t * OM) @ start[:matrix.shape[0]] for t in times]) * C.R

    def test_perturbed_ring_returns_to_round_as_predicted(self):
        """Modes 1, 2 and 3 displaced by millimetres; mode 1 held by the
        stators, the others by the structured law."""
        _, _, K1 = rc.off_centre_controller(MODEL, LAW)
        sim = RingParticleSim(n_keep=4, law=LAW, feedback={1: K1}, dt=0.25, **SIM)
        sim.perturb(1, 0.010)
        sim.perturb(2, 0.005, phase=0.7)
        sim.perturb(3, 0.003, phase=1.9)
        start = {n: sim.full_state(n) for n in (1, 2, 3)}
        t, a, gaps, speeds = sim.run(2400.0, record=(1, 2, 3), every=80)
        self.assertLess(gaps.max(), 0.012)
        self.assertLess(speeds.max(), 1e-4)
        for i, n in enumerate((1, 2, 3)):
            predicted = self.predicted(n, start[n], t, extra=K1 if n == 1 else None)[:, 0]
            self.assertLess(np.abs(a[:, i] - predicted).max(), 0.01 * np.abs(predicted).max(), f"mode {n}")
            self.assertLess(abs(a[-1, i]), 0.5 * abs(predicted[0]))

    def test_many_modes_at_once(self):
        """Every mode from 1 to 8 displaced at random by a millimetre or two."""
        top = 8
        _, _, K1 = rc.off_centre_controller(MODEL, LAW)
        sim = RingParticleSim(n_nodes=16 * top, slugs_per_direction=80 * top, n_keep=top, law=LAW, feedback={1: K1}, dt=0.25, **SIM)
        rng = np.random.default_rng(1)
        modes = range(1, top + 1)
        for n in modes:
            sim.perturb(n, 0.002 * rng.uniform(0.5, 1.0), phase=rng.uniform(0.0, 2.0 * math.pi))
        start = {n: sim.full_state(n) for n in modes}
        t, a, gaps, _ = sim.run(1800.0, record=tuple(modes), every=120)
        rms = lambda row: math.sqrt(0.5 * (np.abs(row) ** 2).sum())
        self.assertLess(rms(a[-1]), 0.3 * rms(a[0]))
        self.assertLess(gaps.max(), 0.012)
        for i, n in enumerate(modes):
            predicted = self.predicted(n, start[n], t, extra=K1 if n == 1 else None)[:, 0]
            self.assertLess(np.abs(a[:, i] - predicted).max(), 0.03 * np.abs(predicted).max(), f"mode {n}")

    def test_sudden_load_is_taken_up_as_predicted(self):
        n, load = 3, 1.0e-4
        _, _, K1 = rc.off_centre_controller(MODEL, LAW)
        sim = RingParticleSim(n_keep=4, law=LAW, feedback={1: K1}, dt=0.25, adapt=rc.ADAPT, **SIM)
        sim.load = load * np.cos(n * sim.th0)
        times, shape, offset = [], [], []
        for i in range(int(2400.0 / sim.dt)):
            sim.step()
            if (i + 1) % 160 == 0:
                state = sim.modal_state(n) * C.R
                times.append(sim.t)
                shape.append(state[0])
                offset.append(state[4] - state[0])
        matrix = rc.closed_loop(MODEL, n, LAW, adapt=rc.ADAPT, **SIM)
        b = np.zeros(matrix.shape[0], complex)
        b[1] = load / (C.m_passive * C.g_h)
        forced = np.linalg.solve(matrix, b)
        x = np.array([(expm(matrix * t * OM) - np.eye(len(b))) @ forced for t in times]) * C.R
        self.assertLess(np.abs(np.array(shape) - x[:, 0]).max(), 0.02 * np.abs(x[:, 0]).max())
        self.assertLess(np.abs(np.array(offset) - (x[:, 4] - x[:, 0])).max(), 0.02 * np.abs(x[:, 4] - x[:, 0]).max())
        self.assertGreater(np.array(shape).real.max(), 0.004)                 # it first moves the way it is pushed
        self.about(np.abs(np.array(offset)).max(), 0.017, 0.1)                 # 17 mm of offset for 0.1 mN/m


if __name__ == "__main__":
    unittest.main()
