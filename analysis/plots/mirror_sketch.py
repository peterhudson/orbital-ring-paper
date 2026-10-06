"""Sketch: what a following guide and a mirroring guide do to a bump in the structure."""
import numpy as np

from . import style


def _panel(ax, title, stream_gain, verdict):
    s = np.linspace(0.0, 1.0, 400)
    y = 0.22 * np.sin(2.0 * np.pi * s)
    ax.plot(s, y, color=style.INK, linewidth=2.6, label="Structure")
    ax.plot(s, stream_gain * y, color=style.SERIES[0], linewidth=1.8, label="Stream path")
    ax.axhline(0.0, color=style.AXIS, linewidth=0.8, linestyle=(0, (4, 3)))
    # The stream pushes the structure toward the outside of its own bends.
    for sc in (0.25, 0.75):
        yc = 0.22 * np.sin(2.0 * np.pi * sc)
        push = np.sign(stream_gain * yc) * 0.17
        ax.annotate("", xy=(sc, yc + push), xytext=(sc, yc), arrowprops=dict(arrowstyle="-|>", color=style.SERIES[1], linewidth=2.0, mutation_scale=14))
    ax.set_title(title)
    ax.text(0.5, -0.5, verdict, ha="center", va="center", color=style.INK_2, fontsize=9, linespacing=1.4)
    ax.set_ylim(-0.62, 0.5)
    ax.set_xlim(-0.05, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)


def make(outdir=None):
    fig, axes = style.figure(6.8, 3.1, ncols=2)
    _panel(axes[0], "Stream follows the structure", 1.0, "The push is outward at every bump.\nThe bump grows.")
    _panel(axes[1], "Stream steered to the mirror image", -0.5, "The push is back toward the middle.\nThe bump shrinks.")
    for ax in axes:
        ax.title.set_fontsize(9.5)
    handles, labels = axes[0].get_legend_handles_labels()
    arrow = axes[0].plot([], [], color=style.SERIES[1], linewidth=2.0)[0]
    fig.legend(handles + [arrow], labels + ["Push of the stream on the structure"], loc="outside lower center", ncol=3)
    return style.save(fig, "mirror-law-sketch", outdir)
