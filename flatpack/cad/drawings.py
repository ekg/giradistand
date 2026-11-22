"""
Flat-pack drawing sheets (A2 landscape) from the same geometry as the DXFs.
  F1  general assembly + dimension chains
  F2  parts, joint detail, fit coupon
  F3  sheet nest
"""

import os, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(_here)), "cad"))
sys.path.insert(0, _here)
import matplotlib.patches as mp
import matplotlib.collections as mc
import cadquery as cq
import params as P
import model as M
import export as X
import drawlib as D

OUT = os.path.join(os.path.dirname(_here), "out", "drawings")
W, H = 594, 420
MAT = "18 mm Baltic birch plywood, B/BB, void-free core; edges sanded R2; unfinished"
REV = "W0.9"


def place(sh, shape, view, xl, yb, scale, label=None, lw=0.6, dy=-9):
    vis, hid = D.project(shape, view)
    xs = [p[0] for pl in vis for p in pl]
    ys = [p[1] for pl in vis for p in pl]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    sh.view(vis, hid, xl - scale * x0, yb - scale * y0, scale, lw=lw)
    w, h = scale * (x1 - x0), scale * (y1 - y0)
    if label:
        sh.note(xl + w / 2, yb + dy, label, size=6.2, ha="center", weight="bold")
    return dict(ox=xl - scale * x0, oy=yb - scale * y0, xl=xl, yb=yb, xr=xl + w,
                yt=yb + h, w=w, h=h, scale=scale)


def notes(sh, x, y, items, size=4.9, lh=4.0, title="NOTES"):
    sh.note(x, y, title, size=size + 0.9, weight="bold")
    yy = y - lh
    for t in items:
        sh.note(x, yy, t, size=size)
        yy -= lh


def sheet_ga():
    sh = D.Sheet(W, H, title="FLAT PACK STAND - GENERAL ASSEMBLY", number="F1",
                 rev=REV, scale_note="1:2.5",
                 subtitle="18 mm birch plywood, tab-and-slot with dowel locks",
                 material=MAT)
    parts = M.build()
    frame = (parts["P1"]["solids"][0].fuse(parts["P1"]["solids"][1])
             .fuse(parts["P2"]["solids"][0]).fuse(parts["P2"]["solids"][1])
             .fuse(parts["P3"]["solids"][0])).clean()
    near = (parts["P1"]["solids"][0].fuse(parts["P2"]["solids"][0])
            .fuse(parts["P2"]["solids"][1]).fuse(parts["P3"]["solids"][0])).clean()
    eq = (M.make_tt().fuse(M.make_speaker(1)).fuse(M.make_speaker(-1))
          .fuse(M.make_crate())).clean()
    sc = 1 / 2.6
    v1 = place(sh, frame, "front", 30, 110, sc, "FRONT ELEVATION")
    v2 = place(sh, near, "side_r", 300, 110, sc, "SIDE ELEVATION (near side removed)")
    xd = 268
    for a, b, t in ((0, P.Z_BASE, "32"), (P.Z_BASE, P.Z_MID, "390"),
                    (P.Z_MID, P.Z_TOP, "208")):
        sh.dim_v(v1["oy"] + sc * a, v1["oy"] + sc * b, xd, t, size=5.6)
    sh.dim_v(v1["oy"], v1["oy"] + sc * P.Z_TOP, xd + 14, "630", size=5.6)
    yb = v1["yb"] - 24
    sh.dim_h(v1["xl"], v1["xr"], yb, "602")
    sh.dim_h(v1["xl"] + sc * P.T, v1["xr"] - sc * P.T, yb - 9, "566 clear")
    sh.dim_h(v2["xl"], v2["xr"], v2["yb"] - 24, "415")
    notes(sh, 460, 285, [
        "1. Dimensions in mm. All parts 18 mm Baltic birch plywood,",
        "   B/BB, void-free 13-ply core, CNC routed, edges sanded R2.",
        "2. Sheet must be measured before cutting: the slot width is",
        f"   the measured thickness + the clearance chosen from the fit",
        "   coupon (P5). Nominal 18.2 mm.",
        "3. Parts: P1 side panel x2, P2 shelf x2, P3 base shelf x1,",
        "   P4 wall strap x1, P5 fit coupon x1. All from one 1525 x 1525",
        "   sheet (see F3).",
        "4. Grain: long axis of every part along the sheet's long axis.",
        "5. Assembly: no tools. 6 x 8 mm birch dowels lock the shelves.",
        "   Rubber mallet for seating only - never force a joint.",
        "6. Clear openings: record bay 566 x 394 x 372 h; speaker bay",
        "   566 x 394 x 190 h; turntable surface 566 x 394.",
        "7. Turntable support surface 630 above the floor; plinth top 772.",
        "8. Feet: 4 x M6 stud glides + flange locknuts in the base shelf",
        "   (same hardware as the metal design).",
        "9. P4 wall strap: fit it. The unrestrained stand resists about",
        "   100 N at bench height when loaded and about 60 N when the",
        "   records are removed.",
        "10. No back panel is used: the shelves act as diaphragms and the",
        "    open back keeps cables and speaker ventilation clear.",
    ])
    sh.save(os.path.join(OUT, "F1_GA_assembly.png"))


