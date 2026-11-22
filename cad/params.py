"""
GI-RAD STAND  --  parametric master parameters (single source of truth)
=======================================================================
Compact three-level sheet-metal stand for:
  Level 3 (top)    : Audio-Technica AT-LP120XUSB turntable
  Level 2 (middle) : 2x AR "Powered Partner" speakers, horizontal, facing listener
  Level 1 (bottom) : removable record crate

All CAD units are millimetres.  Inches are provided for user-facing values.

REVISION: R0.9-PROVISIONAL
Everything marked [P] is an assumption or a value that is NOT yet confirmed by
the owner of the equipment.  See docs/02_input_register.md.

Coordinate system used throughout:
    +X = right (width),  +Y = toward listener (front),  +Z = up
    origin = centre of the bottom tray's top surface, on the floor datum
"""

from dataclasses import dataclass, field, asdict
import json, math

IN = 25.4  # mm per inch

# ---------------------------------------------------------------------------
# 1. MATERIAL / PROCESS  (SendCutSend "Mild Steel, .074in" sheet, cold rolled)
# ---------------------------------------------------------------------------
MATERIAL = dict(
    name="Mild Steel CRS 1008/1010, 0.074 in (1.88 mm), 14 ga",
    E=200_000.0,        # MPa  (200 GPa, conservative vs 210 GPa textbook)
    G=77_000.0,         # MPa
    fy=205.0,           # MPa  0.2% proof / yield, cold-rolled mild steel (conservative)
    fu=340.0,           # MPa  ultimate tensile
    rho=7.85e-6,        # kg/mm^3
    nu=0.30,
    # process data, SendCutSend bending calculator (see docs/06_sources.md)
    T=1.88,
    R_in=1.60,          # effective inside bend radius @90 deg for .074"
    k_factor=0.40,
    bend_deduction_90=3.277,
    min_flange_formed=8.13,
    max_bend_len=1117.6,
    max_flat_x=762.0,   # 30 in  (cut & bend)
    max_flat_y=1117.6,  # 44 in
    max_coat_x=762.0,   # 30 in powder coat limit
    max_coat_y=914.4,   # 36 in powder coat limit  <-- most restrictive
    coat_per_side=0.08,  # mm nominal (range .05-.13)
)

T = MATERIAL["T"]
R_IN = MATERIAL["R_in"]
BD = MATERIAL["bend_deduction_90"]

# ---------------------------------------------------------------------------
# 2. EQUIPMENT  (documented envelope models; see input register)
# ---------------------------------------------------------------------------
TT = dict(  # Audio-Technica AT-LP120XUSB  [documented: A-T manual]
    W=452.0, D=352.0, H=141.6, mass=8.0,
    foot_inset_x=42.0,   # [P] foot centres inset from body sides
    foot_inset_y=45.0,   # [P] foot centres inset from front/rear
    foot_dia=38.0,       # [P] foot pad diameter
    foot_adjust=8.0,     # [P] available foot extension for levelling
    cover_open_rear=310.0,  # [P] rearward projection of open dust cover
)
SPK = dict(  # AR Powered Partner 570 / Advent AV570  (155 x 267 x 194 mm)
    W=267.0, H=155.0, D=194.0, mass=3.16,
    # prism: right-triangle cross-section, baffle = hypotenuse, tilts up
    baffle_tilt_deg=math.degrees(math.atan2(155.0, 194.0)),  # 38.6 deg
)
# isolation pads: IsoAcoustics ISO-PUCK mini (44 dia x 24 high, 2.75 kg ea)
PAD = dict(dia=44.0, h=24.0, cap=2.75, inset=32.0, comp=1.0)
CRATE = dict(  # Groove Crate 14.5 x 14.5 x 14.125 in
    W=368.3, D=368.3, H=358.8, mass_empty=1.9, mass_loaded=22.0)

# ---------------------------------------------------------------------------
# 3. STRUCTURE LAYOUT
# ---------------------------------------------------------------------------
W_OVER = 570.0     # overall width  (trays)
D_OVER = 400.0     # overall depth  (trays / side slabs)
FLANGE = 30.0      # typical down-flange depth (trays)
FLANGE_BOT = 20.0  # bottom tray front/rear flange depth
RACK_CORNER = T + 1.0        # corner clearance between adjacent flanges
PAINT_CLR = 0.30             # per-side clearance for nested (painted) parts

# clear heights
H_REC = 400.0      # bottom (record) bay clear height
H_SPK = 190.0      # speaker bay clear height

Z_BOT = 32.0                 # top surface of bottom tray
Z_MID = Z_BOT + H_REC + T
Z_TOP = Z_MID + H_SPK + T
H_OVER = Z_TOP               # overall stand height

INTERIOR_W = W_OVER - 2 * T          # between side slabs' inner faces
TRAY_W = INTERIOR_W                   # trays span the interior
SIDE_BOT = Z_BOT - 20.0                     # bottom edge of side slab
SIDE_H = (Z_TOP - T) - SIDE_BOT             # side slab height

# speaker placement: pair centred, gap between cabinets, side clearance
SPK_GAP = INTERIOR_W - 2 * SPK["W"] - 2 * 6.0
SPK_SIDE_CLR = (INTERIOR_W - 2 * SPK["W"] - SPK_GAP) / 2
SPK_Y_FRONT = D_OVER / 2                     # speaker front flush with shelf front
SPK_X = SPK["W"] / 2 + SPK_GAP / 2           # speaker centreline |x|

# ---------------------------------------------------------------------------
# 4. HARDWARE
# ---------------------------------------------------------------------------
BOLT = dict(size="M5", d=5.0, clearance=5.5, head_dia=9.5, head_h=2.75,
            length=12.0, grade="A2-70 stainless / 8.8 zinc",
            nut="DIN 6923 M5 flanged nylon-insert locknut, h=5.0", preload_N=4200.0)
