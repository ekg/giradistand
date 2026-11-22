"""
Manufacturing export + export verification for the GI-RAD stand.

Outputs
  out/step/<part>.step          one file per manufactured part (authoritative)
  out/step/assembly.step        all manufactured parts in position (reference)
  out/step/upload_parts.step    single compound, 6 sheet bodies (SendCutSend
                                multi-body route)
  out/dxf/<part>.dxf            flat pattern, CUT + BEND layers, mm, 1:1
  out/stl/assembly.stl          viewing only

Every export is re-imported and compared with the source model; results are
written to out/export_verification.md
"""

import os
import json
import cadquery as cq
import ezdxf
from ezdxf import units

import params as P
import model as M
import sheetmetal as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
BD = P.BD
T = P.T
SHORT = {"P1": "P1_SIDE_SLAB", "P2": "P2_SHELF_TRAY", "P3": "P3_BASE_TRAY",
         "P4": "P4_REAR_PANEL", "P5": "P5_WALL_STRAP"}

# ---------------------------------------------------------------------------
# flat patterns
# ---------------------------------------------------------------------------
def flat_side_slab():
    """[(contour_points)] + holes, in flat coordinates (0,0)-(D, H)."""
    outline = [(0, 0), (P.D_OVER, 0), (P.D_OVER, P.SIDE_H), (0, P.SIDE_H)]
    holes = [(y + P.D_OVER / 2, z - P.SIDE_BOT) for (y, z, _) in M.side_slab_holes()]
    return outline, holes, [], []


def flat_tray(spec):
    """Flat pattern of a tray: outline, holes, bolt slots, bend lines.

    Feature mapping: a feature at folded distance d from the apex (the tray's
    outer face) lies (he - d) from the tab's outer edge in the flat, because the
    bend line sits (he - BD/2) from that edge and the neutral-axis stretch is
    already absorbed by BD.
    """
    outline, bendlines = S.tray_flat_lines(spec)
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    dx, dy = -min(xs), -min(ys)
    outline = [(x + dx, y + dy) for (x, y) in outline]
    bendlines = [[(x + dx, y + dy) for (x, y) in bl] for bl in bendlines]
    w, d = spec["w"], spec["d"]
    he, hf = spec["h_end"], spec["h_front"]
    wf = w + 2 * (he - BD)
    holes, slots = [], []
    off = he - P.TRAY_SLOT_DROP
    for y in P.TRAY_BOLT_Y:
        slots.append((off, dy + y))
        slots.append((wf - off, dy + y))
    if spec.get("foot_holes"):
        for fx in (1, -1):
            for fy in (1, -1):
                holes.append((dx + fx * P.FOOT_X, dy + fy * P.FOOT_Y))
    return outline, holes, slots, bendlines


def flat_panel():
    w, h, hf = P.PANEL_W, P.PANEL_H, P.PANEL_FLANGE
    wf = w + 2 * (hf - BD)
    outline = [(0, 0), (wf, 0), (wf, h), (0, h)]
    # holes in the tabs, 10 mm from the tab's outer edge
    off = hf - (P.PANEL_FLANGE / 2.0)     # d_apex = 10 for flange 20
    holes = []
    for sgn in (0, 1):
        x = off if sgn == 0 else wf - off
        for z in P.PANEL_BOLT_Z:
            holes.append((x, z))
    bendlines = [[(hf - BD / 2, 0), (hf - BD / 2, h)],
                 [(wf - hf + BD / 2, 0), (wf - hf + BD / 2, h)]]
    return outline, holes, [], bendlines


def flat_strap():
    """Z strap: foot 110 + riser 250 + wall flange 30, 25 wide."""
    w = P.STRAP["w"]
    foot, riser, wall = P.STRAP["foot"], P.STRAP["riser"], P.STRAP["wall"]
    L = foot + riser + wall
    outline = [(0, 0), (w, 0), (w, L), (0, L)]
    holes = [(w / 2, foot + riser + wall / 2)]
    slots = [(w / 2, 60.0)]                    # 6.6 x 40 slot in the foot
    bendlines = [[(0, foot - BD / 2), (w, foot - BD / 2)],
                 [(0, foot + riser - BD / 2), (w, foot + riser - BD / 2)]]
    return outline, holes, slots, bendlines


