"""
Sheet-metal geometry library for the GI-RAD stand.

Implements:
  * bend allowance / deduction math using the fabricator's published rule
    (SendCutSend .074in mild steel: R_in = 1.60 mm, K = 0.40, BD = 3.277 mm)
  * a "bent flange" solid builder that produces true radiused, uniform-thickness
    sheet metal (as SendCutSend requires for 3D uploads)
  * tray / channel builders returning (folded solid, flat solid, cut outline)
  * the matching flat pattern, computed analytically from the same parameters,
    so the flat-pattern DXF and the folded STEP can never drift apart.
"""

import math
import cadquery as cq

from params import T, R_IN, BD

EPS = 1e-9


# ---------------------------------------------------------------------------
# bend math
# ---------------------------------------------------------------------------
def ossb(radius, thickness, angle_deg=90.0):
    """Outside setback."""
    return (radius + thickness) * math.tan(math.radians(angle_deg) / 2.0)


def bend_allowance(radius, thickness, k, angle_deg=90.0):
    return math.pi * (radius + k * thickness) * angle_deg / 180.0


def bend_deduction(radius, thickness, k, angle_deg=90.0):
    return 2.0 * ossb(radius, thickness, angle_deg) - bend_allowance(
        radius, thickness, k, angle_deg)


BD_CALC = bend_deduction(R_IN, T, 0.40)      # 3.265 mm (published value 3.277)
FLAT_BEND_LINE = BD / 2.0                    # bend line offset from flat edge


def developed_length(legs):
    """Flat length of a chain of n bends formed from n+1 outside legs."""
    return sum(legs) - BD * (len(legs) - 1)


# ---------------------------------------------------------------------------
# flange geometry (base case: plate in XY, flange down at +X edge)
# ---------------------------------------------------------------------------
def _flange_profile(h, width, x_edge, overlap=6.0):
    """2-D closed profile of a down-turned 90 deg flange at x = +x_edge.

    Returns a list of (x, z) points/arc steps describing the *outline* of the
    bend + flange material, including a short overlap stub into the plate.
    Built with threePointArc-friendly data.
    """
    zt, zb = T / 2.0, -T / 2.0
    cx = x_edge - T - R_IN
    cz = zb - R_IN
    ro = R_IN + T
    bottom_z = zt - h
    # inner arc start/end and mid
    i0 = (cx, zb)
    i1 = (x_edge - T, cz)
    imid = (cx + R_IN / math.sqrt(2), cz + R_IN / math.sqrt(2))
    # outer arc start/end and mid
    o0 = (x_edge, cz)
    o1 = (cx, zt)
    omid = (cx + ro / math.sqrt(2), cz + ro / math.sqrt(2))
    return dict(p0=(cx - overlap, zb), i0=i0, i1=i1, imid=imid,
                b_in=(x_edge - T, bottom_z), b_out=(x_edge, bottom_z),
                o0=o0, o1=o1, omid=omid, p1=(cx - overlap, zt))


def flange_solid(h, u0, u1, x_edge, rot_deg=0.0):
    """Solid of a 90 deg down-flange along the +X edge, extruded u0..u1 in Y,
    then rotated rot_deg about Z (0:+X, 90:+Y, 180:-X, 270:-Y)."""
    p = _flange_profile(h, u1 - u0, x_edge)

    def P(pt):                      # (x, z) -> workplane (x, -z) so that a
        return (pt[0], -pt[1])      # rotation about X maps it back correctly

    wp = (cq.Workplane("XY")
          .moveTo(*P(p["p0"]))
          .lineTo(*P(p["i0"]))
          .threePointArc(P(p["imid"]), P(p["i1"]))
          .lineTo(*P(p["b_in"]))
          .lineTo(*P(p["b_out"]))
          .lineTo(*P(p["o0"]))
          .threePointArc(P(p["omid"]), P(p["o1"]))
          .lineTo(*P(p["p1"]))
          .close())
    wire = wp.wires().val()
    # extrude along +Z (workplane normal) = flange width direction, then stand up
    solid = cq.Solid.extrudeLinear(wire, [], cq.Vector(0, 0, u1 - u0))
    solid = solid.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), -90.0)
    solid = solid.translate(cq.Vector(0, u0, 0))
    if abs(rot_deg) > EPS:
        solid = solid.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), rot_deg)
    return solid



def plate_solid(w, d, z=0.0, thickness=T):
    return cq.Solid.makeBox(w, d, thickness,
                             cq.Vector(-w / 2, -d / 2, z - thickness / 2))


