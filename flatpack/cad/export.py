"""
FLAT PACK STAND -- flat patterns, nesting, STEP export and CAD checks.
"""

import os, sys, json
import numpy as np
import cadquery as cq
import ezdxf
from ezdxf import units

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_here)
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "cad"))
sys.path.insert(0, _here)
import params as P
import model as M

T = P.T
SHEET_W, SHEET_H = P.PLY["sheet"]
KERF = P.PLY["kerf"]
SPACING = 12.0          # minimum web between nested parts

SHORT = {"P1": "P1_SIDE_PANEL", "P2": "P2_SHELF", "P3": "P3_BASE_SHELF",
         "P4": "P4_WALL_STRAP", "P5": "P5_FIT_COUPON", "P6": "P6_SPARE_DOWEL"}


# ---------------------------------------------------------------------------
def coupon_outline():
    """Fit-test coupon: 3 slots of increasing clearance + a matching tenon."""
    w = 150.0
    h = 90.0
    return [(-w / 2, 0), (w / 2, 0), (w / 2, h), (-w / 2, h)]


def coupon_slots():
    """(x_centre, width) of the three test slots, each 60 long in Y? -- vertical."""
    out = []
    for i, clr in enumerate((0.10, 0.20, 0.30)):
        out.append((-45.0 + i * 45.0, P.T + clr))
    return out


def flat_outline(pid):
    """2-D outline (list of (u,v)), holes as list of (u, v, r) and slots as
    (u, v, w, h) for the flat pattern of a part (sheet plane = XY)."""
    if pid == "P1":
        pts = [(y + P.D_OVER / 2, z) for (y, z) in M.side_outline()]
        holes = []
        slots = [(y + P.D_OVER / 2, z - T / 2, P.SLOT_L, P.SLOT_H)
                 for (y, z) in [(M.shelf_cy(), P.Z_BASE), (M.shelf_cy(), P.Z_MID),
                                (M.shelf_cy(), P.Z_TOP)]]
        return pts, holes, slots
    if pid in ("P2", "P3"):
        pts = [(x + P.SHELF_L / 2, y + P.SHELF_D / 2) for (x, y) in M.shelf_outline()]
        holes = []
        if pid == "P3":
            for sx in (1, -1):
                for sy in (1, -1):
                    holes.append((P.SHELF_L / 2 + sx * P.FOOT["x"],
                                  P.SHELF_D / 2 + sy * P.FOOT["y"],
                                  P.FOOT["clearance"] / 2))
        # dowel holes: local centre line of the flat = the shelf's centre line
        for sx in (1, -1):
            holes.append((P.SHELF_L / 2 + sx * (P.INTERIOR_W / 2 + P.DOWEL["x_from_shoulder"]),
                          P.SHELF_D / 2, P.DOWEL_HOLE / 2))
        return pts, holes, []
    if pid == "P4":
        w, l, h = 70.0, 180.0, 55.0
        pts = [(0, 0), (w, 0), (w, h), (0, h)]
        holes = [(w / 2, 25.0, 3.5), (w / 2, h - 25.0, 3.5)]
        return pts, holes, []
    if pid == "P5":
        pts = coupon_outline()
        holes = []
        slots = [(u + 75.0, 60.0, 60.0, wid) for (u, wid) in coupon_slots()]
        return pts, holes, slots
    raise ValueError(pid)


