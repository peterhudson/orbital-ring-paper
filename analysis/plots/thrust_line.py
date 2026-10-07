"""Opposed tug fields on a braced frame: the structure moves by minus the
thrust-line offset when there is a shear path, and not at all without one."""
import math

import numpy as np

from .. import ladder
from . import style


def _centreline(length, panels, ea_web, e0):
    s_mid = (np.arange(panels) + 0.5) * length / panels
    shift = e0 * np.sin(math.pi * s_mid / length) ** 2
    truss, x0, fixed = ladder.ladder_truss(length=length, panels=panels, shift=shift, ea_web=ea_web)
    x, _ = truss.equilibrium(x0, fixed=fixed, tol=1e-10)
    n_side = panels + 1
    return np.linspace(0, length, n_side), 0.5 * (x[:n_side, 1] + x[n_side:, 1])


def make(outdir=None):
    length, panels, e0 = 20e3, 200, 0.05
    s, y_braced = _centreline(length, panels, 2.5e11, e0)
    _, y_soft = _centreline(length, panels, 2.5e5, e0)
    e = e0 * np.sin(math.pi * s / length) ** 2
    fig, ax = style.figure(6.8, 3.6)
    km = s / 1e3
    ax.plot(km, e * 1e3, color=style.SERIES[0], label="Thrust line, offset from the structure")
    ax.plot(km, y_braced * 1e3, color=style.SERIES[1], label="Structure, cross-braced")
    ax.plot(km, y_soft * 1e3, color=style.SERIES[2], label="Structure, no shear path")
    ax.axhline(0, color=style.AXIS, linewidth=0.8)
    ax.set_xlabel("Position along the frame (km)")
    ax.set_ylabel("Sideways position (mm)")
    ax.set_title("Opposed tug fields push the structure off the thrust line")
    ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.2), columnspacing=1.2, handlelength=1.4)
    return style.save(fig, "thrust-line-shift", outdir)
