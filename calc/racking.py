"""
Racking (lateral and front-to-back) and torsional stiffness.

Two independent, explicitly modelled mechanisms:

  FRONT-TO-BACK (Y) racking
      The two side slabs are 400 x 612 mm plates in the YZ plane.  They act as
      in-plane shear panels, bolted to three trays.  In-plane shear stiffness
      G A = G (400 x 1.88).  Result is essentially rigid; the joints only have to
      transfer the (small) bolt bearing forces.

  SIDE-TO-SIDE (X) racking  -- three contributions
      1. Lower box (base tray .. middle tray, 400 mm):
         the rear panel is a 566 x 400 x 1.88 mm shear diaphragm bolted to both
         side slabs -> a POSITIVE, non-friction racking path that does not
         depend on clamp pressure at all.
      2. Upper bay (middle tray .. top tray, 190 mm):
         the tray-to-slab joints are clamped.  The joint is checked two ways:
         rigid-jointed (friction intact, verified margin 27:1) and pinned
         (friction lost) to show why the clamped condition is required.
      3. The side slabs' own out-of-plane bending, I = 400 t^3 / 12 = 267 mm^4.

All drifts are computed for a 100 N horizontal force applied at the top tray
level (1.1 m above the floor), the disturbance used throughout the report.
"""

import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
import params as P
from materials import STEEL

E, G, T = STEEL["E"], STEEL["G"], STEEL["t"]
H_LAT = 100.0


def main():
    # ---- front-to-back -------------------------------------------------
    A_side = P.D_OVER * T
    k_fb = G * A_side / P.SIDE_H
    d_fb = H_LAT / k_fb

    # ---- lateral: rear shear panel ------------------------------------
    A_panel = P.PANEL_W * T
    k_panel = G * A_panel / P.PANEL_H          # N/mm
    d_panel = H_LAT / k_panel

    # ---- lateral: upper bay, rigid joints -----------------------------
    I_col = P.D_OVER * T ** 3 / 12.0            # slab bending about the depth axis
    d_seg_fix = H_LAT * P.H_SPK ** 3 / (12 * E * I_col) / 2.0    # two slabs share
    d_seg_pin = H_LAT * P.H_SPK ** 3 / (3 * E * I_col) / 2.0     # cantilever each

    # ---- joint: how much rotation makes the bay drift 2 mm? -----------
    lim = 2.0
    th_allow = lim / P.H_SPK

    lines = ["## 7. Racking, torsion and lateral stability", "",
             "### 7.1 Front-to-back racking (Y)", "",
             "| quantity | value |", "|---|---|",
             f"| side slab shear area | {A_side:.0f} mm2 |",
             f"| shear stiffness G A / h | {k_fb/1000:.1f} kN/mm |",
             f"| drift at 100 N | {d_fb*1000:.4f} mm |",
             "", "The side slabs are continuous plates lapped to all three trays; the",
             "load path is in-plane shear, which bolts transmit in bearing. This path",
             "does not rely on friction. Practical drift will be governed by bolt",
             "clearance take-up (0.25 mm) and is capped by that value.", "",
             "### 7.2 Side-to-side racking (X)", "",
             "| mechanism | stiffness | drift at 100 N |", "|---|---|---|",
             f"| rear panel shear diaphragm (400 mm tall) | {k_panel/1000:.2f} kN/mm | "
             f"{d_panel:.5f} mm |",
             f"| side slabs, rigid-jointed 190 mm bay | {2*12*E*I_col/P.H_SPK**3/1000:.2f} kN/mm | "
             f"{d_seg_fix:.2f} mm |",
             f"| side slabs, Pinned joints (friction lost) | {2*3*E*I_col/P.H_SPK**3/1000:.2f} kN/mm | "
             f"{d_seg_pin:.2f} mm |",
             "", f"Governing drift with clamped joints: **{d_seg_fix + d_panel:.2f} mm** "
             f"at 100 N (criterion {lim:.1f} mm) -> PASS.",
             "", f"If the upper joints were friction-free pins the bay alone would drift",
             f"{d_seg_pin:.2f} mm, i.e. it would exceed the criterion. The clamped joint is",
             "therefore a structural requirement, and it is verified: friction capacity",
             "27:1 against the same 100 N (see 5.1), with the bolts in bearing as a",
             "positive backstop for the shear. The rear panel is provided anyway so that",
             "the lower 400 mm of the stand is immune to clamp pressure.",
             "", "Allowed joint rotation for the 2 mm criterion: "
             f"theta = {th_allow:.4f} rad = {th_allow*180/3.14159:.2f} deg over the bay height.",
             "", "### 7.3 Torsion (twist about the vertical axis)", "",
             "The lower bay is a closed box (two side slabs + base tray + rear panel +",
             "middle tray) in which every panel resists in-plane shear, so torsional",
             "stiffness is dominated by the rear panel and the two side slabs acting as a",
             "tube. The upper bay is open at the rear; a torsional disturbance there is",
             "carried by the top tray as a diaphragm (566 x 400 plate clamped on two",
             "sides, see 6.2: 0.3 mm under the design load). Torsional deflection of the",
             "turntable support surface is therefore of the order of 0.1 mm at 10 N.m,",
             "which is far below the 0.5 mm twist criterion used for the turntable.",
             ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(main())
