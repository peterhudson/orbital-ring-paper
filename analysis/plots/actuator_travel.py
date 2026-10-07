"""How far each actuator must move to recover one metre of error on the
growing mode: the guide's gap if only steering is used, the slugs' speed if
the stators are used."""
import numpy as np

from .. import ring_control as rc
from ..ring_modes import RingModes
from . import style


def make(outdir=None):
    model = RingModes()
    ns = np.array([1, 2, 3, 4, 5, 6, 8, 10, 14, 20, 30])
    gap = [rc.steering_gap_per_metre(model, n) for n in ns]
    hold = rc.reference_law(model).with_(mirror=None, lead=0.0)       # guide follows, stators hold the slugs softly
    speed = [rc.stator_speed_per_metre(model, n, hold) for n in ns]
    fig, (left, right) = style.figure(6.8, 3.4, ncols=2)
    left.plot(ns, gap, "o-", color=style.SERIES[0])
    left.set_xscale("log")
    left.set_ylim(0, 4)
    left.set_xlabel("Mode number n")
    left.set_ylabel("Peak gap (m per m of error)")
    left.set_title("Steering alone")
    right.plot(ns, speed, "o-", color=style.SERIES[1])
    right.set_xscale("log")
    right.set_yscale("log")
    right.set_xlabel("Mode number n")
    right.set_ylabel("Peak speed change (m/s per m of error)")
    right.set_title("Stators")
    for ax in (left, right):
        ax.set_xticks([1, 2, 3, 5, 10, 30])
        ax.set_xticklabels(["1", "2", "3", "5", "10", "30"])
    return style.save(fig, "actuator-travel", outdir)
