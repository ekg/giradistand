"""
FLAT PACK STAND, VARIANT B: UPRIGHT SPEAKERS  [revision WU0.9-PROVISIONAL]
=======================================================================================
Cheaper alternative to the steel stand. Same equipment, same three levels,
same footprint logic -- different material, different joinery, target < US$300.

Design intent: a plywood "puzzle" that goes together with a rubber mallet and no
tools, and comes apart again. All joints are through-cuts (one-face routing).

Coordinate system: +X right, +Y toward the listener (front), +Z up.
Origin: centre of the base shelf's top surface, floor datum at z = -32.
Units: millimetres.
"""

import math

IN = 25.4

# ---------------------------------------------------------------------------
# 1. Material: 18 mm birch plywood (Baltic birch, 13 ply, void-free core)
# ---------------------------------------------------------------------------
PLY = dict(
    name="Baltic birch plywood, 18 mm nominal, 13-ply, void-free core, B/BB face",
    t=18.0,               # NOMINAL - the actual sheet must be measured
    t_range=(17.4, 18.4),  # what "18 mm" actually measures in practice
    # plywood-appropriate, direction-aware properties (conservative):
    E_face=7_000.0,       # MPa  bending, load parallel to face grain plies
    E_cross=2_500.0,      # MPa  bending, load across the plies
    G=700.0,              # MPa  rolling shear / panel shear (conservative)
    rho=680.0e-9,         # kg/mm^3  (680 kg/m^3)
    f_bend_face=38.0,     # MPa  0.2% offset bending strength parallel to grain (B/BB)
    f_bend_cross=22.0,    # MPa  across
    f_bearing=8.0,        # MPa  bearing on plywood edge/face (conservative)
    f_shear_panel=1.0,    # MPa  panel (rolling) shear, conservative
    f_glue_line=1.0,      # MPa  glue-line shear, conservative
    bend_radius=45.0,     # mm   minimum cold-bend radius for 18 mm -- not used here
    sheet=(1525.0, 1525.0),   # 5 x 5 ft sheet
    kerf=6.35,            # 1/4 in cutter
    dogbone=3.2,          # dogbone relief radius for internal corners
)

T = PLY["t"]

# fit allowances (independent parameters, see docs 06)
FIT = dict(
    slot=0.20,        # slot wider than panel nominal
    slot_range=(0.10, 0.30),   # what the fit coupon tests
    depth=6.0,        # clearance for panel-in-slot lateral position
    edge_margin=12.0, # material between a slot and a panel edge
)

# ---------------------------------------------------------------------------
# 2. Equipment (same envelope models as the steel design)
# ---------------------------------------------------------------------------
TT = dict(W=452.0, D=352.0, H=141.6, mass=8.0,
          foot_inset_x=42.0, foot_inset_y=45.0, foot_dia=38.0)
# AR Powered Partner standing UPRIGHT: 150 x 196 mm triangular plan, 270 high
SPK = dict(legs=(150.0, 196.0), H=270.0, mass=3.5, toe_deg=20.0,
           baffle_tilt_deg=0.0)
SPK_H = SPK["H"]


def _rot_bbox(legs, deg):
    t = math.radians(deg)
    pts = [(0.0, 0.0), (legs[0], 0.0), (0.0, legs[1])]
    r = [(x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t))
         for x, y in pts]
    xs = [p[0] for p in r]
    ys = [p[1] for p in r]
    return max(xs) - min(xs), max(ys) - min(ys), min(xs), min(ys)


SPK_WB, SPK_DB, _, _ = _rot_bbox(SPK["legs"], -SPK["toe_deg"])
PAD = dict(dia=44.0, h=24.0, cap=2.75, inset=0.0, comp=1.0, qty=3)
CRATE = dict(W=368.3, D=368.3, H=358.8, mass_loaded=22.0)

# ---------------------------------------------------------------------------
# 3. Layout
# ---------------------------------------------------------------------------
W_OVER = 518.0       # 2 x 18 side + 482 interior = 452 turntable + 2 x 15 margin
D_OVER = 415.0       # 394 shelf + 18 rear band + 3 gap
INTERIOR_W = W_OVER - 2 * T            # 482.0
H_REC = 372.0        # base shelf top -> mid shelf underside (crate 358.8 + 13.2)
H_SPK = 305.0        # mid shelf top  -> top shelf underside (270 + 23 + 12)
Z_BASE = 32.0        # base shelf top surface above floor
Z_MID = Z_BASE + H_REC + T
Z_TOP = Z_MID + H_SPK + T
H_OVER = Z_TOP
SIDE_H = Z_TOP                     # side panels run from the floor line to the top
TENON_L = 150.0      # length of the shelf tabs (in Y)
TENON_OUT = 18.0     # how far a tab protrudes past the side panel's outer face
DOWEL = dict(d=8.0, l=40.0, x_from_shoulder=T + 4.0, qty=6)
BACK_T = T
BACK_D = 330.0
SHELF_D = D_OVER - T - 3.0          # 394
SHELF_L = INTERIOR_W + 2 * (T + TENON_OUT)   # 638
SPK_GAP = INTERIOR_W - 2 * SPK_WB - 2 * 6.0
SPK_X = SPK_WB / 2 + SPK_GAP / 2
SPK_Y_FRONT = D_OVER / 2 - 12.0
SPK_SIDE_CLR = 6.0

# feet: same M6 glide + locknut scheme as the steel version
FOOT = dict(thread="M6", stud_len=40.0, base_dia=23.0, base_h=9.0,
            clearance=6.6, x=INTERIOR_W / 2 - 34.0, y=SHELF_D / 2 - 45.0)

# slots in the side panels
SLOT_H = T + FIT["slot"]            # 18.20
SLOT_L = TENON_L + FIT["slot"]      # 150.20
SLOT_X_MARGIN = 12.0                # slot end to panel edge along Y
REAR_SLOT_L = 340.0                 # back panel slot, open at the top edge

DOWEL_HOLE = 8.4


def chains():
    return dict(
        interior_w=INTERIOR_W,
        spk_pair=2 * SPK_WB,
        spk_gap=SPK_GAP,
        spk_centres=2 * SPK_X,
        overall_w=W_OVER,
        shelf_l=SHELF_L,
        shelf_d=SHELF_D,
        overall_d=D_OVER,
        rec_clear_h=H_REC,
        spk_clear_h=H_SPK,
        base_h=Z_BASE,
        mid_h=Z_MID,
        top_h=Z_TOP,
        tt_top=Z_TOP + TT["H"],
        crate_top=Z_BASE + CRATE["H"],
        margin_x=(INTERIOR_W - TT["W"]) / 2,
        margin_y=(SHELF_D - TT["D"]) / 2,
        side_h=SIDE_H,
    )


if __name__ == "__main__":
    c = chains()
    print(f"{'dimension':38s}{'mm':>9s}{'in':>8s}")
    for k, v in c.items():
        print(f"{k:38s}{v:9.1f}{v/IN:8.3f}")
