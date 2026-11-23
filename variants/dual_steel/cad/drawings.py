"""
Dimensioned drawing sheets generated from the CAD geometry (A2 landscape).

  S1 GA-01  general assembly: front elevation, side elevation (near slab
            removed), plan, vertical dimension chain, notes
  S2 P1-02  side slab (face view + flat pattern)
  S3 P2-03  shelf tray (plan, section, elevation, flat pattern with bend lines)
  S4 P3-04  base tray (as P2, with foot holes and 20 mm front flanges)
  S5 P4-06  rear panel (elevation, section, flat pattern)
  S6 P5-07  wall strap + clamped joint detail at 4:1

Units mm, revision R0.9, CRS 1.88 mm, powder coat BK01 textured black.
"""

import os, sys, math
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
import matplotlib.collections as mc
import matplotlib.patches as mp
import params as P
import model as M
import sheetmetal as S
import drawlib as D
import export as X

OUT = os.path.join(os.path.dirname(_here), "out", "drawings")
W, H = 594, 420
MAT = "CRS 1.88 mm (0.074 in) - powder coat TEXTURED BLACK (BK01)"
REV = "R0.9"


def place(sh, shape, view, xl, yb, scale=1.0, label=None, hidden=True, dy=-9):
    vis, hid = D.project(shape, view)
    xs = [p[0] for pl in vis for p in pl]
    ys = [p[1] for pl in vis for p in pl]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    sh.view(vis, hid if hidden else [], xl - scale * x0, yb - scale * y0, scale)
    w, h = scale * (x1 - x0), scale * (y1 - y0)
    if label:
        sh.note(xl + w / 2, yb + dy, label, size=6.0, ha="center", weight="bold")
    return dict(ox=xl - scale * x0, oy=yb - scale * y0, xl=xl, yb=yb, xr=xl + w,
                yt=yb + h, w=w, h=h, scale=scale, x0=x0, y0=y0)


def place_group(sh, groups, view, xl, yb, scale=1.0, label=None, dy=-9):
    """groups = [(shape, lw, colour, show_hidden), ...] drawn with one origin."""
    ref = groups[0][0]
    vis0, _ = D.project(ref, view)
    xs = [p[0] for pl in vis0 for p in pl]
    ys = [p[1] for pl in vis0 for p in pl]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    ox, oy = xl - scale * x0, yb - scale * y0
    for (shape, lw, col, hid_on) in groups:
        vis, hid = D.project(shape, view)
        sh.view(vis, hid if hid_on else [], ox, oy, scale, lw=lw, color=col)
    w, h = scale * (x1 - x0), scale * (y1 - y0)
    if label:
        sh.note(xl + w / 2, yb + dy, label, size=6.4, ha="center", weight="bold")
    return dict(ox=ox, oy=oy, xl=xl, yb=yb, xr=xl + w, yt=yb + h, w=w, h=h,
                scale=scale, x0=x0, y0=y0)


def notes(sh, x, y, items, size=5.6, lh=4.6, title="NOTES", width=None):
    sh.note(x, y, title, size=size + 0.9, weight="bold")
    yy = y - lh
    for i, t in enumerate(items, 1):
        sh.note(x, yy, t, size=size)
        yy -= lh
    return yy


def flat_outline(sh, outline, bends, holes, slots, xl, yb, sc, label,
                 hole_d=5.5, slot=None, dims=True):
    pts = [(xl + sc * x, yb + sc * y) for (x, y) in outline]
    sh.ax.add_collection(mc.LineCollection([pts + [pts[0]]], colors="#111",
                                           linewidths=0.65))
    for bl in bends:
        sh.ax.add_collection(mc.LineCollection(
            [[(xl + sc * x, yb + sc * y) for (x, y) in bl]], colors="#b02020",
            linewidths=0.5, linestyles=(0, (6, 2, 1, 2))))
    for (x, y) in holes:
        sh.ax.add_patch(mp.Circle((xl + sc * x, yb + sc * y), sc * hole_d / 2,
                                  fill=False, lw=0.65, ec="#111"))
    for (x, y) in slots:
        w, h = slot or P.TRAY_SLOT
        sh.ax.add_patch(mp.FancyBboxPatch((xl + sc * (x - w / 2), yb + sc * (y - h / 2)),
                                          sc * w, sc * h,
                                          boxstyle=f"round,pad=0,rounding_size={sc*w/2}",
                                          fill=False, lw=0.65, ec="#111"))
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    rect = dict(xl=xl, yb=yb, xr=xl + sc * max(xs), yt=yb + sc * max(ys))
    sh.note((rect["xl"] + rect["xr"]) / 2, yb - 11, label, size=6.0, ha="center",
            weight="bold")
    if dims:
        sh.dim_h(rect["xl"], rect["xr"], rect["yt"] + 11, f"{max(xs):.1f}")
        sh.dim_v(rect["yb"], rect["yt"], rect["xr"] + 13, f"{max(ys):.1f}")
    return rect


