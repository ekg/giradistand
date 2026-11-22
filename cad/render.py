"""
Offscreen VTK renderer for the GI-RAD stand -- produces the published views.
All geometry comes from the parametric CAD model (cad/model.py).
"""

import os
import vtk
import cadquery as cq

import params as P
import model as M

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "renders")

C = {
    "P1": (0.50, 0.51, 0.54), "P2": (0.44, 0.45, 0.48),
    "P3": (0.40, 0.41, 0.44), "P4": (0.33, 0.34, 0.37),
    "P5": (0.58, 0.58, 0.60),
    "bolt": (0.80, 0.81, 0.84), "foot": (0.16, 0.16, 0.17),
    "tt": (0.66, 0.67, 0.70), "tt_foot": (0.10, 0.10, 0.11),
    "spk": (0.26, 0.26, 0.28), "spk_front": (0.42, 0.42, 0.45),
    "pad": (0.95, 0.58, 0.08), "crate": (0.74, 0.58, 0.36),
    "crate_ghost": (0.85, 0.75, 0.55), "cover": (0.55, 0.72, 0.92),
}

_RW = None
_REN = None


def _pd(shape, tol=0.2, ang=0.3):
    verts, tris = shape.tessellate(tol, ang)
    pts = vtk.vtkPoints()
    for v in verts:
        pts.InsertNextPoint(v.x, v.y, v.z)
    cells = vtk.vtkCellArray()
    for t in tris:
        cells.InsertNextCell(3)
        for k in t:
            cells.InsertCellPoint(k)
    pd = vtk.vtkPolyData()
    pd.SetPoints(pts)
    pd.SetPolys(cells)
    n = vtk.vtkPolyDataNormals()
    n.SetInputData(pd)
    n.SetFeatureAngle(35)
    n.SplittingOn()
    n.ConsistencyOn()
    n.Update()
    return n.GetOutput()


class Item:
    def __init__(self, shape, color, mode="solid", tol=0.2):
        self.shape, self.color, self.mode, self.tol = shape, color, mode, tol

    def actors(self):
        pd = _pd(self.shape, self.tol)
        m = vtk.vtkPolyDataMapper()
        m.SetInputData(pd)
        m.ScalarVisibilityOff()
        a = vtk.vtkActor()
        a.SetMapper(m)
        pr = a.GetProperty()
        pr.SetColor(*self.color)
        pr.SetAmbient(0.45)
        pr.SetDiffuse(0.60)
        pr.SetSpecular(0.08)
        pr.SetSpecularPower(18)
        out = [a]
        if self.mode == "solid":
            if self.color[0] < 0.6:
                e = self._edges(pd, (0.06, 0.06, 0.07), 1.3)
                out.append(e)
        elif self.mode == "ghost":
            pr.SetRepresentationToWireframe()
            pr.SetLineWidth(1.2)
            a.GetProperty().SetColor(*self.color)
        elif self.mode == "wire":
            pr.SetRepresentationToWireframe()
            pr.SetLineWidth(1.8)
        return out

    @staticmethod
    def _edges(pd, color, lw):
        e = vtk.vtkFeatureEdges()
        e.SetInputData(pd)
        e.BoundaryEdgesOff()
        e.NonManifoldEdgesOff()
        e.ManifoldEdgesOff()
        e.FeatureEdgesOn()
        e.SetFeatureAngle(26)
        e.ColoringOff()
        e.Update()
        em = vtk.vtkPolyDataMapper()
        em.SetInputData(e.GetOutput())
        em.ScalarVisibilityOff()
        ea = vtk.vtkActor()
        ea.SetMapper(em)
        ea.GetProperty().SetColor(*color)
        ea.GetProperty().SetLineWidth(lw)
        ea.GetProperty().SetLighting(False)
        return ea


def _init(size=(1800, 1350)):
    global _RW, _REN
    if _RW is not None:
        return _RW, _REN
    rw = vtk.vtkRenderWindow()
    rw.SetOffScreenRendering(1)
    rw.SetSize(*size)
    rw.SetMultiSamples(8)
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.SetUseDepthPeeling(1)
    ren.SetMaximumNumberOfPeels(8)
    rw.SetAlphaBitPlanes(1)
    rw.AddRenderer(ren)
    for (pos, inten) in [((0.8, 0.9, 1.5), 0.85), ((-1.1, -0.5, 0.8), 0.40),
                         ((0.1, -1.3, 0.5), 0.28)]:
        L = vtk.vtkLight()
        L.SetPosition(*pos)
        L.SetFocalPoint(0, 0, 330)
        L.SetIntensity(inten)
        ren.AddLight(L)
    ren.SetAmbient(0.32, 0.32, 0.34)
    _RW, _REN = rw, ren
    return rw, ren


def shot(items, pos, focal=(0, 0, 330), up=(0, 0, 1), scale=430,
         path="view.png", floor=True, parallel=True):
    rw, ren = _init()
    ren.RemoveAllViewProps()
    for it in items:
        for a in it.actors():
            ren.AddActor(a)
    if floor:
        pl = vtk.vtkPlaneSource()
        pl.SetOrigin(-1200, -1200, -0.4)
        pl.SetPoint1(1200, -1200, -0.4)
        pl.SetPoint2(-1200, 1200, -0.4)
        pm = vtk.vtkPolyDataMapper()
        pm.SetInputConnection(pl.GetOutputPort())
        pa = vtk.vtkActor()
        pa.SetMapper(pm)
        pa.GetProperty().SetColor(0.90, 0.90, 0.91)
        pa.GetProperty().SetAmbient(0.55)
        pa.GetProperty().SetDiffuse(0.55)
        ren.AddActor(pa)
    cam = ren.GetActiveCamera()
    cam.SetFocalPoint(*focal)
    cam.SetPosition(*pos)
    cam.SetViewUp(*up)
    if parallel:
        cam.ParallelProjectionOn()
        cam.SetParallelScale(scale)
    else:
        cam.SetViewAngle(26)
    ren.ResetCameraClippingRange()
    rw.Render()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(rw)
    w2i.ReadFrontBufferOff()
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(path)
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
    print("wrote", path)
    return path


