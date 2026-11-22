## 11. BOM, fabrication schedule and cost model

### 11.1 Manufactured parts

| part | description | qty | flat area (mm2) | cut length (m) | bends | holes/slots | mass each (kg) |
|---|---|---|---|---|---|---|---|
| P1 | SIDE SLAB | 2 | 244752 | 2.21 | 0 | 11 | 3.61 |
| P2 | SHELF TRAY | 2 | 270688 | 2.33 | 4 | 6 | 4.04 |
| P3 | BASE TRAY | 1 | 261813 | 2.37 | 4 | 10 | 3.90 |
| P4 | REAR PANEL | 1 | 238736 | 2.06 | 2 | 4 | 3.54 |
| P5 | WALL STRAP | 1 | 9750 | 0.85 | 1 | 1 | 0.14 |

Total sheet area 1.541 m2, total cut length 14.38 m, 15 bends, 5 distinct parts, 7 pieces.

### 11.2 Purchased items

| item | spec | qty | unit (USD) | ext (USD) | basis |
|---|---|---|---|---|---|
| M5x12 button head screw, ISO 7380-1, A2-70 black | M5x12, 3 mm hex socket | 22 | 0.42 | 9.24 | assumption, fastener supplier |
| M5 flanged nylon-insert locknut, DIN 6923, A2 | M5, 8 mm AF | 22 | 0.34 | 7.48 | assumption |
| M6 levelling glide, male stud | M6x40 thread, 23 mm polymer base, 9 mm high | 4 | 1.85 | 7.40 | assumption |
| M6 flanged nylon-insert locknut, DIN 6923 | M6, 10 mm AF | 4 | 0.38 | 1.52 | assumption |
| IsoAcoustics ISO-PUCK mini (box of 8) | 44 mm dia x 24 mm, 2.75 kg each | 1 | 79.00 | 79.00 | supplier list price, verify |
| Groove Crate 14.5 x 14.5 x 14.125 in record crate | HDPE, 368 x 368 x 359 mm, ~80-100 LPs | 1 | 34.00 | 34.00 | supplier list price, verify |
| 3M 2552 aluminium-foil damping tape (optional) | 25 mm x 5 m roll | 1 | 22.00 | 22.00 | optional, assumption |
| Wall fixings for P5 strap (user supplies) | 2 x 4.0 x 40 screw or plasterboard anchor | 2 | 0.30 | 0.60 | user supplies |

### 11.3 Cost model (ESTIMATE - not a quotation)

| line | amount (USD) |
|---|---|
| laser cutting | 141.41 |
| CNC bending | 60.00 |
| deburring | 14.00 |
| powder coating | 73.57 |
| **fabrication subtotal** | **288.97** |
| purchased items | 161.24 |
| shipping (estimate) | 28.00 |
| sales tax 8.25% (assumption) | 39.45 |
| **TOTAL ESTIMATE** | **517.66** |

Rates used (assumptions, not published prices):

* laser: $6.00/part + $55.00/m2 + $0.90/m of cut, minimum $9/part
* bending: $3.50/bend, minimum $9.00
* deburr: $2.00/part
* powder coat: $6.00/part + $18.00/m2, minimum $10.00

**Status: estimate only.** SendCutSend returns an instant price when the
five STEP files in `out/step/` are uploaded; no upload was performed and no
quotation exists. Expect +/-25 % on the fabrication line, and note that
one-off orders are dominated by per-part setup, not by area - which is why
the design deliberately uses only 7 pieces of 5 distinct parts.

### 11.4 Cost drivers and the cheaper alternative

1. **Part count and per-part setup** (~40 % of the fabrication cost).
   Already minimised: 5 part numbers, 6 pieces, 2 of which are identical.
2. **Powder coating** (~25 %). Cheaper alternative: order bare/deburred parts
   and finish at home with a single aerosol of matte black etch-primer +
   topcoat (about $25 and 2 hours, OUTSIDE the guarantee of edge coverage).
   Saves roughly 15 % of the total but breaks the 'ready to assemble'
   promise, so it is offered only as an explicit choice.
3. **Material thickness.** 0.059 in (1.5 mm) CRS would cut about 20 % of the
   material cost but the shelf and racking checks would have to be re-run
   (plate stiffness scales with t^3, so deflections would roughly double).
   Not adopted.
4. The single biggest optional saving is to drop P4 REAR PANEL and accept a
   friction-only racking path - rejected: it removes the only
   non-friction racking element (see 7.2).