# ---------------------------------------------------------------------------
def sheet_assembly():
    sh = D.Sheet(W, H, title="GI-RAD STAND - GENERAL ASSEMBLY", number="GA-01D",
                 rev=REV, scale_note="1:2.5",
                 subtitle="three-level stand: AT-LP120XUSB / 2 x Powered Partner / "
                          "record crate", material=MAT)
    parts = M.build()
    allp = (parts["P1"]["solids"][0].fuse(parts["P1"]["solids"][1])
            .fuse(parts["P2"]["solids"][0]).fuse(parts["P2"]["solids"][1])
            .fuse(parts["P3"]["solids"][0]).fuse(parts["P4"]["solids"][0])).clean()
    near = (parts["P1"]["solids"][0].fuse(parts["P2"]["solids"][0])
            .fuse(parts["P2"]["solids"][1]).fuse(parts["P3"]["solids"][0])
            .fuse(parts["P4"]["solids"][0])).clean()
    eq = (M.make_tt().fuse(M.make_speaker(1)).fuse(M.make_speaker(-1))
          .fuse(M.make_crate())).clean()
    sc = 1 / 2.5
    v1 = place_group(sh, [(allp, 0.6, "#111", True), (eq, 0.35, "#8d8d8d", False)],
                     "front", 35, 110, sc, "FRONT ELEVATION (equipment phantom)")
    v2 = place_group(sh, [(near, 0.6, "#111", True), (eq, 0.35, "#8d8d8d", False)],
                     "side_r", 292, 110, sc,
                     "SIDE ELEVATION - near side slab removed")
    v3 = place_group(sh, [(allp, 0.6, "#111", True), (eq, 0.35, "#8d8d8d", False)],
                     "top", 462, 306, 1 / 5, "PLAN")

    xd = 272
    for a, b, txt in [(0, P.Z_BOT, "32"), (P.Z_BOT, P.Z_MID, "402"),
                      (P.Z_MID, P.Z_TOP, "307")]:
        sh.dim_v(v1["oy"] + sc * a, v1["oy"] + sc * b, xd, txt, size=5.6)
    sh.dim_v(v1["oy"], v1["oy"] + sc * P.Z_TOP, xd + 13, "741", size=5.6)
    sh.dim_v(v1["oy"], v1["oy"] + sc * (P.Z_TOP + P.TT["H"]), xd + 26, "882", size=5.6)

    yb = v1["yb"] - 22
    sh.dim_h(v1["xl"], v1["xr"], yb, "570")
    sh.dim_h(v1["xl"] + sc * P.T, v1["xr"] - sc * P.T, yb - 9, "566.2 clear")
    sh.dim_h(v1["xl"] + sc * (P.W_OVER / 2 - P.SPK_X_L - P.SPK_W / 2),
             v1["xl"] + sc * (P.W_OVER / 2 - P.SPK_X_L + P.SPK_W / 2), yb - 18,
             "534 lying down")
    sh.dim_h(v2["xl"], v2["xr"], v2["yb"] - 22, "400")
    sh.dim_h(v3["xl"], v3["xr"], v3["yb"] - 10, "570")

    notes(sh, 462, 284, [
        "1. Dimensions in mm. Material CRS 1.88 mm throughout; deburr all",
        "   edges, external corners R3 min.",
        "2. Fabricate per part sheets: P1 x2, P2 x2, P3 x1, P4 x1, P5 x1.",
        "3. Powder coat textured black BK01 after bending. No threads on",
        "   parts: all threads are in purchased locknuts (capped when coated).",
        "4. Fasteners: 23 x M5x12 ISO 7380-1 button head + DIN 6923 M5",
        "   flanged locknut. BUTTON HEAD INSIDE the bay, LOCKNUT OUTSIDE, so",
        "   every nut is reachable with a wrench (with the head outside the base",
        "   tray's flange pocket would have been closed). Torque 3.0 N.m.",
        "5. Feet: 4 x M6 male-stud glide, 35 mm thread, 23 mm base on the floor,",
        "   + DIN 6923 M6 flanged locknut on the deck's TOP face.",
        "6. Clear openings: record bay 566.2 W x 393.8 D x 400 H (370 usable);",
        "   speaker bay 566.2 x 400 x 305 H; turntable surface 566.2 x 400 flat.",
        "7. Turntable plinth top at 882 above floor at nominal foot setting.",
        "8. The bay takes the Powered Partner BOTH way up:",
        "   (A) upright 150 x 196 plan x 270 H, 3 isolators each, toed in 20 deg;",
        "   (B) lying down 267 W x 194 D x 155 H, 4 isolators each, 20 gap.",
        "   Positions and both layouts are on the render sheets and in docs/NOTES.md.",
        "9. Turntable rear connectors face open air; keep 80 mm clear of the",
        "   wall for cables. If the dust cover is hinged open instead of removed",
        "   (A-T recommend removing it to play), allow 40 mm behind the stand",
        "   and 360 mm of headroom above the plinth.",
        "10. No welding, drilling, tapping, filing or painting at assembly.",
        "11. P5 wall strap is part of the standard kit - see sheet S6.",
    ], size=4.9, lh=4.0)
    sh.save(os.path.join(OUT, "S1_GA-01_assembly.png"))