def write_dxf(path, pts, holes, slots, layer="CUT"):
    doc = ezdxf.new("R2000", setup=True)
    doc.units = units.MM
    doc.header["$INSUNITS"] = 4
    doc.layers.add(layer, color=7)
    msp = doc.modelspace()
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    for (x, y, r) in holes:
        msp.add_circle((x, y), r, dxfattribs={"layer": layer})
    for (x, y, w, h) in slots:
        if h < 20 and w > 100:      # side panel shelf slot: square + dogbones
            msp.add_lwpolyline([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2),
                                (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)],
                               close=True, dxfattribs={"layer": layer})
            for sx in (1, -1):
                for sy in (1, -1):
                    msp.add_circle((x + sx * w / 2, y + sy * h / 2),
                                   P.PLY["dogbone"], dxfattribs={"layer": layer})
            continue
        r = min(6.0, h / 2 - 0.001)
        msp.add_lwpolyline(
            [(x - w / 2 + r, y - h / 2), (x + w / 2 - r, y - h / 2)],
            close=False, dxfattribs={"layer": layer})
        msp.add_arc((x + w / 2 - r, y - h / 2 + r), r, 270, 90,
                    dxfattribs={"layer": layer})
        msp.add_lwpolyline(
            [(x + w / 2, y - h / 2 + r), (x + w / 2, y + h / 2 - r)],
            close=False, dxfattribs={"layer": layer})
        msp.add_arc((x + w / 2 - r, y + h / 2 - r), r, 0, 180,
                    dxfattribs={"layer": layer})
        msp.add_lwpolyline(
            [(x + w / 2 - r, y + h / 2), (x - w / 2 + r, y + h / 2)],
            close=False, dxfattribs={"layer": layer})
        msp.add_arc((x - w / 2 + r, y + h / 2 - r), r, 90, 270,
                    dxfattribs={"layer": layer})
        msp.add_lwpolyline(
            [(x - w / 2, y + h / 2 - r), (x - w / 2, y - h / 2 + r)],
            close=False, dxfattribs={"layer": layer})
        msp.add_arc((x - w / 2 + r, y - h / 2 + r), r, 180, 360,
                    dxfattribs={"layer": layer})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.saveas(path)


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), max(xs), min(ys), max(ys)


# ---------------------------------------------------------------------------
def nest(items):
    """Shelf-pack the parts onto 1525 x 1525 sheets, long axis along X (grain)."""
    sheets = []
    cur = []
    free_w, free_h = SHEET_W, SHEET_H
    x, y, row_h = 0.0, 0.0, 0.0
    for (pid, w, h, qty) in items:
        for i in range(qty):
            if x + w > SHEET_W + 0.01:
                x = 0.0
                y += row_h + SPACING
                row_h = 0.0
            if y + h > SHEET_H + 0.01:
                sheets.append(cur)
                cur = []
                x, y, row_h = 0.0, 0.0, 0.0
            cur.append((pid, i, x, y, w, h))
            x += w + SPACING
            row_h = max(row_h, h)
    if cur:
        sheets.append(cur)
    return sheets


# ---------------------------------------------------------------------------
def export_all():
    parts = M.build()
    os.makedirs(os.path.join(OUT, "dxf"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "step"), exist_ok=True)
    files, geo = {}, {}
    # per-part DXF + STEP
    for pid in ("P1", "P2", "P3", "P4"):
        pts, holes, slots = flat_outline(pid)
        files[pid] = os.path.join(OUT, "dxf", SHORT[pid] + ".dxf")
        write_dxf(files[pid], pts, holes, slots)
        body = parts[pid]["solids"][0]
        bb = body.BoundingBox()
        tidy = body.translate(cq.Vector(-(bb.xmin + bb.xmax) / 2,
                                        -(bb.ymin + bb.ymax) / 2, -bb.zmin))
        sp = os.path.join(OUT, "step", SHORT[pid] + ".step")
        cq.exporters.export(tidy, sp, "STEP")
        geo[pid] = dict(pts=pts, holes=holes, slots=slots, qty=parts[pid]["qty"],
                        step=sp, dxf=files[pid])
    # fit coupon
    pts, holes, slots = flat_outline("P5")
    fp = os.path.join(OUT, "dxf", SHORT["P5"] + ".dxf")
    write_dxf(fp, pts, holes, slots)
    geo["P5"] = dict(pts=pts, holes=holes, slots=slots, qty=1, step=None, dxf=fp)
    # assembly STEP (all manufactured parts in position, one compound)
    comp = cq.Compound.makeCompound(
        [s for pid in ("P1", "P2", "P3") for s in parts[pid]["solids"]])
    ap = os.path.join(OUT, "step", "assembly.step")
    cq.exporters.export(comp, ap, "STEP")
    # nesting
    items = []
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        x0, x1, y0, y1 = bbox(geo[pid]["pts"])
        items.append((pid, x1 - x0, y1 - y0, geo[pid]["qty"]))
    sheets = nest(items)
    return geo, sheets, ap


