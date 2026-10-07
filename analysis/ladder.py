"""A straight two-chord frame for testing what opposed tug fields do.

Two chords a distance 2a apart, joined by rungs and cross-braced. Each chord
carries half the streams. Speeding up the streams in one chord and slowing
them in the other moves the centroid of momentum flux (the thrust line)
sideways by

    e = a (Pi_outer - Pi_inner) / Pi_total.

Beam theory for the frame-plus-streams gives, with q the lateral load,

    EI y'''' + Pi y'' = q - (Pi e)''.

For wavelengths well beyond 2 pi sqrt(EI / Pi) the bending term drops out and
y = -e: the structure moves so that the thrust line stays where it was.
"""
from __future__ import annotations

import math

import numpy as np

from .params import EARTH_500, RefCase
from .truss import MomentumTruss


def ladder_truss(
    length: float = 20.0e3,
    panels: int = 200,
    case: RefCase = EARTH_500,
    ea_chord: float = 2.5e10,
    ea_web: float = 2.5e9,
    shift: np.ndarray | None = None,
):
    """Build the frame. `shift` is the wanted thrust-line offset e at each
    panel (m, positive toward the upper chord); it is produced by a speed
    difference between the chords at fixed mass flux.

    Returns (truss, x0, fixed) with all four end nodes held.
    """
    a = case.a
    h = length / panels
    pi_total = case.Pi_total
    e = np.zeros(panels) if shift is None else np.asarray(shift, dtype=float)
    frac = e / a                                  # (Pi_up - Pi_dn) / Pi_total
    n_side = panels + 1
    xs = np.linspace(0.0, length, n_side)
    up = np.column_stack([xs, np.full(n_side, a)])
    dn = np.column_stack([xs, np.full(n_side, -a)])
    x0 = np.vstack([up, dn])
    iu = np.arange(panels)
    idn = n_side + np.arange(panels)
    chords_up = np.column_stack([iu, iu + 1])
    chords_dn = np.column_stack([idn, idn + 1])
    rungs = np.column_stack([np.arange(n_side), n_side + np.arange(n_side)])
    diag1 = np.column_stack([iu, idn + 1])
    diag2 = np.column_stack([idn, iu + 1])
    members = np.vstack([chords_up, chords_dn, rungs, diag1, diag2])
    diag_len = math.hypot(h, 2 * a)
    rest = np.concatenate([np.full(2 * panels, h), np.full(n_side, 2 * a), np.full(2 * panels, diag_len)])
    ea = np.concatenate([np.full(2 * panels, ea_chord), np.full(n_side, ea_web), np.full(2 * panels, ea_web)])
    thrust = np.concatenate([0.5 * pi_total * (1 + frac), 0.5 * pi_total * (1 - frac), np.zeros(n_side + 2 * panels)])
    lam = np.concatenate([0.5 * case.lam_stream / (1 + frac), 0.5 * case.lam_stream / (1 - frac), np.zeros(n_side + 2 * panels)])
    node_mass = np.full(2 * n_side, 0.5 * case.m_passive * h)
    truss = MomentumTruss(members=members, rest_length=rest, ea=ea, thrust=thrust, stream_density=lam, node_mass=node_mass)
    fixed = np.zeros((2 * n_side, 2), dtype=bool)
    for node in (0, panels, n_side, n_side + panels):
        fixed[node] = True
    return truss, x0, fixed


def bending_stiffness(case: RefCase = EARTH_500, ea_chord: float = 2.5e10) -> float:
    return 2.0 * ea_chord * case.a**2


def crossover_wavelength(case: RefCase = EARTH_500, ea_chord: float = 2.5e10) -> float:
    """Wavelength beyond which the streams, not the frame's bending stiffness,
    decide the lateral response: 2 pi sqrt(EI / Pi)."""
    return 2.0 * math.pi * math.sqrt(bending_stiffness(case, ea_chord) / case.Pi_total)