def flat_panel(sh, geo, pid, xl, yb, sc, label, dims=()):
    pts, holes, slots = geo[pid]["pts"], geo[pid]["holes"], geo[pid]["slots"]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, y0 = min(xs), min(ys)
    P2 = [(xl + sc * (u - x0), yb + sc * (v - y0)) for (u, v) in pts]
    sh.ax.add_collection(mc.LineCollection([P2 + [P2[0]]], colors="#111",
                                           linewidths=0.65))
    for (u, v, r) in holes:
        sh.ax.add_patch(mp.Circle((xl + sc * (u - x0), yb + sc * (v - y0)), sc * r,
                                  fill=False, lw=0.6, ec="#111"))
    for (u, v, w, h) in slots:
        sh.ax.add_patch(mp.Rectangle((xl + sc * (u - w / 2 - x0), yb + sc * (v - h / 2 - y0)),
                                     sc * w, sc * h, fill=False, lw=0.6, ec="#111"))
        for sx in (1, -1):
            for sy in (1, -1):
                sh.ax.add_patch(mp.Circle(
                    (xl + sc * (u + sx * w / 2 - x0), yb + sc * (v + sy * h / 2 - y0)),
                    sc * P.PLY["dogbone"], fill=False, lw=0.4, ec="#b02020"))
    w, h = (max(xs) - x0) * sc, (max(ys) - y0) * sc
    sh.note(xl + w / 2, yb - 11, label, size=6.0, ha="center", weight="bold")
    sh.dim_h(xl, xl + w, yb + h + 10, f"{max(xs)-x0:.1f}", size=5.4)
    sh.dim_v(yb, yb + h, xl + w + 11, f"{max(ys)-y0:.1f}", size=5.4)
    return dict(xl=xl, yb=yb, xr=xl + w, yt=yb + h)


def sheet_parts():
    sh = D.Sheet(W, H, title="FLAT PACK STAND - PARTS AND JOINERY", number="F2",
                 rev=REV, scale_note="1:6 / 1:2", subtitle="all parts are through-cut",
                 material=MAT)
    geo, sheets, ap = X.export_all()
    sc = 1 / 6.0
    flat_panel(sh, geo, "P1", 20, 250, sc, "P1 SIDE PANEL x2  (415 x 630 x 18)")
    flat_panel(sh, geo, "P2", 200, 250, sc, "P2 SHELF x2  (638 x 394 x 18)")
    flat_panel(sh, geo, "P3", 20, 90, sc, "P3 BASE SHELF x1  (+ 4 foot holes)")
    flat_panel(sh, geo, "P4", 200, 90, 1 / 2.0, "P4 WALL STRAP x1")
    flat_panel(sh, geo, "P5", 360, 90, 1 / 2.0, "P5 FIT COUPON x1")
    # joint detail 1:1 of a tab in a slot
    bolt = None
    tray = M.make_shelf(P.Z_TOP)
    side = M.make_side(1)
    clip = cq.Solid.makeBox(90, 130, 50, cq.Vector(255, -40, 596))
    grp = (tray.intersect(clip).fuse(side.intersect(clip))).clean()
    v = place(sh, grp, "top", 330, 255, 1.6, "DETAIL A  (1.6:1) - tab in slot + dowel")
    sh.leader(v["xl"] + 40, v["yb"] + 40, v["xr"] + 6, v["yt"] - 4,
              "shelf tab (18 thick) through the side slot")
    sh.leader(v["xl"] + 12, v["yb"] + 62, v["xr"] + 6, v["yt"] - 12,
              "8 mm dowel, 11 proud each side")
    sh.leader(v["xl"] + 6, v["yb"] + 20, v["xr"] + 6, v["yt"] - 20,
              "dogbone reliefs at the slot corners")
    notes(sh, 330, 170, [
        "1. Every feature is a through-cut: one routing setup, one face.",
        "2. Slots + dogbones: square slot 150.2 x 18.2 with 4 x R4 corner",
        "   reliefs, so the shelf tab's square corners pass. Cut the",
        "   slot width to the MEASURED panel thickness + the clearance",
        "   chosen from the fit coupon.",
        "3. Fit coupon P5 has three slots at +0.10 / +0.20 / +0.30 mm",
        "   clearance. Cut it from the same sheet in the same setup,",
        "   test the real panel, then set the production slot width.",
        "4. Grain: long axis along the sheet's long axis for P1 and P2/P3.",
        "5. Do not sand or force a joint: adjust the cut.",
        "6. Edges sanded R2, faces sanded 120 grit, unfinished.",
    ])
    sh.save(os.path.join(OUT, "F2_parts_and_joinery.png"))


