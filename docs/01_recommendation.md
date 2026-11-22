# 01 — Recommendation

Revision R0.9 · provisional · 570 × 400 × 626 mm · 22.8 kg · ≈US$520 estimated

## 1. What is recommended

A two-slab steel frame with three clamped shelf trays and one rear shear panel:

* **Two identical 1.88 mm side slabs** (400 × 612 mm) stand vertically and carry every
  vertical load directly to the floor. Because they are plates in the depth direction
  they also act as shear panels for front-to-back racking, which is therefore rigid
  without any bracing.
* **Three identical-family trays** (566 × 400 mm, four 30 mm down-flanges) bolt to the
  *outside* of both slabs with three M5 screws per flange. The flanges are clamped
  (friction-grip) joints: three M5 bolts at 3 N·m give ≈9 kN of clamp per flange, so
  the joint does not slip at service loads (slip margin 27:1 at 100 N) and the bolt
  group carries the moment in bearing if it ever did slip.
* **One rear C-channel panel** closes the back of the record bay. It is a shear
  diaphragm between the two slabs, i.e. a *positive* racking element that does not
  depend on bolt preload at all. It also stops the crate sliding out backwards.
* **No threads on any part.** Every thread is in a purchased flanged nylon-insert
  locknut, so powder coating cannot damage a thread and no thread chasing exists.
* **Open front, open rear above the record bay**: turntable connectors, speaker
  connectors and ventilation are all in free air; cables drop straight down the back.

## 2. Overall dimensions and clear openings

| item | mm | in |
|---|---|---|
| overall width | 570.0 | 22.44 |
| overall depth (body; add 80 mm wall clearance for cables) | 400.0 | 15.75 |
| overall height (turntable support surface) | 626.0 | 24.64 |
| turntable plinth top in use | 767.4 | 30.21 |
| record bay clear | 566.2 W × 393.8 D × 400.0 H | 22.29 × 15.60 × 15.75 |
| speaker bay clear | 566.2 W × 400 D × 190.0 H | 22.29 × 15.75 × 7.48 |
| turntable surface | 566.2 × 400.0, flat, no holes or fixings | 22.29 × 15.75 |
| speaker clearance, each side of pair | 6.0 | 0.24 |
| gap between the two speaker cabinets | 20.2 | 0.80 |
| turntable margin, sides | 57.1 | 2.25 |
| turntable margin, front/rear | 24.0 | 0.94 |
| support polygon (between foot centres) | 524 × 366 | 20.6 × 14.4 |

**What sets each dimension** (full chains in `docs/03`):

* **Width 570 = 2 × 267 speaker + 20 central gap + 2 × 6 side clearance + 4 × 1.88
  sheet.** The speaker pair alone is 534 mm; there is no smaller credible width if
  both speakers stay horizontal, side by side, grilles forward. The turntable (452 mm)
  is not the driver — it is 114 mm narrower than the stand.
* **Depth 400 = 368.3 crate + 25.5 crate-bay clearance + 2 sheets of tray + the
  rear-panel offset.** The turntable's 352 mm depth is not the driver; the record
  crate is. Trimming the depth below ≈380 mm would prevent the crate from sliding in.
* **Height 626** = 32 (floor clearance + base tray) + 400 (record bay, which must clear
  the 358.8 crate *and* the 30 mm front flange of the tray above, plus 11 mm of
  tolerance) + 190 (speaker bay: 155 speaker + 23 compressed isolator + 12 handling)
  + 2 × 1.88 sheet.

## 3. Material, process, finish

* **CRS 1008/1010 cold-rolled steel, 1.88 mm (0.074 in)**, SendCutSend's stock.
  Inside bend radius 1.60 mm, K factor 0.40, bend deduction 3.277 mm per 90°, exactly
  their published rule for this stock, so the flat patterns and the folded STEP files
  agree with their tooling.
* Laser cut, CNC air bent, deburred, **powder coat textured black (BK01)**. All
  hardware is capped/plugged before coating (their published process), and no part
  carries a thread, so there is nothing to chase afterwards.
