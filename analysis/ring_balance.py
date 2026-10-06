"""What an imbalance between the two directions of travel does to the
controlled ring, in the linear model.

The two directions can differ in mass per metre (`flux_imbalance`) or in speed
(`speed_imbalance`); analysis/ring_modes.py scales the pair so that together
they still carry the structure. The structure itself is at rest in these
models. A ring that turns with its planet has streams whose inertial speeds
differ, by 5% for the reference case, and that part is covered here. The
structure's own rotation is not.
"""
from __future__ import annotations

from . import ring_control as rc
from .ring_loads import SCALES, RingLoads
from .ring_modes import RingModes

STEERED_MODES = list(range(2, 400)) + [500, 700, 1000, 2000, 3000, 5000, 10000, 20000, 30000]


def steered_unstable(flux: float = 0.0, speed: float = 0.0, adapt: float = rc.ADAPT, modes=STEERED_MODES) -> list[int]:
    """Modes that grow under the mirror law (with set points adapting at `adapt`) when the streams are unequal."""
    model = RingModes(flux_imbalance=flux, speed_imbalance=speed)
    law = rc.reference_law(model)
    return [n for n in modes if rc.slowest_rate(model, rc.closed_loop(model, n, law, adapt=adapt)) >= 0.0]


def stator_held_unstable(flux: float = 0.0, speed: float = 0.0, redesign: bool = False, modes=range(2, 171)) -> list[int]:
    """Stator-held modes that grow when the streams are unequal. With
    `redesign` the stator feedback is designed for the unequal streams;
    without, it is the one designed for equal streams."""
    model = RingModes(flux_imbalance=flux, speed_imbalance=speed)
    law = rc.reference_law(model)
    nominal = RingLoads(RingModes(), stator_modes=max(modes))
    out = []
    for n in modes:
        gain = rc.stator_lqr(model, n, rc.law_for_mode(1, law), SCALES)[2] if redesign else nominal.stator_gain(n)
        if rc.slowest_rate(model, rc.closed_loop(model, n, law, mirror_from=n + 1, extra=gain)) >= 0.0:
            out.append(n)
    return out


def off_centre_rate(flux: float = 0.0, speed: float = 0.0) -> float:
    """Slowest rate of the off-center mode, 1/s, with the controller designed for equal streams."""
    model = RingModes(flux_imbalance=flux, speed_imbalance=speed)
    base = RingModes()
    gain = rc.off_centre_controller(base, rc.reference_law(base))[2]
    return rc.slowest_rate(model, rc.closed_loop(model, 1, rc.reference_law(model), extra=gain))
