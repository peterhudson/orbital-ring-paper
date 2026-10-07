"""Stream-supported structures other than the orbital ring.

Everything here follows from the ring's own equilibrium equation,

    d/ds (T_eff t) + q = 0,        T_eff = N - Pi,

applied to other curves. Three cases cover the family:

* a free loop, with no load: T_eff = 0;
* an arch, loaded across the stream: T_eff = -(weight per metre) * R_c;
* a column, loaded along the stream: T_eff = -(weight above).

A ring is an arch with no ends, and R_c is then the ring's own radius.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .params import EARTH_500, MARS, MOON_20, RefCase, same_speed_ratio

MARS_200 = same_speed_ratio(MARS, 200.0e3)


# --- arches (and rings) ------------------------------------------------------

def threshold_speed(g: float, radius: float) -> float:
    """Stream speed at which a stream curving at `radius` just carries itself, m/s.
    For a ring this is orbital speed."""
    return math.sqrt(g * radius)


def stream_per_passive(speed_ratio: float) -> float:
    """Stream mass needed per unit of passive mass, lambda/m, at u = speed_ratio * threshold."""
    return 1.0 / (speed_ratio**2 - 1.0)


def arch_thrust(mass_per_length: float, g: float, radius: float) -> float:
    """|T_eff| of an arch of total mass per length M curving at `radius`, N.
    This is also the thrust its abutments must take if it has ends."""
    return mass_per_length * g * radius


def energy_floor(passive_per_length: float, g: float, radius: float) -> float:
    """Least kinetic energy per metre that can hold `passive_per_length`, J/m:
    the limit of very fast, very thin streams."""
    return 0.5 * passive_per_length * g * radius


def energy_over_floor(speed_ratio: float) -> float:
    """Stream kinetic energy per metre as a multiple of the floor."""
    return speed_ratio**2 / (speed_ratio**2 - 1.0)


def growth_speed(g: float, radius: float) -> float:
    """Shape errors of wavenumber k grow at k times this speed when the streams
    follow the structure, m/s. In equilibrium |T_eff| = M g R_c whatever share of
    it is tension, so the speed is sqrt(g R_c): the threshold speed again."""
    return math.sqrt(g * radius)


def steering_gain_limit(speed_ratio: float) -> float:
    """Largest mirror gain c_m the structure's mass allows: m / lambda."""
    return speed_ratio**2 - 1.0


def least_speed_ratio_for_gain(gain: float) -> float:
    """Slowest stream, as a multiple of the threshold speed, that can be steered at mirror gain `gain`."""
    return math.sqrt(1.0 + gain)


def world_row(case: RefCase) -> dict:
    """The quantities compared between worlds."""
    return dict(
        radius=case.R, g=case.g_h, threshold=case.u_orb, speed=case.u, circumference=case.circumference,
        period=2.0 * math.pi / case.omega_orb, thrust=case.Pi_total, energy_per_metre=case.E_prime,
        energy_total=case.total_kinetic_energy, slug_energy=case.slug_energy(), headway=case.headway(),
        delay_budget_100m=100.0 / (12.0 * case.u), local_efold_100km=1.0 / (2.0 * math.pi / 1.0e5 * case.u_orb),
        helix_deg=math.degrees(case.alpha_cross()), guide_load_lane=case.normal_load_lane,
    )


LAUNCH_LOOP_LIKE = RefCase(altitude=80.0e3, u=14.0e3)   # only its altitude and speed are used


def arch_row(case: RefCase) -> dict:
    """Ratios for an arch that follows the planet's curvature at the case's altitude and stream speed."""
    nu = case.u / case.u_orb
    return dict(threshold=case.u_orb, speed_ratio=nu, stream_per_passive=stream_per_passive(nu),
                passive_per_stream=nu**2 - 1.0, energy_over_floor=energy_over_floor(nu),
                gain_limit=steering_gain_limit(nu), efold_100km=1.0 / (2.0 * math.pi / 1.0e5 * case.u_orb))


# --- columns -----------------------------------------------------------------

