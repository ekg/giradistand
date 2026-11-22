# 04 — Validation summary and matrix

Full numbers: `out/calc_report.md` (calculations), `out/cad_checks.md` (geometry).
Evidence classes: **A** analytical, **C** CAD-checked, **S** supplier rule applied,
**P** physically tested (**none**).

## 1. Structure in one page

| check | result | criterion | verdict |
|---|---|---|---|
| shelf deflection, top (15 kg on 4 feet) | 0.03 mm (0.19 mm with pinned ends) | ≤ 1.5 mm | PASS |
| shelf deflection, top (15 kg uniform) | 0.05 mm | ≤ 1.5 mm | PASS |
| shelf deflection, middle (10 kg on 8 pads) | 0.05 mm | ≤ 1.5 mm | PASS |
| shelf deflection, base (40 kg uniform) | 0.12 mm | ≤ 2.5 mm | PASS |
| maximum bending stress | 1.35 MPa | ≤ 38 MPa (plywood bending) | PASS, factor 28 |
| tab bearing in the slot | 0.027 MPa | ≤ 8 MPa | PASS, factor 294 |
| tab shear at the dowel line | 0.039 MPa | ≤ 1 MPa (panel shear, conservative) | PASS |
| racking side-to-side, clamped joints | 0.17 mm at 100 N | ≤ 2.0 mm | PASS |
| racking side-to-side, pinned joints (worst case) | 0.69 mm at 100 N | ≤ 2.0 mm | PASS |
| racking front-to-back | 0.012 mm elastic, ≤ 0.25 mm with connection clearance | ≤ 2.0 mm | PASS |
| tipping, unrestrained, loaded | ~95–100 N at 900 mm | ≥ 60 N | PASS |
| tipping, unrestrained, records removed | ~60 N at 900 mm | ≥ 60 N | MARGINAL → strap supplied |
| tipping, restrained (strap) | not credible | — | PASS by design |
| sliding | 170 N at μ = 0.3 | ≥ 120 N | PASS |

**Why the numbers are so far below the limits.** 18 mm plywood is 30× stiffer in bending
than the 1.88 mm steel plate of the other design, and its bending strength is a sixth of
steel's — but the section modulus is 55× larger. The consequence is honest to state: the
thickness is **not** chosen for strength. It is chosen because the joint needs an 18 mm
tab, because a thinner panel's edges look and wear badly in a knock-down kit, and because
18 mm is the stock a router shop actually keeps. A 15 mm version would also pass; it would
save about $12 of material and make every joint more fragile.

## 2. Where the model could be wrong

| idealisation | direction | magnitude |
|---|---|---|
| grillage FE (validated against two closed-form plate solutions in the steel package: +15 % / +8 % flexible) | conservative | — |
| shelves treated as clamped at the slots (they can rotate 0.076° before bearing) | optimistic | bounded by the pinned run: 0.19 mm vs 0.03 mm |
| no long-term creep of plywood under 40 kg | optimistic | the stress is 1.35 MPa against 38 MPa, so creep is negligible |
| panel edges assumed square and undamaged | optimistic | a crushed tab edge loses bearing area, not stability |
| moisture movement of plywood (±0.3 % across the grain) | not modelled | ~1 mm over 394 mm; the slot clearance and the ±0.1 mm Y location are unaffected |
| payloads 15/10/40 kg | assumption | linear scaling, factor 28 in reserve |

## 3. Atmosphere and acoustics

The plywood stand is a different acoustic object from the steel one: birch ply is
heavily damped compared with sheet steel, so panel ringing is much less likely — but
plywood is also a worse conductor of vibration *into* the floor at low frequencies, which
is generally good for a turntable. The speaker isolators are the same specification
(4 per speaker, 44 × 24 mm, 29 % of rated load), the speakers do not touch the frame, and
the shelf under them is a solid 18 mm panel rather than a folded tray. Nothing about this
is measured; the staged test plan is `../../docs/06` and applies unchanged.

## 4. Validation matrix

