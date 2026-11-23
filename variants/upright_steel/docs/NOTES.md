# Variant A notes: what changed relative to the parent design

All reasoning that is not specific to the upright speakers is unchanged and lives in
`../../../docs/` — read `01_recommendation.md` (decisions), `02_input_register.md`
(measurements), `04_structural_validation.md` (method), `05_assembly_instructions.md`
(sequence), `08_upload_guide.md` (ordering) and `11_review_log.md` (review findings, all
of which are already fixed in this variant).

## Changes

| item | parent (speakers lying down) | variant A (upright) |
|---|---|---|
| speaker envelope | 155 H × 267 W × 194 D, 3.16 kg | 270 H × 150 × 196 triangular plan, 3.5 kg, toed in 20° |
| isolators | 4 per speaker | **3 per speaker** (one in from each triangle corner; the 44 mm pad cannot sit in the acute corners) |
| overall width | 570 | **486** |
| interior width | 566.24 | 482.24 |
| speaker bay height | 190 | **305** |
| overall height | 626 | **741** |
| turntable margin (sides) | 57.1 | 15.1 |
| base tray width / feet | 566.24 / ±255 | 482.24 / ±207 |
| tray flat width | 619.7 | 535.7 |
| side slab height | 611.9 | 726.9 |

Unchanged: material, thickness, bends, radius/K/bend deduction, fastener family and
orientation (button head inboard, locknut outboard), rear panel as the lower-bay shear
diaphragm, foot hardware, strap, the strap hole in the top tray, and the slot geometry.

## Assembly differences

Steps 1–9 of `../../../docs/05_assembly_instructions.md` are unchanged (the trays are the
same parts, just narrower). Only two things differ:

* **Step 10** — three isolators per speaker, not four. Place them inside the triangle:
  one 36 mm in from the right-angle corner along its bisector, one 74 mm in from each
  acute corner along their bisectors (the model's `pad_points()` prints the exact
  coordinates; the positions are also shown on the render `02_front_loaded.png`).
* **Step 11** — set each speaker upright on its three isolators with the **diagonal
  grille face turned 20° toward the listening position** (left cabinet turned clockwise
  seen from above, right cabinet anticlockwise). The 188 mm gap between the cabinets
  gives room to do this without touching the frame.

## What to watch first on a real build

1. **Toe-in clearance.** The modelled envelope is the rotated footprint (141 × 235). If
   your cabinets are bigger than the documented AR 570, check the swing before loading.
2. **Three-point support.** A 3.5 kg, 270 mm tall cabinet on three 24 mm pads is stable
   but lively; if it rocks, the pads are not all contacting — check with a feeler gauge
   under the cabinet's base edge.
3. **Height.** 741 mm puts the platter at 882. Confirm that suits how you actually cue
   records; it is 115 mm taller than the parent design.
4. **Side stability.** The base is 414 mm wide instead of 524; fit the strap.