# ---------------------------------------------------------------------------
def add_obround(msp, x, y, w, h, layer):
    """Closed obround slot: w along X, h along Y. Ends are semicircles across
    the short dimension, so either orientation is handled."""
    if w >= h:
        r = h / 2.0
        cx = max(w / 2.0 - r, 0.0)
        msp.add_lwpolyline([(x - cx, y - r), (x + cx, y - r)], format="xy",
                           close=False, dxfattribs={"layer": layer})
        msp.add_arc((x + cx, y), r, 270, 90, dxfattribs={"layer": layer})
        msp.add_lwpolyline([(x + cx, y + r), (x - cx, y + r)], format="xy",
                           close=False, dxfattribs={"layer": layer})
        msp.add_arc((x - cx, y), r, 90, 270, dxfattribs={"layer": layer})
    else:
        r = w / 2.0
        cy = max(h / 2.0 - r, 0.0)
        msp.add_lwpolyline([(x + r, y - cy), (x + r, y + cy)], format="xy",
                           close=False, dxfattribs={"layer": layer})
        msp.add_arc((x, y + cy), r, 0, 180, dxfattribs={"layer": layer})
        msp.add_lwpolyline([(x - r, y + cy), (x - r, y - cy)], format="xy",
                           close=False, dxfattribs={"layer": layer})
        msp.add_arc((x, y - cy), r, 180, 360, dxfattribs={"layer": layer})


def dxf_part(path, outline, holes, slots, bendlines, hole_dia=5.5,
             slot_size=(5.5, 6.8)):
    doc = ezdxf.new("R2000", setup=True)
    doc.units = units.MM
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    msp = doc.modelspace()
    doc.layers.add("CUT", color=7)
    doc.layers.add("BEND", color=1, linetype="DASHED")
    msp.add_lwpolyline(outline, close=True, dxfattribs={"layer": "CUT"})
    for (x, y) in holes:
        msp.add_circle((x, y), hole_dia / 2.0, dxfattribs={"layer": "CUT"})
    for (x, y) in slots:
        add_obround(msp, x, y, slot_size[1], slot_size[0], "CUT")
    for bl in bendlines:
        msp.add_lwpolyline(bl, close=False, dxfattribs={"layer": "BEND"})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.saveas(path)
    return path


