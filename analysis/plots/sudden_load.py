"""Particle simulation of the whole ring: a dead load applied suddenly, with
the set point adapting."""
import numpy as np
from scipy.linalg import expm

from .. import ring_control as rc
from ..ring_modes import RingModes
from ..ring_particles import RingParticleSim
from . import style

GUIDE = 0.5


def make(outdir=None):
    model = RingModes()
    om, c = model.omega, model.case
    law = rc.reference_law(model)
    n, load, duration = 3, 1.0e-4, 4.0 * 3600.0
    sim = RingParticleSim(n_keep=4, law=law, dt=0.25, adapt=rc.ADAPT, guide_bandwidth=GUIDE)
    sim.load = load * np.cos(n * sim.th0)
    times, shape, gap = [0.0], [0.0], [0.0]
    steps_per_sample = 480
    for _ in range(int(duration / sim.dt / steps_per_sample)):
        for _ in range(steps_per_sample):
            sim.step()
        state = sim.modal_state(n) * c.R
        times.append(sim.t)
        shape.append(state[0].real)
        gap.append((0.5 * (state[4] + state[8]) - state[0]).real)
    closed = rc.adaptive_closed_loop(model, n, law, guide_bandwidth=GUIDE)
    b = np.zeros(closed.shape[0], complex)
    b[1] = load / (c.m_passive * c.g_h)
    forced = np.linalg.solve(closed, b)
    fine = np.linspace(0.0, duration, 500)
    x = np.array([(expm(closed * ti * om) - np.eye(len(b))) @ forced for ti in fine]) * c.R
    funicular = -load * c.R**2 / (c.Pi_total * n * n)
    fig, ax = style.figure(6.8, 3.8)
    hours = np.array(times) / 3600.0
    ax.axhline(0.0, color=style.AXIS, linewidth=1.0)
    ax.axhline(1e3 * funicular, color=style.MUTED, linestyle=(0, (4, 3)), linewidth=1.2, label="Where the streams carry the load with no offset")
    ax.plot(fine / 3600.0, 1e3 * x[:, 0].real, color=style.SERIES[0], label="Structure: linear model")
    ax.plot(hours, 1e3 * np.array(shape), "o", color=style.SERIES[0], markersize=5, markeredgewidth=0.8)
    ax.plot(fine / 3600.0, 1e3 * (0.5 * (x[:, 4] + x[:, 8]) - x[:, 0]).real, color=style.SERIES[1], label="Mean offset of streams from structure: linear model")
    ax.plot(hours, 1e3 * np.array(gap), "o", color=style.SERIES[1], markersize=5, markeredgewidth=0.8)
    ax.plot([], [], "o", color=style.MUTED, markersize=5, markeredgewidth=0.8, label="Particle simulation")
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Outward displacement (mm)")
    ax.set_xlim(0, duration / 3600.0)
    ax.set_title("A sudden outward load of 0.1 mN/m, three waves round the ring")
    ax.legend(loc="upper right")
    return style.save(fig, "sudden-load", outdir)
