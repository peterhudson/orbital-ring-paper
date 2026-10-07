"""Whole-ring models built on the momentum truss, with the matching formulas.

Conventions: the ring lies in the x-y plane, centred on the body. `mu` is the
total mass per unit length (passive structure plus stream). Effective tension
is T_eff = N - Pi; a ring that supports itself has T_eff = -mu g R < 0.
"""
from __future__ import annotations

import math

import numpy as np

from .params import EARTH_500, RefCase
from .truss import MomentumTruss


# ---- closed-form results ------------------------------------------------------
def hoop_stiffness_ratio(ea: float, case: RefCase = EARTH_500, mu: float | None = None) -> float:
    """c / Omega^2 with c = EA / (mu R^2): how stiff the ring's hoop is
    compared with the gravity-gradient scale. Large means inextensible."""
    mu = case.m_passive + case.lam_stream if mu is None else mu
    return ea / (mu * case.R**2) / case.omega_orb**2


def growth_rate_in_plane(n: int, case: RefCase = EARTH_500, ea: float | None = None) -> float:
    """Growth rate of in-plane mode n of a momentum-supported ring in a
    central field, 1/s.

    Inextensible ring (ea=None): sigma^2 = Omega^2 n^4 / (n^2 + 1).

    With hoop stiffness EA the radial and tangential motions obey
        W'' = A W + i n B V,      V'' = i n (c - Omega^2) W - c n^2 V,
        A = Omega^2 (n^2 + 2 - phi) - c,   B = Omega^2 (1 - phi) - c,
    where c = EA / (mu R^2) and phi = lambda / mu is the stream's share of the
    mass (a guide that stretches holds more stream, hence the phi terms).
    sigma^2 is the larger root s of
        s^2 - (A - c n^2) s - A c n^2 + n^2 B (c - Omega^2) = 0.
    """
    om2 = case.omega_orb**2
    if ea is None:
        return math.sqrt(om2 * n**4 / (n**2 + 1.0))
    phi = case.lam_stream / (case.lam_stream + case.m_passive)
    c = hoop_stiffness_ratio(ea, case) * om2
    A = om2 * (n**2 + 2.0 - phi) - c
    B = om2 * (1.0 - phi) - c
    tr = A - c * n**2
    det = -A * c * n**2 + n**2 * B * (c - om2)
    return math.sqrt(0.5 * (tr + math.sqrt(tr**2 - 4.0 * det)))


def growth_rate_out_of_plane(n: int, case: RefCase = EARTH_500) -> float:
    """Out-of-plane mode n: sigma^2 = Omega^2 (n^2 - 1). Mode 1 is neutral."""
    return case.omega_orb * math.sqrt(max(n**2 - 1.0, 0.0))


def growth_rate_local(wavelength: float, case: RefCase = EARTH_500, mu: float | None = None, t_eff: float | None = None) -> float:
    """Short-wave limit: sigma = k sqrt(-T_eff / mu)."""
    mu = case.m_passive + case.lam_stream if mu is None else mu
    t_eff = -mu * case.g_h * case.R if t_eff is None else t_eff
    return 2.0 * math.pi / wavelength * math.sqrt(-t_eff / mu)


def speed_ripple_response(eps: float, p: int, case: RefCase = EARTH_500, prestress: float = 0.0):
    """First-order static response of an inextensible ring to a stationary
    speed ripple u = u0 (1 + eps cos(p theta)) at fixed mass flux.

    Returns (W, N1): the radial displacement amplitude (outward positive, at
    theta = 0) and the amplitude of the tension ripple in the structure.
    """
    lam, m = case.lam_stream, case.m_passive
    mu = lam + m
    pi0 = mu * case.g_h * case.R + prestress
    W = -(lam / mu) * case.R * eps / p**2
    N1 = eps * (pi0 - lam * case.g_h * case.R / p**2)
    return W, N1


