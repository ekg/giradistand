# 09 — Sources, and exactly what each was used for

All sources were read on 2026‑11‑22. Supplier rules change; re-check before ordering.

## Equipment

[1] **Audio-Technica, AT-LP120XUSB user manual** (162501380‑01, 2019) —
<https://docs.audio-technica.com/eu/AT-LP120XUSB_UM_162501380_V1_EN_web_190312.pdf>
Used for: dimensions 452 × 352 × 141.6 mm (p.15); mass 8 kg without dust cover (p.16);
the fact that the feet are levelling feet; that the dust cover is removable and should
be off during play; connector set (RCA, USB, DC input) on the rear; the instruction not
to place the turntable on or next to loudspeakers (p.4) — which is why the stand is
shared but the speakers are isolated and the plinth is a separate flat plate.

[2] **Advent AV570 instruction manual** (v.102203, Audiovox) —
<https://files.d-tools.com/Visualizations/Approved/Advent/Documents/Advent_AV570_Manual1.pdf>
Used for: cabinet envelope 6⅛ × 10½ × 7⅝ in deep = 155 × 267 × 194 mm *including
grille*; mass 3.16 kg (8 lb) per speaker; the rear input/output panel contents; the
power/bass/treble/volume controls; the spherical end caps with 3 × 8‑32 and
1 × 7/16‑10 mounting holes; 40 lb mounting-surface requirement. This is the same
hardware as the AR‑badged unit (sold as Advent after the Jensen/Advent purchase).

[3] **audio‑heritage.jp, AR Powered Partners 570 spec sheet** —
<https://audio-heritage.jp/AR/speaker/poweredpartners570.html>
Used for: the same cabinet as 150 W × 270 H × 196 D (i.e. the *other* resting
orientation — the same box on its end), 3.5 kg, "triangle design" note, and the product
photograph from which the wedge profile (baffle = hypotenuse, tilted) was read.

## Storage

[4] **Groove Crate, "Vinyl Record Storage Crate … Collapsible and Stackable"** —
<https://groovecrate.com/vinyl-record-milk-crates> and the corresponding Amazon listing
Used for: exterior 14.5 × 14.5 × 14.125 in (368.3 × 368.3 × 358.8 mm), interior 13 in
square, capacity ~80–100 LPs. The record bay is sized to this product as a
*documented default*, not as a requirement.

## Supplier rules — SendCutSend

[5] **Materials catalogue** — <https://sendcutsend.com/materials/>,
**processing min/max** — <https://sendcutsend.com/materials/processing-min-max/>
Used for: mild steel stocked thicknesses (.030/.048/.059/.074/.104/.119/.135/…);
0.074 in availability; max flat part 30 × 44 in cut/bend and 30 × 36 in for coating;
minimum flange lengths before/after bending (0.255/0.320 in).

[6] **Bending calculator / bend specs** — <https://sendcutsend.com/bending-calculator/>
Used for: **K factor 0.40, effective inside radius 0.063 in (1.60 mm), bend deduction
0.1290 in (3.277 mm) at 90°, die width 0.472 in, min formed flange 0.320 in, min corner
relief distances, bend relief depth 0.157 in** for .074 mild steel. These numbers are
the basis of every flat pattern in this package.

[7] **CNC bending service page** — <https://sendcutsend.com/services/cnc-bending/>
Used for: max flat part 30 × 44 in, max bend length 16–44 in, max bend angle 130°
(**therefore no hems are available** — relevant to the "safe exposed edge" question),
bend-to-edge tolerance ±0.015 in per bend, bend angle ±1° (≤24 in), C-channel rule
(base ≥ 2 × flange), box-flange rules, "boxes that close in on themselves" not formed,
air-bending process and die-line witness marks.

[8] **Assembly upload guidelines** — <https://sendcutsend.com/guidelines/assembly/>
Used for: ≤25 bodies and ≤5 MB per file, remove hardware from the upload, align a face
to a primary plane, uniform-thickness solid sheet bodies, model at stock thickness with
their K factor and radius, use **square** bend reliefs (rounded reliefs can be read as
machined features).

[9] **Hardware insertion** — <https://sendcutsend.com/services/hardware/>
Used for: PEM nut/stud load directions ("nuts: load pulls the nut into the part"),
"H hardware installed before powder coating, hardware capped/plugged", automatic hole
resizing — **and the decision not to use inserts at all**, because through-bolts with
locknuts remove every thread from the parts.

[10] **Powder coating** — <https://sendcutsend.com/services/powder-coating/>
Used for: 7 materials / 15 colours including **Textured Black (BK01)**, max part
30 × 36 in, coating build +0.002–0.005 in per side (0.05–0.13 mm), min hole 0.040 in,
"tapped holes are not plugged before coating — expect to chase threads after"
(the direct reason this design has no tapped holes), and that Hot Rolled A36 powder
coats poorly (so CRS, not HRS, is specified).

## Alternative supplier

[11] **OSH Cut, ordering fabricated parts / bending design rules** —
<https://www.oshcut.com/design-guide/ordering-fabricated-metal>,
<https://www.oshcut.com/design-guide/metal-bending-design-rules>
Used for: the second-quote route. OSH Cut accepts STEP and applies its own tooling
radii, so the flat patterns here would need re-checking against its bend table if it is
used. Not selected as primary because its inside radius varies with tooling rather than
being fixed per stock thickness, which makes a fully pre-dimensioned package harder to
hold.

## Engineering references

[12] Timoshenko & Woinowsky‑Krieger, *Theory of Plates and Shells*, 2nd ed. —
simply supported square plate w_max = 0.00406 q a⁴/D; clamped square plate
0.00126 q a⁴/D. Used to validate the grillage FE (`calc/grillage.py`).
[13] EN 1993‑1‑8 style bolt resistances (0.6/0.9 fu·As/1.25, 2.5 d t fu/1.25) — used
for the joint capacities. These are *design* values, not test data for this joint.
[14] ASTM A1008 CS Type B — minimum yield 205 MPa for cold-rolled sheet; used as fy.
[15] Isostatic/elastomer isolation practice (IsoAcoustics published capacity figures:
ISO‑PUCK mini 2.75 kg per unit, 44 × 24 mm) — used to size the isolators, 4 per 3.16 kg
speaker.

## What was deliberately *not* used

* The earlier "M5 hardware, 5 mm Allen key, five or six panels, 16–24 bolts" and the
  "24 × 16 × 32 in cabinet" from the prior conversation: treated as illustrative only.
  The design arrived at 5 part numbers / 6 pieces / 22 bolts / 570 × 400 × 626 mm on its
  own derivation.
* The AR Powered Partner 570 dimensions were **not** substituted silently: the envelope
  used is the one that matches *both* the owner's 10.5 × 6 × 7.9 in recollection and the
  documented AV570 specification, and the identification is flagged as provisional
  (register item E8/E9).
