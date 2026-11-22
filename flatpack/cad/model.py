"""
FLAT PACK STAND -- part geometry, nesting, exports and checks.

Joinery (all through-cuts, one-face routing):
    shelf  --- 2 tabs per end, each 150 x 18.2, protruding 18 mm past the side panel
            --- vertical dowel hole (8.4) in each tab, 22 mm from the shoulder
    side   --- 3 through-slots 150.2 x 18.2, one per shelf
    lock   --- a 8 mm birch dowel dropped through each tab; it bears on the side
               panel's outer face, so the shelf can neither be pushed in (shoulder)
               nor pulled out (dowel) - and it lifts out for disassembly.

Everything is located:  X by shoulder + dowel,  Y by the slot ends (150.2 vs 150.0),
Z by bearing on the slot's lower face,  rotations by the 18 mm thickness in the slot.
"""

import math
import os
import sys
import cadquery as cq

import params as P

T = P.T
R = 6.0            # internal corner radius (>= cutter radius 3.175)
SLOT_H = P.SLOT_H
SLOT_L = P.SLOT_L
EPS = 0.01


# ---------------------------------------------------------------------------
def rrect(w, h, r=R):
    """Rounded rectangle centred at the origin, as a wire."""
    return (cq.Workplane("XY").moveTo(-w / 2 + r, -h / 2).lineTo(w / 2 - r, -h / 2)
            .radiusArc((w / 2, -h / 2 + r), r).lineTo(w / 2, h / 2 - r)
            .radiusArc((w / 2 - r, h / 2), r).lineTo(-w / 2 + r, h / 2)
            .radiusArc((-w / 2, h / 2 - r), r).lineTo(-w / 2, -h / 2 + r)
            .radiusArc((-w / 2 + r, -h / 2), r).close().wires().val())


def slot_cutter(depth, h_z, l_y, x0, y_c, z_c, r=R):
    """Prism through a side panel in X: h_z tall in Z, l_y long in Y, rounded."""
    sol = cq.Solid.extrudeLinear(rrect(h_z, l_y, r), [], cq.Vector(0, 0, depth))
    sol = sol.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0)   # +Z -> +X
    return sol.translate(cq.Vector(x0, y_c, z_c))


def panel(pts, thickness, z0=0.0, plane="XY"):
    """Extrude a closed polygon (list of (u,v)) by `thickness` from z0."""
    wp = cq.Workplane("XY").polyline(pts).close()
    return wp.extrude(thickness).translate(cq.Vector(0, 0, z0))


# ---------------------------------------------------------------------------
# P1  SIDE PANEL   (x 0..T, y -D/2..+D/2, z 0..H)
# ---------------------------------------------------------------------------
def side_outline():
    """Panel outline in (y, z), with 2 chamfered top corners for a softer look."""
    d, h = P.D_OVER, P.SIDE_H
    c = 22.0
    return [(-d / 2 + c, 0), (d / 2 - c, 0), (d / 2, c), (d / 2, h),
            (-d / 2, h), (-d / 2, c)]


def make_side(sign=1, z_shift=0.0):
    d, h = P.D_OVER, P.SIDE_H
    body = (cq.Workplane("YZ").polyline(side_outline()).close()
            .extrude(T).val())
    # workplane "YZ": local (u,v) -> global (y,z), extrude along the plane normal
    bb = body.BoundingBox()
    body = body.translate(cq.Vector(-bb.xmin, 0, 0))

    # 3 shelf slots (through in X): square slot + 4 dogbone corner reliefs so
    # that the square corners of the shelf tab can pass (a round cutter cannot
    # make a sharp internal corner).
    for z in (P.Z_BASE, P.Z_MID, P.Z_TOP):
        slot = cq.Solid.makeBox(T + 2 * EPS, SLOT_L, SLOT_H,
                                cq.Vector(-EPS, shelf_cy() - SLOT_L / 2, z - T - 0.1))
        body = body.cut(slot)
        for sy in (1, -1):
            for sz in (1, -1):
                dc = cq.Solid.makeCylinder(
                    P.PLY["dogbone"], T + 2 * EPS,
                    cq.Vector(-EPS, shelf_cy() + sy * SLOT_L / 2,
                              z - 0.1 - T + (0 if sz > 0 else 0) + (0 if sz > 0 else T) + (0 if sz > 0 else 0)),
                    cq.Vector(1, 0, 0))
                # centre the dogbone exactly on the slot corner
                dc = cq.Solid.makeCylinder(
                    P.PLY["dogbone"], T + 2 * EPS,
                    cq.Vector(-EPS, shelf_cy() + sy * SLOT_L / 2,
                              (z - T) if sz > 0 else z),
                    cq.Vector(1, 0, 0))
                body = body.cut(dc)
    body = body.translate(cq.Vector((P.W_OVER / 2 - T) if sign > 0 else -P.W_OVER / 2,
                                   0, 0))
    return body.clean()


