"""The energies a fault can release, on one logarithmic scale, beside TNT equivalents."""
from ..params import EARTH_500
from . import style

TNT_TONNE = 4.184e9     # J, by definition


def ladder(case=EARTH_500):
    """(label, joules, is_ring) from smallest to largest."""
    lane_fault = 0.010 * case.mdot_lane * 0.5 * case.v**2
    rows = [
        ("One 10 kg slug", case.slug_energy(), True),
        ("1 tonne of TNT", TNT_TONNE, False),
        ("One lane for 10 ms", lane_fault, True),
        ("One metre of ring, all streams", case.E_prime, True),
        ("1 kiloton of TNT", 1e3 * TNT_TONNE, False),
        ("One kilometre of ring", 1e3 * case.E_prime, True),
        ("1 megaton of TNT", 1e6 * TNT_TONNE, False),
        ("The whole ring", case.total_kinetic_energy, True),
    ]
    return sorted(rows, key=lambda r: r[1])


def _text(joules: float) -> str:
    for unit, size in (("EJ", 1e18), ("PJ", 1e15), ("TJ", 1e12), ("GJ", 1e9), ("MJ", 1e6)):
        if joules >= size:
            value = joules / size
            return f"{value:.0f} {unit}" if value >= 10.0 else f"{value:.1f} {unit}"
    return f"{joules:.0f} J"


def make(outdir=None):
    rows = ladder()
    fig, ax = style.figure(6.8, 3.6)
    seen = set()
    for i, (label, joules, is_ring) in enumerate(rows):
        colour = style.SERIES[0] if is_ring else style.SERIES[1]
        name = "This ring" if is_ring else "Explosive, for scale"
        ax.plot([1e8, joules], [i, i], color=style.GRID, linewidth=1.2, zorder=1)
        ax.plot([joules], [i], marker="o" if is_ring else "D", linestyle="none", color=colour, markersize=8 if is_ring else 6.5,
                label=None if name in seen else name, zorder=3)
        seen.add(name)
        ax.annotate(_text(joules), (joules, i), xytext=(9, 0), textcoords="offset points", va="center", color=style.INK_2, fontsize=9)
    ax.set_yticks(range(len(rows)), labels=[r[0] for r in rows])
    ax.set_xscale("log")
    ax.set_xlim(1e8, 1e20)
    ax.set_xticks([1e9, 1e12, 1e15, 1e18], labels=["1 GJ", "1 TJ", "1 PJ", "1 EJ"])
    ax.minorticks_off()
    ax.grid(axis="y", visible=False)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_title("Kinetic energy of the streams")
    ax.legend(loc="lower right")
    return style.save(fig, "fault-energy-ladder", outdir)
