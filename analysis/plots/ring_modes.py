"""Growth rate of whole-ring modes against azimuthal number."""
import numpy as np

from .. import ring
from ..params import EARTH_500 as C
from . import style


def make(outdir=None):
    om = C.omega_orb
    ns = np.arange(1, 9)
    fig, ax = style.figure(6.8, 3.9)
    ea = 5e10
    truss, x0 = ring.ring_truss(n_nodes=360, ea=ea)
    in_plane = ring.growth_rates_by_mode(truss, x0, "in")
    truss3, x03 = ring.ring_truss(n_nodes=240, ea=5e12, dim=3)
    out_plane = ring.growth_rates_by_mode(truss3, x03, "out")
    curves = [
        ("In plane, inextensible ring", [ring.growth_rate_in_plane(n) / om for n in ns], None),
        ("In plane, hoop stiffness 50 GN", [ring.growth_rate_in_plane(n, ea=ea) / om for n in ns], [np.sqrt(max(in_plane[n], 0)) / om for n in ns]),
        ("Out of plane", [ring.growth_rate_out_of_plane(n) / om for n in ns], [np.sqrt(max(out_plane[n], 0)) / om for n in ns]),
    ]
    for colour, (label, formula, computed) in zip(style.SERIES, curves):
        ax.plot(ns, formula, color=colour, label=label)
        if computed is not None:
            ax.plot(ns, computed, "o", color=colour)
    ax.plot([], [], "o", color=style.MUTED, label="Momentum-truss model")
    ax.set_xlabel("Azimuthal mode number n (waves round the ring)")
    ax.set_ylabel("Growth rate / orbital rate")
    ax.set_xticks(ns)
    ax.set_ylim(0, 9)
    ax.legend(loc="upper left")
    ax.set_title("Every mode of a momentum-supported ring grows, short waves fastest")
    return style.save(fig, "ring-mode-growth", outdir)
