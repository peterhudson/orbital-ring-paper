"""Controllers for the whole-ring modes of analysis/ring_modes.py.

Two kinds are built here, both as state feedback u = -K x on the plant of
`RingModes.plant`:

  * the structured law: the guide holds each stream on the mirror image of
    the structure's shape, read a little ahead, and the stators hold each
    slug softly to its place in their traveling wave;
  * optimal (LQR) feedback for one mode at a time, used where the structured
    law is not enough and to measure how much actuator travel a
    stabilizing law must spend.

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

from .collective import LEAD, MIRROR_GAIN
from .ring_modes import ALONG_TRACK, FOLLOW, LATERAL, N_INPUTS, N_STATES, GuideLaw, RingModes

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


GUIDE_BANDWIDTH = 2.0 * math.pi * 10.0      # rad/s: the reference guide holds its commanded path at 10 Hz
FILTER_BANDWIDTH = 2.0 * math.pi * 1000.0   # rad/s: bandwidth of the path command (sensing and actuation lag)

# Layout of the closed loop's state: the plant's N_STATES, then each stream's
# filtered path command and its rate, then (if the set point adapts) the
# common set point z and the differential set point z_d.
I_CMD = N_STATES
I_SET = N_STATES + 4


def closed_loop(model: RingModes, n: int, law: GuideLaw, mirror_from: int = MIRROR_FROM, adapt: float = 0.0,
                guide_bandwidth: float = GUIDE_BANDWIDTH, guide_zeta: float = 0.7,
                filter_bandwidth: float = FILTER_BANDWIDTH, filter_zeta: float = 0.7,
                extra: np.ndarray | None = None) -> np.ndarray:
    """Closed-loop matrix of mode n under the structured law, nondimensional.

    Each stream's target path is  p_i w + z +- z_d,  with p_i = 1 where the
    stream follows the structure and -c_m exp(+-i lead) where it is
    mirrored. The target passes through a second-order filter of bandwidth
    `filter_bandwidth` to give the command c_i, and the guide's force per
    unit slug mass is

        a_n = -(slug's own centrifugal and gravity terms)
              + D^2 c_i                       the force that flies the commanded path
              - wb^2 (eta_i - c_i) - 2 zeta wb D (eta_i - c_i).

    The stators follow `law`. With `adapt` > 0 the set points drift at the
    rate adapt * n * nu:

        z'   = +rate * (mean of the streams' offsets from the structure),
        z_d' = -rate * (half the difference of the streams' positions),

    so that under a steady load every stream ends in the middle of its
    guide. `extra` is further state feedback u = -extra x on the plant's
    states. analysis/ring_particles.py implements the same law.
    """
    A, B = model.plant(n)
    this = law_for_mode(n, law, mirror_from)
    rate = adapt * n * model.nu if (adapt and this.mirror is not None) else 0.0
    size = N_STATES + 4 + (2 if rate else 0)
    out = np.zeros((size, size), complex)
    wb, wf = guide_bandwidth / model.omega, filter_bandwidth / model.omega
    G = np.zeros((N_INPUTS, size), complex)                    # u = G @ state
    G[:, :N_STATES] = -model.stator_gain(n, this)
    if extra is not None:
        G[:, :N_STATES] -= extra
    for q, (_, v) in enumerate(model._streams()):
        sign = 1.0 if v > 0 else -1.0
        ie, ied, io = 4 + 4 * q, 5 + 4 * q, 6 + 4 * q
        ic = I_CMD + 2 * q
        D = 1j * n * v
        # the command filter:  c'' = wf^2 (target - c) - 2 zeta_f wf c'
        target = np.zeros(size, complex)
        target[0] = model._path(this, v)
        if rate:
            target[I_SET], target[I_SET + 1] = 1.0, sign
        acc = wf**2 * target
        acc[ic] -= wf**2
        acc[ic + 1] -= 2.0 * filter_zeta * wf
        out[ic, ic + 1] = 1.0
        out[ic + 1] = acc
        # the guide
        row = 2 * q
        G[row] += acc                                           # D^2 c = c'' + 2 D c' + D^2 c
        G[row, ic + 1] += 2.0 * D
        G[row, ic] += D * D
        G[row, ie] += -(v * v + 2.0) - wb**2 - 2.0 * guide_zeta * wb * D
        G[row, ied] += -2.0 * guide_zeta * wb
        G[row, io] += -2.0 * v
        G[row, ic] += wb**2 + 2.0 * guide_zeta * wb * D
        G[row, ic + 1] += 2.0 * guide_zeta * wb
    out[:N_STATES, :N_STATES] = A
    out[:N_STATES] += B @ G
    if rate:
        out[I_SET, 4], out[I_SET, 8], out[I_SET, 0] = 0.5 * rate, 0.5 * rate, -rate
        out[I_SET + 1, 4], out[I_SET + 1, 8] = -0.5 * rate, 0.5 * rate
    return out


def slowest_rate(model: RingModes, matrix: np.ndarray) -> float:
    """Largest real part of the closed loop's eigenvalues, 1/s (negative = everything decays)."""
    return float(np.linalg.eigvals(matrix).real.max() * model.omega)


def static_response(model: RingModes, matrix: np.ndarray, load: float = 1.0):
    """Under a radial dead load on the structure of amplitude `load` N/m
    (outward positive) in the mode `matrix` was built for: the structure's
    steady radial displacement, and the larger of the two streams' steady
    offsets from the structure, m."""
    b = np.zeros(matrix.shape[0], complex)
    b[1] = load / (model.case.m_passive * model.case.g_h)
    x = -np.linalg.solve(matrix, b) * model.case.R
    return x[0].real, max(abs(x[4] - x[0]), abs(x[8] - x[0]))


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


def steering_scales(model: RingModes) -> Scales:
    """A cost that weighs a metre of stream offset and a metre of shape error
    equally and makes guide force almost free, for asking how much offset a
    steering-only controller needs."""
    c = model.case
    return Scales(gap=1.0, speed=1e12, shape=1.0, floor=1e-3, guide=c.g_h / c.R * 1e5)


def steering_gap_per_metre(model: RingModes, n: int) -> float:
    """Peak offset of a stream from the structure, per metre of error on the
    growing mode, when mode n is recovered by steering alone under the
    optimal law for `steering_scales`."""
    K = lqr_gain(model, n, inputs=LATERAL, scales=steering_scales(model))
    return recovery(model, n, K, unstable_direction(model, n), duration=12.0 / model.growth_rate(n), samples=6000)["gap"]


def stator_speed_per_metre(model: RingModes, n: int, law: GuideLaw = FOLLOW, scales: Scales = Scales(shape=10.0)) -> float:
    """Peak change of slug speed, m/s per metre of error on the growing
    mode, when mode n is recovered by optimal stator feedback with the
    guide and stators otherwise following `law`."""
    closed, _, _ = stator_lqr(model, n, law, scales)
    vals, vecs = np.linalg.eig(model.tracking_matrix(n, law))
    x = vecs[:, np.argmax(vals.real)]
    x = x / x[0]
    paths = [model._path(law, v) for _, v in model._streams()]
    times = np.linspace(0.0, 12.0 / vals.real.max(), 3000)
    step = expm(closed * (times[1] - times[0]))
    peak = 0.0
    for _ in times:
        peak = max(peak, *(abs(x[4 + 2 * q] + v * paths[q] * x[0]) for q, (_, v) in enumerate(model._streams())))
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
