"""Reference cases.

One place for every input number. The paper's "reference bookkeeping case" is
EARTH_500. All derived quantities are properties, so changing an input here
changes every number downstream, and the tests in tests/test_refcase.py show
which statements in the text no longer hold.

SI units throughout.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

MU_0 = 4.0e-7 * math.pi  # permeability of free space, T m / A


@dataclass(frozen=True)
class Body:
    """A body to put a ring around."""

    name: str
    gm: float            # gravitational parameter, m^3 / s^2
    radius: float        # mean radius, m
    sidereal_day: float  # s


EARTH = Body("Earth", 3.986004418e14, 6.371e6, 86164.1)
MOON = Body("Moon", 4.9048695e12, 1.7374e6, 27.321661 * 86400.0)
MARS = Body("Mars", 4.282837e13, 3.3895e6, 88642.66)


@dataclass(frozen=True)
class RefCase:
    """A ring design point.

    Inputs follow the table in the introduction: altitude, ring-direction
    slug speed u, tube radius a, supported non-stream load w_p, lane count
    and prestress ratio Gamma.
    """

    body: Body = EARTH
    altitude: float = 500.0e3   # m
    u: float = 1.0e4            # ring-direction slug speed relative to the guide, m/s
    a: float = 50.0             # tube radius, m
    w_p: float = 1.0e4          # net inward non-stream load, N/m
    n_lanes: int = 300
    gamma: float = 10.0         # prestress ratio N_theta / w_p
    slug_mass: float = 10.0     # kg, the paper's bookkeeping slug

    # ---- geometry and gravity -------------------------------------------
    @property
    def R(self) -> float:
        """Ring radius from the body's centre, m."""
        return self.body.radius + self.altitude

    @property
    def circumference(self) -> float:
        return 2.0 * math.pi * self.R

    @property
    def g_h(self) -> float:
        """Gravitational acceleration at ring altitude, m/s^2."""
        return self.body.gm / self.R**2

    @property
    def u_orb(self) -> float:
        """Circular orbital speed at the ring radius, m/s."""
        return math.sqrt(self.g_h * self.R)

    @property
    def v_esc(self) -> float:
        return math.sqrt(2.0) * self.u_orb

    @property
    def omega_orb(self) -> float:
        """Orbital angular rate at the ring radius, rad/s."""
        return math.sqrt(self.g_h / self.R)

    @property
    def U_g(self) -> float:
        """Inertial speed of a guide that co-rotates with the body, m/s."""
        return self.circumference / self.body.sidereal_day

    # ---- lift ------------------------------------------------------------
    @property
    def lift_accel(self) -> float:
        """Net outward acceleration of the stream, u^2/R - g_h, m/s^2."""
        return self.u**2 / self.R - self.g_h

    @property
    def lam_stream(self) -> float:
        """Moving mass per unit ring length needed to carry w_p, kg/m."""
        return self.w_p / self.lift_accel

    @property
    def lam_lane(self) -> float:
        return self.lam_stream / self.n_lanes

    @property
    def mdot_lane(self) -> float:
        """Mass flux in one lane, kg/s."""
        return self.lam_lane * self.u

    @property
    def mdot_total(self) -> float:
        return self.lam_stream * self.u

    @property
    def T_eq_lane(self) -> float:
        """Dynamic-tension scale of one lane, N."""
        return self.mdot_lane * self.u

    @property
    def Pi_total(self) -> float:
        """Momentum flux of all lanes together, N."""
        return self.lam_stream * self.u**2

    @property
    def m_passive(self) -> float:
        """Passive mass per unit ring length that weighs w_p, kg/m."""
        return self.w_p / self.g_h

    @property
    def E_prime(self) -> float:
        """Stream kinetic energy per unit ring length, J/m."""
        return 0.5 * self.lam_stream * self.u**2

    @property
    def beta(self) -> float:
        """Lift-coupling coefficient 1/R + g_h/u^2, 1/m."""
        return 1.0 / self.R + self.g_h / self.u**2

    @property
    def lift_multiplier(self) -> float:
        """Fractional lift change per fractional speed change, stream only."""
        return self.beta / (1.0 / self.R - self.g_h / self.u**2)

    # ---- helix and prestress ----------------------------------------------
    def alpha_cross(self, gamma: float | None = None) -> float:
        """Helix angle at which inflation and lift requirements meet, rad."""
        g = self.gamma if gamma is None else gamma
        t2 = 2.0 * math.pi * self.a * g * (1.0 / self.R - self.g_h / self.u**2)
        return math.atan(math.sqrt(t2))

    @property
    def alpha(self) -> float:
        return self.alpha_cross()

    def pitch(self, gamma: float | None = None) -> float:
        """Length of ring over which a lane wraps once round the tube, m."""
        return 2.0 * math.pi * self.a / math.tan(self.alpha_cross(gamma))

    @property
    def N_theta(self) -> float:
        """Hoop membrane force target, N/m."""
        return self.gamma * self.w_p

    @property
    def p_eq(self) -> float:
        """Equivalent inflation pressure, Pa."""
        return self.N_theta / self.a

    @property
    def kappa_helix(self) -> float:
        return math.sin(self.alpha) ** 2 / self.a

    @property
    def v(self) -> float:
        """Slug speed along its lane, m/s."""
        return self.u / math.cos(self.alpha)

    @property
    def normal_load_lane(self) -> float:
        """Helical normal load on one lane's guide, N per metre of lane."""
        return self.mdot_lane * self.v * self.kappa_helix

    @property
    def theta_flux_lane(self) -> float:
        """Circumferential momentum flux of one lane, N."""
        return self.mdot_lane * self.u * math.tan(self.alpha)

    # ---- slugs -------------------------------------------------------------
    def slug_rate(self, slug_mass: float | None = None) -> float:
        """Slugs per second in one lane."""
        return self.mdot_lane / (self.slug_mass if slug_mass is None else slug_mass)

    def headway(self, slug_mass: float | None = None) -> float:
        return 1.0 / self.slug_rate(slug_mass)

    def spacing(self, slug_mass: float | None = None) -> float:
        return self.u * self.headway(slug_mass)

    def slug_energy(self, slug_mass: float | None = None) -> float:
        return 0.5 * (self.slug_mass if slug_mass is None else slug_mass) * self.u**2

    # ---- whole ring ---------------------------------------------------------
    @property
    def total_passive_mass(self) -> float:
        return self.m_passive * self.circumference

    @property
    def total_stream_mass(self) -> float:
        return self.lam_stream * self.circumference

    @property
    def total_kinetic_energy(self) -> float:
        return self.E_prime * self.circumference

    def with_(self, **changes) -> "RefCase":
        return replace(self, **changes)


def magnetic_pressure(b_tesla: float) -> float:
    """Ideal upper bound on magnetic normal stress, B^2 / (2 mu_0), Pa."""
    return b_tesla**2 / (2.0 * MU_0)


EARTH_500 = RefCase()


def same_speed_ratio(body: Body, altitude: float, base: RefCase = EARTH_500) -> RefCase:
    """A case on another body with the same u/u_orb and the same passive mass
    per metre as `base`, so the two differ only in the gravity well."""
    probe = RefCase(body=body, altitude=altitude)
    u = probe.u_orb * base.u / base.u_orb
    w_p = base.m_passive * probe.g_h
    return replace(probe, u=u, w_p=w_p, a=base.a, n_lanes=base.n_lanes, gamma=base.gamma)


MOON_20 = same_speed_ratio(MOON, 20.0e3)
