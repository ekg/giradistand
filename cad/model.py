"""
GI-RAD STAND -- part construction and assembly.

Parts (sheet metal, all from 1.88 mm mild steel):
  P1  SIDE SLAB      qty 2   flat part, no bends
  P2  SHELF TRAY     qty 2   top + middle shelf, 4 flanges
  P3  BASE TRAY      qty 1   bottom level, 4 flanges + foot holes
  P4  REAR PANEL     qty 1   C-channel, racking diaphragm in the record bay
  P5  WALL STRAP     qty 1   optional discreet anti-tip strap (flat)

Folded solids are the authoritative geometry for the fabricator (SendCutSend
accepts STEP for bent parts and unfolds with its own tooling); flat solids are
generated from the same parameters for DXF flat patterns and area/weight checks.
"""

import math
import cadquery as cq

import params as P
import sheetmetal as S

T = P.T
BD = P.BD

# ---------------------------------------------------------------------------
# flat parts
# ---------------------------------------------------------------------------
def side_slab_holes():
    """[(y, z, x_inboard_face)] bolt positions on a side slab (both sides use the
    same pattern).  x_inboard_face is the face the button head bears on: the tray
    flange's inner face, or the rear panel flange's inner face."""
    h = []
    tray_face = P.W_OVER / 2 - 2 * T
    for zl in (P.Z_BOT, P.Z_MID, P.Z_TOP):
        for y in P.TRAY_BOLT_Y:
            h.append((y, zl - P.TRAY_SLOT_DROP, tray_face))
    for z in P.PANEL_BOLT_Z:
        h.append((panel_flange_mid_y(), P.Z_BOT + z, P.PANEL_W / 2 - T))
    return h


def panel_flange_mid_y():
    return P.PANEL_Y_BACK + P.PANEL_FLANGE / 2.0


def make_side_slab(sign=1):
    """Vertical slab, inner face at sign*(W_OVER/2 - T)."""
    z0, z1 = P.SIDE_BOT, P.Z_TOP - T
    body = cq.Solid.makeBox(T, P.D_OVER, z1 - z0,
                            cq.Vector(sign * (P.W_OVER / 2 - T) - (T / 2 if sign > 0 else 0) - (0 if sign > 0 else 0), -P.D_OVER / 2, z0))
    # place precisely: outer face at sign*W_OVER/2
    x_out = sign * P.W_OVER / 2.0
    body = cq.Solid.makeBox(T, P.D_OVER, z1 - z0,
                            cq.Vector(min(x_out, x_out - sign * T), -P.D_OVER / 2, z0))
    for (y, z, _) in side_slab_holes():
        body = S.hole_through(body, sign * (P.W_OVER / 2 - T / 2), y, z,
                              P.BOLT["clearance"], axis="X")
    return body.clean()


def make_tray(z_top, front_h=P.FLANGE, foot_holes=False):
    """Shelf tray whose TOP surface is at z_top."""
    body, spec = S.make_tray(P.TRAY_W, P.D_OVER, P.FLANGE, front_h,
                             z=z_top - T / 2.0)
    w = P.TRAY_SLOT[0]
    l = P.TRAY_SLOT[1]
    for sgn in (1, -1):
        for y in P.TRAY_BOLT_Y:
            body = S.slot_through(body, sgn * (P.TRAY_W / 2 - T / 2), y,
                                  z_top - P.TRAY_SLOT_DROP, w, l, axis="X")
    if foot_holes:
        for sx in (1, -1):
            for sy in (1, -1):
                body = S.hole_through(body, sx * P.FOOT_X, sy * P.FOOT_Y,
                                      z_top + T, P.FOOT["clearance"], axis="Z",
                                      depth=3 * T)
    spec["z_top"] = z_top
    spec["foot_holes"] = foot_holes
    return body.clean(), spec


def make_tray_top():
    """Top tray: identical to the shelf tray plus one 6.6 hole through the rear
    margin of the deck for the anti-tip strap (P5). It is outside the turntable
    footprint (the plinth's rear face is 24 mm further forward)."""
    body, spec = make_tray(P.Z_TOP)
    sh = P.STRAP_HOLE
    body = S.hole_through(body, sh["x"], sh["y"], P.Z_TOP + T, sh["d"],
                          axis="Z", depth=3 * T)
    spec["strap_hole"] = True
    return body.clean(), spec


