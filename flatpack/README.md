# FLAT PACK STAND — CNC plywood alternative

**Revision W0.9 — provisional: dimensioned, analytically checked, not built, not
supplier-quoted.** Same three levels and equipment as the steel design, made from
**one 1525 × 1525 × 18 mm sheet of Baltic birch**, CNC-routed, assembled by hand with
six 8 mm dowels and a rubber mallet.

| | steel design | this design |
|---|---|---|
| overall | 570 × 400 × 626 | **602 × 415 × 630** |
| material | 1.88 mm CRS, powder coat | 18 mm Baltic birch, sanded, unfinished |
| pieces / part numbers | 7 / 5 | 6 / 4 (+1 coupon) |
| assembly | 23 × M5 + 4 feet, hex key + wrench | 6 dowels by hand, no tools |
| racks free-standing | yes (with friction-grip joints) | yes (thick panels, snug joints) |
| estimated delivered cost | ≈ US$518 | **≈ US$331** |
| tool needed | 3 mm hex key, 2 wrenches | rubber mallet |

Target was ≈US$300: **material + CNC = $240** (inside the $220–250 allowance) and the
total lands at about $331 with accessories, shipping and tax. The gap and the three
levers to close it are in `out/cost_model.md`.

## Why plywood is cheaper here, and where the money goes

One sheet, one setup, no bends, no finish, no thread protection, no hardware insertion:
the plywood kit replaces 15 CNC bends and a five-part powder-coat order with a single
routing pass. The nine dollars of dowels replace twenty-three bolts.

## What it is

* **Two side panels**, 415 × 630 × 18, identical, each with three 150.2 × 18.2 slots
  (square, with R4 dogbone corner reliefs — a round cutter cannot make a sharp internal
  corner) and four 6.6 foot holes in the base shelf.
* **Three shelves** (two identical + one base shelf with foot holes), 638 × 394 × 18,
  each with a 150 × 18 tab at both ends that passes through the side slots and protrudes
  18 mm, and a vertical 8.4 mm dowel hole in each tab.
* **Six 8 mm birch dowels**, dropped through the protruding tabs. They are the lock: the
  shelf cannot be pushed further in (the tab shoulder bears on the side panel) and cannot
  be pulled out (the dowel bears on the panel's outer face 4 mm away). Lift the dowel out
  and the shelf slides free — that is the whole disassembly procedure.
* **P4 anti-tip strap** cut from the same sheet (a "Z" with a slot that suits a 50–110 mm
  wall gap).
* **P5 fit coupon** with three slots at +0.10 / +0.20 / +0.30 mm clearance, cut from the
  same sheet in the same setup. This is the one thing that must be done before the kit is
  cut: *measure the actual panel thickness and test the coupon.*

## Package contents

```
README.md                    this file
docs/01_design.md            recommendation, dimensions, clear openings
docs/02_inputs.md            input register + the measurements still needed
docs/03_joinery_and_assembly.md  joinery logic, assembly and disassembly sequence
docs/04_validation.md        structural fit/stability summary + validation matrix
docs/05_cost_and_upload.md   BOM, cost model, upload guide, cleanup requirements
cad/params.py                one authoritative parameter set
cad/model.py                 part geometry (2.5-D panels), assembly, equipment envelopes
cad/export.py                DXF flat patterns, STEP, nesting, CAD checks
cad/drawings.py              three A2 sheets (assembly, parts+joinery, nest)
cad/render.py                six rendered views
cad/bom.py                   BOM + cost model
calc/run_all.py              engineering calculations
out/dxf/                     P1..P5 flat profiles + NEST_1525x1525.dxf
out/step/                    4 part STEPs + assembly.step
out/drawings/                F1, F2, F3 (PNG + PDF)
out/renders/                 6 views
out/calc_report.md           calculations
out/cad_checks.md            interference / fit / crate-path checks
out/bom.csv, out/cost_model.md
FLATPACK-W09-package.zip
```

Regenerate everything:

```bash
cd flatpack
../.venv/bin/python cad/export.py      # dxf + step + checks + nest
../.venv/bin/python calc/run_all.py    # calculations
../.venv/bin/python cad/drawings.py
../.venv/bin/python cad/render.py
../.venv/bin/python cad/bom.py
../.venv/bin/python make_package.py
```

## Status, honestly

* **Not built, not quoted, not supplier-reviewed.** Material+CNC is a rate-based
  estimate; Pixels to Prototype quote by review, not instantly, so no price exists yet.
* **Not released for cutting** until (a) the actual panel thickness is measured and the
  fit coupon tested, and (b) the two equipment unknowns from the steel package are
  settled (which face of the speaker rests on the shelf, and the turntable model).
* The design has **no fasteners in the shelves at all**, so joint tightness depends on
  the slot clearance being right for the actual sheet. That is exactly what the coupon
  is for; it is not a formality.
