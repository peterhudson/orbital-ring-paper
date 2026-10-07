"""Sketch: the four lanes of a balanced cell on the unrolled tube surface, and what the wrap does in cross-section."""
import math

import numpy as np

from ..params import EARTH_500
from . import style

# lane number: (right-handed?, travels toward +s?), as in the table of the four-lane chapter
LANES = {1: (True, True), 2: (True, False), 3: (False, True), 4: (False, False)}


def helix_numbers(case=EARTH_500):
    alpha = case.alpha_cross()
    v_round = case.v * math.sin(alpha)
    return dict(alpha_deg=math.degrees(alpha), pitch_km=case.pitch() / 1e3, girth=2.0 * math.pi * case.a,
                v_round=v_round, accel=v_round**2 / case.a, load=case.normal_load_lane)


def _surface(ax, num):
    ax.set_title("Tube surface, laid flat")
    offsets = {1: 0.00, 2: 0.50, 3: 0.25, 4: 0.75}       # where each lane crosses the left edge, in turns
    label_at = {1: 0.20, 2: 0.30, 3: 0.70, 4: 0.56}      # clear of the crossings
    for lane, (right, forward) in LANES.items():
        colour = style.SERIES[0] if right else style.SERIES[1]
        start = offsets[lane]
        for shift in (-1.0, 0.0, 1.0):                   # draw the wrapped copies
            s = np.array([0.0, 1.0])
            ax.plot(s, start + shift + (s if right else -s), color=colour, linewidth=1.9, clip_on=True)
        s0 = label_at[lane]
        y0 = (start + (s0 if right else -s0)) % 1.0
        step = 1.0 if forward else -1.0                  # direction of travel along s
        slope = 1.0 if right else -1.0
        ax.annotate("", xy=(s0 + 0.125 * step, y0 + 0.125 * step * slope), xytext=(s0 + 0.045 * step, y0 + 0.045 * step * slope),
                    arrowprops=dict(arrowstyle="-|>", color=style.INK, linewidth=1.6, mutation_scale=14), zorder=5)
        ax.plot([s0], [y0], marker="o", markersize=15, color=style.SURFACE, markeredgecolor=style.INK, markeredgewidth=1.2, linestyle="none", zorder=6)
        ax.text(s0, y0, str(lane), color=style.INK, fontsize=9.5, fontweight="bold", ha="center", va="center", zorder=7)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks([0.0, 1.0], labels=["0", f"{num['pitch_km']:.0f} km"])
    ax.set_yticks([0.0, 1.0], labels=["0", f"{num['girth']:.0f} m"])
    ax.set_xlabel("Along the ring, s  (one wrap)")
    ax.set_ylabel("Round the tube, aθ")
    ax.grid(False)
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    handles = [ax.plot([], [], color=style.SERIES[0], linewidth=1.9)[0], ax.plot([], [], color=style.SERIES[1], linewidth=1.9)[0]]
    return handles, ["Right-handed lanes", "Left-handed lanes"]


def _section(ax, num):
    ax.set_title("Looking along the ring")
    t = np.linspace(0.0, 2.0 * np.pi, 361)
    ax.plot(np.cos(t), np.sin(t), color=style.INK, linewidth=2.2)
    for ang in np.radians(np.arange(0, 360, 45)):
        ax.annotate("", xy=(1.34 * np.cos(ang), 1.34 * np.sin(ang)), xytext=(1.04 * np.cos(ang), 1.04 * np.sin(ang)),
                    arrowprops=dict(arrowstyle="-|>", color=style.SERIES[2], linewidth=1.6, mutation_scale=11))
    arc = np.radians(np.linspace(20, 70, 40))
    ax.plot(0.8 * np.cos(arc), 0.8 * np.sin(arc), color=style.INK_2, linewidth=1.3)
    ax.annotate("", xy=(0.8 * np.cos(arc[-1]), 0.8 * np.sin(arc[-1])), xytext=(0.8 * np.cos(arc[-3]), 0.8 * np.sin(arc[-3])),
                arrowprops=dict(arrowstyle="-|>", color=style.INK_2, linewidth=1.3, mutation_scale=11))
    ax.text(0.0, 0.12, f"{num['v_round']:.0f} m/s round the tube", ha="center", va="center", color=style.INK_2, fontsize=9)
    ax.text(0.0, -0.14, f"{num['accel']:.0f} m/s² inward", ha="center", va="center", color=style.INK_2, fontsize=9)
    ax.text(0.0, -0.40, f"{num['load'] / 1e3:.1f} kN/m per lane", ha="center", va="center", color=style.INK_2, fontsize=9)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    return [ax.plot([], [], color=style.SERIES[2], linewidth=1.6)[0]], ["Push of the slugs on the wall"]


def make(outdir=None):
    num = helix_numbers()
    fig, (ax_s, ax_c) = style.figure(6.8, 3.6, ncols=2, gridspec_kw=dict(width_ratios=[1.25, 1.0]))
    h1, l1 = _surface(ax_s, num)
    h2, l2 = _section(ax_c, num)
    fig.legend(h1 + h2, l1 + l2, loc="outside lower center", ncol=3)
    return style.save(fig, "unrolled-helix", outdir)
