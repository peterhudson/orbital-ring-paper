"""In-plane modes of the whole ring, with the streams as separate fields.

analysis/truss.py lumps the stream's mass and momentum flux into the
structure, which is exact only if the stators hold every slug at a fixed
speed. Here each stream has its own radial displacement, speed and spacing,
so slugs can coast, trade speed for height, and bunch. The price is that the
model is linear and works on one mode exp(i n theta) at a time.

Unknowns, per unit of the ring's radius R and of the orbital rate
Omega = sqrt(g/R) (so time is in units of 1/Omega and mass per radian in
units of m R):

    w, v        radial and tangential displacement of the structure
    eta_i       radial displacement of stream i from the circle
    om_i        perturbation of stream i's angular rate
    xi_i        along-track displacement of its slugs; density = -lam_i d(xi_i)/d(theta)

and with nu_i = +-u/u_orb, D_i = d/dt + i n nu_i following the slugs:

    slug, radial       D^2 eta = (nu^2 + 2) eta + 2 nu om + a_n
    slug, along track  D om    = -2 nu D eta + (nu^2 - 1) i n w + a_t
    slug spacing       D xi    = om
    structure, radial  w''     = (2 - k) w + (1 - k) i n v - sum[(nu^2 - 1) l_i i n xi_i + l_i a_n,i]
    structure, tang.   v''     = -k n^2 v + (k - 1) i n w - sum[l_i a_t,i]

Here a_n is the change in the guide's normal force per unit slug mass and a_t
the stators' along-track force per unit slug mass; l_i = lambda_i / m; and
k = EA / (m g R) is the hoop stiffness. The term (nu^2 - 1) i n w is the
steady lift force acting along the track where the guide is tilted: a guide
pushes at right angles to itself, not to the slug's path.

Two descriptions of the lateral guide are provided. `plant` leaves a_n and
a_t as inputs, for control design. `tracking_matrix` assumes the guide holds
each stream on a commanded path eta_i = c_i w exactly, which removes eta as
an unknown.

Checked against: the truss model's closed form when speed is held; a cubic
derived by hand for coasting streams on a stiff hoop; and the nonlinear
particle simulation in analysis/ring_particles.py.
"""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass, replace

import numpy as np

from .params import EARTH_500, RefCase

N_STATES = 12      # plant: w, w', v, v', then (eta, eta', om, xi) for the +u and -u streams
N_INPUTS = 4       # plant: a_n and a_t for the +u stream, then for the -u stream
LATERAL = (0, 2)
ALONG_TRACK = (1, 3)


@dataclass(frozen=True)
class GuideLaw:
    """How the guide and stators treat the streams.

    mirror        None: each stream is held on the structure's own shape.
                  A number c0: it is held on the mirror image, eta = -c0 w.
    lead          phase, rad, by which each stream reads the structure's shape
                  ahead of itself in its own direction of travel.
    speed_rate    rate at which the stators pull a slug's speed toward its
                  reference, 1/s. Zero lets the slugs coast.
    lock_rate     the same for a slug's position, 1/s^2: a soft spring to the
                  stator's travelling wave.
    reference     "bucket": the reference is a point of the stator pattern,
                  which is fixed in the structure and moves with it.
                  "speed": the reference is a fixed speed relative to the
                  structure.
    """
    mirror: float | None = None
    lead: float = 0.0
    speed_rate: float = 0.0
    lock_rate: float = 0.0
    reference: str = "bucket"

    def with_(self, **kw) -> "GuideLaw":
        return replace(self, **kw)


FOLLOW = GuideLaw()