# ---------------------------------------------------------------------------
def frame_items(explode=0.0, hardware=True, include_strap=False, drop=None):
    parts = M.build()
    items = []
    for pid, p in parts.items():
        if pid == "P5" and not include_strap:
            continue
        for i, s in enumerate(p["solids"]):
            if drop and (pid, i) in drop:
                continue
            sh = s
            if explode:
                if pid == "P1":
                    sh = s.translate(cq.Vector((1 if i == 0 else -1) * 200 * explode, 0, 0))
                elif pid == "P2":
                    sh = s.translate(cq.Vector(0, 0, (150 if i == 0 else 50) * explode))
                elif pid == "P3":
                    sh = s.translate(cq.Vector(0, 0, -80 * explode))
                elif pid == "P4":
                    sh = s.translate(cq.Vector(0, -190 * explode, 0))
            items.append(Item(sh, C[pid]))
    if hardware:
        for sgn in (1, -1):
            for (y, z, xf) in M.side_slab_holes():
                b = M.make_bolt(sgn, y, z, xf)
                if explode:
                    b = b.translate(cq.Vector(sgn * 130 * explode, 0, 0))
                items.append(Item(b, C["bolt"], tol=0.4))
        for sx in (1, -1):
            for sy in (1, -1):
                f = M.make_foot(sx, sy)
                if explode:
                    f = f.translate(cq.Vector(0, 0, -80 * explode))
                items.append(Item(f, C["foot"], tol=0.5))
    return items


def equipment_items(crate_dy=0.0, cover="wire", pads=True):
    items = [Item(M.make_tt(), C["tt"]), Item(M.make_tt_feet(), C["tt_foot"], tol=0.4)]
    items.append(Item(M.make_dust_cover(), C["cover"], mode=cover, tol=0.4))
    for sgn in (1, -1):
        items.append(Item(M.make_speaker(sgn), C["spk"]))
        items.append(Item(M.make_speaker_baffle(sgn), C["spk_front"], tol=0.4))
        if pads:
            items.append(Item(M.make_pads(sgn), C["pad"], tol=0.4))
    cr = M.make_crate()
    if crate_dy:
        cr = cr.translate(cq.Vector(0, crate_dy, 0))
    items.append(Item(cr, C["crate"]))
    return items


def main():
    f = frame_items()
    fr_only = frame_items(hardware=False)

    shot(f + equipment_items(), (2000, 2300, 1900), focal=(0, 0, 430),
         path=f"{OUT}/01_iso_loaded.png", scale=620)
    shot(f + equipment_items(), (0, 3000, 430), focal=(0, 0, 430),
         path=f"{OUT}/02_front_loaded.png", scale=560)
    f_near = frame_items(drop={("P1", 1)})
    shot(f_near + equipment_items(), (-3000, 400, 430), focal=(0, 0, 430),
         path=f"{OUT}/03_side_near_slab_removed.png", scale=560)
    shot(f + equipment_items(), (0, 0, 3000), focal=(0, 0, 0), up=(0, 1, 0),
         path=f"{OUT}/04_top_loaded.png", scale=420, floor=False)
    shot(f + equipment_items(), (2000, -2300, 1600), focal=(0, 0, 430),
         path=f"{OUT}/05_rear.png", scale=620)
    shot(f, (1300, 1000, -900), focal=(0, 0, 240), path=f"{OUT}/06_underside.png",
         scale=560, floor=False)
    shot(fr_only, (1900, 2200, 1800), focal=(0, 0, 430),
         path=f"{OUT}/07_frame_only.png", scale=600)
    shot(frame_items(explode=1.0), (2400, 2600, 2100), focal=(0, 0, 430),
         path=f"{OUT}/08_exploded.png", scale=780)
    shot(f + [it for it in equipment_items(crate_dy=420) if it.color == C["crate"]]
         + [Item(M.make_crate(), C["crate_ghost"], mode="ghost")],
         (1200, 3000, 900), focal=(0, 0, 380),
         path=f"{OUT}/09_crate_removal.png", scale=680)
    shot(f + equipment_items(cover="solid"), (-3000, 600, 500), focal=(0, 0, 460),
         path=f"{OUT}/10_cover_open_side.png", scale=620)


def section(z0, z1, which="both"):
    """Clip every solid to a slab, for a horizontal section view."""
    import cadquery as cq
    out = []
    for it in frame_items() + equipment_items():
        try:
            sec = it.shape.intersect(cq.Solid.makeBox(2000, 2000, z1 - z0,
                                                      cq.Vector(-1000, -1000, z0)))
            if sec.Volume() > 1:
                out.append(Item(sec, it.color, tol=it.tol))
        except Exception:
            pass
    return out


def extra_views():
    # horizontal sections: cut through the bay at a bolt/flange height, thick
    # enough to read (25 mm slice), viewed in isometric so the cut faces show
    shot(section(470, 500), (1600, 1800, 2200), focal=(0, 0, 430),
         path=f"{OUT}/11_section_speaker_bay.png", scale=480, floor=False)
    shot(section(180, 230), (1600, 1800, 2200), focal=(0, 0, 430),
         path=f"{OUT}/12_section_record_bay.png", scale=480, floor=False)


if __name__ == "__main__":
    main()
    extra_views()
