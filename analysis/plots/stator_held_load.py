"""Particle simulation of the whole ring: a load put on suddenly, with the stators holding the long modes."""
import numpy as np
from scipy.linalg import expm

from .. import ring_control as rc
from ..ring_loads import RingLoads
from ..ring_modes import RingModes
from ..ring_particles import RingParticleSim
from . import style

LOOPS = dict(guide_bandwidth=0.5, filter_bandwidth=1.5)


def run(n: int = 3, load: float = 1.0e-4, duration: float = 2.0 * 3600.0, sample: float = 120.0, dt: float = 0.25):
    """The simulation and the linear prediction for a load of `load` N/m in mode n
    put on at t = 0, with stator feedback on modes 1 to n and the streams following
    the structure in them. Returns times (s) and, for each of 'sim' and 'linear',
    the structure's displacement (m), the larger stream offset (m) and the larger
    speed change (m/s)."""
    model = RingModes()
    om, c = model.omega, model.case
    law = rc.reference_law(model)
    held = RingLoads(model, stator_modes=n)
    gains = {m: held.stator_gain(m) for m in range(1, n + 1)}
    (_, v1), (_, v2) = model._streams()

    def measures(state):
        speed = max(abs(state[6] + v1 * state[4]), abs(state[10] + v2 * state[8])) * om
        return state[0].real, max(abs(state[4] - state[0]), abs(state[8] - state[0])), speed

    sim = RingParticleSim(n_keep=n + 1, law=law, mirror_from=n + 1, feedback=gains, dt=dt, adapt=rc.ADAPT, **LOOPS)
    sim.load = load * np.cos(n * sim.th0)
    steps = int(round(sample / dt))
    times, sim_rows = [0.0], [(0.0, 0.0, 0.0)]
    for _ in range(int(duration / sample)):
        for _ in range(steps):
            sim.step()
        times.append(sim.t)
        sim_rows.append(measures(sim.modal_state(n) * c.R))
    closed = rc.closed_loop(model, n, law, mirror_from=n + 1, extra=gains[n], **LOOPS)
    b = np.zeros(closed.shape[0], complex)
    b[1] = load / (c.m_passive * c.g_h)
    forced = np.linalg.solve(closed, b)
    eye = np.eye(len(b))
    lin_rows = [measures((expm(closed * t * om) - eye) @ forced * c.R) for t in times]
    return np.array(times), dict(sim=np.array(sim_rows), linear=np.array(lin_rows))


def make(outdir=None):
    times, data = run()
    minutes = times / 60.0
    fig, (ax_d, ax_s) = style.figure(6.8, 3.7, ncols=2)
    dots = dict(linestyle="none", marker="o", markersize=5, markeredgewidth=0.8)
    handles = []
    for ax, column, colour, label in ((ax_d, 0, style.SERIES[0], "Structure, outward displacement"),
                                      (ax_d, 1, style.SERIES[1], "Offset of the streams from the structure"),
                                      (ax_s, 2, style.SERIES[2], "Change of slug speed")):
        handles.append(ax.plot(minutes, 1e3 * data["linear"][:, column], color=colour, label=label)[0])
        ax.plot(minutes[::3], 1e3 * data["sim"][::3, column], color=colour, **dots)
    handles.append(ax_d.plot([], [], color=style.MUTED, label="Dots: particle simulation. Lines: linear model", **dots)[0])
    ax_d.set_title("Millimetres")
    ax_s.set_title("Millimetres per second")
    for ax in (ax_d, ax_s):
        ax.set_xlabel("Time (minutes)")
        ax.set_xlim(0, minutes[-1])
        ax.set_ylim(0, None)
    fig.legend(handles=handles, loc="outside lower center", ncol=2, fontsize=8.5)
    return style.save(fig, "stator-held-load", outdir)
