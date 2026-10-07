"""How the controlled ring answers loads that change: a point load put on
suddenly, and a point load that moves along the ring.

Two arrangements are compared.

* The baseline of analysis/ring_control.py: the mirror law steers every mode
  from n = 2 up, and the stators hold only the off-center mode.
* Stators holding the first `stator_modes` modes by optimal feedback while the
  streams follow the structure in those modes, and the mirror law steering the
  rest. Mode 1 keeps the off-center controller of analysis/ring_control.py;
  the others use the tuning `SCALES`, chosen for its margins (see
  tests/test_ring_loads.py).

A point load W at angle phi0 on the ring is the sum over modes

    q(theta) = W / (2 pi R) * sum_n exp(i n (theta - phi0)),

so every mode n >= 1 carries a load of amplitude W / (pi R). Each mode's
response comes from its closed-loop matrix, and the modes are added up at the
place of interest. Mode numbers run to `n_max`; the sums have converged to
0.1% by 5,000. The uniform part, n = 0, adds no stream offset and is treated
separately in `breathing_kick`.

"Tonnes" of load in the text are tonnes-force: 9.80665 kN each.
"""
from __future__ import annotations


import numpy as np

from . import ring_control as rc
from .ring_modes import RingModes

SCALES = rc.Scales(shape=10.0, stator=0.1)
MOON_TIDE = 8.9e-7      # m/s^2: amplitude of the Moon's tidal acceleration at the ring, radial and along-track


