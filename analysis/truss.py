"""Momentum truss: a pin-jointed frame whose members also carry streams.

Each member has an elastic tension N = EA * strain and, running along it, a
balanced pair of counter-propagating streams with total momentum flux Pi and
total line density lam. By the momentum theorem the streams load the joints
exactly as a member in compression Pi would, so the member's stress
resultant is

    T_eff = N - Pi          (tension positive)

and the stream mass rides with the member. Because the two travel directions
are balanced there is no net convective (gyroscopic) term.

The class gives forces, the tangent stiffness, static equilibria (stable or
not) by Newton iteration, small-motion modes, and a time stepper. It works
in two or three dimensions.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class MomentumTruss:
    members: np.ndarray            # (m, 2) node indices
    rest_length: np.ndarray        # (m,) unstrained length of the structure, m
    ea: np.ndarray                 # (m,) axial stiffness of the structure, N
    thrust: np.ndarray             # (m,) stream momentum flux Pi, N
    stream_density: np.ndarray     # (m,) stream mass per unit member length, kg/m
    node_mass: np.ndarray          # (n,) structural mass lumped at nodes, kg
    gm: float = 0.0                # central gravity GM, m^3/s^2 (0 for none)
    g_uniform: np.ndarray | None = None  # uniform gravity vector, m/s^2
    external: np.ndarray | None = None   # (n, d) dead loads on nodes, N
    tension_only: bool = False     # structure goes slack instead of taking compression
    _ij: tuple = field(init=False, repr=False)

    def __post_init__(self):
        self.members = np.asarray(self.members, dtype=int)
        m = len(self.members)
        for name in ("rest_length", "ea", "thrust", "stream_density"):
            setattr(self, name, np.broadcast_to(np.asarray(getattr(self, name), dtype=float), (m,)).copy())
        self.node_mass = np.asarray(self.node_mass, dtype=float)
        self._ij = (self.members[:, 0], self.members[:, 1])

    # ---- pieces -------------------------------------------------------------
    def geometry(self, x):
        i, j = self._ij
        d = x[j] - x[i]
        length = np.sqrt((d * d).sum(axis=1))
        return d / length[:, None], length

    def tension(self, x):
        """Elastic tension N in each member's structure, N."""
        _, length = self.geometry(x)
        n = self.ea * (length - self.rest_length) / self.rest_length
        return np.maximum(n, 0.0) if self.tension_only else n

    def effective_tension(self, x):
        return self.tension(x) - self.thrust

    def masses(self, x):
        """Node masses including the stream mass riding in adjoining members."""
        _, length = self.geometry(x)
        i, j = self._ij
        half = 0.5 * self.stream_density * length
        m = self.node_mass.copy()
        np.add.at(m, i, half)
        np.add.at(m, j, half)
        return m

    def gravity(self, x):
        """Gravitational acceleration at each node."""
        acc = np.zeros_like(x)
        if self.gm:
            r = np.sqrt((x * x).sum(axis=1))
            acc -= self.gm * x / r[:, None] ** 3
        if self.g_uniform is not None:
            acc = acc + self.g_uniform
        return acc

    # ---- forces and stiffness -------------------------------------------------
    def force(self, x):
        """Net force on every node, shape (n, d)."""
        t, _ = self.geometry(x)
        i, j = self._ij
        pull = self.effective_tension(x)[:, None] * t
        f = self.masses(x)[:, None] * self.gravity(x)
        np.add.at(f, i, pull)
        np.add.at(f, j, -pull)
        if self.external is not None:
            f = f + self.external
        return f

    def stiffness(self, x, sparse=False):
        """Tangent stiffness K = -dF/dx, shape (n d, n d).

        Dense by default; pass sparse=True for a scipy CSR matrix.
        """
        n, d = x.shape
        t, length = self.geometry(x)
        i, j = self._ij
        strain_n = self.ea * (length - self.rest_length) / self.rest_length
        active = np.ones_like(length) if not self.tension_only else (strain_n > 0).astype(float)
        t_eff = strain_n * active - self.thrust
        eye = np.eye(d)
        tt = t[:, :, None] * t[:, None, :]
        k_el = (self.ea / self.rest_length * active)[:, None, None] * tt
        k_geo = (t_eff / length)[:, None, None] * (eye - tt)
        k_mem = k_el + k_geo
        g = self.gravity(x)
        rows, cols, vals = [], [], []

        def add(node_a, node_b, block):
            """block[m, p, q] goes to K[(node_a[m], p), (node_b[m], q)]."""
            pp, qq = np.meshgrid(np.arange(d), np.arange(d), indexing="ij")
            rows.append((node_a[:, None, None] * d + pp[None]).ravel())
            cols.append((node_b[:, None, None] * d + qq[None]).ravel())
            vals.append(block.ravel())

        for na, nb, sign in ((i, i, 1.0), (j, j, 1.0), (i, j, -1.0), (j, i, -1.0)):
            add(na, nb, sign * k_mem)
        # A member that lengthens holds more stream: dm = lam/2 * t . (dx_j - dx_i),
        # and that extra mass is pulled by gravity at both end nodes.
        half = 0.5 * self.stream_density
        for node in (i, j):
            gt = half[:, None, None] * g[node][:, :, None] * t[:, None, :]
            add(node, j, -gt)
            add(node, i, gt)
        if self.gm:
            r = np.sqrt((x * x).sum(axis=1))
            m = self.masses(x)
            grad = self.gm * m[:, None, None] * (eye / r[:, None, None] ** 3 - 3.0 * x[:, :, None] * x[:, None, :] / r[:, None, None] ** 5)
            idx = np.arange(n)
            add(idx, idx, grad)
        rows, cols, vals = np.concatenate(rows), np.concatenate(cols), np.concatenate(vals)
        from scipy.sparse import coo_matrix

        K = coo_matrix((vals, (rows, cols)), shape=(n * d, n * d)).tocsr()
        return K if sparse else K.toarray()

    def stiffness_fd(self, x, h=1e-3):
        """Finite-difference tangent stiffness, for checking `stiffness`."""
        n, d = x.shape
        K = np.zeros((n * d, n * d))
        for col in range(n * d):
            dx = np.zeros(n * d)
            dx[col] = h
            fp = self.force(x + dx.reshape(n, d)).ravel()
            fm = self.force(x - dx.reshape(n, d)).ravel()
            K[:, col] = -(fp - fm) / (2 * h)
        return K

    # ---- statics ----------------------------------------------------------------
    def equilibrium(self, x0, fixed=None, tol=1e-9, max_iter=30):
        """Newton iteration to a static equilibrium near x0.

        `fixed` is a boolean mask of shape (n, d) for coordinates held at their
        starting value. If nothing is fixed, free rigid-body motions are
        handled by a minimum-norm step, so a floating ring needs no artificial
        supports. Returns the positions and the largest residual force
        relative to the largest gravity load (or, without gravity, to 1e-9 of
        the largest thrust).
        """
        from scipy.sparse.linalg import spsolve

        x = np.array(x0, dtype=float)
        n, d = x.shape
        free = np.ones(n * d, dtype=bool) if fixed is None else ~np.asarray(fixed).ravel()
        scale = max(np.abs(self.masses(x)[:, None] * self.gravity(x)).max(), np.abs(self.thrust).max() * 1e-9, 1.0)
        res = np.inf
        for _ in range(max_iter):
            f = self.force(x).ravel()
            new_res = np.abs(f[free]).max() / scale
            if new_res < tol or (new_res > 0.5 * res and new_res < 1e-4):
                res = new_res          # converged, or stalled at round-off
                break
            res = new_res
            if fixed is None:
                step = np.linalg.lstsq(self.stiffness(x), f, rcond=1e-12)[0]
            else:
                K = self.stiffness(x, sparse=True)[free][:, free]
                step = spsolve(K.tocsc(), f[free])
            flat = x.ravel().copy()
            flat[free] += step
            x = flat.reshape(n, d)
        return x, res

    # ---- dynamics -----------------------------------------------------------------
    def modes(self, x, fixed=None):
        """Small motions about x: returns (sigma2, shapes) with x'' = sigma2 * x.

        Positive sigma2 is exponential growth at rate sqrt(sigma2); negative is
        oscillation at frequency sqrt(-sigma2). Sorted most unstable first.
        """
        n, d = x.shape
        free = np.ones(n * d, dtype=bool) if fixed is None else ~np.asarray(fixed).ravel()
        K = self.stiffness(x)[np.ix_(free, free)]
        m = np.repeat(self.masses(x), d)[free]
        s = 1.0 / np.sqrt(m)
        A = -(K * s[:, None]) * s[None, :]
        # K is symmetric except for one small term: a member that lengthens
        # holds more stream, so its weight changes. Use the symmetric solver
        # when that term is negligible and the general one otherwise.
        if np.abs(A - A.T).max() < 1e-9 * np.abs(A).max():
            w, v = np.linalg.eigh(0.5 * (A + A.T))
        else:
            w, v = np.linalg.eig(A)
            if np.abs(w.imag).max() > 1e-6 * np.abs(w.real).max():
                raise ValueError("complex sigma^2: the linearised motion is oscillatory-unstable")
            w, v = w.real, v.real
        order = np.argsort(-w)
        shapes = np.zeros((n * d, len(w)))
        shapes[free] = v[:, order] * s[:, None]
        return w[order], shapes.reshape(n, d, -1)

    def simulate(self, x0, v0, dt, steps, damping=0.0, callback=None, every=1):
        """Velocity-Verlet time stepping. `damping` is a mass-proportional rate, 1/s."""
        x = np.array(x0, dtype=float)
        v = np.array(v0, dtype=float)
        m = self.masses(x)[:, None]
        a = self.force(x) / m - damping * v
        out = []
        for step in range(steps):
            v_half = v + 0.5 * dt * a
            x = x + dt * v_half
            m = self.masses(x)[:, None]
            a = self.force(x) / m - damping * v_half
            v = v_half + 0.5 * dt * a
            if callback is not None:
                callback(step, x, v)
            if (step + 1) % every == 0:
                out.append(x.copy())
        return x, v, np.array(out)