* Steel rather than aluminium: 2.9× the stiffness per unit thickness, cheaper per unit
  stiffness, and the 22.8 kg mass is useful (it lowers the stand's centre of
  gravity relative to its stiffness and makes the frame less lively). An aluminium
  5052-H32 version at 3.17 mm would weigh ≈10 kg and cost more; it is a documented
  alternative, not the recommendation.

## 4. Why this architecture (and not the others)

| candidate | usable space | racking | manufacturing | verdict |
|---|---|---|---|---|
| **A. Trays bolted to two side slabs + rear panel** (chosen) | best — no internal posts or rails intrude into any bay | rigid: side slabs shear in Y, rear panel shears in X, clamped joints in the 190 mm top bay | 5 part numbers, 15 bends total, 7 pieces, 23 screws | **chosen** |
| B. Shelves on a bolted square-tube frame | loses 25-40 mm per side to posts, and posts foul the crate corners | truss action, excellent | 4 posts + 12 shelves rails + 24+ joints, tube cutting + welding or 3D brackets; roughly 2× the part count and cost | rejected |
| C. Folded sheet "ladder" sides (shelves formed as part of the side blanks) | same as A | excellent | each side blank unfolds to ≈1.4 m; exceeds the 1.117 m maximum bend length and needs a Z-fold sequence the supplier will not guarantee | rejected |
| D. Welded frame | n/a | n/a | destroys the home-assembly and flat-pack requirement | rejected |

Two slabs plus trays also gives the visual quality the brief asks for: one crisp
material, exposed 1.88 mm edges, and a 1.9 mm shadow line where every tray is set
back from the slab face.

## 5. Heights and ergonomics

* Turntable support at **626 mm**, plinth top at **767 mm**. That is a low-console
  height: comfortable for cueing from a chair or a low stool, slightly low for
  standing. The alternative (a 740 mm support) would need either +114 mm of empty
  height in the speaker bay or a plinth, and the brief asks for no unexplained empty
  height. The parameter `H_SPK` in `cad/params.py` sets this directly; raising it to
  300 mm moves the support to 736 mm and adds visible air around the speakers.
* The speaker baffle in the documented horizontal orientation is a wedge set at
  **38.6° above horizontal** (the product's own geometry). With the baffle's bottom
  edge 40 mm above the shelf, its axis crosses a seated ear height of ≈1.0 m at
  ≈1.5 m listening distance. This is the product's design intent, not a stand
  compromise — but it must be understood before buying: the stand cannot aim the
  speakers flatter without a wedge (documented as an accessory in `docs/13`).

## 6. Loads and payload statement

Design payloads (assumptions, *not* ratings): 15 kg on top, 10 kg on the speaker
shelf, 40 kg on the record shelf, plus 22.8 kg of structure.

Worst computed utilisation: panel stress 47 MPa against a 102.5 MPa limit (factor 4.4
on yield at the design loads); governing shelf deflection 1.94 mm (base tray under
40 kg); racking drift 0.65 mm at 100 N. Details in `docs/04` and `out/calc_report.md`.

## 7. Open decisions that change hardware

| # | decision | default used | consequence if different |
|---|---|---|---|
| E1 | turntable model | AT-LP120XUSB (provisional) | any deck ≤ 566 × 400 fits without change; deeper decks need `D_OVER` |
| E2 | which Powered Partner variant | 570 / AV570 envelope 155 × 267 × 194 | a 150–196 mm tall cabinet fits; a taller one needs `H_SPK` |
| E3 | speaker base face | the 194 mm leg (wedge resting on its long face) | if it must rest on the 155 mm face, the bay must be 194 high → `H_SPK` +39 mm |
| E4 | record container | Groove Crate 14.5 in (368 × 368 × 359) | any container ≤ 566 × 393 × 370 fits; two 14.5 in crates do **not** (they need 745 mm) |
| E5 | finish colour | textured black BK01 | any of the supplier's 15 colours, same price |
| E6 | wall strap | fitted as standard | without it, the stand still resists a 74–116 N push at bench height |

## 8. Status statement

> **Provisional concept, dimensionally checked and analytically validated; quote-ready
> for the six manufacturing files, subject to confirming E1–E4.** Not supplier-accepted
> (nothing was uploaded), not physically tested (nothing was built), and not
> fabrication-released: E3 in particular would change the height chain if the speaker
> rests on a different face.