| # | requirement | criterion | evidence | result | unresolved |
|---|---|---|---|---|---|
| A1 | turntable fits with a margin | ≥ 20 mm | C: 57 / 21 mm | PASS | deck unconfirmed |
| A2 | feet fully supported on a flat face | no feature under the feet | C: shelf top is flat, only 4 foot holes in the *base* shelf | PASS | foot positions assumed |
| A3 | two speakers horizontal, grilles forward | bay ≥ 534 + gaps | C: 566 vs 534 + 12 + 20 | PASS | variant unconfirmed |
| A4 | speaker isolation + loaded height | bay ≥ 155 + pad + clearance | A/C: 190 ≥ 178 | PASS | pad compression estimated |
| A5 | one removable record container | 0 interference over the path | C: 0.000 mm³ at 0–400 mm (`out/cad_checks.md` §4) | PASS | container not chosen |
| A6 | no two-crate assumption | explicitly evaluated | C: 736.6 > 566 | PASS (surfaced) | — |
| B1 | shelf deflection | ≤ 1.5 / 1.5 / 2.5 mm | A: 0.03 / 0.05 / 0.12 mm | PASS | payloads assumed |
| B2 | shelf stress | ≤ 38 MPa | A: 1.35 MPa | PASS | — |
| B3 | joint bearing / shear / dowel | ≤ 8 / 1 / 8 MPa | A: 0.027 / 0.039 / 0.69 MPa | PASS | — |
| B4 | racking both directions | ≤ 2.0 mm at 100 N | A: 0.17 / 0.69 / 0.012–0.25 mm | PASS | joints not measured |
| B5 | tipping, unrestrained | ≥ 60 N at 900 mm | A: ~95 N loaded, ~60 N records-removed | MARGINAL → strap | strap needs a wall fixing |
| B6 | tipping, restrained | not credible | design | PASS by design | — |
| B7 | sliding | ≥ 120 N | A: 170 N | PASS | floor friction assumed |
| C1 | material and sheet size | stocked, one sheet | S: to be confirmed by the shop | PENDING QUOTE | stock not verified |
| C2 | all cuts are through-cuts, one face | no pockets/dados | C: every feature is a through-cut | PASS | shop must agree |
| C3 | cutter-compatible internal corners | ≥ R3.2 | C: R4 dogbones in slots, R6 outlines | PASS | — |
| C4 | part size within the machine | ≤ sheet | C: largest 638 × 394 | PASS | — |
| C5 | nesting | one sheet, grain-aligned | C: 1 sheet, 56 % used, 12 mm webs | PASS (proposal) | shop may re-nest |
| C6 | DXF validity | closed contours, mm, feature counts | C: all five parts `ok` | PASS | — |
| C7 | fit coupon | present, same stock, 3 clearances | design: P5 | PASS (by design) | **coupon test not run** |
| D1 | tool-free assembly | mallet only | design: 6 dowels | PASS (by design) | not built |
| D2 | no home machining | none except the wall pilot | `docs/03` §5 | PASS (by design) | — |
| D3 | reversible | take apart without damage | design: lift dowels | PASS (by design) | not built |
| D4 | assembly path checked | no trapped part | two-step ladder sequence, checked on the CAD (side 2 slides over 3 tabs with 0.1 mm clearance each way) | PASS (reasoned) | **not built** |
| D5 | feet / levelling | ±5 mm, floor-protecting | design: same M6 glides as the steel version | PASS (by design) | — |
| E1 | BOM and cost | itemised, dated, labelled estimate | `out/bom.csv`, `out/cost_model.md` | PASS (estimate) | no quote |
| E2 | drawings | dimensioned, revisioned, grain stated | `out/drawings/` F1–F3 | PASS | — |
| E3 | renders | assembled, exploded, sections | `out/renders/` 6 views | PASS | — |
| E4 | calculations | reproducible, sourced, units | `calc/run_all.py` → `out/calc_report.md` | PASS | — |
| E5 | upload guide | exact files, quantities, operations | `docs/05` §5 | PASS | not executed |
| E6 | independent review | findings resolved | not performed for this variant — the steel design's review (`../../docs/11`) drove the shared conventions (equipment envelopes, tolerance thinking, status language), but **no reviewer has seen these files** | **NOT RUN** | schedule one before ordering |
| F1–F5 | physical tests (deflection, joint tightness, assembly time, racking, rattles) | — | — | **NOT RUN** | first build |

## 5. Release status

> **Provisional design; the files are fit to *quote* but not to cut.** Blockers:
> (1) measure the panel thickness and run the fit coupon; (2) confirm the speaker's
> resting face and the turntable model; (3) get the shop to confirm stock, tab removal and
> sanding. None of these is a design change — they are measurements and confirmations.
