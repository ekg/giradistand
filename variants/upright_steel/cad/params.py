"""
GI-RAD STAND, VARIANT A: UPRIGHT SPEAKERS (steel)  --  revision U0.9-PROVISIONAL
===============================================================================
The Powered Partners stand *upright*: 270 mm tall on a 150 x 196 mm triangular
footprint, baffle on the diagonal face.  That changes everything about the width:

  * the pair is only 2 x ~141 mm of envelope instead of 534 mm
  * so the TURNTABLE (452) finally sets the width, not the speakers
  * and the speaker bay must be 305 mm tall instead of 190

Net effect: a narrow tower -- 486 x 400 x 741 mm -- with 15 mm turntable margins
(the horizontal design needed 57), the speakers 329 mm apart on acoustic centres
(the horizontal design: 287), a vertical baffle axis, and the platter 25 mm
higher.  Cost: 115 mm taller and a much taller visual mass.

All steel, process, fastener and joint decisions are unchanged from the parent
design (see ../../docs/).  Only the equipment envelopes and the stack change.

Coordinates and units as in the parent: mm, +X right, +Y front, +Z up.
"""

from dataclasses import dataclass
import math
import json

IN = 25.4

# ---------------------------------------------------------------------------
# 1. Material / process -- identical to the parent design
# ---------------------------------------------------------------------------
MATERIAL = dict(
    name="Mild Steel CRS 1008/1010, 0.074 in (1.88 mm), 14 ga",
    E=200_000.0, G=77_000.0, fy=205.0, fu=340.0, rho=7.85e-6, nu=0.30,
    T=1.88, R_in=1.60, k_factor=0.40, bend_deduction_90=3.277,
    min_flange_formed=8.13, max_bend_len=1117.6,
    max_flat_x=762.0, max_flat_y=1117.6, max_coat_x=762.0, max_coat_y=914.4,
    coat_per_side=0.08,
)
T = MATERIAL["T"]
R_IN = MATERIAL["R_in"]
BD = MATERIAL["bend_deduction_90"]

# ---------------------------------------------------------------------------
# 2. Equipment
# ---------------------------------------------------------------------------
TT = dict(W=452.0, D=352.0, H=141.6, mass=8.0,
          foot_inset_x=42.0, foot_inset_y=45.0, foot_dia=38.0, foot_adjust=8.0,
          cover_open_rear=310.0)

# AR Powered Partner, UPRIGHT: 150 W x 270 H x 196 D, triangular plan
SPK = dict(legs=(150.0, 196.0),          # plan triangle legs (X, Y)
           H=270.0, mass=3.5,            # 3.5 kg per the AR 570 sheet (3.16 Advent)
           toe_deg=20.0,                 # each cabinet rotated so the diagonal
           #                              baffle aims at the listening position
           )
SPK_H = SPK["H"]


def _rotated_bbox(legs, deg):
    t = math.radians(deg)
    pts = [(0.0, 0.0), (legs[0], 0.0), (0.0, legs[1])]
    r = [(x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t))
         for x, y in pts]
    xs = [p[0] for p in r]
    ys = [p[1] for p in r]
    return dict(w=max(xs) - min(xs), d=max(ys) - min(ys),
                xmin=min(xs), ymin=min(ys))


BB = _rotated_bbox(SPK["legs"], -SPK["toe_deg"])     # the narrow rotation
SPK_WB, SPK_DB = BB["w"], BB["d"]

PAD = dict(dia=44.0, h=24.0, cap=2.75, comp=1.0, inset=0.0, qty=3)
CRATE = dict(W=368.3, D=368.3, H=358.8, mass_empty=1.9, mass_loaded=22.0)

# ---------------------------------------------------------------------------
# 3. Layout -- narrower, taller
# ---------------------------------------------------------------------------
W_OVER = 486.0        # interior 482.2 = 452 turntable + 2 x 15.1 margin
D_OVER = 400.0        # still set by the record crate, not by the speakers
FLANGE = 30.0
FLANGE_BOT = 20.0
RACK_CORNER = T + 1.0
PAINT_CLR = 0.30

H_REC = 400.0         # unchanged: crate + the mid tray's front flange
H_SPK = 305.0         # 270 speaker + 23 compressed pad + 12 handling
Z_BOT = 32.0
Z_MID = Z_BOT + H_REC + T
Z_TOP = Z_MID + H_SPK + T
H_OVER = Z_TOP

INTERIOR_W = W_OVER - 2 * T
TRAY_W = INTERIOR_W
SIDE_BOT = Z_BOT - 20.0
SIDE_H = (Z_TOP - T) - SIDE_BOT