def sheet_side_slab():
    sh = D.Sheet(W, H, title="P1   SIDE SLAB", number="P1-02", rev=REV,
                 scale_note="1:2", subtitle="qty 2 - identical, handing by position",
                 material=MAT)
    body = M.make_side_slab(1)
    v = place(sh, body, "side_r", 25, 95, 1 / 2, "FACE VIEW (from outside)")
    outline = [(0, 0), (P.D_OVER, 0), (P.D_OVER, P.SIDE_H), (0, P.SIDE_H)]
    holes = [(y + P.D_OVER / 2, z - P.SIDE_BOT) for (y, z, _) in M.side_slab_holes()]
    f = flat_outline(sh, outline, [], holes, [], 255, 95, 1 / 2,
                     "FLAT PATTERN (qty 2)", hole_d=P.BOLT["clearance"])
    # flat dims
    sh.dim_h(f["xl"], f["xr"], f["yb"] - 20, "400")
    sh.dim_v(f["yb"], f["yt"], f["xl"] - 16, "611.9")
    # hole rows on the flat
    rows = {}
    for (y, z, _) in M.side_slab_holes():
        rows.setdefault(round(z - P.SIDE_BOT, 1), []).append(y)
    for i, (zz, ys) in enumerate(sorted(rows.items())):
        yy = f["yb"] + (1 / 2) * zz
        sh.dim_v(f["yb"], yy, f["xr"] + 18 + 10 * i, "", size=5)
        sh.note(f["xr"] + 20 + 10 * i, yy, f"{zz:.1f}", size=5.0)
    sh.note(f["xr"] + 16, f["yt"] - 6, "hole rows z:", size=5.2, weight="bold")
    sh.note(f["xr"] + 16, f["yt"] - 12, f"z = {', '.join(f'{k:.1f}' for k in sorted(rows))}",
            size=5.0)
    sh.note(f["xr"] + 16, f["yt"] - 18, "y = -120, 0, +120 (3 per row)", size=5.0)
    sh.note(f["xr"] + 16, f["yt"] - 24, "5.5 dia, 11 off", size=5.0)

    notes(sh, 470, 400, [
        "1. Flat part, no bends. 2 off, interchangeable (the hole",
        "   pattern is symmetric front/rear).",
        "2. 11 x 5.5 dia holes for M5: +0.3/-0.0.",
        "   z (from the bottom edge) = 8.0, 409.9, 601.8 for the",
        "   3 x 3 tray joints; 130.0 and 340.0 for the rear panel",
        "   (y = -187.0).",
        "3. Do not tap - threads are in purchased locknuts.",
        "4. Bend-to-edge tolerance of the trays (+/-0.38) is absorbed",
        "   by the 6.8 mm slots in the trays, not here.",
        "5. Deburr, powder coat BK01.",
    ], size=4.9, lh=4.0)
    sh.save(os.path.join(OUT, "S2_P1-02_side_slab.png"))


