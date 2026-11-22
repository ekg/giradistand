# FLAT PACK STAND -- calculations (plywood)  W0.9 provisional

Generated 2026-11-23 by `flatpack/calc/run_all.py`.
All inputs come from `flatpack/cad/params.py`.

## 0. Basis

| item | value | note |
|---|---|---|
| panel | Baltic birch plywood, 18 mm nominal, 13-ply, void-free core, B/BB face | must be measured before cutting |
| thickness | 18.0 mm nominal, actual 17.4-18.4 | the slot is cut to the measured value + 0.20 |
| E (bending, load along the face grain) | 7000 MPa | conservative for birch ply (7-12 GPa); the shelf span runs along the sheet's long axis |
| E (across the plies) | 2500 MPa | used as a sensitivity |
| bending strength (along grain) | 38 MPa | B/BB Baltic birch, 0.2 % offset |
| bearing (plywood edge/face) | 8.0 MPa | conservative |
| density | 680 kg/m3 | |

Load cases (assumptions, not ratings): 15 kg top, 10 kg middle, 40 kg base, self weight from the CAD.

## 1. Shelf bending (grillage FE, same solver validated in the steel package)

Span 566 mm between the side panels, depth 394 mm, 18 mm ply, simply supported and clamped variants.

| shelf | load case | deflection (mm) | sigma (MPa) | SF on bending strength |
|---|---|---|---|---|
| top | 15 kg on 4 turntable feet | 0.03 | 0.29 | 128.9 |
| top | 15 kg on 4 turntable feet (pinned ends) | 0.19 | 0.38 | 99.6 |
| top | 15 kg uniform | 0.05 | 0.30 | 128.3 |
| top | 15 kg uniform (pinned ends) | 0.23 | 0.47 | 80.4 |
| top | 15 kg on one foot | 0.06 | 0.98 | 38.8 |
| top | 15 kg on one foot (pinned ends) | 0.27 | 1.08 | 35.2 |
| middle | 10 kg on 8 isolator pads | 0.05 | 0.34 | 111.6 |
| base | 40 kg on crate corners | 0.10 | 1.35 | 28.1 |
| base | 40 kg uniform | 0.12 | 0.79 | 48.1 |

Criteria: deflection <= 1.5 mm (top/middle), <= 2.5 mm (base); SF on bending strength >= 3.

## 2. Shelf-to-side joint (tab in slot, dowel locked)

| quantity | value | check |
|---|---|---|
| tab bearing area in the slot | 2700 mm2 | |
| bearing stress, top shelf (15 kg / 2 ends) | 0.027 MPa | vs 8.0 MPa -> SF 294 |
| tab shear area at the dowel line | 2556 mm2 | |
| shear stress at 100 N lateral | 0.039 MPa | vs 1.0 MPa -> SF 26 |
| slot length / tab length | 150.20 / 150.0 mm | 0.10 mm per end = Y location +/-0.10 mm |
| tab thickness / slot height | 18.00 / 18.20 mm | 0.10 mm per face |
| dowel | 8 mm birch, 40 mm, 11 mm proud each side | bearing on 18 mm tab: 0.694 MPa |
| material remaining above/below a slot | 177 mm to the next slot | no local weakness |

## 3. Racking

Side panel second moment of area (out-of-plane, about the depth axis): I = 415.0 x 18.0^3/12 = 201690 mm4, EI = 1.41 kN.m2.

| joint idealisation | drift at 100 N | criterion | result |
|---|---|---|---|
| clamped shelves (tab in a 0.1 mm-clearance slot, i.e. effectively rigid) | 0.172 mm | 2.0 mm | PASS |
| pinned shelves (worst case) | 0.689 mm | 2.0 mm | PASS |

Plywood wins here: the 18 mm panels are ~30x stiffer than the 1.88 mm steel
slabs of the metal version, so even with pinned joints the frame passes the
racking criterion. No back panel is needed for racking; the open back is kept
for cable and ventilation access.

Front-to-back: the side panels act as in-plane shear panels, G A / h = 8.3 kN/mm -> 0.01205 mm at 100 N.

## 4. Stability

Support polygon: feet at +/-243 (x) and +/-152 (y) -> 486 x 304 mm.

| case | mass (kg) | CoM (x,y,z) | tip force at 900 mm, front/rear | side |
|---|---|---|---|---|
| loaded | 51.1 | (0,-9,353) | 89 N | 135 N |
| records removed | 29.1 | (0,0,461) | 48 N | 77 N |
| stand only | 14.8 | (0,0,315) | 24 N | 39 N |

Same conclusion as the steel design: the loaded stand resists ~100 N at
bench height, the records-removed case is lower, and a wall strap (P4) is
supplied with the kit for that case.

## 5. Thickness and fit (the one real risk with plywood)

| item | value |
|---|---|
| nominal sheet thickness | 18.0 mm |
| actual range to expect | 17.4-18.4 mm |
| slot as designed | 18.20 mm (nominal + 0.20) |
| if the sheet measures 17.6 | slot must be 17.80 -> joint is 0.30 loose |
| if the sheet measures 18.3 | slot must be 18.50 -> 18.20 would not fit |

**Therefore the slot width is a cutter-program parameter, not a design
constant.** The kit includes a fit coupon (P5) with three slots at +0.10,
  +0.20 and +0.30 mm clearance, cut from the same sheet in the same setup.
Cut the coupon first, test the actual panel in all three slots, then set the
clearance for the production parts. Take-up for a slightly loose joint is
provided by the dowel and by a tap with a rubber mallet; a joint that needs
force is a signal to increase the clearance, never to sand the part.
