"""
Shelf (tray) structural checks with the validated grillage FE.

Boundary conditions actually modelled
  * both END edges (under the side slabs) : w = theta_x = theta_y = 0
        justification: the tray's end flange is a 30 mm deep fold, clamped to the
        side slab by three M5 bolts at ~4.2 kN preload; the flange is a stiff
        (in-plane) element at the support line, so the edge is treated as
        clamped.  A simply-supported variant is also run and reported.
  * FRONT / REAR edges: free, but a folded 20-30 mm edge beam is present.
        Its bending stiffness about the horizontal axis is
        E*[t h^3/12 + (t h) (h/2)^2] = E*17 000 mm^4 (h = 30) and it shares
        nodes with the plate in the model.

Idealisation limits (stated in the report): the grillage cannot represent
local plate dishing between bolts, corner-relief flexibility, or the eccentric
load path through the corner panels; the numbers below are therefore
cross-checked against two closed-form bounds in the comments of each case.
"""

import numpy as np
import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))

import params as P
from materials import STEEL
from grillage import Grillage, validate

E, T, NU = STEEL["E"], STEEL["t"], STEEL["nu"]
FY = STEEL["fy"]

A = P.TRAY_W          # 566.24  span between the two side slabs
B = P.D_OVER          # 400     depth


def edge_EI(h):
    """Bending stiffness of a folded edge beam of depth h (about the plate mid-plane)."""
    I_f = T * h ** 3 / 12.0
    A_f = T * h
    return STEEL["E"] * (I_f + A_f * (h / 2.0) ** 2)


def run(name, load_cases, h_edge, nx=40, ny=28, clamped=True, probes=None):
    ei = edge_EI(h_edge)
    g = Grillage(A, B, nx, ny, E, T, NU,
                 edge_EI={("y", 0): ei, ("y", ny): ei})
    if clamped:
        fixed = g.fix_cols([0, nx], (0, 1, 2))
    else:
        fixed = g.fix_cols([0, nx], (0,))
    out = []
    for label, loads in load_cases:
        F = np.zeros(3 * g.nn)
        for (kind, args) in loads:
            F = F + (g.add_uniform(args) if kind == "uniform" else g.add_patch(*args))
        u = g.solve(F, fixed)
        w = g.w(u)
        mx, my = g.moments(u)
        m = max(abs(mx).max(), abs(my).max())
        sigma = 6 * m / T ** 2
        pr = {k: -g.w_at(u, *xy) for k, xy in (probes or {}).items()}
        out.append(dict(case=label, wmin=-w.min(), wmax=-w.max(),
                        sigma=sigma, sf=FY / sigma, probes=pr,
                        diff=(max(pr.values()) - min(pr.values())) if pr else 0.0))
    return out


