"""Whole ring: growth or decay rate of every mode under three guide laws."""
import numpy as np

from .. import ring_control as rc
from ..ring_modes import FOLLOW, GuideLaw, RingModes
from . import style


def make(outdir=None):
    model = RingModes()
    om = model.omega
    law = rc.reference_law(model)
    ns = np.unique(np.round(np.geomspace(1, 3000, 90)).astype(int))
    follow = np.array([model.growth_rate(n, FOLLOW) for n in ns]) / om
    alone = np.array([model.growth_rate(n, GuideLaw(mirror=law.mirror, lead=law.lead)) for n in ns]) / om
    full = np.array([model.growth_rate(n, rc.law_for_mode(n, law)) for n in ns]) / om
    closed, _, _ = rc.off_centre_controller(model, law)
    fig, ax = style.figure(6.8, 4.0)
    ax.axhline(0.0, color=style.AXIS, linewidth=1.0)
    ax.plot(ns, follow, color=style.SERIES[1], label="Stream follows the structure")
    ax.plot(ns, alone, color=style.SERIES[3], label="Mirror law, slugs coasting")
    steered = ns >= rc.MIRROR_FROM
    ax.plot(ns[steered], full[steered], color=style.SERIES[2], label="Mirror law, slugs held softly by the stators")
    ax.plot([1], [np.linalg.eigvals(closed).real.max()], "o", color=style.SERIES[0], markersize=8, label="Mode 1 under stator feedback")
    ax.set_xscale("log")
    ax.set_ylim(-1.0, 3.2)
    ax.set_xlim(0.9, 3000)
    ax.set_xlabel("Mode number n (waves round the ring)")
    ax.set_ylabel("Growth (+) or decay (−) rate / orbital rate")
    ax.set_title("Which modes of the ring each law holds")
    ax.legend(loc="upper right")
    return style.save(fig, "ring-control-rates", outdir)