def slot_through(solid, x, y, z, w, l, axis="X"):
    """Cut a through slot.  axis = the plate's normal direction."""
    if axis == "X":       # slots in a vertical flange, normal = X, long axis = Z
        tool = cq.Solid.makeBox(60.0, w, l, cq.Vector(x - 30.0, y - w / 2, z - l / 2))
    elif axis == "Y":
        tool = cq.Solid.makeBox(w, 60.0, l, cq.Vector(x - w / 2, y - 30.0, z - l / 2))
    elif axis == "Z":
        tool = cq.Solid.makeBox(w, l, 60.0, cq.Vector(x - w / 2, y - l / 2, z - 30.0))
    else:
        raise ValueError(axis)
    return solid.cut(tool)


def hole_through(solid, x, y, z, d, axis="Z", depth=60.0):
    if axis == "Z":
        tool = cq.Solid.makeCylinder(d / 2, depth, cq.Vector(x, y, z - depth / 2), cq.Vector(0, 0, 1))
    elif axis == "X":
        tool = cq.Solid.makeCylinder(d / 2, depth, cq.Vector(x - depth / 2, y, z), cq.Vector(1, 0, 0))
    elif axis == "Y":
        tool = cq.Solid.makeCylinder(d / 2, depth, cq.Vector(x, y - depth / 2, z), cq.Vector(0, 1, 0))
    else:
        raise ValueError(axis)
    return solid.cut(tool)


# ---------------------------------------------------------------------------
# tray  (4 flanges down; per-edge heights and spans)
# ---------------------------------------------------------------------------
def make_tray(w, d, h_end, h_front, z=0.0):
    """Folded tray centred in XY with its top surface at z + T/2.

    h_end   : depth of the two end (left/right, +/-X) flanges
    h_front : depth of the two front/rear (+/-Y) flanges
    Corner clearance between adjacent flanges is RACK_CORNER from params.
    Returns (solid, spec) where spec records the spans used for the flat pattern.
    """
    from params import RACK_CORNER
    body = plate_solid(w, d, 0.0)
    ends = []
    for hx, rot in ((h_end, 0.0), (h_end, 180.0)):
        span = d / 2 - (h_front + RACK_CORNER)
        s = flange_solid(hx, -span, span, w / 2, rot)
        body = body.fuse(s).clean()
        ends.append((hx, -span, span, rot))
    fronts = []
    for hy, rot in ((h_front, 90.0), (h_front, 270.0)):
        span = w / 2 - (h_end + RACK_CORNER)
        s = flange_solid(hy, -span, span, d / 2, rot)
        body = body.fuse(s).clean()
        fronts.append((hy, -span, span, rot))
    if abs(z) > EPS:
        body = body.translate(cq.Vector(0, 0, z))
    spec = dict(w=w, d=d, z=z, h_end=h_end, h_front=h_front,
                end_span=d / 2 - (h_front + RACK_CORNER),
                front_span=w / 2 - (h_end + RACK_CORNER))
    return body, spec


def _tray_flat_pts(spec):
    """Developed outline of a 4-flange tray (cross shape) in flat coordinates."""
    w, d = spec["w"], spec["d"]
    he, hf = spec["h_end"], spec["h_front"]
    wf = w + 2 * (he - BD)          # flat width  (over the end flanges)
    df = d + 2 * (hf - BD)          # flat depth  (over the front/rear flanges)
    xc = w / 2 - BD / 2             # half width of the flat plate core
    yc = d / 2 - BD / 2             # half depth of the flat plate core
    se = spec["end_span"]           # half span of the end tabs
    sf = spec["front_span"]         # half span of the front/rear tabs
    return [(-xc, -yc), (-sf, -yc), (-sf, -df / 2), (sf, -df / 2), (sf, -yc),
            (xc, -yc), (xc, -se), (wf / 2, -se), (wf / 2, se), (xc, se),
            (xc, yc), (sf, yc), (sf, df / 2), (-sf, df / 2), (-sf, yc),
            (-xc, yc), (-xc, se), (-wf / 2, se), (-wf / 2, -se), (-xc, -se)]


def tray_flat_face(spec):
    """Developed (flat) outline of a tray, as a cq.Workplane polyline."""
    return cq.Workplane("XY").polyline(_tray_flat_pts(spec)).close()


def tray_flat_solid(spec):
    return tray_flat_face(spec).extrude(T)


def tray_flat_lines(spec):
    """(outline_points, bend_line_segments) in the flat state, for DXF export."""
    w, d = spec["w"], spec["d"]
    he, hf = spec["h_end"], spec["h_front"]
    se, sf = spec["end_span"], spec["front_span"]
    outline = _tray_flat_pts(spec)
    xe = w / 2 - BD / 2
    ye = d / 2 - BD / 2
    bl = []
    for sgn in (1, -1):
        bl.append([(sgn * xe, -se), (sgn * xe, se)])       # end flanges
        bl.append([(-sf, sgn * ye), (sf, sgn * ye)])       # front/rear flanges
    return outline, bl
