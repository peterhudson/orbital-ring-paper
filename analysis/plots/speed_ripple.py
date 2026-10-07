"""What a stationary speed ripple does to the ring: the tug goes into hoop
tension, and the shape moves only because weight moves, the streams' and the
stretching structure's."""
import numpy as np

from .. import ring
from ..params import EARTH_500 as C, HOOP_EA
from . import style


def make(outdir=None):
    n, p, eps, ea = 720, 8, 1e-4, HOOP_EA
    angles = ring.member_angles(n)
    ripple = 1 + eps * np.cos(p * angles)
    truss, x0 = ring.ring_truss(n_nodes=n, ea=ea, speed_ratio=ripple)
    x, _ = truss.equilibrium(x0)
    truss_fixed, _ = ring.ring_truss(n_nodes=n, ea=ea, speed_ratio=ripple, shift_weight=False)
    x_fixed, _ = truss_fixed.equilibrium(x0)
    truss_stiff, x0_stiff = ring.ring_truss(n_nodes=n, ea=1000.0 * ea, speed_ratio=ripple, shift_weight=False)
    x_stiff, _ = truss_stiff.equilibrium(x0_stiff)
    deg = np.degrees(angles)
    node_deg = np.degrees(np.arctan2(x[:, 1], x[:, 0])) % 360
    order = np.argsort(node_deg)
    d_pi = (truss.thrust - truss.thrust.mean()) / 1e6
    d_n = truss.tension(x) / 1e6
    d_teff = truss.effective_tension(x) - truss.effective_tension(x).mean()
    style.apply()
    import matplotlib.pyplot as plt

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(6.8, 5.2), sharex=True, constrained_layout=True)
    top.plot(deg, d_pi, color=style.SERIES[0], label="Stream momentum flux, change")
    top.plot(deg[::12], d_n[::12], "o", color=style.SERIES[1], label="Tension in the structure")
    top.plot(deg, d_teff / 1e6, color=style.SERIES[2], label="Effective tension, change")
    top.set_ylabel("Force (MN)")
    top.set_title("Tension in the structure takes up the tug")
    top.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.02), columnspacing=1.2, handlelength=1.4)
    w = ring.radial_displacement(x)
    w_fixed = ring.radial_displacement(x_fixed)
    bottom.plot(node_deg[order], w[order], color=style.SERIES[0], label="The real case")
    bottom.plot(node_deg[order], w_fixed[order], color=style.SERIES[1], label="Stream weight held uniform")
    bottom.plot(node_deg[order], ring.radial_displacement(x_stiff)[order], color=style.SERIES[2], label="And a structure too stiff to stretch")
    bottom.set_ylabel("Radial displacement (m)")
    bottom.set_xlabel("Angle round the ring (degrees)")
    bottom.set_xlim(0, 360)
    bottom.set_xticks(np.arange(0, 361, 45))
    bottom.set_title("The shape changes because weight moves")
    bottom.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.22), columnspacing=1.2, handlelength=1.4)
    return style.save(fig, "speed-ripple-response", outdir)
