"""Time-domain particle simulation of the collective model.

A straight periodic run of structure, discretised into nodes that move only
sideways, carries two counter-propagating trains of slugs. Each slug is a
free particle except for the guide force, which steers it toward a commanded
path exactly as in analysis/collective.py:

    a_slug = ff * D^2 eta*  -  w_beta^2 (eta - eta*)  -  2 zeta w_beta (eta' - D eta*)

and the reaction of every slug is put back on the two nodes either side of
it. The commanded path is built from the structure's own shape exactly as
the model's `path_gain` and `lookahead` say: mirrored, low-passed in space so
the stream ignores short-wave shape, read ahead of each stream, and passed
through a second-order lag that stands for sensing and actuation delay.

This is an independent check on the Fourier-mode eigenvalues: nothing here
assumes a single wavelength, a small amplitude, or a continuous stream.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .collective import CollectiveModel


@dataclass
class LocalParticleSim:
    model: CollectiveModel
    length: float = 20.0e3          # periodic domain, m
    n_nodes: int = 1000
    slugs_per_direction: int = 2000
    stroke: float | None = None     # limit on |eta* - y|, m
    dt: float = 2.0e-4
    load: np.ndarray | None = None  # dead load on the structure, N/m at each node
    # state
    y: np.ndarray = field(init=False)
    yd: np.ndarray = field(init=False)
    t: float = field(init=False, default=0.0)

    def __post_init__(self):
        m = self.model
        if not m.counter:
            raise ValueError("the particle simulation assumes balanced counter-propagating streams")
        n, L = self.n_nodes, self.length
        self.h = L / n
        self.s_nodes = np.arange(n) * self.h
        self.k = 2.0 * math.pi * np.fft.rfftfreq(n, d=self.h)
        self.y = np.zeros(n)
        self.yd = np.zeros(n)
        P = self.slugs_per_direction
        base = (np.arange(P) + 0.5) * L / P
        self.s = np.concatenate([base, base + 0.37 * L / P]) % L   # stagger the two trains
        self.direction = np.concatenate([np.ones(P), -np.ones(P)])
        self.eta = np.zeros(2 * P)
        self.etad = np.zeros(2 * P)
        self.slug_mass = 0.5 * m.lam * L / P
        self.cmd = np.zeros((2, n))      # commanded path for the +v and -v streams
        self.cmdd = np.zeros((2, n))
        self.wf = 2.0 * math.pi * m.f_filter
        if self.wf * self.dt > 0.5:
            raise ValueError("time step too long for the command filter; reduce dt or f_filter")
        self.path = np.array([m.path_gain(k) for k in self.k])
        self.ahead = np.array([k * m.lookahead(k) for k in self.k])       # look-ahead as a phase
        self.damp = np.array([m.structural_damping(k) for k in self.k])

    # ---- helpers ------------------------------------------------------------------
    def _interp(self, values, s):
        """Linear interpolation of a node array (periodic) at positions s."""
        x = s / self.h
        j = np.floor(x).astype(int) % self.n_nodes
        w = x - np.floor(x)
        return (1.0 - w) * values[j] + w * values[(j + 1) % self.n_nodes], j, w

    def mode_amplitude(self, mode: int, what: str = "structure") -> complex:
        """Complex amplitude of Fourier mode `mode` (wavelength = length / mode)."""
        if what == "structure":
            return np.fft.rfft(self.y)[mode] * 2.0 / self.n_nodes
        phase = np.exp(-1j * 2.0 * math.pi * mode * self.s / self.length)
        return 2.0 * np.mean(self.eta * phase)

    def gap(self) -> np.ndarray:
        """Offset of each slug from the structure at its position, m."""
        y_here, _, _ = self._interp(self.y, self.s)
        return self.eta - y_here

    # ---- one step -------------------------------------------------------------------
    def step(self):
        m, n, dt = self.model, self.n_nodes, self.dt
        v = m.v
        yk = np.fft.rfft(self.y)
        acc_nodes = np.zeros(n)
        slug_acc = np.zeros_like(self.eta)
        w_beta, zeta = m.w_beta, (m.C / (2.0 * m.lam * m.w_beta) if m.K else 0.0)
        P = self.slugs_per_direction
        for q, sgn in ((0, +1.0), (1, -1.0)):
            target = np.fft.irfft(self.path * np.exp(1j * sgn * self.ahead) * yk, n)
            if self.stroke is not None:
                target = np.clip(target, self.y - self.stroke, self.y + self.stroke)
            cmd, cmdd = self.cmd[q], self.cmdd[q]
            cmddd = self.wf**2 * (target - cmd) - 2.0 * m.zeta_filter * self.wf * cmdd
            ck, cdk = np.fft.rfft(cmd), np.fft.rfft(cmdd)
            cmd_s = np.fft.irfft(1j * self.k * ck, n)
            cmd_ss = np.fft.irfft(-self.k**2 * ck, n)
            cmdd_s = np.fft.irfft(1j * self.k * cdk, n)
            vi = sgn * v
            D_cmd = cmdd + vi * cmd_s
            D2_cmd = cmddd + 2.0 * vi * cmdd_s + vi**2 * cmd_ss
            sl = slice(q * P, (q + 1) * P)
            c_here, j, w = self._interp(cmd, self.s[sl])
            Dc_here, _, _ = self._interp(D_cmd, self.s[sl])
            D2c_here, _, _ = self._interp(D2_cmd, self.s[sl])
            a = m.ff * D2c_here - w_beta**2 * (self.eta[sl] - c_here) - 2.0 * zeta * w_beta * (self.etad[sl] - Dc_here)
            slug_acc[sl] = a
            react = -self.slug_mass * a                      # force on the structure
            acc_nodes += np.bincount(j, weights=react * (1.0 - w), minlength=n)
            acc_nodes += np.bincount((j + 1) % n, weights=react * w, minlength=n)
            # advance the command filter
            self.cmdd[q] = cmdd + dt * cmddd
            self.cmd[q] = cmd + dt * self.cmdd[q]
        force = acc_nodes / self.h                            # N per metre of structure
        if m.EI or m.N:
            force += np.fft.irfft(-(m.EI * self.k**4 + m.N * self.k**2) * yk - self.damp * np.fft.rfft(self.yd), n)
        if self.load is not None:
            force = force + self.load
        self.yd += dt * force / m.m
        self.y += dt * self.yd
        self.etad += dt * slug_acc
        self.eta += dt * self.etad
        self.s = (self.s + dt * self.direction * v) % self.length
        self.t += dt

    def run(self, duration: float, record_modes=(1,), every: int = 50):
        """Advance by `duration` seconds. Returns times and the recorded
        structure mode amplitudes, shape (len(times), len(record_modes))."""
        steps = int(round(duration / self.dt))
        times, amps = [], []
        for i in range(steps):
            self.step()
            if (i + 1) % every == 0:
                yk = np.fft.rfft(self.y) * 2.0 / self.n_nodes
                times.append(self.t)
                amps.append([yk[mode] for mode in record_modes])
        return np.array(times), np.array(amps)


def fitted_rate(times: np.ndarray, amplitude: np.ndarray, window: tuple[float, float] | None = None) -> float:
    """Exponential rate of |amplitude| over time, 1/s, by a log-linear fit."""
    a = np.abs(amplitude)
    sel = np.ones_like(times, dtype=bool) if window is None else (times >= window[0]) & (times <= window[1])
    sel &= a > 0
    return float(np.polyfit(times[sel], np.log(a[sel]), 1)[0])


def envelope_rate(times: np.ndarray, amplitude: np.ndarray) -> float:
    """Decay or growth rate of an oscillating signal, from its successive peaks, 1/s."""
    a = np.abs(amplitude)
    peaks = [i for i in range(1, len(a) - 1) if a[i] >= a[i - 1] and a[i] > a[i + 1]]
    if len(peaks) < 3:
        return fitted_rate(times, amplitude)
    return float(np.polyfit(times[peaks], np.log(a[peaks]), 1)[0])