def sheet_tray(pid, z_top, front_h, foot_holes, title, number, fname):
    sh = D.Sheet(W, H, title=title, number=number, rev=REV, scale_note="1:2.5",
                 subtitle=("qty 2 - top and middle shelf" if pid == "P2" else
                           "qty 1 - bottom level, foot holes"),
                 material=MAT)
    body, spec = M.make_tray(z_top, front_h=front_h, foot_holes=foot_holes)
    sc = 1 / 2.5
    v1 = place(sh, body, "top", 20, 235, sc, "PLAN (top face up)")
    v2 = place(sh, body, "side_r", 20, 194, sc, "SECTION A-A", dy=-8)
    v3 = place(sh, body, "front", 20, 166, sc, "FRONT ELEVATION", dy=-8)
    outline, holes, slots, bends = X.flat_tray(spec)
    f = flat_outline(sh, outline, bends, holes, slots, 265, 190, sc,
                     "FLAT PATTERN - bend lines dashed red",
                     hole_d=P.FOOT["clearance"])
    # plan dims
    sh.dim_h(v1["xl"], v1["xr"], v1["yb"] - 10, "482.2")
    sh.dim_v(v1["yb"], v1["yt"], v1["xr"] + 10, "400")
    sh.dim_h(v1["xl"] + sc * (P.TRAY_W / 2 + P.TRAY_BOLT_Y[0]),
             v1["xl"] + sc * (P.TRAY_W / 2 + P.TRAY_BOLT_Y[-1]),
             v1["yb"] - 20, "240 = 2 x 120")
    sh.dim_v(v2["yb"], v2["yt"], v2["xr"] + 10, f"{front_h:.0f}")
    items = [
        "1. Sheet metal, 4 bends, 90 deg, inside radius 1.60, K = 0.40,",
        "   bend deduction 3.277 mm per bend (SendCutSend .074 mild steel).",
        "2. All four flanges turn DOWN (away from the top face).",
        "3. Corner relief 31.88 mm from each corner (see flat pattern).",
        f"4. Slot {P.TRAY_SLOT[0]} x {P.TRAY_SLOT[1]}, long axis vertical in the",
        "   formed part, centre 12.0 below the top surface (18.0 from the",
        "   flange free edge in the flat).",
        "5. Slots and holes >= 6 mm clear of bend centre lines (die 12.0).",
        "6. The TOP FACE must be flat and featureless: it carries the",
        "   turntable (P2 top) or the speaker isolators (P2 middle).",
        "7. Folded STEP is authoritative for the 3D bending workflow; the",
        "   flat pattern is a checked reference.",
        "8. Deburr, powder coat BK01, cap threads.",
    ]
    if foot_holes:
        items.append("9. 4 x 6.6 dia foot holes at x = +/-262, y = +/-183.")
    notes(sh, 265, 172, items, size=4.8, lh=3.9)
    sh.save(os.path.join(OUT, fname))


def sheet_panel():
    sh = D.Sheet(W, H, title="P4   REAR PANEL", number="P4-06", rev=REV,
                 scale_note="1:2.5", subtitle="qty 1 - racking diaphragm, record bay",
                 material=MAT)
    body = M.make_rear_panel()
    sc = 1 / 2.5
    v1 = place(sh, body, "front", 20, 235, sc, "ELEVATION (from front)")
    v2 = place(sh, body, "top", 20, 196, sc, "PLAN", dy=-8)
    outline, holes, slots, bends = X.flat_panel()
    f = flat_outline(sh, outline, bends, holes, slots, 265, 190, sc,
                     "FLAT PATTERN - bend lines dashed red")
    sh.dim_h(v1["xl"], v1["xr"], v1["yb"] - 10, f"{P.PANEL_W:.1f}")
    sh.dim_v(v1["yb"], v1["yt"], v1["xr"] + 10, f"{P.PANEL_H:.1f}")
    sh.dim_v(v2["yb"], v2["yt"], v2["xr"] + 10, "20")
    notes(sh, 265, 172, [
        "1. C-channel, 2 bends, both flanges turn toward +Y (the front).",
        "2. This part is the shear diaphragm of the lower bay: positive,",
        "   friction-independent side-to-side racking resistance. Do not omit.",
        "3. Width 0.6 mm under the clear internal width (laser + coating",
        "   allowance); the bolts pull the flanges onto the side slabs.",
        "4. Height 1.5 mm under the bay height so it drops in freely.",
        "5. Holes 5.5 dia, 10.0 from the flange outer face, at z =",
        "   +110 and +320 above the base tray.",
        "6. Deburr, powder coat BK01, cap threads.",
    ], size=4.8, lh=3.9)
    sh.save(os.path.join(OUT, "S5_P4-06_rear_panel.png"))


