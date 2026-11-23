# 05 — BOM, cost model, upload guide and cleanup requirements

**No quote was obtained. Nothing was uploaded. Nothing was ordered.** Figures are a
dated, rate-based estimate plus supplier list prices.

## 1. Bill of materials

| id | part | qty | material | size (mm) | notes |
|---|---|---|---|---|---|
| P1 | side panel | 2 | 18 mm Baltic birch | 415 × 745 | 3 slots 150.2 × 18.2 with R4 dogbones |
| P2 | shelf | 2 | 18 mm Baltic birch | 554 × 394 | 4 tabs 150 × 18, 4 dowel holes 8.4 |
| P3 | base shelf | 1 | 18 mm Baltic birch | 554 × 394 | as P2 + 4 foot holes 6.6 |
| P4 | anti-tip strap | 1 | 18 mm Baltic birch | 245 × 25 | 1 slot 6.6 × 40, 1 hole 6.6 |
| P5 | fit coupon | 1 | same stock | 150 × 90 | 3 slots at +0.10/+0.20/+0.30 |
| — | birch dowel Ø8 | 6 × 40 mm | — | — | from one 1 m dowel |
| — | M6 glide, male stud | 4 | polymer base | M6 × 35, Ø23 base | + 4 × DIN 6923 M6 locknuts |
| — | isolation pads | 8 | Sorbothane 30 duro | 50 × 50 × 6 | or upgrade to ISO-PUCK mini (8-pack, ~$79) |
| — | M5 × 12 button head + locknut | 1 | A2 | — | for the strap's foot |
| — | wall fixings | 2 | — | 4 × 40 screw or anchor | user supplies, matched to the wall |

Full machine-readable list: `out/bom.csv`.

## 2. Cost model (ESTIMATE)

| line | USD | basis |
|---|---|---|
| plywood, 1 sheet 1525 × 1525 × 18 Baltic birch | 110 | supplier list price; verify locally |
| CNC routing, one sheet (outlines + slot/dogbone pass) | 95 | ~1.2 h at ~$80/h; **quote required** |
| edge + face sanding | 35 | shop operation, per sheet |
| dowels, feet, isolators, fixings | 32 | itemised |
| shipping (sheet-sized parcel) | 32 | estimate |
| sales tax 9 % | 27 | assumption on rate |
| **TOTAL** | **331** | |

**Material + CNC = $240**, inside the brief's $220–250 allowance. The total is ~$31 over
the $300 target, and the gap is shipping + tax.

Levers, in order of least damage:
1. birch-faced **poplar** core instead of Baltic birch: −$35 (more voids, weaker edges);
2. **collect in person**: −$32;
3. **no shop sanding**: −$35, but you then sand 3 m of edge and 2.5 m² of face yourself,
   which is exactly the work the brief says not to move onto the owner.

Taking 1 and 2 lands at ≈$264 — comfortably under target with the joint quality intact.
Taking all three lands at ≈$230 but breaks the "arrives ready to assemble" promise.

## 3. Sheet utilisation

One 1525 × 1525 sheet; parts total 1.29 m² (55 %). Longest part 554 mm. Grain along the
sheet's long axis for every part. Nest proposal in `out/dxf/NEST_1525x1525.dxf` and
`out/drawings/F3_sheet_nest.png`. **The shop may re-nest**; the individual part DXFs in
`out/dxf/` are authoritative and no part file depends on the nest.

## 4. Cleanup and finish — who does what

| operation | who | note |
|---|---|---|
| routing (all cuts) | shop | every feature is a through-cut, one setup per face |
| holding-tab removal | **shop** | must not be on mating or visible faces; if unavoidable, underside + removed by the shop |
| edge sanding R2, face 120 grit | shop | is a priced line in `docs/05` §2 |
| finish (oil/wax/lacquer) | owner, or shop as a quoted extra | **not included**; if applied before assembly allow for film thickness in the slots |
| wall pilot hole (3 mm) | owner | the only home operation outside the kit |
| dowels, glides, pads, strap bolt | owner | hand assembly |

## 5. Upload guide

1. Get a quote from **Pixels to Prototype** (their form returns a reviewed quote, not an
   instant price) and, if you want a comparison, from a local CNC shop. Send:
   * `out/dxf/P1_SIDE_PANEL.dxf` ×2
   * `out/dxf/P2_SHELF.dxf` ×2
   * `out/dxf/P3_BASE_SHELF.dxf` ×1
   * `out/dxf/P4_WALL_STRAP.dxf` ×1
   * `out/dxf/P5_FIT_COUPON.dxf` ×1
   * optionally `out/dxf/NEST_1525x1525.dxf` as a nesting suggestion
2. Ask for: **18 mm Baltic birch, B/BB, void-free core**; **all cuts through, one face**;
   **no holding tabs on mating or visible faces**; **edges sanded R2, faces 120 grit**;
   **no finish**.
3. Tell them the **slot width is 18.2 mm nominal but must be set to the measured panel
   thickness + the coupon result** — and ask them to cut **P5 first** from the same sheet
   and report its result before cutting the rest. (If they will not do a two-stage order,
   have them cut everything with +0.20 mm and accept the risk, or measure the sheet
   yourself before ordering.)
4. Do **not** ask for a laser/waterjet cut: 18 mm birch needs routing, and the dogbones
   and R6 corners are routing features.
5. Confirm the price against `docs/05` §2 before ordering. If material + CNC exceeds
   $280, get a second quote; if it exceeds $320, take the poplar-core or collection lever.

## 6. What is still unknown

* the actual sheet thickness (blocks the slot width);
* the shop's quote, lead time and shipping;
* whether the shop will remove holding tabs and sand (it changes the price and the
  "ready to assemble" claim);
* the local price of Baltic birch (varies ±30 % by region);
* the isolation-pad choice (Sorbothane assumed; ISO-PUCK mini +$61).
