# GI-RAD STAND — compact three-level sheet-metal stand

**Revision R0.9 — PROVISIONAL DESIGN, dimensionally checked, quote-ready subject to
equipment confirmation.** Not supplier-accepted, not physically tested.

A three-level mild-steel stand, made from seven CNC-laser-cut and CNC-bent pieces of
1.88 mm cold-rolled steel, powder coated textured black, assembled with 23 M5 screws
and locknuts and four screw-in levelling feet using a hex key and one small wrench.

| level | carries | clear opening |
|---|---|---|
| top (626 mm above floor) | Audio-Technica AT-LP120XUSB turntable | 566 × 400 mm flat surface |
| middle | 2 × AR Powered Partner, horizontal, grilles forward | 566 × 400 × 190 mm high |
| bottom | one removable 14.5 in record crate | 566 × 393 × 370 mm high |

**Overall: 570 W × 400 D × 626 H mm** (22.4 × 15.7 × 24.6 in), 22.8 kg of steel,
turntable plinth top at 767 mm. Estimated delivered cost **≈ US$520** (estimate, not a
quote; a leaner $430 configuration is described in `docs/07`).

---

## 1. Where to start

| if you want to… | read |
|---|---|
| understand what was decided and why | `docs/01_recommendation.md` |
| know which numbers are confirmed and which are assumptions | `docs/02_input_register.md` |
| see the evidence that it fits, is strong enough and is stable | `docs/03_fit_and_clearances.md`, `docs/04_structural_validation.md`, `out/calc_report.md`, `out/cad_checks.md` |
| look at it | `out/renders/` (10 rendered views from the CAD) |
| check dimensions | `out/drawings/` (6 A2 sheets, PNG + PDF) |
| order it | `docs/08_upload_guide.md` → `out/step/*.step` |
| build it | `docs/05_assembly_instructions.md` |
| test it safely | `docs/06_inspection_and_test_plan.md` |
| see the cost model | `out/cost_model.md`, `out/bom.csv` |
| know what is *not* proven | `docs/12_validation_matrix.md` |

## 2. The five manufactured parts

| id | part | qty | bends | role |
|---|---|---|---|---|
| P1 | side slab | 2 | 0 | columns, front-to-back shear panels, joint backing |
| P2 | shelf tray | 2 | 4 | turntable shelf and speaker shelf (identical parts) |
| P3 | base tray | 1 | 4 | record-bay floor, foot mounting |
| P4 | rear panel | 1 | 2 | lower-bay shear diaphragm = positive racking path |
| P5 | wall strap | 1 | 1 | anti-tip restraint (part of the standard kit) |

Purchased: 22 × M5×12 button head + flanged locknuts, 4 × M6 stud glides + locknuts,
8 × IsoAcoustics ISO-PUCK mini, 1 × record crate. Full list in `out/bom.csv`.

## 3. Regenerating everything

All geometry, drawings, renders, DXF flat patterns, the BOM and every number in the
calculation report come from one parameter file, `cad/params.py`.

```bash
cd giradisctand
python3 -m venv .venv && .venv/bin/pip install cadquery==2.8.0 ezdxf scipy matplotlib
.venv/bin/python cad/params.py        # print the dimension chains
.venv/bin/python cad/check.py         # CAD interference / fit / alignment checks
.venv/bin/python cad/export.py        # STEP + DXF + export verification
.venv/bin/python cad/drawings.py      # A2 drawing sheets (PNG + PDF)
.venv/bin/python cad/render.py        # rendered views (PNG)
.venv/bin/python cad/bom.py           # BOM + cost model
.venv/bin/python calc/run_all.py      # engineering calculations -> out/calc_report.md
.venv/bin/python make_package.py      # zip everything
```

Versions used here: Python 3.12.3, CadQuery 2.8.0, OCP 7.9.3, ezdxf 1.4.5,
numpy 2.5.5, matplotlib 3.11.2, VTK 9.6.2 (offscreen EGL rendering).

## 4. Honest status

* **Equipment identity is unconfirmed.** The turntable model was inferred by an
  assistant, not stated by the owner. The speakers' variant is unconfirmed; the
  envelope used (155 × 267 × 194 mm, 3.16 kg each) matches the documented
  AR Powered Partner 570 / Advent AV570 and the owner's "10.5 × 6 × 7.9 in", but
  the *orientation of the wedge* is an assumption. See `docs/02`, items E1–E4.
* **No supplier has seen these files.** No upload, no quotation, no acceptance.
* **Nothing has been built or tested.** All structural statements are analytical,
  using a self-written grillage FE validated against two closed-form plate
  solutions; the acoustic claims are qualitative and are handled by a test plan.
* The metal version costs about $520, not $300; the brief's $300 target belongs to
  the plywood alternative, which is delivered separately in `../flatpack/`.
* **Nothing here has been assembled.** The assembly sequence is reasoned and
  geometrically checked (every fastener clears every part and every equipment
  envelope; the crate's removal path is clear at every 50 mm step), but a first build
  can still surprise. Treat `docs/06` as the test that turns this into a verified
  design.

## 5. Package contents

The **cheaper plywood alternative** required by `cncflatpack.md` is in
[`flatpack/`](flatpack/) — 602 × 415 × 630 mm, one 18 mm birch sheet, 6 pieces, 6 dowels,
≈US$331 estimated. It shares this package's equipment tolerances, calculation method and
status language.

```
README.md                     this file
docs/                         13 documents (01-13) (recommendation, register, validation,
                              assembly, test plan, upload guide, sources, log)
cad/                          parametric source (params, sheet metal library,
                              model, checks, exports, drawings, renders, BOM)
calc/                         reproducible engineering calculations
out/step/                     STEP files (1 per manufactured part + assembly)
out/dxf/                       flat patterns, CUT + BEND layers, mm, 1:1
out/drawings/                6 A2 sheets (PNG + PDF)
out/renders/                 10 rendered views (PNG)
out/calc_report.md            full calculation report
out/cad_checks.md             automatic CAD validation results
out/export_verification.json  re-import comparison of every export
out/bom.csv                   bill of materials
out/cost_model.md             cost model and cost drivers
out/input_register.csv        machine-readable input register
GI-RAD-STAND-R09-package.zip  everything above, zipped
flatpack/                     the plywood flat-pack alternative (its own package)
```