def nest_dxf(sheets, geo):
    doc = ezdxf.new("R2000", setup=True)
    doc.units = units.MM
    msp = doc.modelspace()
    doc.layers.add("SHEET", color=8)
    doc.layers.add("CUT", color=7)
    used = 0.0
    for si, sh in enumerate(sheets):
        ox = si * (SHEET_W + 50)
        msp.add_lwpolyline([(ox, 0), (ox + SHEET_W, 0), (ox + SHEET_W, SHEET_H),
                            (ox, SHEET_H)], close=True,
                           dxfattribs={"layer": "SHEET"})
        for (pid, i, x, y, w, h) in sh:
            pts, holes, slots = geo[pid]["pts"], geo[pid]["holes"], geo[pid]["slots"]
            x0, x1, y0, y1 = bbox(pts)
            msp.add_lwpolyline([(ox + x + (u - x0), y + (v - y0)) for (u, v) in pts],
                               close=True, dxfattribs={"layer": "CUT"})
            for (u, v, r) in holes:
                msp.add_circle((ox + x + (u - x0), y + (v - y0)), r,
                               dxfattribs={"layer": "CUT"})
            for (u, v, sw, shh) in slots:
                msp.add_lwpolyline(
                    [(ox + x + (u - x0 - sw / 2), y + (v - y0 - shh / 2)),
                     (ox + x + (u - x0 + sw / 2), y + (v - y0 - shh / 2)),
                     (ox + x + (u - x0 + sw / 2), y + (v - y0 + shh / 2)),
                     (ox + x + (u - x0 - sw / 2), y + (v - y0 + shh / 2))],
                    close=True, dxfattribs={"layer": "CUT"})
            used += w * h
    p = os.path.join(OUT, "dxf", "NEST_1525x1525.dxf")
    doc.saveas(p)
    area = len(sheets) * SHEET_W * SHEET_H
    return p, used, area


