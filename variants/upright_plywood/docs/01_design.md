# 01 — Design recommendation (plywood flat-pack)

**VARIANT B — speakers upright. 518 × 415 × 745 mm, 18 mm Baltic birch, 6 pieces,
6 dowels, ≈US$331 estimated, $240 of it material + CNC.** Provisional: dimensioned and
checked in CAD and analytically, not built, not quoted.

## 1. The design in one paragraph

Two identical 18 mm side panels with three horizontal through-slots each; three shelves
whose ends pass through those slots as 150 × 18 tabs; a vertical 8 mm dowel dropped
through each protruding tab to lock it. The shelf is located in X by the tab shoulder +
dowel, in Y by the slot ends (150.2 vs 150.0 mm), in Z by bearing on the slot's lower
face, and against rotation by the 18 mm thickness in the slot. Nothing else is needed:
no fasteners in the shelves, no back panel, no glue. One anti-tip strap and one fit
coupon are cut from the same sheet. Assembly is a "ladder" build (one side flat, shelves
and dowels in, second side on) and takes about 20 minutes with a mallet.

## 2. Dimensions

| item | mm | in |
|---|---|---|
| overall width | 518.0 | 20.39 |
| overall depth | 415.0 | 16.34 |
| overall height (turntable support surface) | 745.0 | 29.33 |
| plinth top in use | 886.6 | 34.91 |
| record bay clear | 482.0 W × 394.0 D × 372 H | 18.98 × 15.51 × 14.65 |
| speaker bay clear | 482.0 W × 394.0 D × 305 H | 18.98 × 15.51 × 12.01 |
| turntable surface | 482.0 × 394.0, flat | 18.98 × 15.51 |
| speaker side clearance / gap between cabinets | 6.0 / 188.0 | 0.24 / 7.40 |
| turntable margins (sides / front-rear) | 15.0 / 21.0 | 0.59 / 0.83 |
| support polygon (feet) | 414 × 304 | 16.3 × 12.0 |

**Why 518 wide.** With the speakers upright the pair is only 282 mm, so the TURNTABLE
(452) sets the width: 452 + 2 × 15 mm of margin = 482 interior, + 2 × 18 mm of panel =
518. The 188 mm gap between the cabinets is what is left over — it is not a design goal,
it is the space the narrow equipment leaves behind.

**Why 415 deep.** 394 of shelf + 18 of... nothing: the shelf is 394 deep and the side
panels are 415, so the shelf sits 3 mm back from the front and 18 mm back from the rear
face — that rear band is what the design would use for a back panel if one were ever
added. The 394 comes from the record crate (368.3) + 25.7 mm of insertion clearance.

**Why 745 high.** 32 (glides) + 372 (crate 358.8 + 13) + 18 (shelf) + 305 (speaker
270 + isolator 23 + 12 handling) + 18 (shelf). The upright cabinets are 115 mm taller
than the lying-down ones, and that is the whole of the height difference.

## 3. What sets each opening, and what it accepts

| opening | set by | accepts |
|---|---|---|
| record bay 566 × 394 × 372 | crate 368.3³ + crate-slide clearance + the middle shelf's thickness (no flange intrudes, unlike the steel design) | any crate up to 566 × 394 × 372 and ~40 kg |
| speaker bay 482 × 394 × 305 | turntable width + margins; height = 270 upright cabinet + 23 compressed isolator + 12 | an upright Powered Partner on its triangular base, toed in 20° |
| turntable surface 482 × 394 | the turntable + 15 mm margins | any deck up to 482 × 394 (AT-LP120XUSB is 452 × 352) |

The record bay is 372 high against the crate's 358.8: **13 mm of clearance, and no
flange hanging into it** (the steel design needed 400 mm for the same crate because a
30 mm flange intruded). This is the plywood design's one clear ergonomic advantage.

## 4. Material and process

* **18 mm Baltic birch, 13-ply, void-free core, B/BB face** — chosen for edge quality
  (the edges are exposed and sanded), dimensional stability and screw-free joint strength.
  A birch-faced poplar core is an acceptable cheaper substitute (−$35) if the budget
  matters more than void content.
* **All parts are 2.5-D: through-cuts only, one face, one setup.** The slots' internal
  corners are relieved with R4 dogbones so the square tab corners pass; the outlines use
  R6 internal radii. No pockets, no dados, no two-sided machining, no edge drilling.
* Grain: the long axis of every part runs along the sheet's long axis (the shelves bend
  along the grain, which is 2.8× stiffer than across it).
* Finish: **sanded, unfinished.** Edges R2, faces 120 grit. Oil, wax or lacquer is the
  owner's choice — and if you finish before assembly, allow for the film thickness in the
  slots (it is one more reason the fit coupon exists).

## 5. Why this architecture

| candidate | verdict |
|---|---|
| **Through-tab + dowel lock (chosen)** | 4 part numbers, 6 pieces, 6 dowels, no fasteners in the shelves, tool-free, reversible, all through-cuts |
| Dados + screws | dados are partial-depth cuts (two-sided or a different machine), and screws into plywood edges hold poorly |
| Wedge-locked tenons | 12–18 wedges, and the wedge slot risks splitting the tab |
| Cam-lock flat-pack hardware | +$60 of hardware and a drilling pattern the router shop must jig for |
| Steel design (see `../`) | 3× the cost, different process, still the right answer if you want metal |

## 6. Loads and performance (summary — details in `docs/04`)

Design payloads as before: 15 kg top, 10 kg speaker shelf, 40 kg record shelf.
Governing results: **maximum shelf deflection 0.12 mm** (base shelf, 40 kg uniform),
**maximum bending stress 1.09 MPa** against a 38 MPa plywood bending strength (factor
28), **racking drift 0.17 mm** at 100 N with clamped shelves and 0.69 mm even if the
joints are idealised as pins. 18 mm plywood is, in structural terms, heavily
over-designed for this stand — which is what makes the joint-based flat-pack approach
workable at all. The thickness is chosen for the *joints* and for a solid edge, not for
shelf strength.

## 7. Open decisions

| # | decision | default | consequence |
|---|---|---|---|
| W1 | measured panel thickness | 18.0 nominal, 17.4–18.4 typical | sets the slot width; **must** be measured before cutting |
| W2 | slot clearance | +0.20 mm | set from the fit coupon; ±0.05 is the useful range |
| W3 | speaker standing orientation | upright on the triangular base, toed in 20° | settled by this variant; the lying-down variants are in `../../` |
| W4 | turntable model | AT-LP120XUSB (provisional) | any deck ≤ 566 × 394 fits |
| W5 | record container | Groove Crate 14.5 in | any ≤ 566 × 394 × 372 |
| W6 | finish | none (sanded) | oil/wax at home, or ask the shop to quote a hardwax oil |
| W7 | wall strap | supplied | required for the records-removed stability case |

## 8. Status

> **Provisional design; quote-ready files after the fit coupon (W1/W2) is run and the
> equipment is confirmed (W3/W4).** Not built, not quoted, not supplier-reviewed. The
> design has no hidden fabrication: everything is a through-cut and the assembly needs
> no tool.