def slot_cy():
    """Y centre of the shelf tab / side slot."""
    return (P.D_OVER / 2 - P.SHELF_D) / 2.0 + P.SHELF_D / 2.0 - P.D_OVER / 2 + \
        (P.D_OVER / 2 - 3.0 - P.SHELF_D / 2.0)


def shelf_cy():
    """Y centre of the shelf body (3 mm back from the stand front)."""
    return P.D_OVER / 2 - 3.0 - P.SHELF_D / 2.0


# ---------------------------------------------------------------------------
# P2  SHELF  (with 2 tabs per end)
# ---------------------------------------------------------------------------
def shelf_outline():
    L, Dd = P.SHELF_L, P.SHELF_D
    body_half = P.INTERIOR_W / 2.0          # 283
    out = L / 2.0                            # 319
    th = P.TENON_L / 2.0                     # 75
    c = 6.0                                  # 45 deg chamfer on the tab corners
    return [(-body_half, -Dd / 2), (-body_half, -th),
            (-out + c, -th), (-out, -th + c), (-out, th - c), (-out + c, th),
            (-body_half, th), (-body_half, Dd / 2), (body_half, Dd / 2),
            (body_half, th), (out - c, th), (out, th - c), (out, -th + c),
            (out - c, -th), (body_half, -th), (body_half, -Dd / 2)]


def make_shelf(z_top, foot_holes=False, sign=0):
    """Shelf whose top surface is at z_top."""
    body = (cq.Workplane("XY").polyline(shelf_outline()).close().extrude(T).val()
            .translate(cq.Vector(0, shelf_cy(), z_top - T)))
    # dowel holes in the tab ends
    for sx in (1, -1):
        x = sx * (P.INTERIOR_W / 2 + P.DOWEL["x_from_shoulder"])
        body = body.cut(cq.Solid.makeCylinder(
            P.DOWEL_HOLE / 2, T + 2, cq.Vector(x, shelf_cy(), z_top - T - 1),
            cq.Vector(0, 0, 1)))
    if foot_holes:
        for sx in (1, -1):
            for sy in (1, -1):
                body = body.cut(cq.Solid.makeCylinder(
                    P.FOOT["clearance"] / 2, T + 2,
                    cq.Vector(sx * P.FOOT["x"], shelf_cy() + sy * P.FOOT["y"],
                              z_top - T - 1), cq.Vector(0, 0, 1)))
    return body.clean()


# ---------------------------------------------------------------------------
# P3  WALL STRAP (anti-tip, cut from the same sheet)
# ---------------------------------------------------------------------------
def make_strap():
    w, l, h = 70.0, 180.0, 55.0
    body = (cq.Workplane("XY").moveTo(-w / 2, 0).lineTo(w / 2, 0)
            .lineTo(w / 2, h).lineTo(-w / 2, h).close().extrude(T).val())
    for i, z in enumerate((25.0, h - 25.0)):
        body = body.cut(cq.Solid.makeCylinder(3.5, T + 2,
                                              cq.Vector(0, 0, z - 1),
                                              cq.Vector(0, 0, 1)))
    return body.clean()


# ---------------------------------------------------------------------------
# equipment reference envelopes
# ---------------------------------------------------------------------------
def make_tt():
    return cq.Solid.makeBox(P.TT["W"], P.TT["D"], P.TT["H"],
                            cq.Vector(-P.TT["W"] / 2, -P.TT["D"] / 2, P.Z_TOP))


