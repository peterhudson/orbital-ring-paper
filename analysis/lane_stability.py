"""Single-lane screens from the local-stability appendices.

The lane carrier is treated as a beam riding on a fixed shell, with the
stream locked to it. See analysis/collective.py for the case where shell
and streams move together.
"""
from __future__ import annotations

import math

import numpy as np

from .params import EARTH_500, RefCase


def stream_stiffness(wavelength: float, case: RefCase = EARTH_500, k_par: float | None = None) -> float:
    """Destabilising stiffness T_eq k^2 of one lane, N/m^2."""
    k = 2.0 * math.pi / wavelength if k_par is None else k_par
    return case.T_eq_lane * k**2


def bending_stiffness_required(wavelength: float, case: RefCase = EARTH_500) -> float:
    """Carrier bending stiffness that alone cancels the stream term, N m^2."""
    return case.T_eq_lane * (wavelength / (2.0 * math.pi)) ** 2


def lane_wavenumber(axial_wavelength: float, n: int, case: RefCase = EARTH_500, handed: int = +1) -> float:
    """Wavenumber seen along a helical lane for axial wavelength L_s and
    cross-section mode number n."""
    k_s = 2.0 * math.pi / axial_wavelength
    return k_s * math.cos(case.alpha) + handed * n / case.a * math.sin(case.alpha)


def delay_budget(wavelength: float, speed: float, phase_deg: float = 30.0) -> float:
    """Delay that costs `phase_deg` of phase at the convective frequency, s."""
    return wavelength / speed * phase_deg / 360.0


def closed_loop_roots(
    wavelength: float,
    tau_a: float,
    case: RefCase = EARTH_500,
    mass: float = 50.0,
    stiffness_margin: float = 3.0,
    zeta: float = 0.35,
    bending: float = 0.0,
    k0: float = 0.0,
    damping: float = 0.0,
    convective: bool = True,
) -> np.ndarray:
    """Roots of the scalar closed-loop characteristic equation in Appendix A.

    (1 + tau_a s) {M s^2 + (C + 2 i lambda v k) s + B k^4 + K0 - T k^2} + Kc + Cc s = 0
    with Kc = stiffness_margin * T k^2 and Cc set for damping ratio zeta on the
    net stiffness.
    """
    k = 2.0 * math.pi / wavelength
    T = case.T_eq_lane
    k_c = stiffness_margin * T * k**2
    k_net = k_c - T * k**2
    c_c = 2.0 * zeta * math.sqrt(mass * k_net)
    gyro = 2j * case.lam_lane * case.u * k if convective else 0.0
    stiff = bending * k**4 + k0 - T * k**2
    coeffs = [tau_a * mass, mass + tau_a * (damping + gyro), damping + gyro + tau_a * stiff + c_c, stiff + k_c]
    return np.roots(coeffs)


def max_growth_rate(wavelength: float, tau_a: float, **kwargs) -> float:
    """Largest real part of the closed-loop roots, 1/s. Negative is stable."""
    return float(closed_loop_roots(wavelength, tau_a, **kwargs).real.max())
