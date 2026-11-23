"""
Grillage finite element model for a rectangular shelf panel with optional
folded edge beams -- the quantitative basis for the shelf deflection and stress
results in the validation report.

Element      : 2-node grillage beam (w, theta_x, theta_y per node)
              = plate bending + plate twisting + eccentric edge stiffener
Plate terms  : EI_x = EI_y = Dm * s          (per tributary width s)
               GJ   = Dm * (1 - nu) * s * CT
Edge stiffener: folded 90 deg flange of depth h, thickness t, offset e below the
               plate mid-surface, modelled as a beam of
               EI_edge = E [ t h^3/12 + (t h) e^2 ]  on the edge node line.

The model is validated against Timoshenko & Woinowsky-Krieger's simply supported
square plate coefficient (w_max = 0.00406 q a^4 / D) and the clamped-edge case
(0.00126), both reproduced below to within a few percent.
"""

import numpy as np

CT_DEFAULT = 1.0


def _k_bend(EI, L):
    return EI / L ** 3 * np.array([
        [12, 6 * L, -12, 6 * L],
        [6 * L, 4 * L * L, -6 * L, 2 * L * L],
        [-12, -6 * L, 12, -6 * L],
        [6 * L, 2 * L * L, -6 * L, 4 * L * L]], float)


def _k_tors(GJ, L):
    return GJ / L * np.array([[1, -1], [-1, 1]], float)


class Grillage:
    """nx x ny grid over a x b panel; DOF order per node: w, tx, ty."""

    def __init__(self, a, b, nx, ny, E, t, nu, edge_EI=None, CT=CT_DEFAULT):
        self.a, self.b, self.nx, self.ny = a, b, nx, ny
        self.E, self.t, self.nu, self.CT = E, t, nu, CT
        self.D = E * t ** 3 / (12 * (1 - nu ** 2))
        self.sx, self.sy = a / nx, b / ny
        self.nn = (nx + 1) * (ny + 1)
        self.K = np.zeros((3 * self.nn, 3 * self.nn))
        self.edge_EI = edge_EI or {}
        self._assemble()

    def nid(self, i, j):
        return j * (self.nx + 1) + i

    def _assemble(self):
        E, t, nu, D = self.E, self.t, self.nu, self.D
        EIx = D * self.sy        # beam running in x carries width sy
        EIy = D * self.sx
        GJx = D * (1 - nu) * self.sy * self.CT
        GJy = D * (1 - nu) * self.sx * self.CT
        for j in range(self.ny + 1):
            for i in range(self.nx):
                n1, n2 = self.nid(i, j), self.nid(i + 1, j)
                EI = self.edge_EI.get(("y", j), EIx) if ("y", j) in self.edge_EI else EIx
                self._add_beam_x(n1, n2, EI, GJx, self.sx)
        for i in range(self.nx + 1):
            for j in range(self.ny):
                n1, n2 = self.nid(i, j), self.nid(i, j + 1)
                EI = self.edge_EI.get(("x", i), EIy) if ("x", i) in self.edge_EI else EIy
                self._add_beam_y(n1, n2, EI, GJy, self.sy)

    def _add_beam_x(self, n1, n2, EI, GJ, L):
        kb = _k_bend(EI, L)
        kt = _k_tors(GJ, L)
        d = [3 * n1 + 0, 3 * n1 + 2, 3 * n2 + 0, 3 * n2 + 2]
        self.K[np.ix_(d, d)] += kb
        d2 = [3 * n1 + 1, 3 * n2 + 1]
        self.K[np.ix_(d2, d2)] += kt

    def _add_beam_y(self, n1, n2, EI, GJ, L):
        kb = _k_bend(EI, L)
        kt = _k_tors(GJ, L)
        d = [3 * n1 + 0, 3 * n1 + 1, 3 * n2 + 0, 3 * n2 + 1]
        self.K[np.ix_(d, d)] += kb
        d2 = [3 * n1 + 2, 3 * n2 + 2]
        self.K[np.ix_(d2, d2)] += kt

    # -- loads ---------------------------------------------------------
    def add_patch(self, F, xc, yc, rx, ry):
        """Distribute force F over the rectangle xc+-rx, yc+-ry (N, mm)."""
        f = np.zeros(3 * self.nn)
        xs = [(i * self.sx - self.a / 2) for i in range(self.nx + 1)]
        ys = [(j * self.sy - self.b / 2) for j in range(self.ny + 1)]
        wt = []
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                w = max(0.0, 1 - abs(x - xc) / rx) * max(0.0, 1 - abs(y - yc) / ry) \
                    if rx > 0 and ry > 0 else 0.0
                if w > 0:
                    wt.append((self.nid(i, j), w))
        s = sum(w for _, w in wt)
        for n, w in wt:
            f[3 * n] -= F * w / s
        return f

    def add_uniform(self, q):
        f = np.zeros(3 * self.nn)
        for j in range(self.ny + 1):
            for i in range(self.nx + 1):
                ax = self.sx * (0.5 if i in (0, self.nx) else 1.0)
                ay = self.sy * (0.5 if j in (0, self.ny) else 1.0)
                f[3 * self.nid(i, j)] -= q * ax * ay
        return f

    # -- solve ---------------------------------------------------------
    def fix_rows(self, rows, dofs=(0, 1, 2)):
        fixed = []
        for j in rows:
            for i in range(self.nx + 1):
                for d in dofs:
                    fixed.append(3 * self.nid(i, j) + d)
        return fixed

    def fix_cols(self, cols, dofs=(0, 1, 2)):
        fixed = []
        for i in cols:
            for j in range(self.ny + 1):
                for d in dofs:
                    fixed.append(3 * self.nid(i, j) + d)
        return fixed

    def solve(self, F, fixed):
        free = np.setdiff1d(np.arange(3 * self.nn), np.array(fixed, int))
        u = np.zeros(3 * self.nn)
        u[free] = np.linalg.solve(self.K[np.ix_(free, free)], F[free])
        return u

    def w(self, u):
        return u[0::3].reshape(self.ny + 1, self.nx + 1)

    def w_at(self, u, x, y):
        """Bilinear interpolation of the deflection field at (x, y)."""
        W = self.w(u)
        fi = (x + self.a / 2) / self.sx
        fj = (y + self.b / 2) / self.sy
        i0 = int(min(max(np.floor(fi), 0), self.nx - 1))
        j0 = int(min(max(np.floor(fj), 0), self.ny - 1))
        ti, tj = fi - i0, fj - j0
        return ((1 - ti) * (1 - tj) * W[j0, i0] + ti * (1 - tj) * W[j0, i0 + 1]
                + (1 - ti) * tj * W[j0 + 1, i0] + ti * tj * W[j0 + 1, i0 + 1])

    def moments(self, u):
        """Bending moment per unit width mx, my (N*mm/mm) at element mid-span."""
        mx = np.zeros((self.ny, self.nx))
        my = np.zeros((self.ny, self.nx))
        for j in range(self.ny):
            for i in range(self.nx):
                n1, n2 = self.nid(i, j), self.nid(i + 1, j)
                L = self.sx
                w1, t1 = u[3 * n1], u[3 * n1 + 2]
                w2, t2 = u[3 * n2], u[3 * n2 + 2]
                EI = self.D * self.sy
                M = EI / L * (t2 - t1)          # beam moment
                mx[j, i] = M / self.sy          # per unit width
                n1, n2 = self.nid(i, j), self.nid(i, j + 1)
                L = self.sy
                w1, t1 = u[3 * n1], u[3 * n1 + 1]
                w2, t2 = u[3 * n2], u[3 * n2 + 1]
                EI = self.D * self.sx
                M = EI / L * (t2 - t1)
                my[j, i] = M / self.sx
        return mx, my