def make_speaker(sign=1):
    W, H, Dd = P.SPK["W"], P.SPK["H"], P.SPK["D"]
    y0 = P.D_OVER / 2 - 7.0 - Dd          # front face 7 mm behind the shelf front
    z0 = P.Z_MID + P.PAD["h"]
    wire = cq.Workplane("YZ").polyline(
        [(y0, z0), (y0 + Dd, z0), (y0, z0 + H)]).close().wires().val()
    sol = cq.Solid.extrudeLinear(wire, [], cq.Vector(W, 0, 0))
    return sol.translate(cq.Vector(sign * P.SPK_X - W / 2, 0, 0))


def make_pads(sign=1):
    Dd, W = P.SPK["D"], P.SPK["W"]
    yc = P.D_OVER / 2 - 7.0 - Dd / 2
    sol = None
    for sx in (1, -1):
        for sy in (1, -1):
            c = cq.Solid.makeCylinder(
                P.PAD["dia"] / 2, P.PAD["h"],
                cq.Vector(sign * P.SPK_X + sx * (W / 2 - P.PAD["inset"]),
                          yc + sy * (Dd / 2 - P.PAD["inset"]), P.Z_MID),
                cq.Vector(0, 0, 1))
            sol = c if sol is None else sol.fuse(c)
    return sol


def make_crate():
    y_rear = P.D_OVER / 2 - 3.0 - P.SHELF_D + 2.0
    return cq.Solid.makeBox(P.CRATE["W"], P.CRATE["D"], P.CRATE["H"],
                            cq.Vector(-P.CRATE["W"] / 2, y_rear, P.Z_BASE))


def make_dowel(sign, z_top):
    x = sign * (P.INTERIOR_W / 2 + P.DOWEL["x_from_shoulder"])
    return cq.Solid.makeCylinder(P.DOWEL["d"] / 2, P.DOWEL["l"],
                                 cq.Vector(x, shelf_cy(), z_top - T - 11.0),
                                 cq.Vector(0, 0, 1))


# ---------------------------------------------------------------------------
def build():
    parts = {}
    parts["P1"] = dict(name="SIDE PANEL", qty=2, sheet=True,
                       solids=[make_side(1), make_side(-1)])
    clean = make_shelf(P.Z_TOP)
    parts["P2"] = dict(name="SHELF", qty=2, sheet=True,
                       solids=[make_shelf(P.Z_TOP), make_shelf(P.Z_MID)])
    parts["P3"] = dict(name="BASE SHELF", qty=1, sheet=True,
                       solids=[make_shelf(P.Z_BASE, foot_holes=True)])
    parts["P4"] = dict(name="WALL STRAP", qty=1, sheet=True, solids=[make_strap()])
    return parts


def assembly(parts, equipment=True):
    a = cq.Assembly(name="FLATPACK-W0.9")
    cols = {"P1": cq.Color(0.85, 0.72, 0.50), "P2": cq.Color(0.80, 0.66, 0.44),
            "P3": cq.Color(0.78, 0.64, 0.42), "P4": cq.Color(0.75, 0.62, 0.40)}
    for pid, p in parts.items():
        for i, s in enumerate(p["solids"]):
            a.add(s, name=f"{pid}_{i+1}", color=cols[pid])
    for z in (P.Z_BASE, P.Z_MID, P.Z_TOP):
        pass
    for sign in (1, -1):
        for z in (P.Z_BASE, P.Z_MID, P.Z_TOP):
            a.add(make_dowel(sign, z), name=f"dowel_{sign}_{z:.0f}",
                  color=cq.Color(0.65, 0.50, 0.30))
    if equipment:
        a.add(make_tt(), name="TT", color=cq.Color(0.35, 0.35, 0.37))
        for s in (1, -1):
            a.add(make_speaker(s), name=f"SPK{s}", color=cq.Color(0.25, 0.25, 0.27))
            a.add(make_pads(s), name=f"PAD{s}", color=cq.Color(0.95, 0.6, 0.1))
        a.add(make_crate(), name="CRATE", color=cq.Color(0.75, 0.62, 0.45))
    return a


if __name__ == "__main__":
    for pid, p in build().items():
        for i, s in enumerate(p["solids"]):
            bb = s.BoundingBox()
            print(f"{pid} {p['name']:12s} #{i+1} valid={s.isValid()} "
                  f"vol={s.Volume():10.0f} bbox="
                  f"{bb.xlen:7.1f}{bb.ylen:7.1f}{bb.zlen:7.1f}")
