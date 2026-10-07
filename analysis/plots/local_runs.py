"""Local particle simulation: one wave on 5 km of structure, with a spring
guide and with the mirror law, against the eigenvalue predictions."""
import math

import numpy as np

from ..collective import CollectiveModel
from ..particles import LocalParticleSim
from . import style


def _run(model, mode, duration):
    sim = LocalParticleSim(model, length=5e3, n_nodes=250, slugs_per_direction=500)
    sim.y += 1e-3 * np.cos(2 * math.pi * mode * sim.s_nodes / 5e3)
    t, a = sim.run(duration, record_modes=(mode,), every=10)
    return np.concatenate([[0.0], t]), np.concatenate([[1e-3], np.abs(a[:, 0])])


def make(outdir=None):
    mode, wavelength = 2, 2500.0
    k = 2 * math.pi / wavelength
    spring = CollectiveModel.reference(zeta=0.3, f_filter=200.0)
    mirror = CollectiveModel.mirror_reference(f_filter=200.0, preview=30.0)
    fig, ax = style.figure(6.8, 3.8)
    t, a = _run(spring, mode, 0.6)
    rate = spring.growth_rate(k)
    ax.plot(t, 1e3 * a, color=style.SERIES[1], label="Spring guide: simulation")
    ax.plot(t, 1e3 * a[len(a) // 2] * np.exp(rate * (t - t[len(a) // 2])), color=style.SERIES[1], linestyle=(0, (4, 3)), linewidth=1.2,
            label=f"Predicted growth, {rate:.0f} per second")
    t, a = _run(mirror, mode, 0.6)
    rate = mirror.growth_rate(k)
    ax.plot(t, 1e3 * a, color=style.SERIES[2], label="Mirror law: simulation")
    ax.plot(t, 1.0 * np.exp(rate * t), color=style.SERIES[2], linestyle=(0, (4, 3)), linewidth=1.2, label=f"Predicted envelope, decay {-rate:.0f} per second")
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1e3)
    ax.set_xlim(0, 0.6)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude of the wave (mm)")
    ax.set_title("A 2.5 km wave, 1 mm high, in the particle simulation")
    ax.legend(loc="center right")
    return style.save(fig, "local-particle-runs", outdir)
