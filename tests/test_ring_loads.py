"""Loads that change: what the ring can carry with steering alone and with the
stators holding the long modes. Numbers quoted in the chapter on shape control."""
import math
import unittest

import numpy as np

from analysis import ring_control as rc
from analysis import ring_loads
from analysis.params import EARTH_500
from analysis.plots import stator_held_load
from analysis.ring_loads import RingLoads
from analysis.ring_modes import RingModes

G0 = 9.80665        # a "tonne" of load in the text is 1000 * G0 newtons
TONNE = 1000.0 * G0
N_MAX = 5000        # the sums have converged to 0.1% by here


class Base(unittest.TestCase):
    def about(self, value, expected, rel=0.02):
        self.assertLess(abs(value - expected), rel * abs(expected), f"{value} is not within {rel:.0%} of {expected}")


class StatorHeldModes(Base):
    @classmethod
    def setUpClass(cls):
        cls.loads = RingLoads(stator_modes=170)

    def test_every_stator_held_mode_decays(self):
        minutes = {n: -1.0 / self.loads.slowest_rate(n) / 60.0 for n in range(1, 171)}
        self.about(minutes[1], 113.0, 0.02)
        self.about(minutes[2], 29.0, 0.03)
        rest = [minutes[n] for n in range(3, 171)]
        self.assertGreater(min(rest), 14.0)
        self.assertLess(max(rest), 16.0)

    def test_steered_modes_above_them_still_decay(self):
        for n in (171, 300, 1000, 5000, 20000):
            self.assertLess(self.loads.slowest_rate(n), 0.0)

    def test_a_sudden_load_costs_no_offset_where_the_stators_hold(self):
        times = np.linspace(0.0, 4.0 * 3600.0, 400)
        steered = RingLoads(stator_modes=1).step(3, times) * 1.0e-4
        held = self.loads.step(3, times) * 1.0e-4
        self.about(np.abs(steered[:, :2]).max(), 0.017, 0.03)           # 17 mm with steering and set points
        self.assertLess(np.abs(held[:, :2]).max(), 1.0e-8)
        self.about(held[-1, 2].real, 1.9e-3, 0.03)                      # the structure settles 1.9 mm outward, with the load
        self.about(np.abs(held[-1, 3:]).max(), 0.04e-3, 0.03)           # slug speed changes by 0.04 mm/s

    def test_structure_settles_in_the_direction_of_the_load_not_at_the_funicular(self):
        c = self.loads.model.case
        for n in (2, 10, 100):
            final = self.loads.step(n, np.array([0.0, 3.0e5]))[-1, 2].real
            funicular = -1.0 / (c.Pi_total * (n / c.R) ** 2)
            self.assertGreater(final, 0.0)
            self.assertLess(funicular, 0.0)

    def test_tide(self):
        steered = RingLoads(stator_modes=1).tide()
        held = self.loads.tide()
        self.about(ring_loads.MOON_TIDE, 1.5 * 4.9048695e12 * EARTH_500.R / 3.844e8**3, 0.01)
        self.about(ring_loads.MOON_TIDE * (EARTH_500.m_passive + EARTH_500.lam_stream), 2.5e-3, 0.02)
        self.about(steered[:2].max(), 0.64, 0.03)                       # offset asked of steering
        self.about(RingLoads(stator_modes=1).tide(tangential=False)[:2].max(), 0.49, 0.03)
        self.assertLess(held[:2].max(), 1.0e-7)
        self.about(held[2], 0.06, 0.05)
        self.about(held[3:].max(), 1.3e-3, 0.03)

    def test_breathing_is_kicked_by_every_load(self):
        kick = self.loads.breathing_kick()
        c = self.loads.model.case
        # the ring's radial stiffness in the uniform mode, per metre: (m + lambda) Omega^2 (1 + EA / ((m + lambda) g R))
        mass = c.m_passive + c.lam_stream
        stiffness = mass * self.loads.model.omega**2 * (1.0 + 5.0e10 / (mass * c.g_h * c.R))
        self.about(kick["shift"], 1.0 / (2.0 * math.pi * c.R) / stiffness, 0.01)
        self.about(kick["shift"] * TONNE, 0.050, 0.02)
        self.about(kick["swing"], kick["shift"], 0.02)                  # undamped: it swings by as much again
        self.about(kick["period"] / 60.0, 83.0, 0.01)
        self.assertLess(kick["gap"] * TONNE, 1.0e-6)


