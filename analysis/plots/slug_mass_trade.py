"""The slug-size fork: timing gets harder as slugs shrink, energy per slug grows as they swell."""
import numpy as np

from ..params import EARTH_500
from . import style

TNT = 4.184e6      # J per kg of TNT, by definition


def curves(case=EARTH_500, masses=None):
    masses = np.logspace(-2.0, 3.0, 101) if masses is None else masses
    headway = np.array([case.headway(m) for m in masses])
    energy = np.array([case.slug_energy(m) for m in masses])
    return masses, headway, energy


def make(outdir=None):
    case = EARTH_500
    masses, headway, energy = curves(case)
    fig, (ax_t, ax_e) = style.figure(6.8, 3.5, ncols=2)

    ax_t.plot(masses, headway, color=style.SERIES[0], label="Time between slugs")
    ax_t.plot(masses, headway / 100.0, color=style.SERIES[1], label="Timing error for 1% spacing error")
    ax_t.set_title("Timing in one lane, seconds")
    ax_t.set_yscale("log")
    ax_t.set_yticks([1e-9, 1e-6, 1e-3], labels=["1 ns", "1 µs", "1 ms"])
    ax_t.legend(loc="upper left")
    ax_t.set_ylim(1e-9, 1.0)

    ax_e.plot(masses, energy, color=style.SERIES[0])
    ax_e.set_title("Kinetic energy of one slug")
    ax_e.set_yscale("log")
    ax_e.set_yticks([1e6, 1e9, 1e12], labels=["1 MJ", "1 GJ", "1 TJ"])
    ax_e.set_ylim(1e5, 1e12)
    for kg, text, x, ha in ((1.0, "1 kg of TNT", masses[-1], "right"), (1000.0, "1 tonne of TNT", masses[0], "left")):
        ax_e.axhline(kg * TNT, color=style.AXIS, linewidth=1.0, linestyle=(0, (4, 3)))
        ax_e.text(x, kg * TNT * 1.5, text, color=style.INK_2, fontsize=8.5, va="bottom", ha=ha)

    for ax, value in ((ax_t, case.headway()), (ax_e, case.slug_energy())):
        ax.plot([case.slug_mass], [value], marker="o", linestyle="none", color=style.INK, markersize=7)
        ax.set_xscale("log")
        ax.set_xlabel("Slug mass, kg")
        ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000], labels=["0.01", "0.1", "1", "10", "100", "1000"])
        ax.minorticks_off()
    ax_e.annotate("reference slug", (case.slug_mass, case.slug_energy()), xytext=(8, -14), textcoords="offset points", color=style.INK_2, fontsize=9)
    return style.save(fig, "slug-mass-trade", outdir)
