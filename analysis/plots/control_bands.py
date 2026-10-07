"""Which mechanism holds the ring's shape at which wavelength."""
import math

from ..collective import CollectiveModel
from ..params import EARTH_500
from . import style

SHORT = 1.0      # left edge of the chart, m
CUTOFF = 300.0   # the mirror law's short-wave cut-off, m
STATOR_BETTER = 250e3   # above this wavelength the stators recover a shape error with less travel than steering


def bands(case=EARTH_500):
    """(label, shortest wavelength, longest wavelength, kind). Wavelengths in metres."""
    ring = case.circumference
    return [
        ("Bending stiffness and structural damping", SHORT, CUTOFF, "passive"),
        ("Steering: mirror law with look-ahead", CUTOFF, ring / 2.0, "designed"),
        ("Steering set points, for steady loads", CUTOFF, ring / 2.0, "designed"),
        ("Stator weight trim, for changing loads", STATOR_BETTER, ring / 2.0, "open"),
        ("Stators hold slug spacing", SHORT, ring, "designed"),
        ("Stator feedback holds the ring on center", ring, ring, "designed"),
    ]


def growth_times(wavelengths, case=EARTH_500):
    """E-folding time of the shape with streams that follow the structure, s (local rate)."""
    model = CollectiveModel.reference(case)
    return [1.0 / model.rigid_growth_rate(2.0 * math.pi / w) for w in wavelengths]


def _duration(seconds: float) -> str:
    if seconds < 0.1:
        return f"{seconds * 1e3:.0f} ms"
    if seconds < 1.0:
        return f"{seconds:.2f} s"
    if seconds < 90.0:
        return f"{seconds:.1f} s" if seconds < 10 else f"{seconds:.0f} s"
    return f"{seconds / 60.0:.0f} min"


def make(outdir=None):
    case = EARTH_500
    rows = bands(case)
    fig, ax = style.figure(6.8, 3.7)
    colours = {"passive": style.MUTED, "designed": style.SERIES[0], "open": style.SERIES[1]}
    names = {"passive": "Needs no control", "designed": "Designed and simulated here", "open": "Needed, not designed here"}
    seen = set()
    for i, (label, lo, hi, kind) in enumerate(rows):
        y = len(rows) - 1 - i
        name = None if kind in seen else names[kind]
        seen.add(kind)
        if lo == hi:
            ax.plot([lo], [y], marker="o", markersize=9, linestyle="none", color=colours[kind], label=name)
            ax.annotate(label, (lo, y), xytext=(-10, 0), textcoords="offset points", ha="right", va="center", color=style.INK, fontsize=8.5)
            continue
        ax.barh(y, hi - lo, left=lo, height=0.52, color=colours[kind], edgecolor=style.SURFACE, linewidth=1.0,
                hatch="///" if kind == "open" else None, label=name)
        if kind == "open" or lo > 10.0 * SHORT and hi / lo < 1e3:
            ax.annotate(label, (lo, y), xytext=(-6, 0), textcoords="offset points", ha="right", va="center", color=style.INK, fontsize=8.5)
        else:
            ax.text(math.sqrt(lo * hi), y + 0.43, label, ha="center", va="bottom", color=style.INK, fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlim(SHORT, case.circumference * 1.6)
    ticks = [1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6, 1e7]
    ax.set_xticks(ticks, labels=["1 m", "10 m", "100 m", "1 km", "10 km", "100 km", "1,000 km", "10,000 km"])
    ax.minorticks_off()
    ax.set_xlabel("Wavelength of the shape error along the ring")
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.grid(axis="y", visible=False)
    top = ax.secondary_xaxis("top", functions=(lambda w: w, lambda w: w))
    marks = [1e3, 1e4, 1e5, 1e6, 1e7]
    top.set_xticks(marks, labels=[_duration(t) for t in growth_times(marks, case)])
    top.minorticks_off()
    top.set_xlabel("Time for the shape error to grow e-fold if the streams simply follow the structure", fontsize=8.5, color=style.INK_2)
    top.tick_params(colors=style.INK_2, length=0)
    top.spines["top"].set_visible(False)
    ax.legend(loc="lower left", fontsize=8.5)
    return style.save(fig, "control-bands", outdir)