def sheet_strap_and_joint():
    import cadquery as cq
    sh = D.Sheet(W, H, title="P5   WALL STRAP   +   CLAMPED JOINT DETAIL",
                 number="P5-07", rev=REV, scale_note="1:1 / 4:1",
                 subtitle="anti-tip strap (standard kit) and tray-to-slab joint",
                 material=MAT)
    # joint detail: true-scale schematic section (the projection was unreadable
    # at this scale; every dimension below is a model value)
    x0, y0, k = 60.0, 120.0, 3.6

    def R(x, z, dx, dz, **kw):
        sh.ax.add_patch(mp.Rectangle((x0 + k * x, y0 + k * z), k * dx, k * dz,
                                     fill=False, lw=0.7, ec=kw.get("ec", "#111")))
    R(-1.88, -30.0, 1.88, 30.0)                    # tray end flange
    R(0.0, -35.0, 1.88, 40.0)                      # side slab
    R(-46.0, 0.0, 44.12, 1.88)                     # tray plate above
    R(-4.63, -4.75, 2.75, 9.5)                     # button head (inside)
    R(-4.63, -2.5, 14.4, 5.0)                      # shank
    R(1.88, -5.9, 5.0, 11.8)                       # flanged locknut (outside)
    sh.note(x0 + k * -50, y0 + k * -6, "INSIDE (bay)", size=5.2, weight="bold")
    sh.note(x0 + k * 8, y0 + k * -6, "OUTSIDE", size=5.2, weight="bold")
    sh.dim_h(x0 + k * -1.88, x0 + k * 0.0, y0 + k * 2.4, "1.88", size=5.0)
    sh.dim_h(x0 + k * 0.0, x0 + k * 1.88, y0 + k * 2.4, "1.88", size=5.0)
    sh.dim_v(y0 + k * -30, y0 + k * 0, x0 + k * -6.2, "30", size=5.0)
    sh.dim_h(x0 + k * -4.63, x0 + k * 6.88, y0 + k * -13, "12.0 shank", size=5.0)
    sh.leader(x0 + k * -3.2, y0 + k * 4.0, x0 + k * -52, y0 + k * 16,
              "M5x12 button head, 2.75 proud inboard")
    sh.leader(x0 + k * 4.4, y0 + k * 5.0, x0 + k * 10, y0 + k * 16,
              "DIN 6923 M5 flanged locknut")
    sh.leader(x0 + k * 0.9, y0 + k * -22, x0 + k * 14, y0 + k * -28,
              "slab 1.88, hole 5.5")
    sh.leader(x0 + k * -1.0, y0 + k * -26, x0 + k * -52, y0 + k * -34,
              "tray end flange 1.88, slot 6.8 x 5.5")
    sh.note(x0 + k * -52, y0 + k * -44,
            "DETAIL B-B  (3.6:1) - clamped joint at one M5 bolt", size=6.0,
            weight="bold")
    sh.note(x0 + k * -52, y0 + k * -50,
            "3 bolts per flange. 3.0 N.m -> 3.0 kN preload each, 9 kN clamp, slip "
            "margin 27:1 at 100 N. Joint opens at 45 N.m (demand 4.8 N.m).",
            size=4.6)

    strap = M.make_wall_strap()
    v2 = place(sh, strap, "top", 380, 220, 1 / 2.0, "P5 PLAN (1:2)")
    sh.dim_v(v2["yb"], v2["yt"], v2["xr"] + 8, "110")
    sh.dim_h(v2["xl"], v2["xr"], v2["yb"] - 16, "25")
    notes(sh, 400, 400, [
        "P5 ANTI-TIP STRAP - 1 off, part of the standard kit",
        "1. CRS 1.88, 25 wide, two 90 deg bends: foot 110 + riser 250 +",
        "   wall flange 30.",
        "2. The foot has a 6.6 x 40 slot: it bolts down through the 6.6",
        "   hole in the top tray's rear margin (8 mm from the rear edge,",
        "   16 mm behind the turntable) with one M5 bolt + locknut.",
        "3. The slot takes up the wall distance: it suits a gap of about",
        "   50-110 mm between the stand's rear face and the wall.",
        "4. The wall flange takes a 4 x 40 screw or a plasterboard anchor",
        "   (for the user's wall type - not supplied). Drilling that one",
        "   hole is the ONLY home operation outside the kit.",
        "5. Leave the strap slack (no tension) so the stand still sits on",
        "   all four feet; re-check the feet after fixing.",
        "6. With P5 fitted, tipping is not a credible failure mode.",
    ], size=4.7, lh=3.8)
    sh.save(os.path.join(OUT, "S6_P5-07_strap_and_joint.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.startswith("_test"):
            os.remove(os.path.join(OUT, f))
    sheet_assembly()
    sheet_side_slab()
    sheet_tray("P2", P.Z_TOP, P.FLANGE, False, "P2   SHELF TRAY", "P2-03",
               "S3_P2-03_shelf_tray.png")
    sheet_tray("P3", P.Z_BOT, P.FLANGE_BOT, True, "P3   BASE TRAY", "P3-04",
               "S4_P3-04_base_tray.png")
    sheet_panel()
    sheet_strap_and_joint()


if __name__ == "__main__":
    main()
