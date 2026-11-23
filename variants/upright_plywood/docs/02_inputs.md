# 02 — Input register and the measurements still needed (variant B)

Status: **[U]** owner statement · **[M]** manufacturer document · **[P]** design
assumption · **[C]** CAD-derived (guaranteed by construction). Nothing here is a
certified rating.

## A. Equipment (identical source base to the steel package — see `../../docs/09_sources.md`)

| # | item | value | status | consequence if wrong |
|---|---|---|---|---|
| E1 | turntable model | AT-LP120XUSB (assistant-introduced, unconfirmed) | **[P]** | any deck ≤ 566 × 394 fits |
| E2 | turntable body | 452.0 × 352.0 × 141.6 mm, 8.0 kg | **[M]** A-T manual | needs `D_OVER` or `SPK_*` changes only if larger |
| E3 | turntable feet | ~42/45 mm inboard, Ø38, ±8 mm adjustable | **[P]** | shelf top is flat and featureless; any pattern inside 500 × 300 is fine |
| E4 | rear connectors | ~35 mm plug projection | **[P]** | open rear edge; 80 mm wall clearance stated |
| E5 | dust cover open | projects ~40 mm rearward, 360 mm up | **[P]** | clearance note only |
| E6 | speaker variant | UPRIGHT envelope: 150 × 196 triangular plan × 270 high, 3.5 kg | **[M]** AR 570 spec sheet | bay height is driven by it |
| E7 | speaker standing orientation | upright on the triangular base, toed in 20° | **[U]** chosen for this variant | if the cabinet is bigger than documented, check the toe-in swing |
| E8 | speaker rear hardware | RCA / DC / AC / switch on one of the vertical faces | **[M]** | ~150 mm clear behind each cabinet in this orientation |
| E9 | speaker mounting holes | 3 × 8-32 + 7/16-10 in the end caps | **[M]** | deliberately unused (isolation) |

## B. Storage

| # | item | value | status | consequence |
|---|---|---|---|---|
| S1 | container | Groove Crate 14.5 in — 368.3 × 368.3 × 358.8 mm | **[M]** for that product, **[P]** as a choice | any ≤ 482 × 394 × 372 |
| S2 | loaded mass | ~22 kg (80–100 LPs) | **[P]** | design payload 40 kg |
| S3 | two crates | will not fit side by side (736.6 vs 482) | **[C]** | a 2-crate stand must be ≈790 wide |
| S4 | removal path | slides forward, unobstructed | **[C]** `out/cad_checks.md` §4 | — |

## C. Material and process

| # | item | value | status | consequence |
|---|---|---|---|---|
| W1 | panel | 18 mm Baltic birch, 13-ply, B/BB | **[P]** supplier to confirm stock | — |
| W2 | **actual thickness** | 18.0 nominal; expect 17.4–18.4 | **[P] — MUST BE MEASURED** | sets the slot width; a wrong slot is a scrap kit |
| W3 | sheet size | 1525 × 1525 (5 × 5 ft) | **[P]** | the nest uses 56 % of one sheet |
| W4 | cutter | Ø6.35 (1/4 in) | **[P]** | internal radii ≥ R3.2; design uses R4/R6 |
| W5 | routing tolerance | ±0.2 mm on profiles | **[P]** | absorbed by the slot clearance |
| W6 | edge sanding | R2 edges, faces 120 grit | **[P]** shop operation | is a cost line, not an assumption to drop silently |
| W7 | holding tabs | none on mating or visible faces | **[P] requirement** | must be confirmed with the shop |
| W8 | payloads | 15 / 10 / 40 kg | **[P]** | utilisation scales linearly, with a factor of 28 in reserve |
| W9 | lateral disturbance | 100 N at 900 mm reported; 60 N criterion | **[P]** | see `docs/04` |

## D. Measurements still needed (in priority order)

**1 — Panel thickness (blocks cutting).** Measure the actual sheet in at least four
places away from the edges with a caliper. If it reads 17.8, the slot becomes 18.0, not
18.2. The fit coupon exists to confirm this before the production parts are cut.

**2 — Speaker envelope check.** Stand one speaker upright and measure (a) the height to the
top of the cabinet (270 expected), (b) the triangular base's legs (150 × 196 expected).
If either is larger, the speaker bay and the toe-in clearance change.

**3 — Turntable model and body depth.** Confirm the plate under the plinth and measure
the plinth's depth including any rear connector recess. Anything up to 482 × 394 fits.

**4 — Record container.** If you already own one, measure its outside dimensions; the bay
takes 482 × 394 × 372.

**5 — Wall gap where the stand will live.** The strap's foot slot suits 50–110 mm; a
wider gap needs a longer foot (one parameter).

Nothing else is open. Every number above feeds `cad/params.py`; changing one regenerates
the DXF, STEP, drawings, renders, calculations and BOM in about three minutes.
