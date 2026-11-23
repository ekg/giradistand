# Variant B — plywood flat-pack, speakers UPRIGHT

**518 × 415 × 745 mm, one 18 mm Baltic birch sheet, 6 pieces, 6 dowels, ≈US$331
estimated. Revision WU0.9 — provisional, dimensioned, checked, not built, not quoted.**

Same joinery and process as `../../flatpack/`; the speakers stand up and the stand
narrows accordingly.

## Why this variant exists

Upright speakers (150 × 196 triangular plan, 270 high) make the pair 282 mm wide instead
of 534, so the turntable sets the width: 518 mm overall with 15 mm margins, and the
footprint is +22 % on the turntable's instead of +43 %. Combined with the flat-pack
process this is the cheapest of the four designs: **≈US$331 delivered, $240 of it
material + CNC**, and no tools at all for assembly beyond a mallet.

Cost of the choice: 745 mm tall (a tower), and the 305 mm speaker bay dominates the
elevation.

## Dimensions and clear openings

| item | mm | in |
|---|---|---|
| overall | 518 × 415 × 745 | 20.39 × 16.34 × 29.33 |
| turntable surface / plinth top | 745 / 887 | 29.33 / 34.91 |
| record bay clear | 482 × 394 × 372 | 18.98 × 15.51 × 14.65 |
| speaker bay clear | 482 × 394 × 305 | 18.98 × 15.51 × 12.01 |
| turntable surface | 482 × 394 flat (no flanges intrude) | 18.98 × 15.51 |
| speaker envelope each (toed in 20°) | 141 × 235 × 270 | 5.55 × 9.25 × 10.63 |
| gap between cabinets | 188 | 7.41 |
| support polygon (feet) | 414 × 304 | 16.30 × 11.97 |

Height chain: 32 (glides) + 372 (record bay — no flange intrudes in plywood) + 18 +
305 (speaker bay: 270 + 23 + 12) + 18 = 745.

Note the plywood record bay needs only 372 mm for the same 358.8 mm crate, because
plywood shelves have no folded flange hanging into the opening. That is why the plywood
tower is only 4 mm taller than the steel one despite 36 mm thicker side panels.

## Verification actually performed

* `out/cad_checks.md` — all checks pass: 0 mm³ interference between parts; 0 mm³ between
  the structure and the turntable / both speaker envelopes / 6 isolators / crate; the
  crate slides out with no interference at every 100 mm step; every STEP re-imported with
  identical bounding boxes and 0.0000 % volume difference; every DXF re-read (closed,
  correct feature counts and arc radii).
* Nesting: one 1525 × 1525 sheet, 55 % utilisation, 12 mm webs, grain along the sheet's
  long axis.
* `out/calc_report.md` — shelf deflections 0.01–0.12 mm, max bending stress 1.09 MPa
  against 38 MPa (factor 35), racking 0.17 mm at 100 N clamped / 0.69 mm pinned,
  tab bearing 0.02 MPa against 8 MPa. The 18 mm panel thickness is set by the joints and
  the exposed edge, not by strength.
* `out/drawings/` — F1U assembly, F2 parts + joinery detail + fit coupon, F3 nest.
* `out/renders/` — 6 views.

**Not performed:** build, coupon test, supplier quote, independent review of this
variant's geometry.

## Before cutting

Unchanged from `../../flatpack/docs/02_inputs.md`, and still blocking:
1. **Measure the actual panel thickness and cut the fit coupon first** (P5, three slot
   clearances). The slot width is the measured thickness + the coupon result.
2. Confirm the turntable model (any deck ≤ 482 × 394 fits).
3. Confirm the record container (any ≤ 482 × 394 × 372 fits).
4. Ask the shop to confirm stock, **holding-tab removal** and sanding.

## Files

Identical structure to `../../flatpack/`: `cad/`, `calc/`, `docs/`, `out/` (dxf, step,
drawings, renders, calc_report.md, cad_checks.md, bom.csv, cost_model.md) and
`FLATPACK-WU09-package.zip` on regeneration.
