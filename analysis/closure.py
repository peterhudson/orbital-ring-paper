"""The closure loop as a number.

Passive mass needs stream to hold it up; the stream needs guide force; guide
force costs drag, hardware, heat rejection and power supply; and all of those
are passive mass. Every link is proportional to the supported weight, so the
loop is a geometric series with a gain G:

    m = m_0 / (1 - G),        G = phi g_h [ 1/f_g + (u / (D eta)) (1/s_r + 1/s_p) ],

where phi = 1 + 2 pi Gamma is the guide's normal force per unit of supported
weight (lift, plus the inflation load of the helix), D the guide's ratio of
normal force to drag, f_g the guide hardware's force per kilogram, s_r the heat
a kilogram of radiator rejects, s_p the power a kilogram of supply delivers, and
eta the efficiency with which the stators turn supplied power into thrust.

The four hardware numbers are assumptions. They are there to show which of
them the loop is sensitive to, not to predict a design.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

from .params import EARTH_500, RefCase


@dataclass(frozen=True)
class Assumptions:
    lift_to_drag: float = 1.0e5             # guide normal force over guide drag, at operating speed
    guide_specific_force: float = 2000.0    # N of normal force per kg of guide and stator hardware
    radiator_specific_power: float = 500.0  # W rejected per kg of radiator and heat transport
    supply_specific_power: float = 200.0    # W delivered per kg of power supply and distribution
    conversion_efficiency: float = 0.9      # supplied power that reaches the slugs as thrust

    def with_(self, **changes) -> "Assumptions":
        return replace(self, **changes)


REFERENCE = Assumptions()


def guide_force_ratio(gamma: float) -> float:
    """Guide normal force per unit of supported weight: 1 for lift plus 2 pi Gamma for the helix's inflation load."""
    return 1.0 + 2.0 * math.pi * gamma


def guide_force(case: RefCase = EARTH_500, gamma: float | None = None) -> float:
    """Total normal force the guides carry per metre of ring, N/m."""
    return guide_force_ratio(case.gamma if gamma is None else gamma) * case.w_p


def drag_power(case: RefCase = EARTH_500, lift_to_drag: float = REFERENCE.lift_to_drag, gamma: float | None = None) -> float:
    """Power the guides' drag takes out of the streams per metre of ring, W/m."""
    return guide_force(case, gamma) * case.u / lift_to_drag


def ring_power(case: RefCase = EARTH_500, a: Assumptions = REFERENCE, gamma: float | None = None) -> float:
    """Power that has to be supplied to keep the whole ring's streams at speed, W, before the loop's own growth."""
    return drag_power(case, a.lift_to_drag, gamma) / a.conversion_efficiency * case.circumference


def gain_terms(case: RefCase = EARTH_500, a: Assumptions = REFERENCE, gamma: float | None = None) -> dict:
    """The loop gain's three parts: kg of each kind of hardware per kg of passive mass."""
    force = guide_force_ratio(case.gamma if gamma is None else gamma) * case.g_h        # N of guide force per kg carried
    power = force * case.u / (a.lift_to_drag * a.conversion_efficiency)                # W supplied (and rejected) per kg carried
    return dict(guide=force / a.guide_specific_force, radiator=power / a.radiator_specific_power, supply=power / a.supply_specific_power)


def loop_gain(case: RefCase = EARTH_500, a: Assumptions = REFERENCE, gamma: float | None = None) -> float:
    return sum(gain_terms(case, a, gamma).values())


def mass_multiplier(case: RefCase = EARTH_500, a: Assumptions = REFERENCE, gamma: float | None = None) -> float:
    """Total passive mass over the mass that is not guide, radiator or supply. Infinite if the loop does not close."""
    gain = loop_gain(case, a, gamma)
    return 1.0 / (1.0 - gain) if gain < 1.0 else math.inf


def lift_to_drag_needed(target_gain: float, case: RefCase = EARTH_500, a: Assumptions = REFERENCE, gamma: float | None = None) -> float:
    """Lift-to-drag ratio at which the loop gain equals `target_gain`. Infinite if the guide hardware alone exceeds it."""
    terms = gain_terms(case, a.with_(lift_to_drag=1.0), gamma)
    room = target_gain - terms["guide"]
    return (terms["radiator"] + terms["supply"]) / room if room > 0.0 else math.inf
