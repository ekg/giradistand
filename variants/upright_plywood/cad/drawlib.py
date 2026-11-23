"""
Hidden-line-removed 2-D projection of CadQuery shapes -> polylines, plus a small
drawing engine (matplotlib) with dimensions, leaders, notes and title block.

Used to generate the dimensioned assembly and part drawings from the real CAD.
"""

import math
import os
import numpy as np

from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, FancyArrow

MM2M = 1.0


# ---------------------------------------------------------------------------
def _edges_to_polylines(shape, deflection=0.08):
    out = []
    if shape is None:
        return out
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        e = TopoDS.Edge_s(exp.Current())
        try:
            c = BRepAdaptor_Curve(e)
            d = GCPnts_QuasiUniformDeflection(c, deflection)
            if d.IsDone() and d.NbPoints() > 1:
                pts = [d.Value(i) for i in range(1, d.NbPoints() + 1)]
                out.append([(p.X(), p.Y()) for p in pts])
        except Exception:
            pass
        exp.Next()
    return out


def project(shape, view="front", origin=(0, 0, 0), up=(0, 0, 1), xdir=None):
    """Return (visible_polylines, hidden_polylines) in the projection plane.

    view directions: front(+Y->-Y), rear, side(+X->-X), side_r, top, bottom
    """
    # (projection normal pointing from object toward the eye, projection x-axis)
    dirs = {
        "front":  ((0, 1, 0),  (1, 0, 0)),
        "rear":   ((0, -1, 0), (-1, 0, 0)),
        "side_r": ((1, 0, 0),  (0, 1, 0)),
        "side_l": ((-1, 0, 0), (0, -1, 0)),
        "top":    ((0, 0, 1),  (1, 0, 0)),
        "bottom": ((0, 0, -1), (1, 0, 0)),
    }
    nrm, xdflt = dirs[view]
    d = gp_Dir(*nrm)
    xd = gp_Dir(*(xdir if xdir else xdflt))
    ax = gp_Ax2(gp_Pnt(*origin), d, xd)
    proj = HLRAlgo_Projector(ax)
    algo = HLRBRep_Algo()
    algo.Add(shape.wrapped if hasattr(shape, "wrapped") else shape)
    algo.Projector(proj)
    algo.Update()
    algo.Hide()
    hlr = HLRBRep_HLRToShape(algo)
    vis = []
    hid = []
    for getter in (hlr.VCompound, hlr.Rg1LineVCompound, hlr.OutLineVCompound,
                   hlr.IsoLineVCompound):
        s = getter()
        if s is not None and not s.IsNull():
            vis += _edges_to_polylines(s)
    for getter in (hlr.HCompound, hlr.OutLineHCompound, hlr.Rg1LineHCompound):
        s = getter()
        if s is not None and not s.IsNull():
            hid += _edges_to_polylines(s)
    return vis, hid