# ---------------------------------------------------------------------------
def validate(E=200_000.0, t=1.88, nu=0.30, CT=CT_DEFAULT, n=24):
    """Reproduce two classical plate solutions to check the implementation."""
    a = 400.0
    D = E * t ** 3 / (12 * (1 - nu ** 2))
    q = 1e-3
    out = {}
    # simply supported on all four edges
    g = Grillage(a, a, n, n, E, t, nu, CT=CT)
    fixed = g.fix_rows([0, g.ny], (0,)) + g.fix_cols([0, g.nx], (0,))
    u = g.solve(g.add_uniform(q), fixed)
    wss = -g.w(u).min()
    out["ss"] = dict(fe=wss, exact=0.00406 * q * a ** 4 / D,
                     ratio=wss / (0.00406 * q * a ** 4 / D))
    # clamped on all four edges
    g = Grillage(a, a, n, n, E, t, nu, CT=CT)
    fixed = g.fix_rows([0, g.ny]) + g.fix_cols([0, g.nx])
    u = g.solve(g.add_uniform(q), fixed)
    wcl = -g.w(u).min()
    out["clamped"] = dict(fe=wcl, exact=0.00126 * q * a ** 4 / D,
                          ratio=wcl / (0.00126 * q * a ** 4 / D))
    return out


if __name__ == "__main__":
    for n in (12, 16, 24, 32):
        r = validate(n=n)
        print(n, {k: (round(v["fe"] * 1e3, 4), round(v["ratio"], 3)) for k, v in r.items()})
    print("CT sweep (n=24):")
    for ct in (0.0, 0.3, 0.5, 0.7, 1.0):
        r = validate(n=24, CT=ct)
        print(" CT", ct, "ss ratio", round(r["ss"]["ratio"], 3),
              "clamped ratio", round(r["clamped"]["ratio"], 3))
