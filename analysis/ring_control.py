"""Controllers for the whole-ring modes of analysis/ring_modes.py.

Two kinds are built here, both as state feedback u = -K x on the plant of
`RingModes.plant`:

  * the structured law: the guide holds each stream on the mirror image of
    the structure's shape, read a little ahead, and the stators hold each
    slug softly to its place in their travelling wave;
  * optimal (LQR) feedback for one mode at a time, used where the structured
    law is not enough and to measure how much actuator travel any
    stabilising law must spend.

The same gains can be handed to analysis/ring_particles.py to run on the
nonlinear simulation.

Units: the plant is nondimensional (lengths in R, time in 1/Omega, guide and
stator forces per unit slug mass in g). Costs are given in physical units
and converted here.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm, solve_continuous_are

from .ring_modes import ALONG_TRACK, FOLLOW, LATERAL, N_INPUTS, N_STATES, GuideLaw, RingModes

from .collective import LEAD, MIRROR_GAIN

# The reference structured law: the mirror gain and phase lead of the local
# model, and a stator lock whose rates are the orbital rate and its square
# (set in `reference_law`).
MIRROR_FROM = 2          # lowest mode steered by the mirror law
ADAPT = 0.03             # set-point adaptation rate as a fraction of the stream's transit rate n u / R


def reference_law(model: RingModes) -> GuideLaw:
    om = model.omega
    return GuideLaw(mirror=MIRROR_GAIN, lead=LEAD, speed_rate=om, lock_rate=om**2)


def law_for_mode(n: int, law: GuideLaw, mirror_from: int = MIRROR_FROM) -> GuideLaw:
    """What the structured law does to mode n: below `mirror_from` the
    streams follow the structure, and the uniform mode n = 0 is left to coast."""
    if n == 0:
        return FOLLOW
    if n < mirror_from:
        return law.with_(mirror=None, lead=0.0)
    return law


GUIDE_BANDWIDTH = 2.0 * math.pi * 10.0     # rad/s: the reference guide holds its commanded path at 10 Hz


def baseline_gain(model: RingModes, n: int, law: GuideLaw, mirror_from: int = MIRROR_FROM,
                  guide_bandwidth: float = GUIDE_BANDWIDTH, guide_zeta: float = 0.7) -> np.ndarray:
    """The structured law as state feedback on the plant, with a guide of
    finite bandwidth (rad/s) that first cancels each slug's own centrifugal
    and gravity terms, as analysis/ring_particles.py does."""
    this = law_for_mode(n, law, mirror_from)
    K = model.stator_gain(n, this)
    wb = guide_bandwidth / model.omega
    for q, (_, v) in enumerate(model._streams()):
        ie, ied, io = 4 + 4 * q, 5 + 4 * q, 6 + 4 * q
        c = model._path(this, v)
        D = 1j * n * v
        K[2 * q, ie] = wb**2 + 2 * guide_zeta * wb * D + (v * v + 2.0)
        K[2 * q, ied] = 2 * guide_zeta * wb
        K[2 * q, io] = 2.0 * v
        K[2 * q, 0] = -c * (wb**2 + 2 * guide_zeta * wb * D)
        K[2 * q, 1] = -c * 2 * guide_zeta * wb
    return K


def adaptive_closed_loop(model: RingModes, n: int, law: GuideLaw, adapt: float = ADAPT, mirror_from: int = MIRROR_FROM,
                         guide_bandwidth: float = GUIDE_BANDWIDTH, guide_zeta: float = 0.7, extra: np.ndarray | None = None) -> np.ndarray:
    """Closed-loop matrix of the plant under the structured law with a set
    point z added to both streams' commanded paths (state N_STATES, last),

        z' = adapt * n nu * (mean gap),

    which drives the steady gap to zero under a steady load. `extra` is any
    further state feedback on the plant's states."""
    A, B = model.plant(n)
    K = baseline_gain(model, n, law, mirror_from, guide_bandwidth, guide_zeta)
    if extra is not None:
        K = K + extra
    wb = guide_bandwidth / model.omega
    rate = adapt * n * model.nu
    gap_row = np.zeros(N_STATES, complex)
    gap_row[4], gap_row[8], gap_row[0] = 0.5, 0.5, -1.0
    Kz = np.zeros(N_INPUTS, complex)        # u += Kz z + Kzd z'
    Kzd = np.zeros(N_INPUTS, complex)
    for q, (_, v) in enumerate(model._streams()):
        Kz[2 * q] = wb**2 + 2 * guide_zeta * wb * 1j * n * v
        Kzd[2 * q] = 2 * guide_zeta * wb
    out = np.zeros((N_STATES + 1, N_STATES + 1), complex)
    out[:N_STATES, :N_STATES] = A - B @ K + rate * np.outer(B @ Kzd, gap_row)
    out[:N_STATES, N_STATES] = B @ Kz
    out[N_STATES, :N_STATES] = rate * gap_row
    return out


