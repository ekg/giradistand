# 02 — Input register, assumptions and the measurements still needed

Status codes: **[U]** stated by the owner · **[M]** manufacturer document ·
**[P]** design assumption · **[C]** CAD-derived (from this model, guaranteed by construction)

Everything marked P must be confirmed before the files are cut. Nothing in this table
is a certified rating.

## A. Equipment

| # | item | value | unit | source | status | consequence if wrong |
|---|---|---|---|---|---|---|
| E1 | turntable model | Audio-Technica AT-LP120XUSB (introduced by an assistant, **not confirmed by the owner**) | — | conversation | **[P]** | any deck within 566 × 400 mm still fits |
| E2 | turntable body W × D × H | 452.0 × 352.0 × 141.6 | mm | A-T user manual `162501380` p.15–16 [1] | **[M]** | deeper than 400 mm → increase `D_OVER`; taller → only affects the open-top air |
| E3 | turntable mass | 8.0 (without dust cover) | kg | A-T manual [1] | **[M]** | top payload assumption is 15 kg, so any deck up to ~15 kg is covered |
| E4 | turntable foot positions | centres 42 mm inboard of the sides, 45 mm inboard of front/rear, 38 mm pads | mm | **assumed** (not published) | **[P]** | the shelf is flat over its whole top face, so any foot pattern inside 500 × 330 mm is supported |
| E5 | turntable foot height adjustment | ± 8 | mm | A-T manual (feet are levelling feet) [1] | **[M]** | it is the final platter-levelling device, so the stand only has to get close |
| E6 | turntable rear connector projection | ~35 (RCA + USB + DC plugs) | mm | **assumed** | **[P]** | connectors overhang the open rear edge; 80 mm wall clearance is specified |
| E7 | dust cover open envelope | 458 × 358 mm cover, hinge at the rear top, opens ~100° | mm | **assumed** | **[P]** | with the cover hinged open it projects ~34 mm behind the stand; A-T recommend removing it to play |
| E8 | speaker variant | AR "Powered Partners" — variant unconfirmed. Envelope used: 155 H × 267 W × 194 D, 3.16 kg | mm, kg | Advent AV570 manual [2] (identical hardware, later badge) and AR 570 Japanese spec sheet [3] (150 W × 270 H × 196 D) | **[M]** for the envelope, **[P]** for the identification | a different variant changes `SPK_W/H/D`; the bays are driven by them |
| E9 | speaker base face in the horizontal orientation | the 194 mm leg on the shelf (wedge profile `155 × 194`, baffle = hypotenuse, 38.6° above horizontal) | — | inferred from the product photograph and the two spec sheets [2][3] | **[P]** | **if the cabinet must instead rest on its 155 mm face the bay must be 194 mm high → `H_SPK` +39 mm, stand +39 mm** |
| E10 | speaker bottom flatness | assumed flat over the 4 pad positions (44 mm pads inset 32 mm) | — | **assumed** | **[P]** | pads are compliant; a rounded bottom needs 3 pads or a 6 mm plywood shoe |
| E11 | speaker connectors | RCA input, DC input, AC in/out socket, power switch on the rear face | — | AV570 manual [2] | **[M]** | 206 mm of free space behind each cabinet is provided |
| E12 | speaker controls | volume/bass/treble/power on the front-left strip of the baffle | — | product photograph [3] | **[M]** | the front of the shelf is open, so they stay reachable |
| E13 | speaker mounting holes | 3 × 8-32 + 1 × 7/16-10 in the spherical end caps | — | AV570 manual [2] | **[M]** | deliberately **not** used: a rigid bracket would bridge the isolators |

## B. Storage

| # | item | value | unit | source | status | consequence if wrong |
|---|---|---|---|---|---|---|
| S1 | record container | Groove Crate 14.5 × 14.5 × 14.125 in | in | supplier page [4] | **[P]** (owner has not chosen) | the bay accepts any container within 566 × 393 × 370 mm |
| S2 | crate external dimensions | 368.3 × 368.3 × 358.8 | mm | supplier page [4] (14.5 × 14.5 × 14.125 in) | **[M]** for that product | — |
| S3 | crate capacity / loaded mass | 80–100 LPs, ~20 kg of records + 1.9 kg crate ≈ 22 kg | kg | supplier states 13 in square interior, ~80–100 LPs [4]; 0.25 kg per LP assumed | **[P]** | design payload is 40 kg, i.e. ~1.8× the expected loaded mass |
| S4 | two crates side by side | **do not fit**: 2 × 368.3 = 736.6 mm against a 566.2 mm bay | mm | [C] | **[C]** | a two-crate stand must be ≈750 mm wide; the parameter `SPK_W`-driven width would change to ≈752 mm |
| S5 | crate removal path | slides forward (+Y) 400 mm; nothing obstructs it at any point | — | `out/cad_checks.md` §6 | **[C]** | — |
| S6 | crate browsing | records are lifted out after the crate is drawn forward. The bay gives only 41 mm above the crate rim, deliberately: browsing happens with the crate on the floor |

