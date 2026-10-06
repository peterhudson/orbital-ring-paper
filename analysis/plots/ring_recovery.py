"""Particle simulation of the whole ring from a perturbed start: left to
itself, and under the complete controller."""
import numpy as np
from scipy.linalg import expm

from .. import ring_control as rc
from ..ring_modes import FOLLOW, RingModes
from ..ring_particles import RingParticleSim
from . import style

MODES = (1, 2, 3)
START = ((1, 0.010, 0.0), (2, 0.005, 0.7), (3, 0.003, 1.9))
GUIDE = 0.5


def _perturbed(**kw):
    sim = RingParticleSim(n_keep=4, dt=0.25, guide_bandwidth=GUIDE, **kw)
    for n, amplitude, phase in START:
        sim.perturb(n, amplitude, phase=phase)
    return sim


def make(outdir=None):
    model = RingModes()
    om, R = model.omega, model.case.R
    law = rc.reference_law(model)
    _, _, K1 = rc.off_centre_controller(model, law)
    duration = 4500.0
    fig, (left, right) = style.figure(6.8, 3.9, ncols=2, sharey=True)
    for ax, sim, gains, title in (
        (left, _perturbed(law=FOLLOW), lambda n: rc.baseline_gain(model, n, FOLLOW, guide_bandwidth=GUIDE), "Stream follows the structure"),
        (right, _perturbed(law=law, feedback={1: K1}), lambda n: rc.baseline_gain(model, n, law, guide_bandwidth=GUIDE) + (K1 if n == 1 else 0), "Complete controller"),
    ):
        start = {n: sim.modal_state(n) for n in MODES}
        t, a, _, _ = sim.run(duration, record=MODES, every=480)
        fine = np.linspace(0.0, duration, 400)
        for colour, (i, n) in zip(style.SERIES, enumerate(MODES)):
            A, B = model.plant(n)
            closed = A - B @ gains(n)
            step = expm(closed * (fine[1] - fine[0]) * om)
            x, predicted = start[n].copy(), []
            for _ in fine:
                predicted.append(abs(x[0]) * R)
                x = step @ x
            ax.plot(fine / 60.0, predicted, color=colour, label=f"Mode {n}: linear model")
            ax.plot(t / 60.0, np.abs(a[:, i]), "o", color=colour, markersize=5, markeredgewidth=0.8)
        ax.set_yscale("log")
        ax.set_xlabel("Time (minutes)")
        ax.set_title(title)
        ax.set_xlim(0, duration / 60.0)
    left.set_ylabel("Amplitude of the structure's shape (m)")
    left.set_ylim(1e-5, 1e4)
    right.plot([], [], "o", color=style.MUTED, markersize=5, markeredgewidth=0.8, label="Particle simulation")
    right.legend(loc="upper right")
    return style.save(fig, "ring-recovery", outdir)
