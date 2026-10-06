"""Collective transverse motion of a structure and the streams it carries.

Local model: a straight run of ring, wavelengths short compared with the ring
radius, one transverse direction. The structure has displacement y(s, t). The
streams have their own centreline eta_i(s, t): slugs fly ballistically except
for the force the guide puts on them.

    stream i:    lam_i D_i^2 eta_i = f_i,        D_i = d/dt + v_i d/ds
    structure:   m y_tt + EI y_ssss - N y_ss = - sum_i f_i

The guide steers each stream toward a commanded path eta*(s, t):

    f_i = ff * lam_i D_i^2 eta*                      feedforward: the force that
                                                     makes the stream follow eta*
          - K_i (eta_i - eta*) - C_i D_i (eta_i - eta*)   tracking feedback

and the commanded path is a filtered multiple of the structure's displacement,
read a distance d ahead of each stream in its own direction of travel:

    eta*_i_tt + 2 zeta_f w_f eta*_i_t + w_f^2 eta*_i = -c0 H w_f^2 y(s + sign(v_i) d, t).

The look-ahead d is `preview` metres or `lead` radians of the wave's phase,
whichever is longer. H rolls the command off below the wavelength `cutoff`,
so the streams ignore the structure's short-wave shape and fly a smooth path.

Three cases matter:

  c0 = -1, ff = 0   a plain spring guide: the stream is pulled toward the
                    structure.
  c0 = -1, ff = 1   a stiff following guide: the stream is made to follow the
                    structure exactly.
  c0 > 0,  ff = 1   mirror law: the stream is steered the opposite way to the
                    structure's displacement.

With ideal tracking and balanced streams the structure then obeys, for one
Fourier mode,

    (m - c0 lam cos(k d)) y_tt + 2 c0 lam v k sin(k d) y_t + c0 Pi k^2 cos(k d) y = 0,

with d the preview distance. So following (c0 = -1) is a string of tension
-Pi, and the mirror law is a string of tension +c0 Pi, provided c0 < m / lam.
Preview supplies the damping: the two streams' convective terms no longer
cancel, and the sign is set by looking ahead instead of behind.

All functions work on one Fourier mode exp(i k s).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np

from .params import EARTH_500, RefCase


MIRROR_GAIN = 0.5      # commanded path = -MIRROR_GAIN * structure shape
LEAD = 0.3             # look-ahead, rad of the wave's phase
MIRROR_REFERENCE = dict(
    c0=MIRROR_GAIN, ff=1.0, lead=LEAD,
    preview=20.0,          # m: the least look-ahead, to outrun the control delay
    cutoff=300.0,          # m: shorter waves are left to the structure's own stiffness
    zeta=0.3,              # damping ratio of the guide's hold on the commanded path
    EI=6.25e13,            # N m^2: a thin tube of radius 50 m with axial stiffness 50 GN
    loss_factor=1.0e-3,    # structural damping
)


@dataclass(frozen=True)
class CollectiveModel:
    m: float                  # structure mass per unit length, kg/m
    lam: float                # total stream line density, kg/m
    v: float                  # stream speed, m/s
    K: float                  # tracking stiffness, all lanes together, N/m^2
    C: float = 0.0            # tracking damping, all lanes together, N s/m^2
    c0: float = -1.0          # commanded path eta* = -c0 y  (-1 = follow the structure)
    ff: float = 0.0           # 1 to feed forward the force for the commanded path
    preview: float = 0.0      # distance ahead at which each stream reads the structure's shape, m
    f_filter: float = 1.0e3   # bandwidth of the command filter, Hz
    zeta_filter: float = 0.7
    counter: bool = True      # two half-streams at +v and -v; False = one stream at +v
    EI: float = 0.0           # structure bending stiffness, N m^2
    N: float = 0.0            # structure tension, N
    lead: float = 0.0         # look-ahead as a phase of the wave, rad (used where it exceeds `preview`)
    cutoff: float = 0.0       # wavelength below which the commanded path ignores the structure, m (0 = none)
    cutoff_order: int = 2
    loss_factor: float = 0.0  # structural damping: twice the damping ratio of the structure's own bending wave
    adapt: float = 0.0        # set-point adaptation rate as a fraction of v k (0 = none)
    adapt_from: float = 1.0e3 # shortest wavelength whose set point adapts, m

    @classmethod
    def reference(cls, case: RefCase = EARTH_500, guide_hz: float = 10.0, zeta: float = 0.0, **kw) -> "CollectiveModel":
        """Reference case. The tracking stiffness is set so a slug's own
        oscillation about its commanded path is at `guide_hz`, with tracking
        damping at ratio `zeta` of critical."""
        lam = case.lam_stream
        w_beta = 2.0 * math.pi * guide_hz
        return cls(m=case.m_passive, lam=lam, v=case.u, K=lam * w_beta**2, C=2.0 * zeta * lam * w_beta, **kw)

    @classmethod
    def mirror_reference(cls, case: RefCase = EARTH_500, **kw) -> "CollectiveModel":
        """The reference mirror law: see MIRROR_REFERENCE."""
        return cls.reference(case, **{**MIRROR_REFERENCE, **kw})

    def with_(self, **kw) -> "CollectiveModel":
        return replace(self, **kw)

    # ---- scales ----------------------------------------------------------------
    @property
    def Pi(self) -> float:
        """Total stream momentum flux, N."""
        return self.lam * self.v**2

    @property
    def w_beta(self) -> float:
        """Angular frequency of a slug's oscillation about its commanded path, rad/s."""
        return math.sqrt(self.K / self.lam)

    @property
    def guide_wavelength(self) -> float:
        """Distance a slug travels during one such oscillation, m."""
        return 2.0 * math.pi * self.v / self.w_beta

    def rigid_growth_rate(self, k: float) -> float:
        """Growth rate when the stream is locked to the structure, 1/s."""
        M = self.m + self.lam
        if self.counter:
            return k * self.v * math.sqrt(self.lam / M)
        return k * self.v * math.sqrt(self.lam * self.m) / M

    def decoupling_wavelength(self) -> float:
        """Wavelength below which a plain spring guide leaves the motion
        neutral (one-way stream; the two-stream threshold)."""
        w1, w2 = math.sqrt(self.K / self.m), math.sqrt(self.K / self.lam)
        return 2.0 * math.pi * self.v / (w1 ** (2 / 3) + w2 ** (2 / 3)) ** 1.5

    def apparent_tension(self) -> float:
        """Tension of the string the structure behaves as under ideal tracking, N."""
        return self.c0 * self.Pi

    def apparent_mass(self) -> float:
        return self.m - self.c0 * self.lam

    def lookahead(self, k: float) -> float:
        """Distance ahead at which a stream reads the structure's shape, m."""
        return max(self.preview, self.lead / k) if k > 0 else self.preview

    def path_gain(self, k: float) -> float:
        """Commanded path over structure displacement at wavenumber k: -c0 H(k)."""
        if not self.cutoff or k <= 0:
            return -self.c0
        return -self.c0 / (1.0 + (self.cutoff * k / (2.0 * math.pi)) ** (2 * self.cutoff_order))

    def structural_damping(self, k: float) -> float:
        """Damping of the structure's own bending wave, N s/m^2."""
        return self.loss_factor * math.sqrt((self.EI * k**4 + self.N * k**2) * self.m)

    def _ideal(self, k: float):
        c0, d = -self.path_gain(k), self.lookahead(k)
        cs, sn = math.cos(k * d), math.sin(k * d)
        return (self.m - c0 * self.lam * cs,
                2.0 * c0 * self.lam * self.v * k * sn + self.structural_damping(k),
                c0 * self.Pi * k**2 * cs + self.N * k**2 + self.EI * k**4)

    def ideal_roots(self, k: float) -> np.ndarray:
        """Structure roots under ideal tracking, balanced streams, no filter lag."""
        return np.roots(self._ideal(k))

    def ideal_damping_ratio(self, k: float) -> float:
        """Damping ratio of the structure's wave under ideal tracking."""
        a, b, c = self._ideal(k)
        return b / (2.0 * math.sqrt(a * c))

    # ---- linear dynamics ----------------------------------------------------------
    def _streams(self):
        if self.counter:
            return [(0.5 * self.lam, +self.v, 0.5 * self.K, 0.5 * self.C), (0.5 * self.lam, -self.v, 0.5 * self.K, 0.5 * self.C)]
        return [(self.lam, self.v, self.K, self.C)]

    def matrix(self, k: float) -> np.ndarray:
        """State matrix for x = [y, y', (eta_i, eta_i', eta*_i, eta*_i') per stream, z].

        z is the set point: an offset added to every stream's commanded path,
        integrated from the mean gap so that the steady gap is driven to zero,
            z' = adapt * v k * (mean(eta_i) - y),
        for wavelengths of `adapt_from` and longer (the state is absent otherwise).
        The feedback is positive, as in a zero-power magnetic bearing: under a
        steady load the structure settles where the streams carry the load
        with no offset in the guide.
        """
        streams = self._streams()
        rate = self.adapt_rate(k)
        n = 2 + 4 * len(streams) + (1 if rate else 0)
        iz = n - 1
        wf = 2.0 * math.pi * self.f_filter
        A = np.zeros((n, n), dtype=complex)
        A[0, 1] = 1.0
        A[1, 0] -= (self.EI * k**4 + self.N * k**2) / self.m
        A[1, 1] -= self.structural_damping(k) / self.m
        gain, d = self.path_gain(k), self.lookahead(k)
        for q, (lam_i, v_i, K_i, C_i) in enumerate(streams):
            ie = 2 + 4 * q
            ic = ie + 2
            A[ie, ie + 1] = 1.0
            A[ic, ic + 1] = 1.0
            ahead = np.exp(1j * k * math.copysign(d, v_i))
            A[ic + 1, ic], A[ic + 1, ic + 1], A[ic + 1, 0] = -wf**2, -2.0 * self.zeta_filter * wf, wf**2 * gain * ahead
            if rate:
                A[ic + 1, iz] = wf**2
                A[iz, ie] += rate / len(streams)
            ikv = 1j * k * v_i
            err = np.zeros(n, dtype=complex)
            err[ie], err[ic] = 1.0, -1.0
            d_err = np.zeros(n, dtype=complex)
            d_err[ie + 1], d_err[ie], d_err[ic + 1], d_err[ic] = 1.0, ikv, -1.0, -ikv
            d2_cmd = A[ic + 1].copy()                    # eta*'' as a row on the state
            d2_cmd[ic + 1] += 2.0 * ikv
            d2_cmd[ic] -= (k * v_i) ** 2
            f = self.ff * lam_i * d2_cmd - K_i * err - C_i * d_err
            # lam (eta'' + 2 ikv eta' - k^2 v^2 eta) = f
            A[ie + 1] += f / lam_i
            A[ie + 1, ie + 1] -= 2.0 * ikv
            A[ie + 1, ie] += (k * v_i) ** 2
            A[1] -= f / self.m
        if rate:
            A[iz, 0] -= rate
        return A

    def adapt_rate(self, k: float) -> float:
        """Rate of set-point adaptation at wavenumber k, 1/s."""
        if not self.adapt or k <= 0 or 2.0 * math.pi / k < self.adapt_from:
            return 0.0
        return self.adapt * abs(self.v) * k

    def static_response(self, k: float, load: float = 1.0):
        """Steady displacement of the structure and steady mean gap under a
        sinusoidal dead load of amplitude `load` N/m on the structure, m."""
        A = self.matrix(k)
        b = np.zeros(A.shape[0], complex)
        b[1] = load / self.m
        x = -np.linalg.solve(A, b)
        etas = [x[2 + 4 * q] for q in range(len(self._streams()))]
        return x[0].real, (np.mean(etas) - x[0]).real

    def eigenvalues(self, k: float) -> np.ndarray:
        return np.linalg.eigvals(self.matrix(k))

    def growth_rate(self, k: float) -> float:
        """Largest real part of the eigenvalues at wavenumber k, 1/s."""
        return float(self.eigenvalues(k).real.max())

    def growth_curve(self, wavelengths) -> np.ndarray:
        return np.array([self.growth_rate(2.0 * math.pi / L) for L in wavelengths])


def load_capacity(k: float, stroke: float, pi_total: float, c0: float) -> float:
    """Largest sinusoidal static load per unit length the mirror law can hold
    at wavenumber k when the stream can be offset from the structure by at
    most `stroke`, N/m."""
    return pi_total * k**2 * stroke * c0 / (1.0 + c0)


def funicular_deflection(load: float, k: float, pi_total: float) -> float:
    """Displacement of the thrust line needed to carry a sinusoidal load, m."""
    return load / (pi_total * k**2)
