# Two alternative models: speakers standing upright

Both variants are complete parametric designs with their own CAD, exports, drawings,
renders, calculations, BOM and cost model. Nothing here is built or quoted.

| | **A — steel, upright** | **B — plywood, upright** |
| folder | `upright_steel/` | `upright_plywood/` |
| overall (W × D × H) | **486 × 400 × 741** | **518 × 415 × 745** |
| turntable surface / plinth top | 741 / 882 | 745 / 887 |
| material | 1.88 mm CRS, powder coat | 18 mm Baltic birch, sanded |
| pieces / part numbers | 7 / 5 (+1 strap) | 6 / 4 (+1 coupon) |
| assembly | 23 × M5 + 4 M6 feet | 6 × 8 mm dowels, mallet only |
| estimated delivered cost | ≈ US$514 | ≈ US$331 |
| record bay clear | 482 × 394 × 400 (370 usable) | 482 × 394 × 372 |
| speaker bay clear | 482 × 400 × 305 | 482 × 394 × 305 |
| turntable margins (sides / front-rear) | 15.1 / 24.0 | 15.0 / 21.0 |
| speaker acoustic centres | **329 mm apart** | 329 mm apart |
| max shelf deflection | 0.32 mm (base, 40 kg: 1.94 mm) | 0.04 mm (base, 40 kg: 0.12 mm) |
| racking drift at 100 N | 0.65 mm | 0.17 mm (pinned: 0.69) |
| unrestrained tip force (loaded / no records) | 115 / 73 N | ~100 / ~60 N |

**A third option keeps both orientations open** — `dual_steel/`:

| | **C — steel, dual-mode bay** |
|---|---|
| overall | **570 × 400 × 741** |
| speaker bay | 566 × 400 × **305** (takes the pair upright *or* lying down) |
| acoustic centres | 413 mm upright / 287 mm lying down |
| cost estimate | ≈ US$525 |
| the catch | it is as wide as the lying-down design (+43 % on the turntable's footprint) and, when you do lie the speakers down, 115 mm of the bay is visible empty air |

Sizing the bay for both orientations means sizing it for the **union** of the two
envelopes: 566 W (lying-down width) × 305 H (upright height). There is no smaller bay that
takes both, which is why variant C is the parent's width with variant A's height.

## What the upright orientation changes, and why it is worth considering

Standing the Powered Partner up (150 W × 196 D triangular plan × 270 H) instead of laying
it down removes the width problem entirely:

| | speakers horizontal | speakers upright |
|---|---|---|
| speaker pair envelope | 534 mm | **282 mm** |
| what sets the stand width | the speakers | **the turntable (452)** |
| overall width | 570 (steel) / 602 (plywood) | **486 / 518** |
| turntable side margin | 57 mm | **15 mm** (footprint is finally close to the deck) |
| footprint area vs the turntable's | +43 % | **+22 %** |
| baffle axis | tilted up 38.6° (the product's own wedge) | **vertical** — aims at a seated listener |
| speaker acoustic centres | 287 mm | **329 mm** |
| platter height | 767 mm | **882 mm** (standing cue height) |

Cost: 115 mm taller, and the speaker bay becomes a 305 mm void that dominates the
elevation. The stand reads as a narrow tower rather than a low console.

**The one thing to check before choosing:** the upright orientation is the AR 570's own
"tower" position (150 × 270 × 196 per the AR spec sheet), so the cabinet is being used as
designed — but the baffle is on the *diagonal* face of the triangular plan, so each
cabinet must be **toed in about 20°** to aim at the listener. Both variants allow for that
(there is 188 mm of clearance between the cabinets and 6 mm at each side; the modelled
envelope is the *rotated* footprint, 141 × 235 mm).

## What is shared with the parent designs (and what is not)

Shared, unchanged: equipment tolerances and the input register, fastener family and joint
detail (steel), dowel-tab-slot joinery (plywood), the validated grillage FE, the
stability method, the drawing and rendering pipeline, and the status language. The
parent's independent review findings (`../docs/11_review_log.md`) are already folded in:
bolt heads inboard / locknuts outboard, foot holes in the base tray flat pattern,
closed obround slots with the long axis in the correct flat direction, the strap attached
through a real hole in the top tray, and the clamped-joint moment mechanism described
correctly.

Not done, and stated as such in each variant's own documents: no build, no supplier
quote, no independent review of the *variant* geometry, and the same outstanding
equipment measurements (which face of the speaker rests on the shelf is now settled by
choosing upright — but the cabinet's identity, the turntable model and the record
container are still provisional).

## Regenerating any variant

```bash
cd variants/upright_steel          # or upright_plywood
../../.venv/bin/python cad/check.py      # steel only: interference / fit / access
../../.venv/bin/python cad/export.py     # DXF + STEP + export verification (+nest)
../../.venv/bin/python calc/run_all.py   # calculations
../../.venv/bin/python cad/drawings.py
../../.venv/bin/python cad/render.py
../../.venv/bin/python cad/bom.py
../../.venv/bin/python make_package.py   # plywood variant only
```
