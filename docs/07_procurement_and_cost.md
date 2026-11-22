# 07 — Procurement, cost and the quote route

**No live quotation was obtained. No upload was performed. No order was placed.**
Everything below is a *dated estimate built from stated rates*, plus supplier-listed
prices where they exist.

## 1. What to order, from whom

**Fabrication — SendCutSend** (chosen because its published rules for 0.074 in mild
steel — radius 1.60 mm, K 0.40, bend deduction 3.277 mm — are exactly the values this
model was built with, and because it prices bent parts instantly from a STEP file).

| upload file | qty | material | thickness | bending | finish |
|---|---|---|---|---|---|
| `out/step/P1_SIDE_SLAB.step` | 2 | Mild Steel (CRS), 0.074 in | 1.88 mm | — | powder coat BK01 |
| `out/step/P2_SHELF_TRAY.step` | 2 | Mild Steel (CRS), 0.074 in | 1.88 mm | 4 bends, 90° down | powder coat BK01 |
| `out/step/P3_BASE_TRAY.step` | 1 | Mild Steel (CRS), 0.074 in | 1.88 mm | 4 bends, 90° down | powder coat BK01 |
| `out/step/P4_REAR_PANEL.step` | 1 | Mild Steel (CRS), 0.074 in | 1.88 mm | 2 bends, 90° toward +Y | powder coat BK01 |
| `out/step/P5_WALL_STRAP.step` | 1 | Mild Steel (CRS), 0.074 in | 1.88 mm | 1 bend, 90° | powder coat BK01 |

Add **"Deburring"** to every part. Do **not** add hardware insertion or tapping: there
are no threads on any part by design. Step-by-step upload detail in `docs/08`.

**OSH Cut** is the credible alternative: same uploaded STEP files, its own published
bending rules (radius varies with tooling, so re-check the flat patterns), typically
competitive on 3–5 parts. Quote both; the files are supplier-neutral.

## 2. Bill of materials (full list in `out/bom.csv`)

| item | spec | qty | unit (USD) | ext |
|---|---|---|---|---|
| P1–P5 fabrication, powder coated | see above | 6 pieces | — | see below |
| M5 × 12 button head, ISO 7380-1, A2-70 | 3 mm hex socket | 22 | ~0.42 | 9.24 |
| M5 flanged nylon-insert locknut, DIN 6923 | 8 mm AF | 22 (+2 spare) | ~0.34 | 8.16 |
| M6 levelling glide, male stud | M6 × 40, 23 mm base | 4 | ~1.85 | 7.40 |
| M6 flanged locknut, DIN 6923 | 10 mm AF | 4 | ~0.38 | 1.52 |
| IsoAcoustics ISO-PUCK mini (box of 8) | 44 dia × 24 mm, 2.75 kg each | 1 box | list | 79.00 |
| Groove Crate 14.5 in record crate | 368 × 368 × 359 mm, HDPE | 1 | list | 34.00 |
| 3M 2552 damping tape (optional) | 25 mm × 5 m | 1 | ~22.00 | 22.00 |
| Wall fixings for P5 | 2 × 4.0 × 40 screw or anchor | 2 | ~0.30 | 0.60 |

Prices marked "list" exist at the supplier; prices marked "~" are estimates.

## 3. Cost model — **estimate, ±25 %**

| line | USD | basis |
|---|---|---|
| laser cutting | 141.41 | $6/part + $55/m² + $0.90/m of cut, min $9/part |
| CNC bending (15 bends) | 60.00 | $3.50/bend, min $9/part |
| deburring | 14.00 | $2/part |
| powder coating | 73.60 | $6/part + $18/m², min $10/part |
| **fabrication subtotal** | **288.97** | |
| purchased items (incl. ISO-Pucks, crate, damping) | 161.24 | |
| shipping | 28.00 | estimate |
| sales tax @ 8.25 % | 39.45 | assumption on rate and on taxability |
| **TOTAL ESTIMATE** | **517.66** | |

Rounding to a sensible planning number: **≈US$470–560 delivered (model output: $518)**, of which about
US$290 is fabrication and US$160 is purchased parts.

## 4. Is that reasonable?

It is *not* cheap, and it is worth being clear about why. A one-off metal stand with
five distinct parts, four bends, a bend-heavy tray geometry and a powder coat has a
floor of roughly $250–300 in fabrication because per-part setup dominates every line
item. Within that floor this design is already lean:

* 5 part numbers for 6 pieces (the two biggest parts are shared);
* zero hardware insertion, zero tapping, zero welding, zero secondary machining;
* one finish, one material, one thickness;
* the largest part is 620 × 453 mm flat, well inside every supplier limit, so there is
  no split-part penalty.

## 5. The one cheaper alternative that does not compromise anything

**Skip the optional damping tape (−$22) and take the bare-metal route:** order the
parts deburred but unfinished and coat them at home (one aerosol of etch primer and one
of matte black, ~$25, about 2 hours). That saves roughly $60–70 **but breaks the
"arrives ready to assemble" promise** — coating at home means coating the parts before
assembly, and edges get less coverage than a shop's. It is offered as an explicit
choice, not as a hidden saving.

Two cheaper-looking alternatives are **rejected** on purpose:

* **Drop P4 (rear panel)** — saves ~$30 and removes the only friction-independent
  racking element. Not acceptable.
* **0.059 in (1.5 mm) sheet** — saves ~20 % of material cost but roughly doubles every
  deflection (stiffness ∝ t³); every shelf check would have to be re-run and the safety
  factors fall from 12 to about 4. Offered only with that caveat, not adopted.

## 6. What remains unknown

* The actual SendCutSend price (no upload; their checkout price is authoritative).
* Lead time (their published figure is +1–2 days for bending and +3–5 days for coating,
  on top of cutting; not verified for this order).
* Shipping cost and whether tax is charged in your state.
* Current ISO-PUCK mini and crate prices.
* Whether your floor needs the felt-pad variant of the feet.
