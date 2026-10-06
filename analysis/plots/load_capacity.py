"""Largest point load the ring can carry as it moves along the ring, for three divisions of work between steering and stators."""
import numpy as np

from ..ring_loads import ARRANGEMENTS, RingLoads
from . import style

G0 = 9.80665
ROOM = 0.02        # m of guide room
AUTHORITY = 1.0    # m/s of stator speed change
LABELS = {1: "Stators hold the off-center mode only", 30: "Stators hold 30 modes", 170: "Stators hold 170 modes"}


def curves(speeds=None, arrangements=ARRANGEMENTS, n_max: int = 20000):
    """Tonnes against speed: {arrangement: (limit set by guide room, limit set by stator authority)}."""
    speeds = np.geomspace(1.0, 3000.0, 22) if speeds is None else speeds
    out = {}
    for count in arrangements:
        loads = RingLoads(stator_modes=count)
        res = [loads.moving_point_load(v, n_max=n_max) for v in speeds]
        out[count] = (np.array([ROOM / r["gap"] for r in res]) / G0 / 1e3, np.array([AUTHORITY / r["speed"] for r in res]) / G0 / 1e3)
    return speeds, out


def make(outdir=None):
    speeds, data = curves()
    fig, ax = style.figure(6.8, 4.0)
    for colour, (count, (room, authority)) in zip(style.SERIES, data.items()):
        ax.plot(speeds, room, color=colour, label=LABELS[count])
        if authority.min() < 1000.0:
            ax.plot(speeds, authority, color=colour, linewidth=1.3, linestyle=(0, (4, 3)))
    ax.plot([], [], color=style.INK_2, linewidth=1.8, label="Limit set by 20 mm of guide room")
    ax.plot([], [], color=style.INK_2, linewidth=1.3, linestyle=(0, (4, 3)), label="Limit set by 1 m/s of stator speed")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1.0, 3000.0)
    ax.set_ylim(0.03, 3000.0)
    ax.set_xticks([1, 10, 100, 1000], labels=["1 m/s", "10 m/s", "100 m/s", "1 km/s"])
    ax.set_yticks([0.1, 1, 10, 100, 1000], labels=["0.1 t", "1 t", "10 t", "100 t", "1,000 t"])
    ax.minorticks_off()
    ax.set_xlabel("Speed of the load along the ring")
    ax.set_title("Largest point load carried")
    ax.legend(loc="lower left", fontsize=8.5, ncol=1)
    return style.save(fig, "load-capacity", outdir)