@dataclass(frozen=True)
class RingModes:
    case: RefCase = EARTH_500
    ea: float = 5.0e10              # hoop stiffness of the structure, N

    # ---- scales -----------------------------------------------------------------
    @property
    def omega(self) -> float:
        """Orbital rate at the ring radius, 1/s."""
        return self.case.omega_orb

    @property
    def nu(self) -> float:
        """Stream speed over orbital speed."""
        return self.case.u / self.case.u_orb

    @property
    def ell(self) -> float:
        """Stream line density over passive line density, lambda / m."""
        return self.case.lam_stream / self.case.m_passive

    @property
    def hoop(self) -> float:
        """Hoop stiffness k = EA / (m g R)."""
        return self.ea / (self.case.m_passive * self.case.g_h * self.case.R)

    def _streams(self):
        return [(0.5 * self.ell, +self.nu), (0.5 * self.ell, -self.nu)]

    # ---- plant with inputs --------------------------------------------------------
    def plant(self, n: int):
        """(A, B) for mode n, nondimensional, with the guide's normal force and
        the stators' along-track force as inputs. With no input the slugs fly
        under the steady lift force alone."""
        k, i_n = self.hoop, 1j * n
        A = np.zeros((N_STATES, N_STATES), complex)
        B = np.zeros((N_STATES, N_INPUTS), complex)
        A[0, 1] = A[2, 3] = 1.0
        A[1, 0], A[1, 2] = 2.0 - k, (1.0 - k) * i_n
        A[3, 2], A[3, 0] = -k * n * n, (k - 1.0) * i_n
        for q, (l, v) in enumerate(self._streams()):
            ie, ied, io, ix = 4 + 4 * q, 5 + 4 * q, 6 + 4 * q, 7 + 4 * q
            A[ie, ied] = 1.0
            A[ied, ied], A[ied, ie], A[ied, io] = -2.0 * i_n * v, n * n * v * v + v * v + 2.0, 2.0 * v
            B[ied, 2 * q] = 1.0
            A[io, io], A[io, ied], A[io, ie], A[io, 0] = -i_n * v, -2.0 * v, -2.0 * v * i_n * v, (v * v - 1.0) * i_n
            B[io, 2 * q + 1] = 1.0
            A[ix, ix], A[ix, io] = -i_n * v, 1.0
            A[1, ix] += -l * i_n * (v * v - 1.0)
            B[1, 2 * q] = -l
            B[3, 2 * q + 1] = -l
        return A, B

    def stator_gain(self, n: int, law: GuideLaw) -> np.ndarray:
        """Rows of state feedback u = -K x for the along-track inputs under `law`."""
        K = np.zeros((N_INPUTS, N_STATES), complex)
        kv, kx = law.speed_rate / self.omega, law.lock_rate / self.omega**2
        for q, (_, v) in enumerate(self._streams()):
            ie, io, ix = 4 + 4 * q, 6 + 4 * q, 7 + 4 * q
            row = 2 * q + 1
            K[row, io] = kv
            if law.reference == "bucket":          # reference rate D v, reference position v
                K[row, 3], K[row, 2] = -kv, -kv * 1j * n * v
                K[row, ix], K[row, 2] = kx, K[row, 2] - kx
            elif law.reference == "speed":         # hold the speed along the structure: om = v' - nu eta
                K[row, ie], K[row, 3] = kv * v, -kv
            else:
                raise ValueError(law.reference)
        return K

    def tracking_gain(self, n: int, law: GuideLaw, bandwidth: float = 200.0, zeta: float = 0.7) -> np.ndarray:
        """State feedback that makes each stream track its commanded path with
        a spring and damper of the given bandwidth (in units of Omega),
        plus the stator law. Tends to `tracking_matrix` as bandwidth grows."""
        K = self.stator_gain(n, law)
        wb = max(bandwidth, 8.0 * n * self.nu)
        for q, (_, v) in enumerate(self._streams()):
            ie, ied = 4 + 4 * q, 5 + 4 * q
            c = self._path(law, v)
            D = 1j * n * v
            K[2 * q, ie], K[2 * q, ied] = wb**2 + 2 * zeta * wb * D, 2 * zeta * wb
            K[2 * q, 0], K[2 * q, 1] = -c * (wb**2 + 2 * zeta * wb * D), -c * 2 * zeta * wb
        return K

    @staticmethod
    def _path(law: GuideLaw, v: float) -> complex:
        if law.mirror is None:
            return 1.0
        return -law.mirror * cmath.exp(1j * math.copysign(law.lead, v))

    # ---- ideal lateral tracking ------------------------------------------------------
    def tracking_matrix(self, n: int, law: GuideLaw = FOLLOW) -> np.ndarray:
        """State matrix when each stream is held exactly on eta_i = c_i w.
        States: w, w', v, v', then (om, xi) per stream. Nondimensional."""
        k, i_n = self.hoop, 1j * n
        N = 8
        A = np.zeros((N, N), complex)
        rw = np.zeros(N, complex)
        rv = np.zeros(N, complex)
        mw = 1.0
        rw[0], rw[2] = 2.0 - k, (1.0 - k) * i_n
        rv[2], rv[0] = -k * n * n, (k - 1.0) * i_n
        kv, kx = law.speed_rate / self.omega, law.lock_rate / self.omega**2
        for q, (l, v) in enumerate(self._streams()):
            io, ix = 4 + 2 * q, 5 + 2 * q
            c = self._path(law, v)
            at = np.zeros(N, complex)
            at[io] = -kv
            if law.reference == "bucket":
                at[3] += kv
                at[2] += kv * i_n * v + kx
                at[ix] += -kx
            elif law.reference == "speed":
                at[0] += -kv * v * c
                at[3] += kv
            else:
                raise ValueError(law.reference)
            A[io, io] += -i_n * v
            A[io, 1] += -2.0 * v * c
            A[io, 0] += -2.0 * v * c * i_n * v + (v * v - 1.0) * i_n
            A[io] += at
            A[ix, ix], A[ix, io] = -i_n * v, 1.0
            # reaction on the structure: -(density change) * steady lift - l * a_n,
            # with a_n = c (w'' + 2 i n nu w' - n^2 nu^2 w) - (nu^2 + 2) c w - 2 nu om
            rw[ix] += -l * i_n * (v * v - 1.0)
            mw += l * c
            rw[1] += -l * c * 2.0 * i_n * v
            rw[0] += l * c * (n * n * v * v + v * v + 2.0)
            rw[io] += 2.0 * l * v
            rv += -l * at
        A[0, 1] = A[2, 3] = 1.0
        A[1] = rw / mw
        A[3] = rv
        return A

    def eigenvalues(self, n: int, law: GuideLaw = FOLLOW) -> np.ndarray:
        """Eigenvalues for mode n under ideal lateral tracking, 1/s, most unstable first."""
        vals = np.linalg.eigvals(self.tracking_matrix(n, law)) * self.omega
        return vals[np.argsort(-vals.real)]

    def growth_rate(self, n: int, law: GuideLaw = FOLLOW) -> float:
        """Largest real part for mode n, 1/s."""
        return float(self.eigenvalues(n, law)[0].real)

    def closed_loop_eigenvalues(self, n: int, K: np.ndarray) -> np.ndarray:
        """Eigenvalues of the plant under state feedback u = -K x, 1/s."""
        A, B = self.plant(n)
        vals = np.linalg.eigvals(A - B @ K) * self.omega
        return vals[np.argsort(-vals.real)]


