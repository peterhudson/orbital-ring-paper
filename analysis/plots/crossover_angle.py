"""Helix angle at which inflation and lift ask for the same momentum flux, and the wrap pitch."""
import math

import numpy as np

from ..params import EARTH_500
from . import style

SPEEDS = (8.5e3, 10.0e3, 12.0e3, 15.0e3)


def curves(case=EARTH_500, speeds=SPEEDS, gammas=None):
    gammas = np.logspace(0.0, 2.0, 81) if gammas is None else gammas
    out = {}
    for u in speeds:
        c = case.with_(u=u)
        alpha = np.array([c.alpha_cross(g) for g in gammas])
        pitch = np.array([c.pitch(g) for g in gammas])
        out[u] = (np.degrees(alpha), pitch / 1e3)
    return gammas, out


def make(outdir=None):
    gammas, data = curves()
    fig, (ax_a, ax_p) = style.figure(6.8, 3.4, ncols=2)
    for colour, (u, (alpha, pitch)) in zip(style.SERIES, data.items()):
        label = f"{u / 1e3:g} km/s"
        ax_a.plot(gammas, alpha, color=colour, label=label)
        ax_p.plot(gammas, pitch, color=colour, label=label)
    ref = EARTH_500
    for ax, value in ((ax_a, math.degrees(ref.alpha_cross())), (ax_p, ref.pitch() / 1e3)):
        ax.plot([ref.gamma], [value], marker="o", linestyle="none", color=style.INK, markersize=7)
        ax.set_xscale("log")
        ax.set_xlabel("Prestress ratio Γ")
        ax.set_xticks([1, 3, 10, 30, 100], labels=["1", "3", "10", "30", "100"])
        ax.minorticks_off()
    ax_a.annotate("reference case", (ref.gamma, math.degrees(ref.alpha_cross())), xytext=(-8, 16), textcoords="offset points", ha="right", color=style.INK_2, fontsize=9)
    ax_a.set_title("Crossover helix angle, degrees")
    ax_a.set_ylim(0.0, None)
    ax_p.set_title("Length of ring for one wrap, km")
    ax_p.set_yscale("log")
    ax_p.set_yticks([3, 10, 30, 100, 300], labels=["3", "10", "30", "100", "300"])
    ax_p.minorticks_off()
    handles, labels = ax_a.get_legend_handles_labels()
    fig.legend(handles, labels, title="Ring-direction speed", loc="outside lower center", ncol=4, title_fontsize=9)
    return style.save(fig, "crossover-angle", outdir)