class Margins(Base):
    """The stator feedback, designed on the nominal model, tried on a model that differs."""

    @classmethod
    def setUpClass(cls):
        cls.model = RingModes()
        cls.law = rc.reference_law(cls.model)
        cls.held = RingLoads(cls.model, stator_modes=170)

    def rate(self, n, model=None, gain=1.0, follow_error=None, **kw):
        model = model or self.model
        K = gain * self.held.stator_gain(n)
        if follow_error is None:
            return rc.slowest_rate(model, rc.closed_loop(model, n, rc.reference_law(model), mirror_from=n + 1, extra=K, **kw))
        law = self.law.with_(mirror=-(1.0 + follow_error), lead=0.0)       # the streams move (1 + error) times as far as the structure
        return rc.slowest_rate(model, rc.closed_loop(model, n, law, mirror_from=n, extra=K, **kw))

    def test_tolerated_by_every_mode(self):
        for n in (2, 5, 17, 30, 53, 100, 155, 170):
            for factor in (0.5, 3.0):
                self.assertLess(self.rate(n, RingModes(ea=5.0e10 * factor)), 0.0)
            for factor in (0.8, 1.2):
                self.assertLess(self.rate(n, RingModes(case=EARTH_500.with_(w_p=EARTH_500.w_p * factor))), 0.0)
            for change in (-30.0, 30.0):
                self.assertLess(self.rate(n, RingModes(case=EARTH_500.with_(u=EARTH_500.u + change))), 0.0)
            for gain in (0.5, 2.0):
                self.assertLess(self.rate(n, gain=gain), 0.0)
            for error in (-0.1, 0.01):
                self.assertLess(self.rate(n, follow_error=error), 0.0)
            self.assertLess(self.rate(n, filter_bandwidth=2.0 * math.pi * 3.0), 0.0)

    def test_first_thirty_modes_tolerate_the_rest_as_well(self):
        for n in (2, 5, 17, 30):
            self.assertLess(self.rate(n, follow_error=0.1), 0.0)
            self.assertLess(self.rate(n, filter_bandwidth=2.0 * math.pi * 0.3), 0.0)

    def test_where_the_margin_runs_out(self):
        self.assertLess(self.rate(165, follow_error=0.02), 0.0)
        self.assertGreater(self.rate(170, follow_error=0.02), 0.0)
        self.assertLess(self.rate(53, follow_error=0.1), 0.0)
        self.assertGreater(self.rate(54, follow_error=0.1), 0.0)
        self.assertLess(self.rate(154, filter_bandwidth=2.0 * math.pi), 0.0)
        self.assertGreater(self.rate(155, filter_bandwidth=2.0 * math.pi), 0.0)

    def test_least_damped_motion_is_the_spacing_wave(self):
        for n, ratio in ((30, 0.024), (170, 0.0042)):
            vals = np.linalg.eigvals(self.held.matrix(n))
            vals = vals[(np.abs(vals.imag) > 1e-6) & (np.abs(vals) < 1e3 * n)]
            damping = -vals.real / np.abs(vals)
            worst = vals[damping.argmin()]
            self.about(damping.min(), ratio, 0.05)
            self.about(abs(worst.imag), n * self.model.nu, 0.01)        # the slugs' transit frequency n u / R