SPK_SIDE_CLR = 6.0
SPK_GAP = INTERIOR_W - 2 * SPK_WB - 2 * SPK_SIDE_CLR
SPK_X = SPK_WB / 2 + SPK_GAP / 2
SPK_Y_FRONT = D_OVER / 2 - 12.0      # envelope front face, 12 mm back from the edge

# ---------------------------------------------------------------------------
# 4. Hardware -- unchanged family
# ---------------------------------------------------------------------------
BOLT = dict(size="M5", d=5.0, clearance=5.5, head_dia=9.5, head_h=2.75,
            length=12.0, grade="A2-70 stainless / 8.8 zinc",
            nut="DIN 6923 M5 flanged nylon-insert locknut, h=5.0", preload_N=4200.0)
FOOT = dict(thread="M6", stud_len=35.0, base_dia=23.0, base_h=9.0,
            clearance=6.6, nut="DIN 6923 M6 flanged nylon-insert locknut h=6.0")
FOOT_X = TRAY_W / 2.0 - 34.0
FOOT_Y = 183.0
TRAY_BOLT_Y = (-120.0, 0.0, 120.0)
PANEL_BOLT_Z = (110.0, 320.0)
TRAY_SLOT = (5.5, 6.8)
TRAY_SLOT_DROP = 12.0
PANEL_CLEAR_Y = 1.2
PANEL_FLANGE = 20.0
PANEL_W = INTERIOR_W - 2 * PAINT_CLR
PANEL_H = H_REC - 1.5
PANEL_Y_BACK = -D_OVER / 2 + T + PANEL_CLEAR_Y
REAR_FLANGE_X = (-TRAY_W / 2 + RACK_CORNER + FLANGE, TRAY_W / 2 - RACK_CORNER - FLANGE)
FRONT_FLANGE_X = REAR_FLANGE_X
END_FLANGE_Y = D_OVER / 2 - (FLANGE + RACK_CORNER)

STRAP_HOLE = dict(x=0.0, y=-(D_OVER / 2 - 8.0), d=6.6)
STRAP = dict(w=25.0, foot=110.0, riser=250.0, wall=30.0, slot=40.0)
BOLT_TOP = 23


# ---------------------------------------------------------------------------
# 5. Derived dimension chains
# ---------------------------------------------------------------------------
def chains():
    return dict(
        spk_pair=2 * SPK_WB,
        spk_gap=SPK_GAP,
        spk_side_clr=SPK_SIDE_CLR,
        spk_centres=2 * SPK_X,
        pad_req_h=PAD["h"] - PAD["comp"],
        spk_bay_clear_w=INTERIOR_W,
        interior_w=INTERIOR_W,
        overall_w=W_OVER,
        tray_w=TRAY_W,
        rec_bay_clear_d=D_OVER - T - PANEL_CLEAR_Y - T - PANEL_CLEAR_Y,
        overall_d=D_OVER,
        z_bot=Z_BOT, z_mid=Z_MID, z_top=Z_TOP,
        h_rec_clear=H_REC, h_spk_clear=H_SPK,
        stand_h=H_OVER, tt_top=Z_TOP + TT["H"],
        crate_top=Z_BOT + CRATE["H"],
        flange_under_mid=Z_MID - T - FLANGE,
        side_h=SIDE_H,
        margin_x=(INTERIOR_W - TT["W"]) / 2,
        margin_y=(D_OVER - TT["D"]) / 2,
        spk_height=SPK_H,
        spk_footprint_w=SPK_WB, spk_footprint_d=SPK_DB,
    )


def report():
    c = chains()
    rows = [("speaker pair, upright (rotated bbox)", c["spk_pair"]),
            ("gap between cabinets", c["spk_gap"]),
            ("side clearance, each", c["spk_side_clr"]),
            ("acoustic centres, apart", c["spk_centres"]),
            ("speaker bay clear width", c["spk_bay_clear_w"]),
            ("overall width", c["overall_w"]),
            ("record bay clear depth", c["rec_bay_clear_d"]),
            ("overall depth", c["overall_d"]),
            ("record bay clear height", c["h_rec_clear"]),
            ("speaker bay clear height", c["h_spk_clear"]),
            ("stand height (turntable surface)", c["stand_h"]),
            ("turntable body top", c["tt_top"]),
            ("turntable side margin", c["margin_x"]),
            ("turntable front/rear margin", c["margin_y"])]
    print(f"{'dimension':44s}{'mm':>8s}{'in':>8s}")
    for n, v in rows:
        print(f"{n:44s}{v:8.1f}{v/IN:8.3f}")
    print(f"\nspeaker upright: {SPK['legs'][0]} x {SPK['legs'][1]} x {SPK_H} mm, "
          f"toed in {-SPK['toe_deg']} deg -> footprint {SPK_WB:.1f} x {SPK_DB:.1f}")


if __name__ == "__main__":
    report()
