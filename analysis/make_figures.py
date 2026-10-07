"""Regenerate every generated figure:  python -m analysis.make_figures"""
import importlib
import sys
import time

MODULES = ["ring_modes", "speed_ripple", "thrust_line", "mirror_sketch", "guide_laws", "local_runs", "ring_control_rates", "ring_recovery", "actuator_travel", "sudden_load"]


def main(names=None):
    for name in names or MODULES:
        start = time.time()
        out = importlib.import_module(f"analysis.plots.{name}").make()
        print(f"{out.name:36s} {time.time() - start:5.1f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