class RingLoads:
    def __init__(self, model: RingModes | None = None, stator_modes: int = 1, adapt: float = rc.ADAPT, scales: rc.Scales = SCALES):
        self.model = model or RingModes()
        self.law = rc.reference_law(self.model)
        self.stator_modes = max(1, int(stator_modes))
        self.adapt = adapt
        self.scales = scales
        self._cache: dict[int, np.ndarray] = {}

    # -- one mode -------------------------------------------------------------
    def matrix(self, n: int) -> np.ndarray:
        """Closed-loop matrix of mode n under this arrangement, nondimensional."""
        if n not in self._cache:
            if n == 0:
                # n = 0 has several zero eigenvalues, and with the 1 kHz command filter the
                # eigenproblem is too ill-conditioned to give the breathing frequency to
                # better than 2%. A 100 Hz filter changes nothing physical and cures that.
                out = rc.closed_loop(self.model, 0, self.law, filter_bandwidth=2.0 * np.pi * 100.0)
            elif n <= self.stator_modes:
                out = rc.closed_loop(self.model, n, self.law, mirror_from=n + 1, extra=self.stator_gain(n))
            else:
                out = rc.closed_loop(self.model, n, self.law, adapt=self.adapt)
            self._cache[n] = out
        return self._cache[n]

    def stator_gain(self, n: int) -> np.ndarray:
        """Stator feedback for a stator-held mode n, on the plant's states."""
        if n == 1:
            return rc.off_centre_controller(self.model, self.law)[2]
        return rc.stator_lqr(self.model, n, rc.law_for_mode(1, self.law), self.scales)[2]

    def _load_vector(self, size: int) -> np.ndarray:
        """Input vector of a radial load of 1 N/m on the structure."""
        c = self.model.case
        b = np.zeros(size, complex)
        b[1] = 1.0 / (c.m_passive * c.g_h)
        return b

    def outputs(self, x: np.ndarray) -> np.ndarray:
        """From state(s) x (last axis): the two streams' offsets from the structure, the
        structure's radial displacement, and the two streams' speed changes; m and m/s."""
        c, om = self.model.case, self.model.omega
        (_, v1), (_, v2) = self.model._streams()
        gap1, gap2 = x[..., 4] - x[..., 0], x[..., 8] - x[..., 0]
        sp1, sp2 = x[..., 6] + v1 * x[..., 4], x[..., 10] + v2 * x[..., 8]
        return np.stack([gap1 * c.R, gap2 * c.R, x[..., 0] * c.R, sp1 * c.R * om, sp2 * c.R * om], axis=-1)

    def harmonic(self, n: int, omega: float) -> np.ndarray:
        """Steady response of mode n to a load exp(i omega t) of 1 N/m (omega in rad/s): `outputs`."""
        A = self.matrix(n)
        x = np.linalg.solve(1j * omega / self.model.omega * np.eye(A.shape[0]) - A, self._load_vector(A.shape[0]))
        return self.outputs(x)

    def step(self, n: int, times: np.ndarray) -> np.ndarray:
        """Response of mode n to a load of 1 N/m put on at t = 0: `outputs` at each of `times` (s)."""
        A = self.matrix(n)
        vals, vecs = np.linalg.eig(A)
        forced = np.linalg.solve(A, self._load_vector(A.shape[0]))
        coeff = np.linalg.solve(vecs, forced)
        growth = np.exp(np.outer(np.asarray(times) * self.model.omega, vals)) - 1.0     # (time, eigen)
        return self.outputs((growth * coeff) @ vecs.T)

    def slowest_rate(self, n: int) -> float:
        return rc.slowest_rate(self.model, self.matrix(n))

    def tide(self, period: float = 12.42 * 3600.0, amplitude: float = MOON_TIDE, tangential: bool = True) -> np.ndarray:
        """Steady response to the Moon's tide: a body force on structure and
        slugs alike with two waves round the ring, a cos(2 phi) outward and
        -a sin(2 phi) along the ring, turning past the ring once in `period`.
        Returns the magnitudes of `outputs`."""
        A = self.matrix(2)
        g = self.model.case.g_h
        b = np.zeros(A.shape[0], complex)
        b[[1, 5, 9]] = amplitude / g
        if tangential:
            b[[3, 6, 10]] = 1j * amplitude / g
        omega = -2.0 * np.pi / period / self.model.omega
        return np.abs(self.outputs(np.linalg.solve(1j * omega * np.eye(A.shape[0]) - A, b)))

    def breathing_kick(self, periods: float = 6.0, samples: int = 1200) -> dict:
        """What the uniform part of a point load of 1 N does. It is a load of
        1 / (2 pi R) per metre in the mode n = 0, which nothing in this model
        damps. Returns the mean shift of the ring's radius (`shift`, m per
        newton), the amplitude of the oscillation about it that a sudden load
        starts (`swing`), its period (s), and the largest speed change (m/s
        per newton)."""
        from scipy.linalg import expm

        A = self.matrix(0)
        size = A.shape[0]
        vals = np.linalg.eigvals(A)
        osc = vals[np.abs(vals.imag) > 1e-6]
        period = 2.0 * np.pi / np.abs(osc.imag).min()                     # nondimensional
        aug = np.zeros((size + 1, size + 1), complex)
        aug[:size, :size] = A
        aug[:size, size] = self._load_vector(size) / (2.0 * np.pi * self.model.case.R)
        step = expm(aug * (periods * period / samples))
        x = np.zeros(size + 1, complex)
        x[size] = 1.0
        rows = []
        for _ in range(samples + 1):
            rows.append(self.outputs(x[:size]).real)
            x = step @ x
        rows = np.array(rows)
        w = rows[:, 2]
        return dict(shift=float(w.mean()), swing=float(0.5 * (w.max() - w.min())), period=float(period / self.model.omega),
                    speed=float(np.abs(rows[:, 3:]).max()), gap=float(np.abs(rows[:, :2]).max()))

    # -- a point load ---------------------------------------------------------
    def _modes(self, n_max: int) -> np.ndarray:
        """Mode numbers used in the sums: every one up to 400, then spaced by 1% and weighted."""
        dense = np.arange(1, min(n_max, 400) + 1)
        if n_max <= 400:
            return dense, np.ones(len(dense))
        sparse = np.unique(np.round(np.geomspace(401, n_max, int(np.log(n_max / 401.0) / 0.01) + 2)).astype(int))
        edges = np.concatenate([[400.5], 0.5 * (sparse[1:] + sparse[:-1]), [n_max + 0.5]])
        return np.concatenate([dense, sparse]), np.concatenate([np.ones(len(dense)), np.diff(edges)])

    def sudden_point_load(self, times: np.ndarray, n_max: int = 20000, angles=(0.0,)) -> dict:
        """A point load of 1 N put on at t = 0. Returns, at each time, the
        largest stream offset from the structure over `angles` (rad from the
        load) and over the two streams, the structure's displacement under the
        load, and the largest speed change, per newton."""
        c = self.model.case
        modes, weights = self._modes(n_max)
        amp = 1.0 / (np.pi * c.R)
        total = np.zeros((len(angles), len(times), 5), complex)
        for n, w in zip(modes, weights):
            resp = self.step(int(n), times) * (amp * w)
            for j, ang in enumerate(angles):
                total[j] += resp * np.exp(1j * n * ang)
        real = total.real
        gap = np.abs(real[..., :2]).max(axis=(0, 2))
        return dict(gap=gap, shape=real[0, :, 2], speed=np.abs(real[..., 3:]).max(axis=(0, 2)))

    def moving_point_load(self, speed: float, n_max: int = 20000) -> dict:
        """A point load of 1 N moving along the ring at `speed` (m/s, relative
        to the structure, positive toward +s), long after the start; `speed`
        zero is a load that has always been there. Returns the largest stream
        offset and the largest speed change anywhere on the ring, per newton,
        and the profiles against angle from the load."""
        c = self.model.case
        modes, weights = self._modes(n_max)
        rate = speed / c.R                                    # rad/s
        phi = np.unique(np.concatenate([np.linspace(-np.pi, np.pi, 1441), np.linspace(-0.3, 0.3, 1201)]))
        samples = len(phi)
        total = np.zeros((samples, 5), complex)
        for n, w in zip(modes, weights):
            resp = self.harmonic(int(n), -n * rate) * (w / (np.pi * c.R))
            total += np.exp(1j * n * phi)[:, None] * resp[None, :]
        real = total.real
        return dict(gap=np.abs(real[:, :2]).max(), speed=np.abs(real[:, 3:]).max(), phi=phi, gaps=real[:, :2], shape=real[:, 2], speeds=real[:, 3:])