def make_rear_panel():
    """C-channel: web + two forward flanges, spanning the record bay."""
    w, h, hf = P.PANEL_W, P.PANEL_H, P.PANEL_FLANGE
    body = S.plate_solid(w, h, 0.0)
    for rot in (0.0, 180.0):
        body = body.fuse(S.flange_solid(hf, -h / 2, h / 2, w / 2, rot)).clean()
    # stand it up: local -Z (flange direction) -> +Y (forward), local Y -> +Z
    body = body.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0)
    body = body.translate(cq.Vector(0, P.PANEL_Y_BACK + T / 2, P.Z_BOT + h / 2))
    # bolt holes through the two forward flanges
    for sgn in (1, -1):
        for z in P.PANEL_BOLT_Z:
            body = S.hole_through(body, sgn * (P.PANEL_W / 2 - T / 2),
                                  panel_flange_mid_y(), P.Z_BOT + z,
                                  P.BOLT["clearance"], axis="X")
    return body.clean()


def make_wall_strap():
    """Anti-tip 'Z' strap, 1.88 mm CRS, 25 mm wide, two 90 deg bends:
        foot 110 (sits on the top tray's rear margin, 6.6 x 40 slot for the
        wall-distance adjustment) -> riser 250 up the wall -> 30 mm wall flange
        with a 6.6 hole.  One 6.6 hole in the foot bolts it down through the
        tray's deck."""
    w, foot, riser, wall = (P.STRAP["w"], P.STRAP["foot"], P.STRAP["riser"],
                            P.STRAP["wall"])
    # flat: 25 x (110+250+30), bend lines at 110 and 360
    body = cq.Workplane("XY").polyline(
        [(-w / 2, 0), (w / 2, 0), (w / 2, foot + riser + wall),
         (-w / 2, foot + riser + wall)]).close().extrude(T).val()
    # slot in the foot (6.6 wide x 40 long, along the foot)
    body = body.cut(cq.Solid.makeBox(6.6, P.STRAP["slot"], T + 2,
                                     cq.Vector(-3.3, foot - 15.0 - 20.0, -1)))
    # wall hole in the wall flange
    body = body.cut(cq.Solid.makeCylinder(3.3, T + 2,
                                          cq.Vector(0, foot + riser + wall / 2, -1),
                                          cq.Vector(0, 0, 1)))
    # bend 1: foot stays, riser turns up 90 deg about x at y = foot
    # (represented folded: foot horizontal, riser vertical, wall flange vertical)
    foot_s = cq.Solid.makeBox(w, foot, T, cq.Vector(-w / 2, 0, 0))
    foot_s = foot_s.cut(cq.Solid.makeBox(6.6, P.STRAP["slot"], T + 2,
                                         cq.Vector(-3.3, 55.0, -1)))
    riser_s = cq.Solid.makeBox(w, T, riser, cq.Vector(-w / 2, foot - T, 0))
    wall_s = cq.Solid.makeBox(w, T, wall, cq.Vector(-w / 2, foot - T, riser))
    wall_s = wall_s.cut(cq.Solid.makeCylinder(3.3, T + 2,
                                              cq.Vector(0, foot - 2 * T - 1, riser + wall / 2),
                                              cq.Vector(0, 1, 0)))
    return foot_s.fuse(riser_s).fuse(wall_s).clean()


# ---------------------------------------------------------------------------
# reference (purchased) components  --  excluded from manufacturing uploads
# ---------------------------------------------------------------------------
def make_tt():
    b = cq.Solid.makeBox(P.TT["W"], P.TT["D"], P.TT["H"],
                         cq.Vector(-P.TT["W"] / 2, -P.TT["D"] / 2, P.Z_TOP))
    return b


def make_tt_feet():
    sol = None
    for sx in (1, -1):
        for sy in (1, -1):
            x = sx * (P.TT["W"] / 2 - P.TT["foot_inset_x"])
            y = sy * (P.TT["D"] / 2 - P.TT["foot_inset_y"])
            f = cq.Solid.makeCylinder(P.TT["foot_dia"] / 2, 6.0,
                                      cq.Vector(x, y, P.Z_TOP), cq.Vector(0, 0, 1))
            sol = f if sol is None else sol.fuse(f)
    return sol


def make_dust_cover(angle_deg=100.0):
    """Envelope of the dust cover lifted on its rear hinges (reference only)."""
    W, D, th = P.TT["W"] + 6, P.TT["D"] + 6, 4.0
    hinge_y = -P.TT["D"] / 2 + 8.0
    hinge_z = P.Z_TOP + P.TT["H"] - 20.0
    # local frame: hinge at the origin, cover extends forward (+Y)
    c = cq.Solid.makeBox(W, D, th, cq.Vector(-W / 2, 0, 0))
    c = c.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), angle_deg)
    c = c.translate(cq.Vector(0, hinge_y, hinge_z))
    return c