def static_response(model: RingModes, closed_loop: np.ndarray, load: float = 1.0):
    """Steady radial displacement of the structure and steady mean gap, m,
    under a radial dead load on the structure of amplitude `load` N/m
    (outward positive) in the mode the closed loop was built for."""
    b = np.zeros(closed_loop.shape[0], complex)
    b[1] = load / (model.case.m_passive * model.case.g_h)
    x = -np.linalg.solve(closed_loop, b) * model.case.R
    return x[0].real, (0.5 * (x[4] + x[8]) - x[0]).real


# ---- optimal feedback -------------------------------------------------------------------
@dataclass(frozen=True)
class Scales:
    """What counts as 'one unit' of each quantity in the cost."""
    gap: float = 0.02          # stream offset from the structure, m
    speed: float = 1.0         # slug speed deviation, m/s
    shape: float = 100.0       # structure displacement, m
    guide: float = 1.0e-3      # change in guide force per unit slug mass, m/s^2
    stator: float = 1.0e-3     # stator force per unit slug mass, m/s^2
    floor: float = 1.0e-3      # small weight on every state, relative to `shape`


def least_gap_scales(model: RingModes) -> Scales:
    """A cost that counts the gap and almost nothing else, for asking how
    little gap a steering-only controller can get away with."""
    c = model.case
    return Scales(gap=0.02, speed=1e12, shape=2.0, floor=1.0, guide=c.g_h * 0.02 / c.R * 1e5)


def steering_gap_per_metre(model: RingModes, n: int) -> float:
    """Peak gap, per metre of error on the growing mode, when mode n is
    recovered by steering alone under the least-gap optimal law."""
    K = lqr_gain(model, n, inputs=LATERAL, scales=least_gap_scales(model))
    return recovery(model, n, K, unstable_direction(model, n), duration=12.0 / model.growth_rate(n), samples=6000)["gap"]


def stator_speed_per_metre(model: RingModes, n: int, scales: Scales = Scales(shape=10.0)) -> float:
    """Peak change of slug speed, m/s per metre of error on the growing
    mode, when mode n is recovered by the stators with a following guide."""
    closed, _, _ = stator_lqr(model, n, scales=scales)
    vals, vecs = np.linalg.eig(model.tracking_matrix(n))
    x = vecs[:, np.argmax(vals.real)]
    x = x / x[0]
    times = np.linspace(0.0, 12.0 / vals.real.max(), 3000)
    step = expm(closed * (times[1] - times[0]))
    peak = 0.0
    for _ in times:
        peak = max(peak, abs(x[4] + model.nu * x[0]), abs(x[6] - model.nu * x[0]))
        x = step @ x
    return peak * model.omega


def outputs(model: RingModes):
    """Rows that pick out, from the plant's state: the two streams' gaps and
    speed deviations (both as fractions of R and R*Omega)."""
    gap = np.zeros((2, N_STATES), complex)
    speed = np.zeros((2, N_STATES), complex)
    for q, (_, v) in enumerate(model._streams()):
        gap[q, 4 + 4 * q], gap[q, 0] = 1.0, -1.0
        speed[q, 6 + 4 * q], speed[q, 4 + 4 * q] = 1.0, v        # R om + omega0 eta
    return gap, speed


def _solve(A, B, Q, Rm):
    scale = np.abs(Q).max()
    P = solve_continuous_are(A, B, Q / scale, Rm / scale)
    return np.linalg.solve(Rm / scale, B.conj().T @ P)


