"""Sketch: two lanes running opposite ways through the same stationary speed ramps."""
import numpy as np

from . import style

RAMP_A = (0.22, 0.34)
RAMP_B = (0.66, 0.78)
SLOW, FAST = 1.0, 1.6     # exaggerated; the text's ramps are parts in a thousand


def speed(s):
    """Slug speed along the ring as a function of position: the same for both lanes."""
    s = np.asarray(s, dtype=float)
    up = np.clip((s - RAMP_A[0]) / (RAMP_A[1] - RAMP_A[0]), 0.0, 1.0)
    down = np.clip((s - RAMP_B[0]) / (RAMP_B[1] - RAMP_B[0]), 0.0, 1.0)
    return SLOW + (FAST - SLOW) * (up - down)


def slug_positions(count_scale=0.028, phase=0.0):
    """Positions of slugs at one instant. At fixed mass flux the spacing is proportional to speed."""
    s_fine = np.linspace(0.0, 1.0, 4001)
    travel_time = np.concatenate([[0.0], np.cumsum(np.diff(s_fine) / speed(s_fine[:-1]))])
    ticks = np.arange(phase * count_scale, travel_time[-1], count_scale)
    return np.interp(ticks, travel_time, s_fine)


def make(outdir=None):
    style.apply()
    fig, (ax, ax_u) = style.plt.subplots(2, 1, figsize=(6.8, 3.9), constrained_layout=True, sharex=True, gridspec_kw=dict(height_ratios=[2.6, 1.0]))
    for lo, hi in (RAMP_A, RAMP_B):
        for a in (ax, ax_u):
            a.axvspan(lo, hi, color=style.GRID, alpha=0.7, linewidth=0)
    rows = {"Lane running toward +s": (2.0, +1, style.SERIES[0], 0.0), "Lane running toward −s": (1.0, -1, style.SERIES[1], 0.5)}
    for label, (y, direction, colour, phase) in rows.items():
        ax.plot(slug_positions(phase=phase), np.full_like(slug_positions(phase=phase), y), linestyle="none", marker="o", markersize=5.5, color=colour, label=label)
        x0 = 0.03 if direction > 0 else 0.97
        ax.annotate("", xy=(x0 + 0.07 * direction, y + 0.33), xytext=(x0, y + 0.33), arrowprops=dict(arrowstyle="-|>", color=style.INK_2, linewidth=1.3, mutation_scale=12))
        for (lo, hi), push in ((RAMP_A, -1), (RAMP_B, +1)):
            mid = 0.5 * (lo + hi)
            ax.annotate("", xy=(mid + 0.055 * push, y - 0.33), xytext=(mid - 0.055 * push, y - 0.33), arrowprops=dict(arrowstyle="-|>", color=style.SERIES[2], linewidth=2.0, mutation_scale=13))
    # the structure, carrying the two pushes as tension between the ramps
    ax.plot([0.0, 1.0], [0.0, 0.0], color=style.INK, linewidth=2.6)
    a_mid, b_mid = 0.5 * sum(RAMP_A), 0.5 * sum(RAMP_B)
    ax.plot([a_mid, b_mid], [0.0, 0.0], color=style.SERIES[2], linewidth=5.0, solid_capstyle="butt", alpha=0.55)
    ax.text(0.5 * (a_mid + b_mid), -0.38, "structure in tension between the ramps", ha="center", va="center", color=style.INK_2, fontsize=9)
    ax.text(a_mid, 2.72, "ramp A", ha="center", color=style.INK_2, fontsize=9)
    ax.text(b_mid, 2.72, "ramp B", ha="center", color=style.INK_2, fontsize=9)
    ax.set_ylim(-0.75, 3.0)
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    handles, labels = ax.get_legend_handles_labels()
    push = ax.plot([], [], color=style.SERIES[2], linewidth=2.0)[0]

    s = np.linspace(0.0, 1.0, 400)
    ax_u.plot(s, speed(s), color=style.INK, linewidth=1.8)
    ax_u.set_ylim(0.8, 1.8)
    ax_u.set_yticks([SLOW, FAST], labels=["slower", "faster"])
    ax_u.set_xticks([])
    ax_u.set_xlim(0.0, 1.0)
    ax_u.set_xlabel("Position along the ring, s")
    ax_u.set_title("Slug speed at each place, the same in both lanes")
    ax_u.title.set_fontsize(9.5)
    ax_u.grid(False)
    fig.legend(handles + [push], labels + ["Push on the structure"], loc="outside lower center", ncol=3)
    return style.save(fig, "speed-ramp", outdir)
