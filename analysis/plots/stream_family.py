"""Sketch: the three ways a stream can be loaded, and the effective tension in each."""
import numpy as np

from . import style


def _clean(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_aspect("equal")


def _arrow(ax, start, end, colour, width=1.6, scale=11):
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="-|>", color=colour, linewidth=width, mutation_scale=scale))


def _loop(ax):
    t = np.linspace(0.0, 2.0 * np.pi, 400)
    r = 1.0 + 0.22 * np.cos(2 * t + 0.6) + 0.12 * np.sin(3 * t)
    x, y = r * np.cos(t), 0.8 * r * np.sin(t)
    ax.plot(x, y, color=style.SERIES[0], linewidth=2.2)
    for i in (40, 240):
        _arrow(ax, (x[i], y[i]), (x[i + 12], y[i + 12]), style.INK, 1.3, 13)
    ax.set_title("Free loop: no load")
    ax.text(0.0, -1.55, "Effective tension zero.\nAny shape will do.\nIt carries nothing.", ha="center", va="top", color=style.INK_2, fontsize=9, linespacing=1.4)
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.7, 1.7)
    _clean(ax)


def _arch(ax):
    ang = np.radians(np.linspace(140, 40, 200))
    radius = 1.9
    x, y = radius * np.cos(ang), radius * np.sin(ang) - 1.25
    ax.plot(x, y, color=style.SERIES[0], linewidth=2.2)
    ax.plot(x, y + 0.07, color=style.INK, linewidth=2.6)
    for i in (25, 75, 125, 175):
        _arrow(ax, (x[i], y[i] + 0.75), (x[i], y[i] + 0.22), style.SERIES[1])
    for end, sign in ((0, -1), (-1, 1)):
        ax.plot([x[end]], [y[end] - 0.02], marker="^", markersize=11, color=style.INK_2, linestyle="none")
    # thrust at the abutments, along the arch
    _arrow(ax, (x[8], y[8]), (x[0] - 0.42, y[0] - 0.36), style.SERIES[2], 2.0, 13)
    _arrow(ax, (x[-9], y[-9]), (x[-1] + 0.42, y[-1] - 0.36), style.SERIES[2], 2.0, 13)
    ax.set_title("Arch: load across")
    ax.text(0.0, -1.55, "Compression = weight per\nmetre × radius of curvature.\nA ring is an arch with no ends.", ha="center", va="top", color=style.INK_2, fontsize=9, linespacing=1.4)
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.7, 1.7)
    _clean(ax)


def _column(ax):
    ax.plot([-0.09, -0.09], [-1.3, 0.9], color=style.SERIES[0], linewidth=2.2)
    ax.plot([0.09, 0.09], [-1.3, 0.9], color=style.SERIES[0], linewidth=2.2)
    ax.plot([0.0, 0.0], [-1.3, 0.9], color=style.INK, linewidth=1.4)
    _arrow(ax, (-0.09, -0.6), (-0.09, -0.1), style.INK, 1.3, 13)
    _arrow(ax, (0.09, 0.2), (0.09, -0.3), style.INK, 1.3, 13)
    ax.plot([-0.32, 0.32], [0.98, 0.98], color=style.INK, linewidth=6.0, solid_capstyle="butt")
    _arrow(ax, (0.0, 1.5), (0.0, 1.08), style.SERIES[1])
    ax.plot([-0.5, 0.5], [-1.3, -1.3], color=style.INK_2, linewidth=1.2)
    _arrow(ax, (0.42, -0.75), (0.42, -1.25), style.SERIES[2], 2.0, 13)
    ax.set_title("Column: load along")
    ax.text(0.0, -1.55, "Compression at any height\n= weight of everything\nabove it.", ha="center", va="top", color=style.INK_2, fontsize=9, linespacing=1.4)
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.7, 1.7)
    _clean(ax)


def make(outdir=None):
    fig, axes = style.figure(6.8, 3.5, ncols=3)
    _loop(axes[0])
    _arch(axes[1])
    _column(axes[2])
    for ax in axes:
        ax.title.set_fontsize(9.5)
    handles = [axes[0].plot([], [], color=c, linewidth=w)[0] for c, w in ((style.SERIES[0], 2.2), (style.INK, 2.6), (style.SERIES[1], 1.6), (style.SERIES[2], 2.0))]
    fig.legend(handles, ["Streams", "Structure", "Load", "Thrust passed to the ground"], loc="outside lower center", ncol=4)
    return style.save(fig, "stream-family", outdir)
