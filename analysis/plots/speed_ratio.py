"""What the choice of stream speed costs and allows, for any arch of momentum."""
import numpy as np

from .. import generalize as gen
from ..collective import MIRROR_GAIN
from ..params import EARTH_500
from . import style


def curves(ratios=None):
    ratios = np.linspace(1.05, 2.5, 146) if ratios is None else ratios
    return (ratios, np.array([gen.stream_per_passive(r) for r in ratios]),
            np.array([gen.energy_over_floor(r) for r in ratios]), np.array([gen.steering_gain_limit(r) for r in ratios]))


def make(outdir=None):
    ratios, stream, energy, limit = curves()
    marks = {"reference ring": EARTH_500.u / EARTH_500.u_orb, "launch loop": gen.arch_row(gen.LAUNCH_LOOP_LIKE)["speed_ratio"]}
    fig, (ax_c, ax_s) = style.figure(6.8, 3.5, ncols=2)

    ax_c.plot(ratios, stream, color=style.SERIES[0], label="Stream mass per unit of mass carried")
    ax_c.plot(ratios, energy, color=style.SERIES[1], label="Stored energy, as a multiple of its floor")
    ax_c.set_yscale("log")
    ax_c.set_yticks([0.2, 0.5, 1, 2, 5, 10], labels=["0.2", "0.5", "1", "2", "5", "10"])
    ax_c.minorticks_off()
    ax_c.set_ylim(0.15, 12.0)
    ax_c.set_title("What a slower stream costs")
    ax_c.text(2.48, 1.75, "stored energy ÷ its floor", ha="right", va="bottom", color=style.INK_2, fontsize=8.5)
    ax_c.text(2.48, 0.62, "stream mass ÷ mass carried", ha="right", va="bottom", color=style.INK_2, fontsize=8.5)

    ax_s.plot(ratios, limit, color=style.SERIES[0])
    ax_s.axhline(MIRROR_GAIN, color=style.AXIS, linewidth=1.0, linestyle=(0, (4, 3)))
    ax_s.text(ratios[-1], MIRROR_GAIN - 0.12, "gain used in this paper", ha="right", va="top", color=style.INK_2, fontsize=8.5)
    ax_s.axvspan(ratios[0], gen.least_speed_ratio_for_gain(MIRROR_GAIN), color=style.GRID, alpha=0.7, linewidth=0)
    ax_s.set_ylim(0.0, 5.5)
    ax_s.set_title("Largest steering gain allowed")

    for name, nu in marks.items():
        ax_c.plot([nu, nu], [gen.stream_per_passive(nu), gen.energy_over_floor(nu)], linestyle="none", marker="o", color=style.INK, markersize=6.5)
        ax_s.plot([nu], [gen.steering_gain_limit(nu)], linestyle="none", marker="o", color=style.INK, markersize=6.5)
        ax_s.annotate(name, (nu, gen.steering_gain_limit(nu)), xytext=(9, 3), textcoords="offset points", ha="left", va="center", color=style.INK_2, fontsize=8.5)
    for ax in (ax_c, ax_s):
        ax.set_xlabel("Stream speed ÷ threshold speed")
        ax.set_xlim(1.0, 2.5)
        ax.set_xticks([1.0, 1.5, 2.0, 2.5])
    return style.save(fig, "speed-ratio", outdir)