## C. Structure, process and loads

| # | item | value | unit | source | status | consequence if wrong |
|---|---|---|---|---|---|---|
| C1 | material | mild steel CRS 1008/1010, 0.074 in | in | SendCutSend material catalogue [5] | **[M]** | — |
| C2 | sheet thickness | 1.88 | mm | nominal 0.074 in [5] | **[M]** | ±0.10 mm assumed in the tolerance stacks |
| C3 | inside bend radius | 1.60 | mm | SendCutSend bending calculator, .074 mild steel [6] | **[M]** | custom radii are not offered, so this is fixed |
| C4 | K factor / bend deduction | 0.40 / 3.277 per 90° | — / mm | [6] | **[M]** | every flat pattern uses these values |
| C5 | min formed flange length | 8.13 | mm | [6] | **[M]** | smallest flange used is 20 mm |
| C6 | max flat part | 762 × 1117 (cut/bend), 762 × 914 (powder coat) | mm | [5][7] | **[M]** | largest part is 620 × 453 flat |
| C7 | bend-to-edge tolerance | ±0.38 per bend | mm | [8] | **[M]** | absorbed by 6.8 mm slots in the tray flanges |
| C8 | bend angle tolerance | ±1° | ° | [8] | **[M]** | affects flange contact, not part width |
| C9 | coating build | +0.05…0.13 per side | mm | [9] | **[M]** | included in the clearance and tolerance stacks |
| C10 | payload, top / middle / bottom | 15 / 10 / 40 | kg | brief's provisional values | **[P]** | utilisation scales linearly; see `docs/04` |
| C11 | lateral disturbance | 60 N criterion, 100 N reported, at 900 mm height | N, mm | **assumption** | **[P]** | see the stability section; the wall strap covers the higher case |
| C12 | floor | level within ±3 mm over 500 mm | mm | **assumption** | **[P]** | the M6 glides give about ±5 mm of travel |
| C13 | acoustic environment | hard floor, speakers 1.5–2.5 m from the listener | m | **assumption** | **[P]** | see `docs/13` |

## D. The measurements still needed (and how to take them)

These are the only inputs that can still change a manufactured dimension.

**Measurement 1 — which face of the speaker rests on the shelf (E9).**
Put one speaker on a table in the orientation you actually want (grille facing you,
cabinet "lying down"). Measure (a) the height from the table to the highest point of
the cabinet, and (b) the depth front-to-back at table level. Expected: 155 and 194 mm.
*If the height comes out at 194 mm, tell me — `H_SPK` changes from 190 to 229 and the
stand grows 39 mm.*

**Measurement 2 — the real speaker width and mass (E8).**
With the speaker in that same position, measure the width across the two end caps and
weigh one speaker on a kitchen scale. Expected 267 mm and 3.16 kg.
*If the width is 300 mm the stand grows by 2 × 33 = 66 mm.*

**Measurement 3 — the turntable (E1/E4).**
Confirm the model number on the plate under the plinth. Measure the distance between
the centres of the front two feet and the rear two feet, and the plinth's depth
including any rear connector recess. Expected: 452 × 352 mm body, feet about 42/45 mm
inboard.
*Any deck up to 566 × 400 fits unchanged; a deeper deck needs `D_OVER` raised.*

**Measurement 4 — the record container (S1).**
If you already own a crate or box, measure its outside width, depth and height and
weigh it full. Anything within 566 × 393 × 370 mm and 40 kg fits.

**Measurement 5 — the listening height (optional).**
Sit where you listen and measure floor-to-ear. The turntable support sits at 626 mm;
if you want it at desk height (≈740 mm), say so and `H_SPK` is increased.

Send those five numbers and every affected dimension regenerates from
`cad/params.py` in one command. Until then the design is provisional.