# ---------------------------------------------------------------------------
class Sheet:
    """A drawing sheet in mm; (0,0) = lower-left corner of the drawing area."""

    def __init__(self, w=420, h=297, title="", number="", rev="R0.9",
                 scale_note="1:1", subtitle="", material=""):
        self.w, self.h = w, h
        self.fig = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=200)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.add_patch(Rectangle((8, 8), w - 16, h - 16, fill=False, lw=1.6,
                                    ec="#111"))
        self.title = title
        self.number = number
        self.subtitle = subtitle
        self.material = material
        self.rev = rev
        self.scale_note = scale_note
        self._title_block()

    # -- primitives ------------------------------------------------------
    def view(self, vis, hid, ox, oy, scale=1.0, mirrored=False, lw=0.55,
             color="#111"):
        segs = [[(ox + scale * (p[0] if not mirrored else -p[0]), oy + scale * p[1])
                 for p in pl] for pl in vis]
        if segs:
            self.ax.add_collection(LineCollection(segs, colors=color, linewidths=lw,
                                                  capstyle="round"))
        hs = [[(ox + scale * (p[0] if not mirrored else -p[0]), oy + scale * p[1])
               for p in pl] for pl in hid]
        if hs:
            self.ax.add_collection(LineCollection(hs, colors="#8a8a8a",
                                                  linewidths=lw * 0.75,
                                                  linestyles=(0, (3, 2))))

    def centerline(self, x1, y1, x2, y2):
        self.ax.plot([x1, x2], [y1, y2], color="#7a7a7a", lw=0.4,
                     linestyle=(0, (7, 2, 1, 2)))

    def dim_h(self, x1, x2, y, text=None, above=True, size=6.2, color="#0a3d62"):
        self._arrow(x2, y, x1, y)
        if text is None:
            text = f"{abs(x2 - x1):.1f}"
        self.ax.text((x1 + x2) / 2, y + (1.6 if above else -1.6), text,
                     ha="center", va="bottom" if above else "top", fontsize=size,
                     color=color)

    def dim_v(self, y1, y2, x, text=None, left=True, size=6.2, color="#0a3d62",
              rot=90):
        self._arrow(x, y2, x, y1)
        if text is None:
            text = f"{abs(y2 - y1):.1f}"
        self.ax.text(x + (-1.6 if left else 1.6), (y1 + y2) / 2, text,
                     ha="right" if left else "left", va="center",
                     fontsize=size, rotation=rot, color=color)

    def _arrow(self, x1, y1, x2, y2):
        self.ax.annotate("", xy=(x1, y1), xytext=(x2, y2),
                         arrowprops=dict(arrowstyle="<|-|>", lw=0.45,
                                         color="#0a3d62",
                                         shrinkA=0, shrinkB=0,
                                         mutation_scale=5))
        # extension ticks
        for (x, y) in ((x1, y1), (x2, y2)):
            self.ax.plot([x - 1.2, x + 1.2], [y, y], color="#0a3d62", lw=0.45)

    def note(self, x, y, text, size=6.6, ha="left", weight="normal", color="#111"):
        self.ax.text(x, y, text, fontsize=size, ha=ha, va="center",
                     family="DejaVu Sans", color=color, weight=weight)

    def leader(self, x1, y1, x2, y2, text, size=6.0):
        self.ax.annotate(text, xy=(x1, y1), xytext=(x2, y2), fontsize=size,
                         arrowprops=dict(arrowstyle="-|>", lw=0.4, color="#444",
                                         mutation_scale=5),
                         va="center", ha="left" if x2 > x1 else "right")

    def line(self, x1, y1, x2, y2, lw=0.5, color="#111", ls="-"):
        self.ax.plot([x1, x2], [y1, y2], lw=lw, color=color, ls=ls)

    def _title_block(self):
        w, h = self.w, self.h
        x0, y0, tw = w - 8 - 150, 8, 150
        th = 40
        self.ax.add_patch(Rectangle((x0, y0), tw, th, fill=False, lw=0.9, ec="#111"))
        rows = [18, 10, 6, 6]
        yy = y0 + th
        for r in rows[:-1]:
            yy -= r
            self.ax.plot([x0, x0 + tw], [yy, yy], color="#111", lw=0.5)
        self.note(x0 + 2, y0 + th - 9, self.title, size=8.2, weight="bold")
        self.note(x0 + 2, y0 + th - 25, self.subtitle, size=6.0)
        self.note(x0 + 2, y0 + th - 33, self.material, size=5.6)
        self.note(x0 + 2, y0 + 3.2, f"GI-RAD STAND  |  {self.number}  |  rev {self.rev}"
                  f"  |  {self.scale_note}  |  mm", size=5.6)
        # zone markers
        for i in range(1, 8):
            xx = 8 + i * (w - 16 - 160) / 8
            self.ax.plot([xx, xx], [8, 12], color="#111", lw=0.4)
            self.ax.plot([xx, xx], [h - 12, h - 8], color="#111", lw=0.4)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fig.savefig(path, dpi=200)
        self.fig.savefig(path.replace(".png", ".pdf"))
        plt.close(self.fig)
        print("wrote", path)
