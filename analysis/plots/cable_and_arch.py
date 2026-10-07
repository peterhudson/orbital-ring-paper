"""Sketch: a cable and an arch of momentum under the same loads.

Both obey T_eff y'' = q with the ends held; only the sign of T_eff differs,
so each shape is the other upside down.
"""
import numpy as np

from . import style

EXTRA = (0.40, 0.60)     # stretch that carries extra weight
EXTRA_SIZE = 1.2         # extra load there, as a fraction of the uniform load


def shape(extra: float, n: int = 801):
    """Deflection of a unit-tension cable with held ends under a downward load
    of 1 per unit length plus `extra` on the EXTRA stretch. Negative is down."""
    s = np.linspace(0.0, 1.0, n)
    q = 1.0 + extra * ((s >= EXTRA[0]) & (s <= EXTRA[1]))
    ds = s[1] - s[0]
    slope = np.cumsum(q) * ds
    y = np.cumsum(slope) * ds
    y -= y[0] + (y[-1] - y[0]) * s          # hold both ends at zero
    return s, y


def _panel(ax, title, sign, note):
    s, base = shape(0.0)
    _, loaded = shape(EXTRA_SIZE)
    scale = 0.9 / abs(base).max()
    ax.plot(s, sign * scale * base, color=style.INK, linewidth=2.4, label="Uniform load")
    ax.plot(s, sign * scale * loaded, color=style.SERIES[0], linewidth=1.9, label="With extra weight on the middle stretch")
    top = max(0.0, sign * scale * loaded.min(), sign * scale * loaded.max())
    for sc in np.linspace(EXTRA[0] + 0.02, EXTRA[1] - 0.02, 4):
        ax.annotate("", xy=(sc, top + 0.25), xytext=(sc, top + 0.75), arrowprops=dict(arrowstyle="-|>", color=style.SERIES[1], linewidth=1.8, mutation_scale=12))
    ax.plot([0.0, 1.0], [0.0, 0.0], linestyle="none", marker="o", markersize=7, color=style.INK_2)
    ax.set_title(title)
    ax.text(0.5, -2.05, note, ha="center", va="center", color=style.INK_2, fontsize=9, linespacing=1.4)
    ax.set_xlim(-0.06, 1.06)
    ax.set_ylim(-2.4, 2.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)


def make(outdir=None):
    fig, axes = style.figure(6.8, 3.3, ncols=2)
    _panel(axes[0], "Cable: positive effective tension", 1.0, "It hangs, and sags further\nwhere the weight is added.")
    _panel(axes[1], "Arch: negative effective tension", -1.0, "It stands, and rises\nwhere the weight is added.")
    for ax in axes:
        ax.title.set_fontsize(9.5)
    handles, labels = axes[0].get_legend_handles_labels()
    arrow = axes[0].plot([], [], color=style.SERIES[1], linewidth=1.8)[0]
    fig.legend(handles + [arrow], labels + ["Extra weight"], loc="outside lower center", ncol=3)
    return style.save(fig, "cable-and-arch", outdir)