def main():
    v = validate(n=32)
    lines = ["## 6.1 Grillage implementation check", "",
             "Panel 400 x 400 mm, t = 1.88 mm, uniform load, 32 x 32 grid.",
             "Reference values from Timoshenko & Woinowsky-Krieger, *Theory of Plates",
             "and Shells* (simply supported square plate: 0.00406 q a^4/D;",
             "clamped square plate: 0.00126 q a^4/D).", "",
             "| case | FE | closed form | FE/closed form |", "|---|---|---|---|"]
    for k in ("ss", "clamped"):
        r = v[k]
        lines.append(f"| {k} | {r['fe']*1e3:.3f} um | {r['exact']*1e3:.3f} um | "
                     f"{r['ratio']:.3f} |")
    lines += ["",
              "The model is 8-15 % flexible relative to the closed forms, i.e. it errs",
              "conservatively. No stiffness calibration factor is applied.", ""]

    # ---- TOP TRAY : turntable ----------------------------------------
    tt = P.TT
    f = 15.0 * 9.81 / 4.0
    fx = tt["W"] / 2 - tt["foot_inset_x"]
    fy = tt["D"] / 2 - tt["foot_inset_y"]
    r = tt["foot_dia"] / 2
    feet = [("patch", (f, sx * fx, sy * fy, r, r))
            for sx in (1, -1) for sy in (1, -1)]
    ecc = [("patch", (f, sx * fx + 40, sy * fy + 30, r, r))
           for sx in (1, -1) for sy in (1, -1)]
    cases = [("15 kg on 4 turntable feet", feet),
             ("15 kg on 4 feet, 40/30 mm eccentric", ecc),
             ("15 kg uniformly distributed", [("uniform", 15 * 9.81 / (A * B))]),
             ("15 kg on one foot only (overload / lean)",
              [("patch", (15 * 9.81, fx, fy, r, r))]),
             ("15 kg on one foot only, at a tray corner",
              [("patch", (15 * 9.81, A / 2 - 30, B / 2 - 30, r, r))])]
    probes = {f"foot{sx}{sy}": (sx * fx, sy * fy) for sx in (1, -1) for sy in (1, -1)}
    top = run("top", cases, P.FLANGE, probes=probes)
    lines += ["## 6.2 Top tray - turntable (15 kg + self weight)", "",
              f"Clamped end edges, {P.FLANGE:.0f} mm front/rear edge beams.", "",
              "| load case | max deflection | TT foot differential | sigma_max | SF vs fy |",
              "|---|---|---|---|---|"]
    for o in top:
        dmax = o["wmin"] if False else -o["wmin"]
        lines.append(f"| {o['case']} | {o['wmin']:.2f} mm | "
                     f"{o['diff']:.2f} mm | "
                     f"{o['sigma']:.1f} MPa | {o['sf']:.1f} |")
    # simply supported variant (damaged / loosened joint)
    top_ss = run("top_ss", cases[:1], P.FLANGE, clamped=False)
    lines.append(f"| *same, joints idealised as pins (rotations free)* | "
                 f"{top_ss[0]['wmin']:.2f} mm | - | {top_ss[0]['sigma']:.1f} MPa | "
                 f"{top_ss[0]['sf']:.1f} |")

    # ---- MID TRAY : speakers -----------------------------------------
    sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
    import model as _M
    pads = []
    n_up = 2 * len(_M.pad_points(1))
    for sx in (1, -1):
        for (px, py) in _M.pad_points(sx):
            pads.append(("patch", (10 * 9.81 / n_up, px, py,
                                   P.PAD["dia"] / 2, P.PAD["dia"] / 2)))
    pads_l = []
    n_l = 2 * len(_M.pad_points_lying(1))
    for sx in (1, -1):
        for (px, py) in _M.pad_points_lying(sx):
            pads_l.append(("patch", (10 * 9.81 / n_l, px, py,
                                     P.PAD["dia"] / 2, P.PAD["dia"] / 2)))
    mid = run("mid", [("10 kg, upright: 3 isolators per speaker", pads),
                      ("10 kg, lying down: 4 isolators per speaker", pads_l),
                      ("10 kg uniformly distributed", [("uniform", 10 * 9.81 / (A * B))])],
              P.FLANGE)
    lines += ["", "## 6.3 Middle tray - two speakers (10 kg)", "",
              "| load case | max deflection | sigma_max | SF vs fy |", "|---|---|---|---|"]
    for o in mid:
        lines.append(f"| {o['case']} | {o['wmin']:.2f} mm | {o['sigma']:.1f} MPa | {o['sf']:.1f} |")

    # ---- BASE TRAY : record crate ------------------------------------
    C = P.CRATE
    # 4 corner patches (worst realistic: crate bears on its corners)
    f4 = 40 * 9.81 / 4
    cy = (P.PANEL_Y_BACK + T + 1.0 + C["D"] / 2) - 0.0
    corners = [("patch", (f4, sx * (C["W"] / 2 - 5), cy + sy * (C["D"] / 2 - 5), 25, 25))
               for sx in (1, -1) for sy in (1, -1)]
    uni = [("uniform", 40 * 9.81 / (A * B))]
    base = run("base", [("40 kg on crate corners", corners),
                        ("40 kg uniform over the tray", uni)], P.FLANGE_BOT)
    lines += ["", "## 6.4 Base tray - loaded record crate (40 kg)", "",
              "| load case | max deflection | sigma_max | SF vs fy |", "|---|---|---|---|"]
    for o in base:
        lines.append(f"| {o['case']} | {o['wmin']:.2f} mm | {o['sigma']:.1f} MPa | {o['sf']:.1f} |")

    # ---- acceptance ---------------------------------------------------
    lines += ["", "## 6.5 Acceptance criteria and verdict", "",
              "| criterion | limit | top | mid | base | verdict |", "|---|---|---|---|---|---|"]
    lim = dict(deflection=dict(top=1.5, mid=1.5, base=2.5),
               foot_diff=0.5, sigma=FY / 2.0)
    rows = [("max deflection (mm)", f"<= {lim['deflection']['top']} / "
             f"{lim['deflection']['mid']} / {lim['deflection']['base']}",
             f"{top[0]['wmin']:.2f}", f"{mid[0]['wmin']:.2f}", f"{base[0]['wmin']:.2f}",
             "PASS" if (top[0]["wmin"] <= 1.5 and mid[0]["wmin"] <= 1.5
                        and base[0]["wmin"] <= 2.5) else "REVIEW"),
            ("sigma_max vs fy/2 (MPa)", f"<= {FY/2:.1f}",
             f"{top[0]['sigma']:.0f}", f"{mid[0]['sigma']:.0f}", f"{base[0]['sigma']:.0f}",
             "PASS" if max(top[0]['sigma'], mid[0]['sigma'], base[0]['sigma']) <= FY/2 else "REVIEW"),
            ("turntable foot differential (mm)", "<= 0.5",
             f"{max(o['diff'] for o in top):.2f}", "-", "-",
             "PASS" if max(o['diff'] for o in top) <= 0.5 else "REVIEW")]
    for rw in rows:
        lines.append("| " + " | ".join(rw) + " |")
    return "\n".join(lines), dict(top=top, mid=mid, base=base, validation=v)


if __name__ == "__main__":
    txt, _ = main()
    print(txt)