FOOT = dict(thread="M6", stud_len=35.0, base_dia=23.0, base_h=9.0,
            clearance=6.6, nut="DIN 6923 M6 flanged nylon-insert locknut h=6.0")
FOOT_X = 262.0
FOOT_Y = 183.0

# bolt pattern per tray end flange (y positions), and per rear-panel flange (z)
TRAY_BOLT_Y = (-120.0, 0.0, 120.0)
PANEL_BOLT_Z = (110.0, 320.0)
TRAY_SLOT = (5.5, 6.8)      # slot width x length(vertical) in tray flanges
TRAY_SLOT_DROP = 12.0       # slot centre below tray top surface
SIDE_BOT = Z_BOT - 20.0 if 'Z_BOT' in dir() else 12.0
PANEL_CLEAR_Y = 1.2         # gap between rear panel and tray rear flanges
PANEL_FLANGE = 20.0

# derived: rear panel geometry
PANEL_W = INTERIOR_W - 2 * PAINT_CLR
PANEL_H = H_REC - 1.5
STRAP_HOLE = dict(x=0.0, y=-(D_OVER / 2 - 8.0), d=6.6)  # through the top tray deck, rear margin
BOLT_TOP = 23   # 22 tray/panel bolts + 1 strap bolt
STRAP = dict(w=25.0, foot=110.0, riser=250.0, wall=30.0, slot=40.0)
PANEL_Y_BACK = -D_OVER / 2 + T + PANEL_CLEAR_Y   # rear face of panel web
REAR_FLANGE_X = (-TRAY_W / 2 + RACK_CORNER + FLANGE, TRAY_W / 2 - RACK_CORNER - FLANGE)
FRONT_FLANGE_X = (-TRAY_W / 2 + RACK_CORNER + FLANGE, TRAY_W / 2 - RACK_CORNER - FLANGE)
END_FLANGE_Y = D_OVER / 2 - (FLANGE + RACK_CORNER)

# ---------------------------------------------------------------------------
# 5. DERIVED DIMENSION CHAINS  (printed into the documentation)
# ---------------------------------------------------------------------------
def chains():
    """Return the dimension chains required by the brief, mm and inches."""
    w = dict(
        spk_pair_w=2 * SPK["W"],
        spk_gap=SPK_GAP,
        spk_side_clr=SPK_SIDE_CLR,
        pad_req_h=PAD["h"] - PAD["comp"],
        spk_bay_clear_w=INTERIOR_W,
        interior_w=INTERIOR_W,
        overall_w=W_OVER,
        tray_w=TRAY_W,
        rec_bay_clear_d=D_OVER - T - PANEL_CLEAR_Y - T - PANEL_CLEAR_Y,
        overall_d=D_OVER,
        z_bot=Z_BOT,
        z_mid=Z_MID,
        z_top=Z_TOP,
        h_rec_clear=H_REC,
        h_spk_clear=H_SPK,
        stand_h=H_OVER,
        tt_top=Z_TOP + TT["H"],
        crate_top=Z_BOT + CRATE["H"],
        flange_under_mid=Z_MID - T - FLANGE,
        side_h=SIDE_H,
        shelf_x=TRAY_W, shelf_y=D_OVER,
        margin_x=(INTERIOR_W - TT["W"]) / 2,
        margin_y=(D_OVER - TT["D"]) / 2,
    )
    return w


def report():
    c = chains()
    rows = [
        ("speaker pair, horizontal", c["spk_pair_w"]),
        ("gap between cabinets", c["spk_gap"]),
        ("side clearance, each", c["spk_side_clr"]),
        ("speaker bay clear width", c["spk_bay_clear_w"]),
        ("overall width", c["overall_w"]),
        ("shelf width (=record bay clear width)", c["tray_w"]),
        ("record bay clear depth", c["rec_bay_clear_d"]),
        ("overall depth", c["overall_d"]),
        ("record bay clear height", c["h_rec_clear"]),
        ("speaker bay clear height", c["h_spk_clear"]),
        ("stand height (turntable support surface)", c["stand_h"]),
        ("turntable body top", c["tt_top"]),
        ("top of loaded crate", c["crate_top"]),
        ("underside of mid-tray front flange", c["flange_under_mid"]),
        ("side slab height", c["side_h"]),
        ("turntable side margin", c["margin_x"]),
        ("turntable front/rear margin", c["margin_y"]),
    ]
    print(f"{'dimension':42s} {'mm':>9s} {'in':>8s}")
    for n, v in rows:
        print(f"{n:42s} {v:9.1f} {v/IN:8.3f}")
    print(f"\nbaffle tilt (speaker, horizontal) = {SPK['baffle_tilt_deg']:.1f} deg")


def dump(path):
    d = dict(
        material=MATERIAL, turntable=TT, speaker=SPK, pad=PAD, crate=CRATE,
        layout=dict(W_OVER=W_OVER, D_OVER=D_OVER, FLANGE=FLANGE, H_REC=H_REC,
                    H_SPK=H_SPK, Z_BOT=Z_BOT, Z_MID=Z_MID, Z_TOP=Z_TOP,
                    INTERIOR_W=INTERIOR_W, SIDE_H=SIDE_H,
                    SPK_GAP=SPK_GAP, SPK_X=SPK_X),
        hardware=dict(bolt=BOLT, foot=FOOT, tray_bolt_y=TRAY_BOLT_Y,
                      panel_bolt_z=PANEL_BOLT_Z, tray_slot=TRAY_SLOT),
        chains=chains(),
    )
    with open(path, "w") as f:
        json.dump(d, f, indent=2)


if __name__ == "__main__":
    report()