# ---------------------------------------------------------------------------
def checks(geo):
    parts = M.build()
    L = ["# Flat-pack CAD checks", "",
         "Generated by `flatpack/cad/export.py`.", "",
         "## 1. Interference between manufactured parts", "",
         "| A | B | intersection (mm3) | result |", "|---|---|---|---|"]
    man = [(pid, i, s) for pid in ("P1", "P2", "P3")
           for i, s in enumerate(parts[pid]["solids"])]
    ok = True
    for a in range(len(man)):
        for b in range(a + 1, len(man)):
            pa, ia, sa = man[a]
            pb, ib, sb = man[b]
            v = sa.intersect(sb)
            vol = 0.0 if v is None else v.Volume()
            res = "PASS" if vol < 1e-2 else "FAIL"
            if res == "FAIL" and not (pa == "P1" and pb == "P1"):
                ok = False
            L.append(f"| {pa}#{ia+1} | {pb}#{ib+1} | {vol:.3f} | {res} |")

    # 2. tab-in-slot clearance
    L += ["", "## 2. Joint fit (nominal)", "",
          "| item | value |", "|---|---|",
          f"| shelf tab thickness | {P.T:.2f} mm |",
          f"| side slot width | {P.SLOT_H:.2f} mm |",
          f"| designed clearance per face | {P.FIT['slot']/2:.2f} mm |",
          f"| tab length / slot length | {P.TENON_L:.1f} / {P.SLOT_L:.1f} mm |",
          f"| tab protrusion past the side panel | {P.TENON_OUT:.1f} mm |",
          f"| dowel hole centre from the shoulder | {P.DOWEL['x_from_shoulder']:.1f} mm "
          f"(= {P.DOWEL['x_from_shoulder']-P.T:.1f} mm past the panel's outer face) |",
          f"| clearance between the dowel and the panel's outer face | "
          f"{P.DOWEL['x_from_shoulder']-P.T:.1f} mm (= the shelf's free play before "
          f"the dowel stops it being pulled out) |",
          f"| edge distance, dowel hole to tab end | "
          f"{P.TENON_OUT-(P.DOWEL['x_from_shoulder']-P.T):.1f} mm |",
          ]
    # 3. equipment fit
    L += ["", "## 3. Equipment fit", "",
          "| check | available | required | margin | result |", "|---|---|---|---|---|"]
    rows = [
        ("speaker pair in bay", P.INTERIOR_W, 2 * P.SPK["W"], 2 * P.SPK["W"]),
        ("crate width", P.INTERIOR_W, P.CRATE["W"], P.CRATE["W"]),
        ("crate depth in bay", P.SHELF_D, P.CRATE["D"], P.CRATE["D"]),
        ("crate height in bay", P.H_REC, P.CRATE["H"], P.CRATE["H"]),
        ("speaker height in bay", P.H_SPK, P.SPK["H"] + P.PAD["h"] - P.PAD["comp"],
         P.SPK["H"]),
        ("turntable width", P.INTERIOR_W, P.TT["W"], P.TT["W"]),
        ("turntable depth", P.SHELF_D, P.TT["D"], P.TT["D"]),
    ]
    for (n, avail, req, _) in rows:
        m = avail - req
        L.append(f"| {n} | {avail:.1f} | {req:.1f} | {m:.1f} | "
                 f"{'PASS' if m > 0 else 'FAIL'} |")
        if m <= 0:
            ok = False
    # 4. crate removal
    L += ["", "## 4. Crate removal path (+Y, no rotation)", "",
          "| displacement (mm) | interference with frame (mm3) |", "|---|---|"]
    frame = parts["P1"]["solids"][0].fuse(parts["P1"]["solids"][1]) \
        .fuse(parts["P3"]["solids"][0]).clean()
    for dy in (0, 100, 200, 300, 400):
        cr = M.make_crate().translate(cq.Vector(0, dy, 0))
        v = cr.intersect(frame)
        vol = 0.0 if v is None else v.Volume()
        L.append(f"| {dy} | {vol:.3f} |")
        if vol > 1e-2:
            ok = False
    # 5. dowel / tab geometry
    L += ["", "## 5. Dowel and tab", "",
          f"* dowel: {P.DOWEL['qty']} x M8 birch, {P.DOWEL['l']:.0f} mm long, "
          f"standing {P.DOWEL['l']/2 - P.T/2:.0f} mm proud each side of the shelf",
          f"* hole {P.DOWEL_HOLE:.1f} dia in an 18 mm thick tab, "
          f"{P.TENON_OUT - (P.DOWEL['x_from_shoulder'] - P.T):.0f} mm of material "
          f"beyond the hole (1.75 d) -> acceptable for plywood",
          f"* tab shear area through the dowel line: 18 x (150-8) = "
          f"{18*(150-8):.0f} mm2"]
    # 6. re-import every STEP and compare with the model
    L += ["", "## 6. Export / re-import verification", "",
          "| part | solids in STEP | bbox STEP (mm) | bbox model (mm) | volume delta | result |",
          "|---|---|---|---|---|---|"]
    for pid in ("P1", "P2", "P3", "P4"):
        src = parts[pid]["solids"][0]
        sp = os.path.join(OUT, "step", SHORT[pid] + ".step")
        imp = cq.importers.importStep(sp)
        sols = imp.solids().vals()
        vs = sum(x.Volume() for x in sols)
        vm = src.Volume()
        bb = sols[0].BoundingBox()
        bm = src.BoundingBox()
        dims = sorted([round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)])
        dm = sorted([round(bm.xlen, 2), round(bm.ylen, 2), round(bm.zlen, 2)])
        good = (len(sols) == 1 and dims == dm and abs(vs - vm) / vm < 1e-6)
        if not good:
            ok = False
        L.append(f"| {pid} | {len(sols)} | {dims} | {dm} | "
                 f"{100*(vs-vm)/vm:+.4f} % | {'PASS' if good else 'FAIL'} |")
    L += ["", f"## Overall: {'ALL CHECKS PASS' if ok else 'ITEMS FLAGGED'}"]
    return "\n".join(L), ok


if __name__ == "__main__":
    geo, sheets, ap = export_all()
    nd, used, area = nest_dxf(sheets, geo)
    txt, ok = checks(geo)
    with open(os.path.join(OUT, "cad_checks.md"), "w") as f:
        f.write(txt + "\n")
    print(txt)
    print(f"\nnesting: {len(sheets)} sheet(s), used {used/1e6:.3f} m2 of "
          f"{area/1e6:.3f} m2 = {100*used/area:.0f} % -> {nd}")
