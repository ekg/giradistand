# Variant A — steel stand, speakers UPRIGHT

**486 × 400 × 741 mm, 5 part numbers / 7 pieces of 1.88 mm CRS, ≈US$514 estimated.
Revision U0.9 — provisional, dimensionally checked, not built, not quoted.**

Same construction, process and joint as the parent steel design (`../../README.md`);
only the equipment envelopes and the vertical stack differ.

## Why this variant exists

Laying the Powered Partners down forces the stand to 570 mm because the pair is 534 mm
wide. Standing them up (150 × 196 mm triangular plan, 270 high — the AR 570's own tower
position) drops the pair to 282 mm, so the **turntable finally sets the width**: 486 mm,
with 15 mm margins instead of 57. The footprint is +22 % on the turntable's instead of
+43 %, the baffles stand vertical (they are on the diagonal face, so each cabinet is toed
in 20°), the acoustic centres are 329 mm apart instead of 287, and the platter comes up to
882 mm — a standing cue height instead of a coffee-table one.

The price is height: 741 mm of stand. It is a tower, not a console.

## Dimensions and clear openings

| item | mm | in |
|---|---|---|
| overall | 486 × 400 × 741 | 19.13 × 15.75 × 29.16 |
| turntable surface / plinth top | 741 / 882 | 29.16 / 34.74 |
| record bay clear | 482 × 394 × 400 (370 usable under the shelf above) | 18.98 × 15.51 × 14.65 |
| speaker bay clear | 482 × 400 × 305 | 18.98 × 15.75 × 12.01 |
| turntable surface | 482 × 400, flat, no fixings | 18.98 × 15.75 |
| speaker envelope each (toed in 20°) | 141 wide × 235 deep × 270 high | 5.55 × 9.25 × 10.63 |
| gap between cabinets | 188 | 7.41 |
| support polygon (feet) | 414 × 366 | 16.30 × 14.41 |

Height chain: 32 (glide + base tray) + 400 (record bay) + 1.88 + 305 (speaker bay:
270 cabinet + 23 compressed isolator + 12 handling) + 1.88 = 741.

## Verification actually performed

* `out/cad_checks.md` — **all checks pass**: 0 mm³ interference between all part pairs;
  0 mm³ between the structure and the turntable, both speaker envelopes, their 6 isolators
  and the crate; all 22 bolts clear every part **and** every equipment envelope (that is
  also the hole-alignment proof); the crate slides out with 0 interference at every 50 mm
  step; the strap hole clears the turntable footprint.
* `out/export_verification.json` — every STEP re-imported (1 solid, identical bounding
  box, volume delta 0.0000 %); every DXF re-read (closed outline, correct hole/bend
  counts, correct arc radii, holes inside the outline).
* `out/calc_report.md` — top tray 0.32 mm under 15 kg, middle 0.27 mm under 10 kg on six
  isolators, base 1.94 mm under 40 kg; max stress 47 MPa against a 102.5 MPa limit;
  racking 0.65 mm at 100 N side-to-side and 0.001 mm front-to-back; tip force 115 N loaded
  / 73 N with the records out (the strap is supplied for that case); joint slip margin
  27:1 and joint opening moment 45 N·m against a 4.75 N·m demand.
* `out/drawings/` — six A2 sheets regenerated from this geometry (GA-01U, P1-02 … P5-07).
* `out/renders/` — 12 views including the loaded isometric, front, side, top, rear,
  underside, exploded, crate-removal and two sections.

**Not performed:** build, load test, supplier review, acoustic test. The narrow tower has
a smaller side-stability margin than the wide parent (1.3 : 1 at a 100 N push instead of
1.7 : 1) because the base tray narrowed with the stand — still above the 60 N criterion,
and the wall strap is supplied as standard.

## Files

Same structure as the parent: `cad/` (params, sheetmetal, model, check, export, drawings,
render, bom), `calc/`, `out/step/`, `out/dxf/`, `out/drawings/`, `out/renders/`,
`out/calc_report.md`, `out/cad_checks.md`, `out/bom.csv`, `out/cost_model.md`.

Upload the six STEP files in `out/step/` (P1 ×2, P2 ×2, P3, P4, P5) exactly as described
in `../../docs/08_upload_guide.md` — same material, thickness, finish and notes; the only
difference is the part dimensions. `out/step/upload_parts.step` is the multi-body
alternative.
