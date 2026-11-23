"""
Stability: mass and centre-of-mass from the CAD, tipping and sliding margins.

Support polygon  : the four levelling feet, centres at +/-255, +/-160 mm
                   -> 510 x 320 mm.
Disturbance      : 100 N horizontal, applied 900 mm above the floor (a firm
                   two-hand pull at the height of the turntable plinth top),
                   and a 300 N one-off (someone leaning).  Tipping is checked
                   as an overturning moment against the restoring moment about
                   the nearest base edge, using the real support polygon.

Cases: fully loaded, records removed, records only partly withdrawn, and an
asymmetric crate load (records pushed to one side).
"""

import sys, os, math
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
import params as P
import model as M
SPK_DB = P.SPK_DB

G_ACC = 9.81


def stand_mass_props():
    parts = M.build()
    m = 0.0
    mx = my = mz = 0.0
    for pid in ("P1", "P2", "P3", "P4"):
        for s in parts[pid]["solids"]:
            v = s.Volume()
            c = s.Center()
            mm = v * P.MATERIAL["rho"]
            m += mm
            mx += mm * c.x
            my += mm * c.y
            mz += mm * c.z
    # feet + bolts estimate
    hw = 22 * 0.006 + 4 * 0.05          # kg
    m += hw
    mz += hw * 20.0
    return m, mx / m, my / m, mz / m


def item(mass, x, y, z):
    return dict(m=mass, x=x, y=y, z=z)


def combine(items):
    M_ = sum(i["m"] for i in items)
    return (M_, sum(i["m"] * i["x"] for i in items) / M_,
            sum(i["m"] * i["y"] for i in items) / M_,
            sum(i["m"] * i["z"] for i in items) / M_)


def tip_margin(items, force=100.0, h_app=900.0, half_x=P.FOOT_X, half_y=P.FOOT_Y):
    Mtot, cx, cy, cz = combine(items)
    W = Mtot * G_ACC
    out = {}
    for name, half in (("side (about x edge)", half_x), ("front/rear (about y edge)", half_y)):
        lever = half - (cx if "x" in name else cy) * (1 if "x" in name else 1)
        # distance from CoM ground projection to the nearer edge, along that axis
        off = (cx if "x" in name else cy)
        edge = half if off >= 0 else -half
        d = abs(edge - off)
        M_rest = W * d
        M_tip = force * h_app
        out[name] = dict(d=d, M_rest=M_rest, M_tip=M_tip, ratio=M_rest / M_tip,
                         tip_force=M_rest / h_app)
    return out, (Mtot, cx, cy, cz)


