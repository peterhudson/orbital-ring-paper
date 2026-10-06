"""Local model: growth or decay rate against wavelength for three guide laws."""
import math

import numpy as np

from ..collective import CollectiveModel
from . import style


def make(outdir=None):
    wavelengths = np.concatenate([np.geomspace(10.0, 1e3, 200), np.geomspace(1e3, 1e7, 160)[1:]])
    k = 2.0 * math.pi / wavelengths
    spring = CollectiveModel.reference(zeta=0.2)
    following = CollectiveModel.reference(zeta=0.3, ff=1.0)
    mirror = CollectiveModel.mirror_reference()
    g_spring = spring.growth_curve(wavelengths)
    g_follow = following.growth_curve(wavelengths)
    g_mirror = mirror.growth_curve(wavelengths)
    rigid = np.array([spring.rigid_growth_rate(ki) for ki in k])
    fig, (top, bottom) = style.figure(6.8, 5.2, nrows=2, sharex=True)
    top.plot(wavelengths, rigid, color=style.AXIS, linestyle=(0, (4, 3)), linewidth=1.2, label="Stream locked to structure: 0.76 k u")
    top.plot(wavelengths, np.where(g_follow > 0, g_follow, np.nan), color=style.SERIES[1], label="Stiff following guide")
    top.plot(wavelengths, np.where(g_spring > 0, g_spring, np.nan), color=style.SERIES[0], label="Spring guide, 10 Hz")
    top.set_yscale("log")
    top.set_ylabel("Growth rate (1/s)")
    top.set_title("Guides that make the stream follow the structure: every long wave grows")
    top.legend(loc="upper right")
    bottom.plot(wavelengths, -g_mirror, color=style.SERIES[2], label="Mirror law")
    bottom.set_yscale("log")
    bottom.set_xscale("log")
    bottom.set_ylabel("Decay rate (1/s)")
    bottom.set_xlabel("Wavelength (m)")
    bottom.set_title("Mirror law: every wavelength decays")
    bottom.set_xlim(10.0, 1e7)
    return style.save(fig, "guide-law-rates", outdir)