def lqr_gain(model: RingModes, n: int, inputs=LATERAL + ALONG_TRACK, scales: Scales = Scales()) -> np.ndarray:
    """Optimal feedback for mode n on the bare plant (slugs flying under the
    steady lift force), using the listed inputs. N_INPUTS x N_STATES."""
    A, B = model.plant(n)
    cols = sorted(inputs)
    Bs = B[:, cols]
    R, om, g = model.case.R, model.omega, model.case.g_h
    gap, speed = outputs(model)
    Q = (R / scales.gap) ** 2 * gap.conj().T @ gap + (R * om / scales.speed) ** 2 * speed.conj().T @ speed
    Q[0, 0] += (R / scales.shape) ** 2
    Q += scales.floor * (R / scales.shape) ** 2 * np.eye(N_STATES)
    Rm = np.diag([(g / (scales.guide if c in LATERAL else scales.stator)) ** 2 for c in cols]).astype(complex)
    K = np.zeros((N_INPUTS, N_STATES), complex)
    K[cols] = _solve(A, Bs, Q, Rm)
    return K


def stator_lqr(model: RingModes, n: int, law: GuideLaw = FOLLOW, scales: Scales = Scales()):
    """Optimal stator feedback for mode n with the guide holding each stream
    exactly on the path `law` commands, added to whatever stator law `law`
    already contains.

    Returns (A, K8, K12): the closed-loop matrix of the reduced model
    (states of RingModes.tracking_matrix), the gain on those states, and the
    same gain laid out on the plant's states for analysis/ring_particles.py.
    """
    A = model.tracking_matrix(n, law)
    B = np.zeros((8, 2), complex)
    speed = np.zeros((2, 8), complex)
    for q, (l, v) in enumerate(model._streams()):
        B[4 + 2 * q, q] = 1.0
        B[3, q] = -l
        speed[q, 4 + 2 * q] = 1.0
        speed[q, 0] = v * model._path(law, v)
    R, om, g = model.case.R, model.omega, model.case.g_h
    Q = (R * om / scales.speed) ** 2 * speed.conj().T @ speed
    Q[0, 0] += (R / scales.shape) ** 2
    Q += scales.floor * (R / scales.shape) ** 2 * np.eye(8)
    Rm = (g / scales.stator) ** 2 * np.eye(2, dtype=complex)
    K8 = _solve(A, B, Q, Rm)
    K12 = np.zeros((N_INPUTS, N_STATES), complex)
    for q in range(2):
        K12[2 * q + 1, :4] = K8[q, :4]
        for p in range(2):
            K12[2 * q + 1, 6 + 4 * p], K12[2 * q + 1, 7 + 4 * p] = K8[q, 4 + 2 * p], K8[q, 5 + 2 * p]
    return A - B @ K8, K8, K12


def off_centre_controller(model: RingModes, law: GuideLaw, scales: Scales = Scales(shape=10.0)):
    """Stator feedback for mode 1, the ring drifting off centre, which no
    amount of steering can hold. Returns what `stator_lqr` returns."""
    return stator_lqr(model, 1, law_for_mode(1, law), scales)


def unstable_direction(model: RingModes, n: int) -> np.ndarray:
    """State of the plant on the growing mode of the ring with a following
    guide and coasting slugs, scaled to unit structure displacement."""
    A, B = model.plant(n)
    vals, vecs = np.linalg.eig(A - B @ model.tracking_gain(n, FOLLOW, bandwidth=2000.0))
    x = vecs[:, np.argmax(vals.real)]
    return x / x[0]


def recovery(model: RingModes, n: int, K: np.ndarray, x0: np.ndarray, duration: float, samples: int = 2000):
    """Free response of the plant under u = -K x from x0, over `duration`
    seconds. Peak values are per metre of the starting structure
    displacement: 'gap' (m), 'speed' (m/s), 'shape' (m). Time histories are
    under 't', 'w', 'gaps', 'speeds'."""
    A, B = model.plant(n)
    Acl = A - B @ K
    om, R = model.omega, model.case.R
    ts = np.linspace(0.0, duration * om, samples)
    step = expm(Acl * (ts[1] - ts[0]))
    gap_rows, speed_rows = outputs(model)
    x = np.array(x0, complex)
    w, gaps, speeds = [], [], []
    for _ in ts:
        w.append(x[0])
        gaps.append(np.abs(gap_rows @ x).max())
        speeds.append(np.abs(speed_rows @ x).max())
        x = step @ x
    scale = abs(x0[0])
    w, gaps, speeds = np.array(w) / scale, np.array(gaps) / scale, np.array(speeds) * om / scale
    return dict(t=ts / om, w=w, gaps=gaps, speeds=speeds, gap=gaps.max(), speed=speeds.max(), shape=np.abs(w).max(),
                rate=-np.linalg.eigvals(Acl).real.max() * om)