def guide_room_capacity(gap_per_newton: float, room: float = 0.02) -> float:
    """Largest point load, N, that keeps every stream within `room` of the structure."""
    return room / gap_per_newton


def authority_capacity(speed_per_newton: float, authority: float = 1.0) -> float:
    """Largest point load, N, that the stators answer with no more than `authority` m/s of speed change."""
    return authority / speed_per_newton


def handled_power(speed_change: float, model: RingModes | None = None) -> float:
    """Power taken out of one direction's streams where they are slowed by
    `speed_change` (m/s), and put back where they speed up again, W: the
    mass flux of that direction times u times the speed change."""
    c = (model or RingModes()).case
    return 0.5 * c.Pi_total * speed_change


ARRANGEMENTS = (1, 30, 170)      # how many of the longest modes the stators hold


def capacity_table(speeds=(10.0, 100.0, 1000.0), arrangements=ARRANGEMENTS, n_max: int = 20000, room: float = 0.02, authority: float = 1.0) -> dict:
    """For each arrangement: the point load (N) that fills `room` of guide when
    put on suddenly and when moving at each of `speeds`; the load whose sudden
    arrival or passage takes all of the stators' `authority`; the structure's
    largest displacement under a sudden 10 kN (m, modes 1 up); and the speed
    change (m/s) and handled power (W, each direction) per newton of a load
    that stays."""
    times = np.concatenate([[0.0], np.geomspace(0.01, 2.0e5, 240)])
    out = {}
    for count in arrangements:
        loads = RingLoads(stator_modes=count)
        sudden = loads.sudden_point_load(times, n_max=n_max, angles=(0.0, 0.01, 0.1, 1.0))
        moving = [loads.moving_point_load(v, n_max=n_max) for v in speeds]
        resting = loads.moving_point_load(0.0, n_max=n_max)
        out[count] = dict(
            resting_speed=resting["speed"],
            resting_power=handled_power(resting["speed"], loads.model),
            sudden=room / sudden["gap"].max(),
            sudden_time=float(times[sudden["gap"].argmax()]),
            moving=[room / m["gap"] for m in moving],
            authority=authority / max(sudden["speed"].max(), *(m["speed"] for m in moving)),
            shape_10kN=float(np.abs(sudden["shape"]).max() * 1.0e4),
        )
    return out
