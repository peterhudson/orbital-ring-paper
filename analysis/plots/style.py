"""Shared look for the generated figures.

Colours follow a palette checked for colour-vision-deficiency separation:
series hues are used in this fixed order and never for text. Text and axes
use the ink colours.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]   # blue, orange, aqua, yellow
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#ffffff"

OUTDIR = Path(__file__).resolve().parents[2] / "figures" / "generated"


def apply():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "font.family": "sans-serif", "font.size": 10,
        "svg.hashsalt": "orbital-ring-paper",   # fixed ids, so reruns give identical files
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK_2, "axes.titlecolor": INK,
        "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-",
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK_2, "ytick.labelcolor": INK_2,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "lines.linewidth": 1.8, "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
        "lines.markersize": 6.5, "lines.markeredgecolor": SURFACE, "lines.markeredgewidth": 1.4,
        "legend.frameon": False, "legend.fontsize": 9, "legend.labelcolor": INK_2,
        "svg.fonttype": "path",
    })


def figure(width=6.8, height=3.6, **kw):
    apply()
    return plt.subplots(figsize=(width, height), constrained_layout=True, **kw)


def save(fig, name: str, outdir: Path | None = None) -> Path:
    out = (outdir or OUTDIR) / f"{name}.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, metadata={"Date": None})     # no timestamp, so reruns give identical files
    plt.close(fig)
    return out


def end_label(ax, x, y, text, dx=6, dy=0, **kw):
    """A direct label beside the end of a line, in ink (never the series colour)."""
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", color=INK_2, fontsize=9, va="center", **kw)