# ---- builders ---------------------------------------------------------------------
def ring_truss(
    case: RefCase = EARTH_500,
    n_nodes: int = 360,
    ea: float = 5.0e10,
    prestress: float = 0.0,
    speed_ratio: np.ndarray | None = None,
    shift_weight: bool = True,
    dim: int = 2,
    tension_only: bool = False,
):
    """A single-chord ring of `n_nodes` straight members round the body.

    The streams have the reference line density and whatever speed is needed
    to carry the passive weight plus `prestress` (a uniform tension held in
    the structure). `speed_ratio` (one value per member, default 1) scales
    the local slug speed at fixed mass flux, so thrust scales with it and,
    if `shift_weight`, line density scales inversely.

    Returns (truss, x0) with x0 the regular polygon.
    """
    R = case.R
    theta = 2.0 * math.pi * np.arange(n_nodes) / n_nodes
    x0 = np.zeros((n_nodes, dim))
    x0[:, 0], x0[:, 1] = R * np.cos(theta), R * np.sin(theta)
    chord = 2.0 * R * math.sin(math.pi / n_nodes)
    lam0, m = case.lam_stream, case.m_passive
    mu = lam0 + m
    pi0 = mu * case.g_h * R + prestress          # polygon-exact balance: (Pi - N) / R = mu g
    ratio = np.ones(n_nodes) if speed_ratio is None else np.asarray(speed_ratio, dtype=float)
    thrust = pi0 * ratio
    lam = lam0 / ratio if shift_weight else np.full(n_nodes, lam0)
    members = np.column_stack([np.arange(n_nodes), (np.arange(n_nodes) + 1) % n_nodes])
    rest = chord / (1.0 + prestress / ea)
    truss = MomentumTruss(
        members=members, rest_length=rest, ea=ea, thrust=thrust, stream_density=lam,
        node_mass=np.full(n_nodes, m * chord), gm=case.body.gm, tension_only=tension_only,
    )
    return truss, x0


def member_angles(n_nodes: int) -> np.ndarray:
    """Angular position of each member's midpoint."""
    return 2.0 * math.pi * (np.arange(n_nodes) + 0.5) / n_nodes


def radial_displacement(x, case: RefCase = EARTH_500) -> np.ndarray:
    return np.sqrt((x[:, :2] ** 2).sum(axis=1)) - case.R


def fourier_amplitude(values: np.ndarray, p: int, angles: np.ndarray) -> float:
    """Amplitude of the cos(p theta) component of `values` sampled at `angles`."""
    return 2.0 * float(np.mean(values * np.cos(p * angles)))


def classify_modes(shapes: np.ndarray, x: np.ndarray):
    """For each mode shape, the azimuthal number that dominates its radial
    (or, for out-of-plane modes, vertical) motion, and "in" or "out"."""
    n_nodes = x.shape[0]
    theta = np.arctan2(x[:, 1], x[:, 0])
    e_r = np.zeros_like(x)
    e_r[:, 0], e_r[:, 1] = np.cos(theta), np.sin(theta)
    out = []
    for q in range(shapes.shape[2]):
        s = shapes[:, :, q]
        radial = (s * e_r).sum(axis=1)
        vertical = s[:, 2] if x.shape[1] == 3 else np.zeros(n_nodes)
        is_out = (vertical**2).sum() > (radial**2).sum()
        comp = vertical if is_out else radial
        out.append((int(np.argmax(np.abs(np.fft.rfft(comp)))), "out" if is_out else "in"))
    return out


def growth_rates_by_mode(truss: MomentumTruss, x: np.ndarray, kind: str = "in"):
    """Dictionary {n: sigma^2} of the most unstable mode of each azimuthal number."""
    s2, shapes = truss.modes(x)
    found = {}
    for (n, k), value in zip(classify_modes(shapes, x), s2):
        if k == kind and n not in found:
            found[n] = float(value)
    return found
