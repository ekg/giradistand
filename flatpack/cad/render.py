"""Standalone VTK renderer for the flat-pack stand (offscreen)."""

import os
import vtk
import cadquery as cq

import params as P
import model as M

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "out", "renders")
_RW = _REN = None


def _pd(shape, tol=0.4, ang=0.3):
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
    n.SetFeatureAngle(30)
    n.SplittingOn()
    n.Update()
    return n.GetOutput()


def item(shape, color, edges=True, lw=1.2, wire=False, tol=0.4):
    pd = _pd(shape, tol)
    m = vtk.vtkPolyDataMapper()
    m.SetInputData(pd)
    m.ScalarVisibilityOff()
    a = vtk.vtkActor()
    a.SetMapper(m)
    pr = a.GetProperty()
    pr.SetColor(*color)
    pr.SetAmbient(0.55)
    pr.SetDiffuse(0.62)
    pr.SetSpecular(0.04)
    if wire:
        pr.SetRepresentationToWireframe()
        pr.SetLineWidth(lw)
        return [a]
    out = [a]
    if edges:
        e = vtk.vtkFeatureEdges()
        e.SetInputData(pd)
        e.BoundaryEdgesOff()
        e.NonManifoldEdgesOff()
        e.ManifoldEdgesOff()
        e.FeatureEdgesOn()
        e.SetFeatureAngle(24)
        e.ColoringOff()
        e.Update()
        em = vtk.vtkPolyDataMapper()
        em.SetInputData(e.GetOutput())
        em.ScalarVisibilityOff()
        ea = vtk.vtkActor()
        ea.SetMapper(em)
        ea.GetProperty().SetColor(0.25, 0.18, 0.10)
        ea.GetProperty().SetLineWidth(lw)
        ea.GetProperty().SetLighting(False)
        out.append(ea)
    return out


def shot(actors, pos, focal, scale, path, up=(0, 0, 1), floor=True):
    global _RW, _REN
    if _RW is None:
        _RW = vtk.vtkRenderWindow()
        _RW.SetOffScreenRendering(1)
        _RW.SetSize(1800, 1350)
        _RW.SetMultiSamples(8)
        _REN = vtk.vtkRenderer()
        _REN.SetBackground(1, 1, 1)
        _RW.AddRenderer(_REN)
        for (p_, i_) in [((0.8, 0.9, 1.5), 0.85), ((-1.1, -0.5, 0.8), 0.40),
                         ((0.1, -1.3, 0.5), 0.28)]:
            L = vtk.vtkLight()
            L.SetPosition(*p_)
            L.SetFocalPoint(0, 0, 330)
            L.SetIntensity(i_)
            _REN.AddLight(L)
        _REN.SetAmbient(0.33, 0.33, 0.34)
    _REN.RemoveAllViewProps()
    for a in actors:
        _REN.AddActor(a)
    if floor:
        pl = vtk.vtkPlaneSource()
        pl.SetOrigin(-1300, -1300, -0.5)
        pl.SetPoint1(1300, -1300, -0.5)
        pl.SetPoint2(-1300, 1300, -0.5)
        pm = vtk.vtkPolyDataMapper()
        pm.SetInputConnection(pl.GetOutputPort())
        pa = vtk.vtkActor()
        pa.SetMapper(pm)
        pa.GetProperty().SetColor(0.90, 0.90, 0.91)
        pa.GetProperty().SetAmbient(0.55)
        pa.GetProperty().SetDiffuse(0.55)
        _REN.AddActor(pa)
    cam = _REN.GetActiveCamera()
    cam.SetFocalPoint(*focal)
    cam.SetPosition(*pos)
    cam.SetViewUp(*up)
    cam.ParallelProjectionOn()
    cam.SetParallelScale(scale)
    _REN.ResetCameraClippingRange()
    _RW.Render()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(_RW)
    w2i.ReadFrontBufferOff()
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(path)
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
    print("wrote", path)


WOOD = {"P1": (0.90, 0.77, 0.55), "P2": (0.87, 0.73, 0.50),
        "P3": (0.85, 0.71, 0.48), "P4": (0.80, 0.66, 0.44)}


def main():
    parts = M.build()
    base = []
    for pid, p in parts.items():
        for i, s in enumerate(p["solids"]):
            if pid == "P4":
                continue
            base += item(s, WOOD[pid])
    for sign in (1, -1):
        for z in (P.Z_BASE, P.Z_MID, P.Z_TOP):
            base += item(M.make_dowel(sign, z), (0.72, 0.56, 0.34), tol=0.3)
    eq = []
    eq += item(M.make_tt(), (0.34, 0.34, 0.36))
    for s in (1, -1):
        eq += item(M.make_speaker(s), (0.22, 0.22, 0.24))
        eq += item(M.make_pads(s), (0.95, 0.58, 0.08), tol=0.3)
    eq += item(M.make_crate(), (0.62, 0.50, 0.36))
    shot(base + eq, (2000, 2300, 1900), (0, 0, 430), 640, f"{OUT}/01_iso_loaded.png")
    shot(base + eq, (0, 3000, 430), (0, 0, 430), 580, f"{OUT}/02_front.png")
    shot(base + eq, (-3000, 0, 430), (0, 0, 430), 580, f"{OUT}/03_side.png")
    shot(base + eq, (0, 0, 3000), (0, 0, 0), 440, f"{OUT}/04_top.png",
         up=(0, 1, 0), floor=False)
    shot(base, (2000, 2300, 1800), (0, 0, 430), 640, f"{OUT}/05_frame_only.png")
    # exploded: shelves lifted out, sides apart
    ex = []
    for pid, p in parts.items():
        for i, s in enumerate(p["solids"]):
            if pid == "P4":
                continue
            if pid == "P1":
                ex += item(s.translate(cq.Vector((1 if i == 0 else -1) * 420, 0, 0)),
                           WOOD[pid])
            elif pid in ("P2", "P3"):
                z = {0: P.Z_BASE, 1: P.Z_MID, 2: P.Z_TOP}.get(i, P.Z_TOP)
                lift = {P.Z_BASE: -120, P.Z_MID: 60, P.Z_TOP: 240}[z]
                ex += item(s.translate(cq.Vector(0, 0, lift)), WOOD[pid])
    for sign in (1, -1):
        for z, lift in ((P.Z_BASE, -60), (P.Z_MID, 120), (P.Z_TOP, 300)):
            ex += item(M.make_dowel(sign, z).translate(cq.Vector(sign * 500, 0, lift)),
                       (0.72, 0.56, 0.34), tol=0.3)
    shot(ex, (2600, 2800, 2200), (0, 0, 430), 1000, f"{OUT}/06_exploded.png")


if __name__ == "__main__":
    main()