# ---- closed forms --------------------------------------------------------------------
def coasting_growth_rate(n: int, case: RefCase = EARTH_500) -> float:
    """Growth rate of in-plane mode n when the hoop does not stretch, the
    streams follow the structure and the slugs coast, 1/s.

    s = sigma^2 / Omega^2 is the largest real root of

        (1 + 1/n^2 + l) s (s + a)^2
            = l (a - 3 nu^2 + 2) (s + a)^2 + 4 a (s + a) + (nu^2 - 1) n^2 (s - a),

    with a = n^2 nu^2, nu = u / u_orb and l = lambda / m = 1 / (nu^2 - 1).
    For large n, s tends to n^2 minus a constant near 1.2. Returns 0 if no
    root is positive.
    """
    n = int(n)
    nu2 = float((case.u / case.u_orb) ** 2)
    l = 1.0 / (nu2 - 1.0)
    a = n * n * nu2
    sa2 = np.array([1.0, 2.0 * a, a * a])                    # (s + a)^2
    lhs = (1.0 + 1.0 / (n * n) + l) * np.polymul([1.0, 0.0], sa2)
    rhs = np.polyadd(l * (a - 3.0 * nu2 + 2.0) * sa2, np.polyadd(4.0 * a * np.array([1.0, a]), (nu2 - 1.0) * n * n * np.array([1.0, -a])))
    roots = np.roots(np.polysub(lhs, rhs))
    real = [r.real for r in roots if abs(r.imag) < 1e-9 * max(1.0, abs(r.real)) and r.real > 0.0]
    return case.omega_orb * math.sqrt(max(real)) if real else 0.0


def held_speed_growth_rate(n: int, case: RefCase = EARTH_500) -> float:
    """The same with every slug held at constant speed: sigma^2 = Omega^2 n^4 / (n^2 + 1)."""
    return case.omega_orb * math.sqrt(n**4 / (n * n + 1.0))


def out_of_plane_rate(n: int, case: RefCase = EARTH_500, mirror: float | None = None, lead: float = 0.0) -> complex:
    """Out-of-plane mode n: the root with the largest real part, 1/s.

    Nothing along the track is involved, so the local model plus gravity's
    restoring pull is the whole story. With the streams held on
    zeta_+- = c exp(+-i lead) z (c = 1 for a following guide, -c_m for the
    mirror law):

        (m + c lam cos) z'' - 2 c lam n nu Omega sin z'
            + [(m + c lam cos) Omega^2 - c lam n^2 nu^2 Omega^2 cos] z = 0,

    with cos and sin of the lead. For a following guide this is
    sigma^2 = Omega^2 (n^2 - 1).
    """
    c = 1.0 if mirror is None else -mirror
    m, lam, om = case.m_passive, case.lam_stream, case.omega_orb
    nu = case.u / case.u_orb
    cs, sn = math.cos(lead), math.sin(lead)
    roots = np.roots([m + c * lam * cs, -2.0 * c * lam * n * nu * om * sn, (m + c * lam * cs) * om**2 - c * lam * (n * nu * om) ** 2 * cs])
    return complex(max(roots, key=lambda z: z.real))