def make_speaker(sign=1):
    """Right-triangle prism: front-bottom (baffle low edge) to rear-top."""
    W, H, Dd = P.SPK["W"], P.SPK["H"], P.SPK["D"]
    y0 = P.SPK_Y_FRONT - Dd
    z0 = P.Z_MID + P.PAD["h"]
    wire = cq.Workplane("YZ").polyline(
        [(y0, z0), (y0 + Dd, z0), (y0, z0 + H)]).close().wires().val()
    sol = cq.Solid.extrudeLinear(wire, [], cq.Vector(W, 0, 0))
    sol = sol.translate(cq.Vector(sign * P.SPK_X - W / 2, 0, 0))
    return sol


def make_speaker_baffle(sign=1):
    """Thin plane on the baffle (hypotenuse) so the wedge orientation is legible."""
    W, H, Dd = P.SPK["W"] - 8, P.SPK["H"], P.SPK["D"] - 6
    y0 = P.SPK_Y_FRONT - Dd + 3
    z0 = P.Z_MID + P.PAD["h"] + 1.5
    wire = cq.Workplane("YZ").polyline(
        [(y0, z0), (y0 + Dd, z0), (y0 + 3, z0 + H - 6)]).close().wires().val()
    sol = cq.Solid.extrudeLinear(wire, [], cq.Vector(1.0, 0, 0))
    return sol.translate(cq.Vector(sign * P.SPK_X - (W) / 2, 0, 0))


def make_pads(sign=1):
    W, Dd = P.SPK["W"], P.SPK["D"]
    yc = P.SPK_Y_FRONT - Dd / 2
    sol = None
    for sx in (1, -1):
        for sy in (1, -1):
            x = sign * P.SPK_X + sx * (W / 2 - P.PAD["inset"])
            y = yc + sy * (Dd / 2 - P.PAD["inset"])
            c = cq.Solid.makeCylinder(P.PAD["dia"] / 2, P.PAD["h"],
                                      cq.Vector(x, y, P.Z_MID), cq.Vector(0, 0, 1))
            sol = c if sol is None else sol.fuse(c)
    return sol


def make_crate():
    C = P.CRATE
    y_rear = P.PANEL_Y_BACK + T + 1.0
    return cq.Solid.makeBox(C["W"], C["D"], C["H"],
                            cq.Vector(-C["W"] / 2, y_rear, P.Z_BOT))


def make_bolt(x_sign, y, z, x_face=None):
    """M5 x 12 button-head screw inserted from INSIDE the bay (head inboard,
    2.75 mm proud) with a flanged locknut on the OUTSIDE face.

    This orientation is deliberate: every nut is then reachable with a wrench
    from outside the stand, including the base tray, whose flange pocket is
    otherwise closed by its own skirt.  It also reduces the inboard protrusion
    from 5.0 mm (nut body) to 2.75 mm (button head), which matters at the
    speaker shelf.
    """
    d = P.BOLT
    x_in = x_sign * (P.W_OVER / 2.0 - 2 * T if x_face is None else abs(x_face))
    x_out = x_sign * P.W_OVER / 2.0               # slab outer face
    # head sits inboard of the tray flange
    head = cq.Solid.makeCylinder(d["head_dia"] / 2, d["head_h"],
                                 cq.Vector(x_in - x_sign * d["head_h"], y, z),
                                 cq.Vector(x_sign, 0, 0))
    shank = cq.Solid.makeCylinder(d["d"] / 2, d["length"],
                                  cq.Vector(x_in - x_sign * d["head_h"], y, z),
                                  cq.Vector(x_sign, 0, 0))
    nut = cq.Solid.makeCylinder(5.9, 5.0, cq.Vector(x_out, y, z),
                                cq.Vector(x_sign, 0, 0))
    return head.fuse(shank).fuse(nut)