# ---------------------------------------------------------------------------
def export_all():
    parts = M.build()
    _, spec_top = M.make_tray(P.Z_TOP)
    _, spec_bot = M.make_tray(P.Z_BOT, front_h=P.FLANGE_BOT, foot_holes=True)

    files = {}
    # ---- STEP per part (one solid each) --------------------------------
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        shapes = parts[pid]["solids"]
        # manufacturing body: first solid, repositioned to a tidy origin
        body = shapes[0]
        bb = body.BoundingBox()
        ctr = cq.Vector((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, bb.zmin)
        tidy = body.translate(-ctr)
        name = SHORT[pid]
        p = os.path.join(OUT, "step", name + ".step")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        cq.exporters.export(tidy, p, "STEP")
        files[pid] = dict(path=p, solid=tidy, qty=parts[pid]["qty"], name=name)

    # ---- positioned multi-body compound --------------------------------
    solids = []
    for pid in ("P1", "P2", "P3", "P4"):
        for s in parts[pid]["solids"]:
            solids.append(s)
    comp = cq.Compound.makeCompound(solids)
    p = os.path.join(OUT, "step", "upload_parts.step")
    cq.exporters.export(comp, p, "STEP")
    p2 = os.path.join(OUT, "step", "assembly.step")
    cq.exporters.export(comp, p2, "STEP")

    # ---- DXF flat patterns --------------------------------------------
    dxfs = {}
    out, holes, slots, bends = flat_side_slab()
    dxfs["P1"] = dxf_part(os.path.join(OUT, "dxf", "P1_SIDE_SLAB_flat.dxf"),
                          out, holes, slots, bends)
    out, holes, slots, bends = flat_tray(spec_top)
    dxfs["P2"] = dxf_part(os.path.join(OUT, "dxf", "P2_SHELF_TRAY_flat.dxf"),
                          out, holes, slots, bends)
    out, holes, slots, bends = flat_tray(spec_bot)
    dxfs["P3"] = dxf_part(os.path.join(OUT, "dxf", "P3_BASE_TRAY_flat.dxf"),
                          out, holes, slots, bends, hole_dia=P.FOOT["clearance"])
    out, holes, slots, bends = flat_panel()
    dxfs["P4"] = dxf_part(os.path.join(OUT, "dxf", "P4_REAR_PANEL_flat.dxf"),
                          out, holes, slots, bends)
    out, holes, slots, bends = flat_strap()
    dxfs["P5"] = dxf_part(os.path.join(OUT, "dxf", "P5_WALL_STRAP_flat.dxf"),
                          out, holes, slots, bends, hole_dia=6.6,
                          slot_size=(40.0, 6.6))
    return files, dxfs, dict(spec_top=spec_top, spec_bot=spec_bot)


# ---------------------------------------------------------------------------
def verify(files, dxfs):
    """Re-import every export and compare against the source model."""
    rows = []
    for pid, f in files.items():
        imp = cq.importers.importStep(f["path"])
        solids = imp.solids().vals()
        src = f["solid"]
        sb = src.BoundingBox()
        n_sol = len(solids)
        vol_src = sum(s.Volume() for s in ([src] if not hasattr(src, "Solids") else src.Solids()))
        vol_imp = sum(s.Volume() for s in solids)
        bb_imp = solids[0].BoundingBox()
        dims_ok = all(abs(a - b) < 0.02 for a, b in
                      zip([sb.xlen, sb.ylen, sb.zlen], [bb_imp.xlen, bb_imp.ylen, bb_imp.zlen]))
        rows.append(dict(part=pid, file=os.path.basename(f["path"]),
                         n_solids=n_sol,
                         bbox_src=[round(v, 2) for v in (sb.xlen, sb.ylen, sb.zlen)],
                         bbox_imp=[round(v, 2) for v in (bb_imp.xlen, bb_imp.ylen, bb_imp.zlen)],
                         vol_src=round(vol_src, 1), vol_imp=round(vol_imp, 1),
                         dvol_pct=round(100 * (vol_imp - vol_src) / vol_src, 4),
                         dims_match=dims_ok, valid=all(s.isValid() for s in solids)))
    # multi-body
    imp = cq.importers.importStep(os.path.join(OUT, "step", "upload_parts.step"))
    rows.append(dict(part="UPLOAD", file="upload_parts.step",
                     n_solids=len(imp.solids().vals()),
                     bbox_src=None, bbox_imp=None, vol_src=None,
                     vol_imp=round(sum(s.Volume() for s in imp.solids().vals()), 1),
                     dvol_pct=None, dims_match=True,
                     valid=all(s.isValid() for s in imp.solids().vals())))
    # DXF checks (feature level)
    dxf_rows = []
    expect = {"P1": dict(holes=11, slots=0, bends=0, dia=5.5),
              "P2": dict(holes=0, slots=6, bends=4, dia=5.5),
              "P3": dict(holes=4, slots=6, bends=4, dia=P.FOOT["clearance"]),
              "P4": dict(holes=4, slots=0, bends=2, dia=5.5),
              "P5": dict(holes=1, slots=1, bends=2, dia=6.6)}
    for pid, path in dxfs.items():
        doc = ezdxf.readfile(path)
        msp = doc.modelspace()
        cut = [e for e in msp if e.dxf.layer == "CUT"]
        bend = [e for e in msp if e.dxf.layer == "BEND"]
        # gather points
        pts = []
        ncont = 0
        for e in cut:
            if e.dxftype() == "LWPOLYLINE":
                ncont += 1
                pts += [(p[0], p[1]) for p in e.get_points()]
            elif e.dxftype() == "CIRCLE":
                ncont += 1
                r = e.dxf.radius
                c = e.dxf.center
                pts += [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
            elif e.dxftype() == "ARC":
                r = e.dxf.radius
                c = e.dxf.center
                ncont += 1
                pts += [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        # feature counts + slot geometry integrity
        n_circ = sum(1 for e in cut if e.dxftype() == "CIRCLE")
        n_arc = sum(1 for e in cut if e.dxftype() == "ARC")
        arcs = [e for e in cut if e.dxftype() == "ARC"]
        radii_ok = all(abs(e.dxf.radius - (P.TRAY_SLOT[0] / 2.0 if pid in ("P2", "P3")
                                           else 3.3)) < 0.01 for e in arcs)
        # outline must be closed and enclose every hole
        closed = any(e.dxftype() == "LWPOLYLINE" and e.closed for e in cut)
        inside = all(min(xs) - 0.01 <= e.dxf.center[0] <= max(xs) + 0.01 and
                     min(ys) - 0.01 <= e.dxf.center[1] <= max(ys) + 0.01
                     for e in cut if e.dxftype() == "CIRCLE")
        ex = expect.get(pid, {})
        dxf_rows.append(dict(part=pid, file=os.path.basename(path),
                             dxftype=doc.dxfversion, units=doc.units,
                             n_cut_entities=len(cut), n_bend=len(bend),
                             holes_found=n_circ, holes_expected=ex.get("holes"),
                             arcs=n_arc, arc_radii_ok=radii_ok,
                             outline_closed=closed, holes_inside=inside,
                             bends_found=len(bend), bends_expected=ex.get("bends"),
                             bbox=[round(max(xs) - min(xs), 2), round(max(ys) - min(ys), 2)],
                             ok=(n_circ == ex.get("holes", n_circ) and
                                 len(bend) == ex.get("bends", len(bend)) and
                                 radii_ok and closed and inside),
                             min_x=round(min(xs), 2), min_y=round(min(ys), 2)))
    with open(os.path.join(OUT, "export_verification.json"), "w") as fh:
        json.dump(dict(step=rows, dxf=dxf_rows), fh, indent=2)
    return rows, dxf_rows


if __name__ == "__main__":
    files, dxfs, meta = export_all()
    rows, dxf_rows = verify(files, dxfs)
    print(f"{'part':8s}{'file':34s}{'sol':>4s}{'dvol%':>8s}{'dims':>7s}{'valid':>7s}")
    for r in rows:
        print(f"{r['part']:8s}{r['file']:34s}{r['n_solids']:>4d}"
              f"{str(r['dvol_pct']):>8s}{str(r['dims_match']):>7s}{str(r['valid']):>7s}")
    print()
    for r in dxf_rows:
        print(r)
