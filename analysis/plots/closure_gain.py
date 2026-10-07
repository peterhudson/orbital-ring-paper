"""The closure loop's gain, and the power to keep the streams at speed, against the guide's lift-to-drag ratio."""
import numpy as np

from .. import closure
from ..params import EARTH_500
from . import style

GAMMAS = (0.0, 1.0, 10.0, 30.0)
LABELS = {0.0: "No helix prestress", 1.0: "Γ = 1", 10.0: "Γ = 10 (reference)", 30.0: "Γ = 30"}


def curves(ratios=None, gammas=GAMMAS, case=EARTH_500, a=closure.REFERENCE):
    ratios = np.logspace(3.0, 7.0, 81) if ratios is None else ratios
    out = {}
    for gamma in gammas:
        gain = np.array([closure.loop_gain(case, a.with_(lift_to_drag=r), gamma) for r in ratios])
        power = np.array([closure.ring_power(case, a.with_(lift_to_drag=r), gamma) for r in ratios])
        out[gamma] = (gain, power)
    return ratios, out


def make(outdir=None):
    ratios, data = curves()
    fig, (ax_g, ax_p) = style.figure(6.8, 3.7, ncols=2)
    for colour, (gamma, (gain, power)) in zip(style.SERIES, data.items()):
        ax_g.plot(ratios, gain, color=colour, label=LABELS[gamma])
        ax_p.plot(ratios, power / 1e9, color=colour)
    ax_g.axhline(1.0, color=style.INK_2, linewidth=1.0, linestyle=(0, (4, 3)))
    ax_g.set_yscale("log")
    ax_g.set_ylim(0.003, 30.0)
    ax_g.set_yticks([0.01, 0.1, 1.0, 10.0], labels=["0.01", "0.1", "1", "10"])
    ax_g.set_title("Gain of the closure loop")
    ax_p.set_yscale("log")
    ax_p.set_ylim(0.3, 3.0e5)
    ax_p.set_yticks([1.0, 1e1, 1e2, 1e3, 1e4, 1e5], labels=["1 GW", "10 GW", "100 GW", "1 TW", "10 TW", "100 TW"])
    ax_p.set_title("Power to make up guide drag")
    for ax in (ax_g, ax_p):
        ax.set_xscale("log")
        ax.set_xlabel("Guide's ratio of normal force to drag")
        ax.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7], labels=["10³", "10⁴", "10⁵", "10⁶", "10⁷"])
        ax.minorticks_off()
    handles, labels = ax_g.get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=4)
    return style.save(fig, "closure-gain", outdir)