class PointLoads(Base):
    @classmethod
    def setUpClass(cls):
        cls.table = ring_loads.capacity_table(n_max=N_MAX)

    def test_capacity_table(self):
        want = {1: (56.0, (8.2e3, 0.77e3, 76.0)), 30: (1.6e3, (157e3, 15e3, 1.8e3)), 170: (9.0e3, (876e3, 85e3, 10e3))}
        for count, (sudden, moving) in want.items():
            row = self.table[count]
            self.about(row["sudden"] / G0, sudden, 0.03)
            for got, expect in zip(row["moving"], moving):
                self.about(got / G0, expect, 0.03)

    def test_fast_loads_with_170_modes(self):
        loads = RingLoads(stator_modes=170)
        for speed in (2000.0, 3000.0):
            self.about(0.02 / loads.moving_point_load(speed, n_max=N_MAX)["gap"] / TONNE, 8.0, 0.06)

    def test_stator_limits(self):
        self.about(self.table[30]["authority"] / TONNE, 110.0, 0.03)
        self.about(self.table[170]["authority"] / TONNE, 16.0, 0.04)
        self.assertGreater(self.table[1]["authority"] / TONNE, 1000.0)

    def test_power_to_hold_a_load_that_stays(self):
        c = EARTH_500
        self.about(ring_loads.handled_power(1.0e-3), 82e6, 0.01)                    # per mm/s, each direction
        self.about(self.table[170]["resting_speed"] * TONNE, 0.061, 0.02)
        self.about(self.table[170]["resting_power"] * TONNE, 5.0e9, 0.02)
        self.about(self.table[30]["resting_power"] * TONNE, 0.7e9, 0.06)
        self.about(c.Pi_total * self.table[170]["resting_speed"] * TONNE / c.u, 1.0e6, 0.02)   # tension swing per tonne

    def test_guide_limit_rises_in_proportion_to_the_modes_the_stators_hold(self):
        self.about(self.table[170]["sudden"] / self.table[30]["sudden"], 170.0 / 30.0, 0.03)
        self.about(2.0 * math.pi * EARTH_500.R / 170.0, 250e3, 0.02)

    def test_slow_loads_are_carried_in_inverse_proportion_to_their_speed(self):
        for count in (1, 30, 170):
            ten, hundred, _ = self.table[count]["moving"]
            self.about(ten / hundred, 10.0, 0.08)

    def test_sums_have_converged(self):
        loads = RingLoads(stator_modes=30)
        times = np.concatenate([[0.0], np.geomspace(0.01, 2.0e5, 240)])
        coarse = loads.sudden_point_load(times, n_max=2000)["gap"].max()
        fine = loads.sudden_point_load(times, n_max=20000)["gap"].max()
        self.about(coarse, fine, 1e-3)

    def test_fast_step_response_agrees_with_direct_integration(self):
        from scipy.linalg import expm

        loads = RingLoads(stator_modes=30)
        for n in (3, 31, 1000):
            A = loads.matrix(n)
            size = A.shape[0]
            aug = np.zeros((size + 1, size + 1), complex)
            aug[:size, :size], aug[:size, size] = A, loads._load_vector(size)
            direct = loads.outputs(expm(aug * 1000.0 * loads.model.omega)[:size, size])
            fast = loads.step(n, np.array([1000.0]))[0]
            self.assertLess(np.abs(fast - direct)[:3].max(), 1e-3 * np.abs(direct[:3]).max())

    def test_early_response_is_the_spreading_kink_of_a_string(self):
        """Just after a point load goes on, the structure under it moves at
        F / (2 sqrt(T mu)) and the streams go the other way by c_m times that."""
        loads = RingLoads(stator_modes=1)
        c = loads.model.case
        tension, mass = 0.5 * c.Pi_total, c.m_passive - 0.5 * c.lam_stream
        rate = 1.5 / (2.0 * math.sqrt(tension * mass))
        gap = loads.sudden_point_load(np.array([0.0, 0.2, 0.4]), n_max=80000)["gap"]
        self.about((gap[2] - gap[1]) / 0.2, rate, 0.3)


class Simulation(Base):
    def test_particle_simulation_agrees_with_the_linear_model(self):
        times, data = stator_held_load.run(duration=1800.0, sample=300.0)
        sim, lin = data["sim"], data["linear"]
        scale_w, scale_u = np.abs(lin[:, 0]).max(), np.abs(lin[:, 2]).max()
        self.assertLess(np.abs(sim[:, 0] - lin[:, 0]).max(), 0.01 * scale_w)
        self.assertLess(np.abs(sim[:, 2] - lin[:, 2]).max(), 0.01 * scale_u)
        self.assertLess(sim[:, 1].max(), 3.0e-6)                       # offsets stay under 3 micrometres
        # the load in that run against what eight tonnes would put into one mode
        self.about(8.0 * TONNE / (math.pi * EARTH_500.R) / 1.0e-4, 36.0, 0.03)


if __name__ == "__main__":
    unittest.main()
