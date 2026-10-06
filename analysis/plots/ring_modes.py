"""Growth rate of whole-ring modes against mode number."""
import numpy as np

from .. import ring
from ..params import EARTH_500 as C
from ..ring_modes import RingModes
from ..ring_particles import measured_growth_rate
from . import style


def make(outdir=None):
    om = C.omega_orb
    ns = np.arange(1, 9)
    fig, ax = style.figure(6.8, 4.0)
    soft = RingModes(ea=5e10)
    truss3, x03 = ring.ring_truss(n_nodes=240, ea=5e12, dim=3)
    out_plane = ring.growth_rates_by_mode(truss3, x03, "out")
    particle_ns = (1, 2, 3)
    particles = [measured_growth_rate(n, dt=0.25) / om for n in particle_ns]
    blue, orange = style.SERIES[0], style.SERIES[1]
    ax.plot(ns, ns, color=style.AXIS, linestyle=(0, (4, 3)), linewidth=1.2, label="Short-wave rule: n times the orbital rate")
    ax.plot(ns, [soft.growth_rate(n) / om for n in ns], color=blue, label="In plane: linear model")
    ax.plot(particle_ns, particles, "o", color=blue, markersize=8, label="In plane: particle simulation")
    ax.plot(ns, [ring.growth_rate_out_of_plane(n) / om for n in ns], color=orange, label="Out of plane: closed form")
    ax.plot(ns, [np.sqrt(max(out_plane[n], 0)) / om for n in ns], "o", color=orange, markersize=8, label="Out of plane: truss model")
    ax.set_xlabel("Mode number n (waves round the ring)")
    ax.set_ylabel("Growth rate / orbital rate")
    ax.set_xticks(ns)
    ax.set_ylim(0, 9)
    ax.set_xlim(0.6, 8.4)
    ax.legend(loc="upper left")
    ax.set_title("Every shape mode of the ring grows, short waves fastest")
    return style.save(fig, "ring-mode-growth", outdir)
