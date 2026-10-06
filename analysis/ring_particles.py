"""Nonlinear particle simulation of the whole ring in its own plane.

The structure is a ring of nodes joined by hoop springs, in the planet's
inverse-square field. Each stream is a train of point masses in the same
field. A slug feels gravity, the guide's push at right angles to the
structure, and, if the stators are in use, a push along it. Every push on a
slug is put back on the structure. Nothing is linearised, no wavelength is
singled out, and the stream is made of separate slugs.

Its job is to check analysis/ring_modes.py, which is linear and works one
mode at a time, and to run controllers designed there on something closer
to the real thing.

The ring's short waves grow fastest (the rate is roughly n times the orbital
rate), so a simulation that kept every wavelength the mesh can hold would be
swamped by the shortest of them within minutes. Forces on the structure are
therefore filtered to the modes n <= n_keep; shorter waves are the business
of analysis/particles.py.
"""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass, field

import numpy as np

from .params import EARTH_500, RefCase
from .ring_modes import FOLLOW, GuideLaw


@dataclass
class RingParticleSim:
    case: RefCase = EARTH_500
    ea: float = 5.0e10                 # hoop stiffness, N
    n_nodes: int = 120
    slugs_per_direction: int = 600
    dt: float = 0.1                    # s
    n_keep: int = 3                    # highest structural mode kept
    law: GuideLaw = FOLLOW
    mirror_from: int = 2               # lowest mode the mirror law is applied to; lower modes follow
    guide_bandwidth: float = 0.5       # of the guide's hold on the commanded path, rad/s
    guide_zeta: float = 0.7
    feedback: dict | None = None       # extra state feedback, {n: K} with K as in ring_modes.RingModes.plant
    adapt: float = 0.0                 # set-point adaptation rate, as a fraction of the stream's transit rate n u / R
    load: np.ndarray | None = None     # radial dead load on the structure at each node, N/m (outward positive)
    fine: int = 8                      # the shape is rebuilt on fine * n_nodes points for interpolation
    t: float = field(init=False, default=0.0)

    def __post_init__(self):
        c, N, P = self.case, self.n_nodes, self.slugs_per_direction
        if self.n_keep >= N // 2:
            raise ValueError("n_keep must be below half the number of nodes")
        self.R, self.gm, self.u = c.R, c.body.gm, c.u
        self.omega = c.omega_orb
        self.dth = 2.0 * math.pi / N
        self.th0 = self.dth * np.arange(N)
        self.er0 = np.column_stack([np.cos(self.th0), np.sin(self.th0)])
        self.et0 = np.column_stack([-np.sin(self.th0), np.cos(self.th0)])
        self.X = self.R * self.er0
        self.V = np.zeros_like(self.X)
        self.rest = 2.0 * self.R * math.sin(math.pi / N)
        self.node_mass = c.m_passive * self.R * self.dth
        self.slug_mass = 0.5 * c.lam_stream * 2.0 * math.pi * self.R / P
        base = 2.0 * math.pi * (np.arange(P) + 0.5) / P
        self.w0 = np.concatenate([np.full(P, self.u / self.R), np.full(P, -self.u / self.R)])
        self.phi_nominal = np.concatenate([base, base + 0.37 * 2.0 * math.pi / P])
        self.phi = self.phi_nominal.copy()
        self.phid = self.w0.copy()
        self.r = np.full(2 * P, self.R)
        self.rd = np.zeros(2 * P)
        self.stream = (slice(0, P), slice(P, 2 * P))
        self._modes = np.arange(N // 2 + 1)
        self._keep = self._modes <= self.n_keep
        self._M = self.fine * N
        self.set_point = np.zeros(N // 2 + 1, complex)      # rfft coefficients of the set-point field, m

    # ---- the structure's shape as fields ---------------------------------------------
    def structure_fields(self):
        """Radial and tangential displacement of the nodes and their rates, m and m/s."""
        r = np.hypot(self.X[:, 0], self.X[:, 1])
        er = self.X / r[:, None]
        et = np.column_stack([-er[:, 1], er[:, 0]])
        dth = np.angle(np.exp(1j * (np.arctan2(self.X[:, 1], self.X[:, 0]) - self.th0)))
        return r - self.R, self.R * dth, (self.V * er).sum(1), (self.V * et).sum(1), er, et, dth

    def _fine(self, coeffs, derivative=False):
        ck = np.where(self._keep, coeffs, 0.0)
        if derivative:
            ck = 1j * self._modes * ck
        return np.fft.irfft(ck, self.n_nodes) if self.fine == 1 else np.fft.irfft(np.concatenate([ck, np.zeros(self._M // 2 + 1 - len(ck))]), self._M) * self.fine

    def _at(self, values, phi):
        x = (phi % (2.0 * math.pi)) / (2.0 * math.pi) * self._M
        j = np.floor(x).astype(int) % self._M
        f = x - np.floor(x)
        return (1.0 - f) * values[j] + f * values[(j + 1) % self._M]

    def _path_gain(self, sign):
        """Commanded path as a multiple of the structure's shape, mode by mode."""
        c = np.ones(len(self._modes), complex)
        if self.law.mirror is not None:
            c[self._modes >= self.mirror_from] = -self.law.mirror * cmath.exp(1j * sign * self.law.lead)
        return c

    def _set_point_rate(self, wk):
        """Rate of change of the set point: proportional to the mean gap,
        mode by mode, for the modes the mirror law steers."""
        rate = np.zeros_like(self.set_point)
        if not self.adapt or self.law.mirror is None:
            return rate
        N = self.n_nodes
        for n in range(self.mirror_from, self.n_keep + 1):
            eta = sum(np.mean((self.r[sl] - self.R) * np.exp(-1j * n * self.phi[sl])) for sl in self.stream) / 2.0
            gap = eta * N - wk[n]                     # in the scaling of rfft
            rate[n] = self.adapt * n * (self.u / self.R) * gap
        return rate

    # ---- modal amplitudes ---------------------------------------------------------------
    def mode(self, n: int) -> complex:
        """Complex amplitude of the structure's radial displacement in mode n, m."""
        w = self.structure_fields()[0]
        return (2.0 if n else 1.0) * np.mean(w * np.exp(-1j * n * self.th0))

    def modal_state(self, n: int) -> np.ndarray:
        """State of mode n in the units and order of ring_modes.RingModes.plant."""
        w, v, wd, vd = self.structure_fields()[:4]
        f = 2.0 if n else 1.0
        R, Om = self.R, self.omega
        e = np.exp(-1j * n * self.th0)
        x = [f * np.mean(w * e) / R, f * np.mean(wd * e) / (R * Om), f * np.mean(v * e) / R, f * np.mean(vd * e) / (R * Om)]
        for q, sl in enumerate(self.stream):
            w0 = self.w0[sl][0]
            e = np.exp(-1j * n * self.phi[sl])
            eta = f * np.mean((self.r[sl] - R) * e) / R
            eta_t = f * np.mean(self.rd[sl] * e) / (R * Om) - 1j * n * (w0 / Om) * eta
            om = f * np.mean((self.phid[sl] - w0) * e) / Om
            xi = f * np.mean((self.phi[sl] - self.phi_nominal[sl]) * e)
            x += [eta, eta_t, om, xi]
        return np.array(x)

    def gap(self) -> np.ndarray:
        """Radial offset of every slug from the structure at its position, m."""
        w = self._fine(np.fft.rfft(self.structure_fields()[0]))
        return self.r - self.R - self._at(w, self.phi)

    def speed_deviation(self) -> np.ndarray:
        """Each slug's speed minus the nominal stream speed, m/s."""
        return np.hypot(self.rd, self.r * self.phid) - self.u

    # ---- set-up ---------------------------------------------------------------------------
    def perturb(self, n: int, amplitude: float, phase: float = 0.0):
        """Displace the structure in mode n without stretching it, and put
        the slugs on their commanded paths."""
        th = self.th0
        w = amplitude * np.cos(n * th + phase)
        v = -(amplitude / n) * np.sin(n * th + phase) if n else np.zeros_like(th)
        self.X = self.X + w[:, None] * self.er0 + v[:, None] * self.et0
        wk = np.fft.rfft(self.structure_fields()[0])
        for q, sl in enumerate(self.stream):
            sign = 1.0 if q == 0 else -1.0
            path = self._fine(self._path_gain(sign) * wk)
            slope = self._fine(self._path_gain(sign) * wk, derivative=True)
            self.r[sl] = self.R + self._at(path, self.phi[sl])
            self.rd[sl] = self.phid[sl] * self._at(slope, self.phi[sl])

    # ---- one step ---------------------------------------------------------------------------
    def step(self):
        dt, R, N = self.dt, self.R, self.n_nodes
        w, v, wd, vd, er, et, dth_node = self.structure_fields()
        wk, vk, wdk, vdk = (np.fft.rfft(a) for a in (w, v, wd, vd))
        shape, slope = self._fine(wk), self._fine(wk, derivative=True)
        K, C = self.guide_bandwidth**2, 2.0 * self.guide_zeta * self.guide_bandwidth
        a_r = np.empty_like(self.r)
        a_s = np.zeros_like(self.r)                  # stators, along the track
        law = self.law
        if law.speed_rate or law.lock_rate:
            v_f, v_slope, vd_f = self._fine(vk), self._fine(vk, derivative=True), self._fine(vdk)
        zk, zdk = self.set_point, self._set_point_rate(wk)
        for q, sl in enumerate(self.stream):
            sign = 1.0 if q == 0 else -1.0
            gain = self._path_gain(sign)
            path, path_slope, path_rate = self._fine(gain * wk + zk), self._fine(gain * wk + zk, derivative=True), self._fine(gain * wdk + zdk)
            phi, phid = self.phi[sl], self.phid[sl]
            err = self.r[sl] - R - self._at(path, phi)
            err_rate = self.rd[sl] - (self._at(path_rate, phi) + phid * self._at(path_slope, phi))
            a_r[sl] = -(self.r[sl] * phid**2 - self.gm / self.r[sl] ** 2) - K * err - C * err_rate
            if law.speed_rate or law.lock_rate:
                w0 = self.w0[sl][0]
                if law.reference == "bucket":
                    ref_pos = self._at(v_f, phi) / R
                    ref_rate = (self._at(vd_f, phi) + w0 * self._at(v_slope, phi)) / R
                    d_pos = (phi - self.phi_nominal[sl]) - ref_pos
                    d_rate = (phid - w0) - ref_rate
                    d_pos, d_rate = d_pos - d_pos.mean(), d_rate - d_rate.mean()     # the mean is left to coast
                    a_s[sl] = -R * (law.speed_rate * d_rate + law.lock_rate * d_pos)
                else:
                    raise NotImplementedError(law.reference)
        if self.feedback:
            g = self.case.g_h
            for n, gain in self.feedback.items():
                u = -gain @ self.modal_state(n)
                for q, sl in enumerate(self.stream):
                    e = np.exp(1j * n * self.phi[sl])
                    a_r[sl] += g * (u[2 * q] * e).real
                    a_s[sl] += g * (u[2 * q + 1] * e).real
        # the guide pushes at right angles to the structure; the stators push along it
        tilt = self._at(slope, self.phi) / self.r
        a_t = -tilt * a_r + a_s
        # reaction on the structure, shared between the two nearest nodes
        x = (self.phi % (2.0 * math.pi)) / self.dth
        j = np.floor(x).astype(int) % N
        jn = (j + 1) % N
        a0 = self.th0[j] + dth_node[j]
        a1 = self.th0[j] + self.dth + dth_node[jn]
        wt = (self.th0[j] + (x - np.floor(x)) * self.dth - a0) / (a1 - a0)
        fr, ft = -self.slug_mass * a_r, -self.slug_mass * a_t
        Fr = np.bincount(j, weights=fr * (1.0 - wt), minlength=N) + np.bincount(jn, weights=fr * wt, minlength=N)
        Ft = np.bincount(j, weights=ft * (1.0 - wt), minlength=N) + np.bincount(jn, weights=ft * wt, minlength=N)
        if self.load is not None:
            Fr = Fr + self.load * R * self.dth
        F = Fr[:, None] * er + Ft[:, None] * et
        # gravity and the hoop
        rn = np.hypot(self.X[:, 0], self.X[:, 1])
        F -= self.gm * self.node_mass * self.X / rn[:, None] ** 3
        dX = np.roll(self.X, -1, axis=0) - self.X
        length = np.hypot(dX[:, 0], dX[:, 1])
        pull = (self.ea * (length - self.rest) / self.rest / length)[:, None] * dX
        F += pull - np.roll(pull, 1, axis=0)
        # keep the long waves only
        f_r, f_t = (F * self.er0).sum(1), (F * self.et0).sum(1)
        for arr in (f_r, f_t):
            ak = np.fft.rfft(arr)
            ak[~self._keep] = 0.0
            arr[:] = np.fft.irfft(ak, N)
        F = f_r[:, None] * self.er0 + f_t[:, None] * self.et0
        # advance
        self.V += dt * F / self.node_mass
        self.X += dt * self.V
        rdd = self.r * self.phid**2 - self.gm / self.r**2 + a_r
        phidd = (a_t - 2.0 * self.rd * self.phid) / self.r
        self.rd += dt * rdd
        self.phid += dt * phidd
        self.r += dt * self.rd
        self.phi += dt * self.phid
        self.phi_nominal += dt * self.w0
        self.set_point = zk + dt * zdk
        self.t += dt

    def run(self, duration: float, record=(1,), every: int = 100):
        """Advance by `duration` seconds. Returns times, the structure's mode
        amplitudes (one column per entry of `record`), the largest gap and the
        largest speed deviation at each sample."""
        steps = int(round(duration / self.dt))
        times, amps, gaps, speeds = [], [], [], []
        for i in range(steps):
            self.step()
            if (i + 1) % every == 0:
                times.append(self.t)
                amps.append([self.mode(n) for n in record])
                gaps.append(np.abs(self.gap()).max())
                speeds.append(np.abs(self.speed_deviation()).max())
        return np.array(times), np.array(amps), np.array(gaps), np.array(speeds)


def measured_growth_rate(n: int, ea: float = 5.0e10, case: RefCase = EARTH_500, e_folds: float = 10.0, amplitude: float = 1.0, **kw) -> float:
    """Growth rate of mode n in the particle simulation with a following
    guide and coasting slugs, 1/s.

    The run lasts `e_folds` e-folding times of the rate the linear model
    predicts, and the rate is an exponential fit to its second half, by
    which time the growing motion has outrun everything else the starting
    shape excited. The prediction sets only the length of the run.
    """
    from .ring_modes import RingModes

    sim = RingParticleSim(case=case, ea=ea, n_keep=max(n, 1), **kw)
    sim.perturb(n, amplitude)
    duration = e_folds / RingModes(case=case, ea=ea).growth_rate(n)
    t, a, _, _ = sim.run(duration, record=(n,), every=max(1, int(20.0 / sim.dt)))
    late = t > 0.5 * t[-1]
    return float(np.polyfit(t[late], np.log(np.abs(a[late, 0])), 1)[0])