def sheet_nest():
    sh = D.Sheet(W, H, title="FLAT PACK STAND - SHEET NEST", number="F3",
                 rev=REV, scale_note="1:10", subtitle="one 1525 x 1525 mm sheet",
                 material=MAT)
    geo, sheets, ap = X.export_all()
    used = 0.0
    for si, shd in enumerate(sheets):
        sc = 1 / 6.0
        x0, y0 = 30, 120
        sh.ax.add_patch(mp.Rectangle((x0, y0), sc * X.SHEET_W, sc * X.SHEET_H,
                                     fill=False, lw=0.9, ec="#111"))
        for (pid, i, x, y, w, h) in shd:
            pts = geo[pid]["pts"]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ox, oy = min(xs), min(ys)
            pp = [(x0 + sc * (x + u - ox), y0 + sc * (y + v - oy)) for (u, v) in pts]
            sh.ax.add_collection(mc.LineCollection([pp + [pp[0]]], colors="#111",
                                                   linewidths=0.5))
            for (u, v, r) in geo[pid]["holes"]:
                sh.ax.add_patch(mp.Circle((x0 + sc * (x + u - ox), y0 + sc * (y + v - oy)),
                                          sc * r, fill=False, lw=0.4, ec="#111"))
            sh.note(x0 + sc * (x + w / 2), y0 + sc * (y + h / 2), f"{pid}",
                    size=6.0, ha="center")
            used += w * h
    area = len(sheets) * X.SHEET_W * X.SHEET_H
    sh.note(x0 := 30, 105, "SHEET 1525 x 1525 x 18 mm  (5 x 5 ft)  -  grain along X",
            size=6.0, weight="bold")
    sh.dim_h(30, 30 + (1 / 6) * X.SHEET_W, 112, "1525")
    sh.dim_v(120, 120 + (1 / 6) * X.SHEET_H, 22, "1525")
    notes(sh, 320, 300, [
        f"Sheet count: {len(sheets)}",
        f"Parts area: {used/1e6:.3f} m2",
        f"Sheet area: {area/1e6:.3f} m2",
        f"Utilisation: {100*used/area:.0f} %",
        "",
        "Nest rules: 12 mm minimum web between parts, 25 mm margin to",
        "the sheet edge for hold-down, grain along X for every part.",
        "Longest packed part 638 mm (P2 shelf) - inside the sheet with",
        "room to spare, so no part has to be split.",
        "",
        "This nest is a proposal. The fabricator's own nesting may differ;",
        "the individual part DXFs in out/dxf/ are authoritative and must be",
        "used if the shop re-nests. No part file depends on the nest.",
        "",
        "Holding tabs / onion skin: the supplier must say who removes them.",
        "Requirement: NO holding tabs on mating faces (tab ends, slot",
        "walls) and none on the visible faces; if tabs are unavoidable they",
        "must be on the underside and be removed by the shop before",
        "packing. A kit with unremoved tabs is not ready to assemble.",
    ])
    sh.save(os.path.join(OUT, "F3_sheet_nest.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    sheet_ga()
    sheet_parts()
    sheet_nest()


if __name__ == "__main__":
    main()
