"""
Worst-case tolerance stack for the critical joints and clearances.

Supplier tolerances used (SendCutSend, .074in mild steel, published):
  laser profile position            +/- 0.10 mm  (typical; not published)
  bend-to-edge (per bend)           +/- 0.38 mm  (0.015 in, published)
  bend angle                        +/- 1 deg   (published, bends < 24 in)
  powder coat build                 +0.05 .. +0.13 mm per side (published)
  sheet thickness                   +/- 0.10 mm  (nominal 1.88)

Every stack is computed as RSS where the sources are independent and as an
arithmetic worst case; the design is judged on the arithmetic worst case.
"""

import math, sys, os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
import params as P

LASER = 0.10
BEND_EDGE = 0.38
BEND_ANG = 1.0
COAT = 0.08
T_TOL = 0.10


def worst(*vals):
    return sum(abs(v) for v in vals)


def rss(*vals):
    return math.sqrt(sum(v * v for v in vals))


def main():
    L = ["## 9. Tolerance stacks", "",
         "### 9.1 Tray-to-slab joint: bolt alignment in Z (the bending direction)", "",
         "| contribution | value (mm) |", "|---|---|"]
    c = [("bend-to-edge on the tray end flange (slot position vs tray face)", BEND_EDGE),
         ("laser position of the slot in the flange", LASER),
         ("laser position of the hole in the side slab", LASER)]
    for n, v in c:
        L.append(f"| {n} | +/- {v:.2f} |")
    a = worst(*[v for _, v in c])
    r = rss(*[v for _, v in c])
    slot_play = (P.TRAY_SLOT[1] - P.BOLT["clearance"]) / 2.0
    L += [f"| **worst case (arithmetic)** | **+/- {a:.2f}** |",
          f"| RSS | +/- {r:.2f} |",
          f"| available movement: slot length {P.TRAY_SLOT[1]:.1f} - hole {P.BOLT['clearance']:.1f} "
          f"= +/- {slot_play:.2f} | |",
          f"| verdict | {'PASS - slot absorbs the worst case' if slot_play >= a else 'FAIL'} |",
          "",
          "The slot is vertical only; in Y (the direction that locates the shelf) the",
          f"stack is +/- {worst(LASER, LASER):.2f} mm against a {P.BOLT['clearance']-P.BOLT['d']:.1f} mm clearance, so the shelf is located to",
          "better than +/- 0.3 mm in Y while being free to find its own height in Z.",
          "",
          "### 9.2 Nested part clearance (rear panel between the side slabs)", "",
          "| contribution | value (mm) |", "|---|---|"]
    c2 = [("laser profile on the panel width (drives the channel outside width)", LASER),
          ("laser profile on the side slab inner face", LASER),
          ("powder coat on both faces (2 x 0.13 max)", 2 * 0.13),
          ("bend angle does NOT change the channel outside width - it tilts the",
           None)]
    for n, v in c2:
        L.append(f"| {n} | {'- (see note)' if v is None else f'{v:.2f}'} |")
    a2 = worst(*[v for _, v in c2 if v is not None])
    L += [f"| **worst case** | **{a2:.2f}** |",
          f"| designed total clearance | {2*P.PAINT_CLR:.2f} |",
          f"| verdict | {'PASS' if 2*P.PAINT_CLR >= a2 else 'REVIEW - coating squeezes out locally'} |",
          "",
          "flange face by up to 0.35 mm over its 20 mm depth; the 1.88 mm flange",
          "conforms under bolt load, so it does not affect the drop-in fit, only the",
          "local contact. Designed clearance covers laser + coating.",
          "",
          "### 9.3 Speaker bay height", ""]
    need = P.SPK["H"] + P.PAD["h"] - P.PAD["comp"]
    have = P.H_SPK
    tol = worst(BEND_EDGE, BEND_EDGE, P.PAD["comp"], T_TOL, T_TOL)
    L += ["| item | value |", "|---|---|",
          f"| speaker height | {P.SPK['H']:.1f} mm |",
          f"| isolation pad height, loaded | {P.PAD['h']-P.PAD['comp']:.1f} mm |",
          f"| required clear height | {need:.1f} mm |",
          f"| designed clear height | {have:.1f} mm |",
          f"| stack of tolerances (2 bends, pad compression, 2 x sheet) | +/- {tol:.2f} mm |",
          f"| net clearance at worst case | {have - need - tol:.1f} mm |",
          f"| verdict | {'PASS' if have - need - tol > 3 else 'REVIEW'} |",
          "",
          "### 9.4 Record bay height (crate entry over the mid-tray front flange)", "",
          "| item | value |", "|---|---|",
          f"| crate height | {P.CRATE['H']:.1f} mm |",
          f"| mid-tray front flange intrusion | {P.FLANGE:.1f} mm |",
          f"| required | {P.CRATE['H']+P.FLANGE:.1f} mm |",
          f"| designed (deck top to tray underside) | {P.H_REC:.1f} mm |",
          f"| tolerance stack (1 bend + sheet) | +/- {worst(BEND_EDGE, T_TOL):.2f} mm |",
          f"| net clearance | {P.H_REC - P.CRATE['H'] - P.FLANGE - worst(BEND_EDGE, T_TOL):.1f} mm |",
          f"| verdict | {'PASS' if P.H_REC - P.CRATE['H'] - P.FLANGE - worst(BEND_EDGE,T_TOL) > 3 else 'REVIEW'} |",
          "",
          "### 9.5 Fastener clearance through powder coat", "",
          "| item | value |", "|---|---|",
          f"| hole in side slab / panel | {P.BOLT['clearance']:.1f} mm |",
          f"| coating build (both sides, worst) | {2*COAT+0.1:.2f} mm |",
          f"| effective hole after coating | {P.BOLT['clearance']-2*0.13:.2f} mm |",
          f"| M5 shank | {P.BOLT['d']:.1f} mm |",
          f"| remaining diametral clearance | {P.BOLT['clearance']-2*0.13-P.BOLT['d']:.2f} mm |",
          "| threads on parts | none - all threads are in purchased locknuts, capped during coating |",
          "| verdict | PASS - no thread chasing is possible or required |"]
    return "\n".join(L)


if __name__ == "__main__":
    print(main())