@dataclass(frozen=True)
class Fountain:
    """A vertical pair of streams, one up and one down, turned round under a
    station at the top. The slugs coast, so each stream carries its own weight
    by slowing as it climbs. The tower's structure hangs from the station.
    Gravity is taken as uniform, which is good to a few percent up to 100 km."""

    height: float            # m
    station_mass: float      # kg
    tower_per_length: float  # kg/m of stationary structure
    top_speed: float         # slug speed at the top, m/s
    g: float = 9.80665

    @property
    def mdot(self) -> float:
        """Mass flux in each stream, kg/s: the turn-round at the top carries the station and the tower."""
        return (self.station_mass + self.tower_per_length * self.height) * self.g / (2.0 * self.top_speed)

    def speed(self, z: float) -> float:
        return math.sqrt(self.top_speed**2 + 2.0 * self.g * (self.height - z))

    def stream_per_length(self, z: float) -> float:
        """Mass of both streams per metre of height, kg/m."""
        return 2.0 * self.mdot / self.speed(z)

    def momentum_flux(self, z: float) -> float:
        return 2.0 * self.mdot * self.speed(z)

    def tension(self, z: float) -> float:
        """Tension in the tower structure, which hangs from the station, N."""
        return self.tower_per_length * self.g * z

    def effective_tension(self, z: float) -> float:
        return self.tension(z) - self.momentum_flux(z)

    def weight_above(self, z: float, steps: int = 2000) -> float:
        """Weight of station, tower and streams above height z, N, by direct sum."""
        dz = (self.height - z) / steps
        streams = sum(self.stream_per_length(z + (i + 0.5) * dz) for i in range(steps)) * dz
        return (self.station_mass + self.tower_per_length * (self.height - z) + streams) * self.g

    def growth_speed(self, z: float) -> float:
        """Shape errors of wavenumber k grow at k times this, where the wave is short beside the tower, m/s."""
        return math.sqrt(-self.effective_tension(z) / (self.tower_per_length + self.stream_per_length(z)))

    @property
    def base_speed(self) -> float:
        return self.speed(0.0)

    @property
    def stored_energy(self) -> float:
        """Kinetic energy of the slugs in flight, J: each stream holds mdot * (u_base^3 - u_top^3) / (3 g)."""
        return 2.0 * self.mdot * (self.base_speed**3 - self.top_speed**3) / (6.0 * self.g)


FOUNTAIN_100 = Fountain(height=100.0e3, station_mass=1.0e5, tower_per_length=10.0, top_speed=1.0e3)


# --- a tabletop arch ---------------------------------------------------------

@dataclass(frozen=True)
class TabletopArch:
    """A chain running between two wheels and standing as an arch, with a light
    guide riding on it: the smallest arch of momentum.

    A chain that moves along itself takes the same shapes as one at rest, with
    its tension raised by lambda u^2. An arch at rest would be in compression
    everywhere, by (weight per metre) x (height above the catenary's
    directrix): M g R_c at the crown and M g (R_c + rise) at the feet. The
    moving chain can stand in that shape if its tension stays positive, which
    is hardest at the feet.
    """

    radius: float = 1.0            # radius of curvature at the crown, m
    rise: float = 0.3              # height of the crown above the wheels, m
    chain_per_length: float = 0.1  # kg/m
    speed: float = 5.0             # m/s
    guide_per_length: float = 0.08  # kg/m of guide riding on the chain
    g: float = 9.80665

    @property
    def threshold(self) -> float:
        """Slowest speed at which the bare chain stands, m/s."""
        return math.sqrt(self.g * (self.radius + self.rise))

    @property
    def max_carried(self) -> float:
        """Most guide the chain can carry per metre with its tension still positive at the feet, kg/m."""
        return self.chain_per_length * (self.speed**2 / (self.g * (self.radius + self.rise)) - 1.0)

    @property
    def crown_tension(self) -> float:
        total = self.chain_per_length + self.guide_per_length
        return self.chain_per_length * self.speed**2 - total * self.g * self.radius

    @property
    def foot_tension(self) -> float:
        total = self.chain_per_length + self.guide_per_length
        return self.chain_per_length * self.speed**2 - total * self.g * (self.radius + self.rise)

    def growth_rate(self, wavelength: float) -> float:
        """Growth rate at the crown of a kink in a guide locked to the chain, 1/s.
        One stream keeps its convective term, so the rate is
        k sqrt(g R_c - (lambda u / M)^2), and zero if that is negative."""
        total = self.chain_per_length + self.guide_per_length
        k = 2.0 * math.pi / wavelength
        inside = self.g * self.radius - (self.chain_per_length * self.speed / total) ** 2
        return k * math.sqrt(inside) if inside > 0.0 else 0.0

    @property
    def lightest_guide_that_kinks(self) -> float:
        """Below this guide mass per metre one stream's convective term holds the arch neutral, kg/m."""
        return self.chain_per_length * (self.speed / math.sqrt(self.g * self.radius) - 1.0)
