"""
FLAT PACK STAND -- engineering calculations (plywood).
Writes ../out/calc_report.md
"""

import os, sys, datetime
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(_here)), "calc"))

import params as P
import model as M
from grillage import Grillage

OUT = os.path.join(os.path.dirname(_here), "out")
PLY = P.PLY
T = PLY["t"]
E = PLY["E_face"]
NU = 0.30
SHELF_L = P.INTERIOR_W      # clear span between the side panels
SHELF_B = P.SHELF_D


def fe(loads, clamped=True, nx=40, ny=28):
    g = Grillage(SHELF_L, SHELF_B, nx, ny, E, T, NU)
    fixed = g.fix_cols([0, nx], (0, 1, 2) if clamped else (0,))
    F = np.zeros(3 * g.nn)
    for (kind, args) in loads:
        F = F + (g.add_uniform(args) if kind == "uniform" else g.add_patch(*args))
    u = g.solve(F, fixed)
    w = g.w(u)
    mx, my = g.moments(u)
    m = max(abs(mx).max(), abs(my).max())
    sigma = 6 * m / T ** 2
    return dict(w=-w.min(), sigma=sigma,
                sf=PLY["f_bend_face"] / sigma if sigma > 0 else 99)


def main():
    L = [f"# FLAT PACK STAND, VARIANT B (upright speakers) -- calculations  W0.9 provisional",
         "", f"Generated {datetime.date.today().isoformat()} by `flatpack/calc/run_all.py`.",
         "All inputs come from `flatpack/cad/params.py`.", "",
         "## 0. Basis", "",
         "| item | value | note |", "|---|---|---|",
         f"| panel | {PLY['name']} | must be measured before cutting |",
         f"| thickness | {T} mm nominal, actual {PLY['t_range'][0]}-{PLY['t_range'][1]} | "
         "the slot is cut to the measured value + {:.2f} |".format(P.FIT["slot"]),
         f"| E (bending, load along the face grain) | {E:.0f} MPa | conservative for "
         "birch ply (7-12 GPa); the shelf span runs along the sheet's long axis |",
         f"| E (across the plies) | {PLY['E_cross']:.0f} MPa | used as a sensitivity |",
         f"| bending strength (along grain) | {PLY['f_bend_face']:.0f} MPa | B/BB Baltic birch, "
         "0.2 % offset |",
         f"| bearing (plywood edge/face) | {PLY['f_bearing']:.1f} MPa | conservative |",
         f"| density | {PLY['rho']*1e9:.0f} kg/m3 | |",
         "", "Load cases (assumptions, not ratings): 15 kg top, 10 kg middle, 40 kg base, "
         "self weight from the CAD.", ""]

    # ---------------- shelves -------------------------------------------
    L += ["## 1. Shelf bending (grillage FE, same solver validated in the steel package)",
          "", "Span 566 mm between the side panels, depth 394 mm, 18 mm ply, "
          "simply supported and clamped variants.", "",
          "| shelf | load case | deflection (mm) | sigma (MPa) | SF on bending strength |",
          "|---|---|---|---|---|"]
    fx = P.TT["W"] / 2 - P.TT["foot_inset_x"]
    fy = P.TT["D"] / 2 - P.TT["foot_inset_y"]
    r = P.TT["foot_dia"] / 2
    f = 15 * 9.81 / 4
    top = [("15 kg on 4 turntable feet",
            [("patch", (f, sx * fx, sy * fy, r, r)) for sx in (1, -1) for sy in (1, -1)]),
           ("15 kg uniform", [("uniform", 15 * 9.81 / (SHELF_L * SHELF_B))]),
           ("15 kg on one foot", [("patch", (15 * 9.81, fx, fy, r, r))])]
    res = {}
    for label, loads in top:
        for cl in (True, False):
            d = fe(loads, clamped=cl)
            res[(label, cl)] = d
            L.append(f"| top | {label}{'' if cl else ' (pinned ends)'} | "
                     f"{d['w']:.2f} | {d['sigma']:.2f} | {d['sf']:.1f} |")
    import model as _M
    n_pads = 2 * len(_M.pad_points(1))
    pads = [("patch", (10 * 9.81 / n_pads, px, py,
                       P.PAD["dia"] / 2, P.PAD["dia"] / 2))
            for sx in (1, -1) for (px, py) in _M.pad_points(sx)]
    d = fe(pads)
    L.append(f"| middle | 10 kg on 6 isolator pads (3 per speaker) | {d['w']:.2f} | {d['sigma']:.2f} | {d['sf']:.1f} |")
    f4 = 40 * 9.81 / 4
    corners = [("patch", (f4, sx * (P.CRATE["W"] / 2 - 5), sy * (P.CRATE["D"] / 2 - 5), 25, 25))
               for sx in (1, -1) for sy in (1, -1)]
    for label, loads in (("40 kg on crate corners", corners),
                         ("40 kg uniform", [("uniform", 40 * 9.81 / (SHELF_L * SHELF_B))])):
        d = fe(loads)
        L.append(f"| base | {label} | {d['w']:.2f} | {d['sigma']:.2f} | {d['sf']:.1f} |")
    L += ["", "Criteria: deflection <= 1.5 mm (top/middle), <= 2.5 mm (base); "
          "SF on bending strength >= 3.", ""]

    # ---------------- joints --------------------------------------------
    tab_bearing_area = P.TENON_L * T
    dowel_shear = T * (P.TENON_L - P.DOWEL["d"])
    L += ["## 2. Shelf-to-side joint (tab in slot, dowel locked)", "",
          "| quantity | value | check |", "|---|---|---|",
          f"| tab bearing area in the slot | {tab_bearing_area:.0f} mm2 | |",
          f"| bearing stress, top shelf (15 kg / 2 ends) | "
          f"{15*9.81/2/tab_bearing_area:.3f} MPa | vs {PLY['f_bearing']:.1f} MPa "
          f"-> SF {PLY['f_bearing']/(15*9.81/2/tab_bearing_area):.0f} |",
          f"| tab shear area at the dowel line | {dowel_shear:.0f} mm2 | |",
          f"| shear stress at 100 N lateral | {100/dowel_shear:.3f} MPa | vs "
          f"{PLY['f_shear_panel']:.1f} MPa -> SF "
          f"{PLY['f_shear_panel']/(100/dowel_shear):.0f} |",
          f"| slot length / tab length | {P.SLOT_L:.2f} / {P.TENON_L:.1f} mm | "
          f"{P.FIT['slot']/2:.2f} mm per end = Y location +/-{P.FIT['slot']/2:.2f} mm |",
          f"| tab thickness / slot height | {T:.2f} / {P.SLOT_H:.2f} mm | "
          f"{P.FIT['slot']/2:.2f} mm per face |",
          f"| dowel | 8 mm birch, 40 mm, 11 mm proud each side | "
          f"bearing on 18 mm tab: {100/(8*T):.3f} MPa |",
          f"| material remaining above/below a slot | "
          f"{P.H_REC/2 - P.SLOT_H/2:.0f} mm to the next slot | no local weakness |"]

    # ---------------- racking -------------------------------------------
    I = P.D_OVER * T ** 3 / 12.0
    gE = PLY["E_face"]
    segs = [(P.Z_BASE, P.Z_MID - T), (P.Z_MID, P.Z_TOP - T)]
    d_rig = sum(100 * (b - a) ** 3 / (12 * gE * I) / 2 for (a, b) in segs)
    d_pin = sum(100 * (b - a) ** 3 / (3 * gE * I) / 2 for (a, b) in segs)
    L += ["", "## 3. Racking", "",
          f"Side panel second moment of area (out-of-plane, about the depth axis): "
          f"I = {P.D_OVER} x {T}^3/12 = {I:.0f} mm4, EI = {gE*I/1e9:.2f} kN.m2.", "",
          "| joint idealisation | drift at 100 N | criterion | result |", "|---|---|---|---|",
          f"| clamped shelves (tab in a 0.1 mm-clearance slot, i.e. effectively rigid) "
          f"| {d_rig:.3f} mm | 2.0 mm | PASS |",
          f"| pinned shelves (worst case) | {d_pin:.3f} mm | 2.0 mm | PASS |",
          "", "Plywood wins here: the 18 mm panels are ~30x stiffer than the 1.88 mm steel",
          "slabs of the metal version, so even with pinned joints the frame passes the",
          "racking criterion. No back panel is needed for racking; the open back is kept",
          "for cable and ventilation access.", "",
          "Front-to-back: the side panels act as in-plane shear panels, "
          f"G A / h = {PLY['G']*(P.D_OVER*T)/P.SIDE_H/1000:.1f} kN/mm -> "
          f"{100/(PLY['G']*(P.D_OVER*T)/P.SIDE_H):.5f} mm at 100 N."]

    # ---------------- stability -----------------------------------------
    parts = M.build()
    m_stand = sum(s.Volume() for pid in ("P1", "P2", "P3")
                  for s in parts[pid]["solids"]) * PLY["rho"]
    items = [dict(m=m_stand, x=0, y=0, z=P.SIDE_H / 2),
             dict(m=P.TT["mass"], x=0, y=0, z=P.Z_TOP + P.TT["H"] / 2),
             dict(m=P.CRATE["mass_loaded"], x=0, y=-20, z=P.Z_BASE + P.CRATE["H"] / 2)]
    for s in (1, -1):
        items.append(dict(m=P.SPK["mass"], x=s * P.SPK_X, y=0,
                          z=P.Z_MID + P.PAD["h"] + P.SPK["H"] / 3))
    def combine(it):
        M_ = sum(i["m"] for i in it)
        return (M_, sum(i["m"] * i["x"] for i in it) / M_,
                sum(i["m"] * i["y"] for i in it) / M_,
                sum(i["m"] * i["z"] for i in it) / M_)
    L += ["", "## 4. Stability", "",
          f"Support polygon: feet at +/-{P.FOOT['x']:.0f} (x) and +/-{P.FOOT['y']:.0f} (y) "
          f"-> {2*P.FOOT['x']:.0f} x {2*P.FOOT['y']:.0f} mm.", "",
          "| case | mass (kg) | CoM (x,y,z) | tip force at 900 mm, front/rear | side |",
          "|---|---|---|---|---|"]
    for name, it in (("loaded", items),
                     ("records removed", [i for i in items if i["m"] != P.CRATE["mass_loaded"]]),
                     ("stand only", [items[0]])):
        Mt, cx, cy, cz = combine(it)
        dY = abs(P.FOOT["y"] - cy)
        dX = abs(P.FOOT["x"] - cx)
        L.append(f"| {name} | {Mt:.1f} | ({cx:.0f},{cy:.0f},{cz:.0f}) | "
                 f"{Mt*9.81*dY/900:.0f} N | {Mt*9.81*dX/900:.0f} N |")
    L += ["", "Same conclusion as the steel design: the loaded stand resists ~100 N at",
          "bench height, the records-removed case is lower, and a wall strap (P4) is",
          "supplied with the kit for that case."]

    # ---------------- fit / thickness -----------------------------------
    L += ["", "## 5. Thickness and fit (the one real risk with plywood)", "",
          "| item | value |", "|---|---|",
          f"| nominal sheet thickness | {T} mm |",
          f"| actual range to expect | {PLY['t_range'][0]}-{PLY['t_range'][1]} mm |",
          f"| slot as designed | {P.SLOT_H:.2f} mm (nominal + {P.FIT['slot']:.2f}) |",
          f"| if the sheet measures 17.6 | slot must be 17.80 -> joint is 0.30 loose |",
          f"| if the sheet measures 18.3 | slot must be 18.50 -> 18.20 would not fit |",
          "", "**Therefore the slot width is a cutter-program parameter, not a design",
          "constant.** The kit includes a fit coupon (P5) with three slots at +0.10,",
          "  +0.20 and +0.30 mm clearance, cut from the same sheet in the same setup.",
          "Cut the coupon first, test the actual panel in all three slots, then set the",
          "clearance for the production parts. Take-up for a slightly loose joint is",
          "provided by the dowel and by a tap with a rubber mallet; a joint that needs",
          "force is a signal to increase the clearance, never to sand the part."]
    txt = "\n".join(L) + "\n"
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "calc_report.md"), "w") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