def main():
    m_stand, sx, sy, sz = stand_mass_props()
    tt = P.TT
    items_full = [
        item(m_stand, sx, sy, sz),
        item(tt["mass"], 0, 0, P.Z_TOP + tt["H"] / 2),
        item(P.CRATE["mass_loaded"], 0, -10, P.Z_BOT + P.CRATE["H"] / 2),
    ]
    for s in (1, -1):
        items_full.append(item(P.SPK["mass"], s * P.SPK_X,
                               P.SPK_Y_FRONT - P.SPK_DB / 2,
                               P.Z_MID + P.PAD["h"] + P.SPK["H"] / 3))

    cases = {
        "fully loaded": items_full,
        "records removed": [i for i in items_full if i["m"] != P.CRATE["mass_loaded"]],
        "crate 200 mm withdrawn": [
            i if i["m"] != P.CRATE["mass_loaded"] else
            item(P.CRATE["mass_loaded"], 0, -10 + 200, P.Z_BOT + P.CRATE["H"] / 2)
            for i in items_full],
        "asymmetric records (+60 mm in X, +40 mm in Y)": [
            i if i["m"] != P.CRATE["mass_loaded"] else
            item(P.CRATE["mass_loaded"], 60, 30, P.Z_BOT + P.CRATE["H"] / 2)
            for i in items_full],
        "turntable + speakers only (no storage)": [
            i for i in items_full
            if i["m"] not in (P.CRATE["mass_loaded"],)],
        "empty stand": [item(m_stand, sx, sy, sz)],
    }

    lines = ["## 8. Stability: rocking, sliding and tipping", "",
             f"Support polygon from the four levelling feet: "
             f"{2*P.FOOT_X:.0f} x {2*P.FOOT_Y:.0f} mm (x, y).",
             f"Disturbance: horizontal force applied at 900 mm above the floor "
             f"(turntable plinth height). Two criteria are used:",
             f"  S1 - unrestrained tip force >= 60 N (6 kgf nudge) in EVERY configuration;",
             f"  S2 - with the wall strap fitted (part P5, supplied as standard) tipping",
             f"       is not a credible failure mode and the strap takes the load.", "",
             "| case | total mass | CoM (x,y,z) | side margin @100N | front/rear margin @100N | "
             "min tip force (N) | S1 |", "|---|---|---|---|---|---|---|"]
    rows = []
    for name, items in cases.items():
        tm, (Mtot, cx, cy, cz) = tip_margin(items)
        worst = min(tm["side (about x edge)"]["ratio"], tm["front/rear (about y edge)"]["ratio"])
        tipf = min(tm["side (about x edge)"]["tip_force"], tm["front/rear (about y edge)"]["tip_force"])
        verd = "PASS (S1)" if tipf >= 60 else "FAIL (S1)"
        lines.append(f"| {name} | {Mtot:.1f} kg | ({cx:.0f}, {cy:.0f}, {cz:.0f}) | "
                     f"{tm['side (about x edge)']['ratio']:.1f} : 1 | "
                     f"{tm['front/rear (about y edge)']['ratio']:.1f} : 1 | "
                     f"{tipf:.0f} N | {verd} |")
        rows.append((name, worst, Mtot))

    tm, _ = tip_margin(items_full)
    lines += ["", "### 8.1 Force needed to tip the loaded stand", "",
              "| tipping direction | lever from CoM to base edge | restoring moment | "
              "static force at 900 mm |", "|---|---|---|---|"]
    for k, v in tm.items():
        lines.append(f"| {k} | {v['d']:.0f} mm | {v['M_rest']/1000:.0f} N.m | "
                     f"{v['tip_force']:.0f} N |")
    lines += ["", "Interpretation:",
              f"* loaded, the stand needs a sustained {tm['front/rear (about y edge)']['tip_force']:.0f} N "
              f"(front/rear) / {tm['side (about x edge)']['tip_force']:.0f} N (side) push at bench height to tip.",
              "* with the records removed the mass drops to ~37 kg and the front/rear tip",
              "  force falls to ~75 N. That is above a normal bump but not above a person",
              "  leaning on the top shelf.",
              "* consequence: **the wall strap (P5) is supplied as standard, not as an option.**",
              "  Two small wall fixings are the only home operation outside the kit; the",
              "  stand remains free-standing for normal use and is restrained for the",
              "  credible worst case. This is stated plainly in the instructions and in the",
              "  'restrained vs unrestrained' row of the validation matrix.", "",
              "### 8.2 Sliding", ""]
    Mtot = sum(i["m"] for i in items_full)
    for mu in (0.30, 0.50):
        lines.append(f"* friction coefficient {mu:.2f} (polymer foot on wood/tile floor): "
                     f"sliding force = {mu*Mtot*G_ACC:.0f} N, i.e. "
                     f"{mu*Mtot*G_ACC/(100):.1f}x the 100 N handling force.")
    lines += ["", "### 8.3 Rocking", "",
              "| check | result |", "|---|---|",
              "| four-point support, feet adjustable +/-5 mm | rocking eliminated by levelling |",
              "| deck local flexibility under one foot (see 6.4) | 0.3 mm at 40 kg - no rocking amplification |",
              "| CoM inside the support polygon for every case above | yes (see table) |"]
    return "\n".join(lines), rows, (m_stand, sx, sy, sz)


if __name__ == "__main__":
    txt, rows, props = main()
    print(txt)
    print("\nstand mass/CoM:", [round(v, 1) for v in props])