def make_foot(sx, sy):
    """Glide base on the floor (z=0), stud up through the deck, flanged nut on
    the deck's top face. Level by turning the glide, then lock the nut."""
    d = P.FOOT
    x, y = sx * P.FOOT_X, sy * P.FOOT_Y
    base = cq.Solid.makeCylinder(d["base_dia"] / 2, d["base_h"],
                                 cq.Vector(x, y, 0.0), cq.Vector(0, 0, 1))
    stud = cq.Solid.makeCylinder(3.0, d["stud_len"], cq.Vector(x, y, d["base_h"]),
                                 cq.Vector(0, 0, 1))
    nut = cq.Solid.makeCylinder(6.4, 6.0, cq.Vector(x, y, P.Z_BOT), cq.Vector(0, 0, 1))
    return base.fuse(stud).fuse(nut)


# ---------------------------------------------------------------------------
# part registry
# ---------------------------------------------------------------------------
def build():
    parts = {}
    parts["P1"] = dict(name="SIDE SLAB", qty=2, bends=0,
                       solids=[make_side_slab(1), make_side_slab(-1)],
                       mat="CRS 1.88", finish="powder coat textured black")
    tray_mid, spec2 = make_tray(P.Z_MID)
    tray_top, _ = make_tray_top()
    parts["P2"] = dict(name="SHELF TRAY", qty=2, bends=4,
                       solids=[tray_top, tray_mid],
                       mat="CRS 1.88", finish="powder coat textured black",
                       spec=spec2)
    tray3, spec3 = make_tray(P.Z_BOT, front_h=P.FLANGE_BOT, foot_holes=True)
    parts["P3"] = dict(name="BASE TRAY", qty=1, bends=4, solids=[tray3],
                       mat="CRS 1.88", finish="powder coat textured black", spec=spec3)
    parts["P4"] = dict(name="REAR PANEL", qty=1, bends=2, solids=[make_rear_panel()],
                       mat="CRS 1.88", finish="powder coat textured black")
    parts["P5"] = dict(name="WALL STRAP (optional)", qty=1, bends=1,
                       solids=[make_wall_strap()], mat="CRS 1.88",
                       finish="powder coat textured black")
    return parts


def assembly(parts, equipment=True, hardware=True):
    a = cq.Assembly(name="GI-RAD-STAND-R0.9")
    cols = {"P1": cq.Color(0.12, 0.13, 0.15), "P2": cq.Color(0.15, 0.16, 0.19),
            "P3": cq.Color(0.13, 0.14, 0.17), "P4": cq.Color(0.10, 0.11, 0.13),
            "P5": cq.Color(0.20, 0.20, 0.22)}
    for pid, p in parts.items():
        for i, s in enumerate(p["solids"]):
            a.add(s, name=f"{pid}_{p['name'].split()[0]}_{i+1}",
                  color=cols.get(pid, cq.Color(0.5, 0.5, 0.5)))
    if hardware:
        for sgn in (1, -1):
            for (y, z, xf) in side_slab_holes():
                a.add(make_bolt(sgn, y, z, xf), name=f"bolt_{sgn}_{y:.0f}_{z:.0f}",
                      color=cq.Color(0.55, 0.56, 0.60))
        for sx in (1, -1):
            for sy in (1, -1):
                a.add(make_foot(sx, sy), name=f"foot_{sx}_{sy}",
                      color=cq.Color(0.25, 0.25, 0.25))
    if equipment:
        a.add(make_tt(), name="AT-LP120XUSB", color=cq.Color(0.30, 0.31, 0.33))
        a.add(make_tt_feet(), name="TT_feet", color=cq.Color(0.1, 0.1, 0.1))
        a.add(make_dust_cover(), name="dust_cover_open", color=cq.Color(0.75, 0.82, 0.9, 0.35))
        for sgn in (1, -1):
            a.add(make_speaker(sgn), name=f"AR_PP570_{'R' if sgn>0 else 'L'}",
                  color=cq.Color(0.22, 0.22, 0.24))
            a.add(make_pads(sgn), name=f"ISO-PUCK-mini_{sgn}", color=cq.Color(0.9, 0.55, 0.1))
        a.add(make_crate(), name="GrooveCrate_14.5", color=cq.Color(0.35, 0.25, 0.12, 0.55))
    return a


MANUFACTURING_IDS = ("P1", "P2", "P3", "P4")

if __name__ == "__main__":
    import sys
    parts = build()
    for pid, p in parts.items():
        for i, s in enumerate(p["solids"]):
            print(pid, p["name"], i, "valid", s.isValid(),
                  "vol", round(s.Volume(), 1),
                  "bbox", [round(v, 1) for v in (s.BoundingBox().xlen,
                                                 s.BoundingBox().ylen,
                                                 s.BoundingBox().zlen)])
