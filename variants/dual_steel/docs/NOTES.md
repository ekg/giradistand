# Variant C notes — the dual-mode bay

Everything about material, process, joints, fasteners, record bay, rear panel, strap and
assembly sequence is the parent design unchanged; read `../../../docs/`. This file records
only what is specific to keeping both speaker orientations open.

## 1. The two arrangements

| | A: upright | B: lying down |
|---|---|---|
| cabinet envelope | 150 × 196 plan × 270 high, triangular, toed in 20° | 267 W × 194 D × 155 H, wedge section |
| pair width in the bay | 282 mm, 272 mm gap | 534 mm, 20 mm gap |
| acoustic centres apart | **413 mm** | 287 mm |
| baffle axis | vertical (aims at a seated listener) | 38.6° above horizontal (the product's own wedge) |
| isolators | **3 per cabinet** (one in from each triangle corner) | **4 per cabinet** (rectangle, 30 mm inset) |
| headroom left in the bay | 11 mm | **115 mm** (visible air) |

## 2. Isolator positions — both layouts

The shelf is bare; the ISO-PUCK mini isolators are not glued, so you can switch layouts at
any time. Positions are in the stand's coordinates (origin at the bay's front-rear centre,
x = 0 at the centre line); both are printed by `cad/model.py`:

* **Upright (3 per cabinet).** Right cabinet: (203.8, 23.8), (127.6, −2.9), (166.9, 113.4).
  Left cabinet: mirror x. These sit one in from each corner of the triangular base —
  the two acute corners need the pad further in (74 mm and 55 mm along the bisector) or
  the 44 mm pad overhangs the cast edge.
* **Lying down (4 per cabinet).** Right cabinet: (146.9, 96.0), (146.9, −20.0),
  (−46.9, 96.0), (−46.9, −20.0) — that is 30 mm in from the 267 × 194 base's edges.
  Left cabinet: mirror x.

Eight pucks in the box cover either layout (6 + 2 spare, or 8 exactly).

## 3. What to check on the first build

1. **Upright stance.** A 3.5 kg, 270 mm cabinet on three 24 mm pucks is stable but lively.
   Check all three pads contact with a feeler gauge or a sheet of paper; if one does not,
   the base's three corners are not coplanar enough and you should go to four pads.
2. **Toe-in swing.** The upright envelope is modelled *after* the 20° rotation
   (141 × 235 mm). If your cabinets are larger than the documented AR 570, swing them
   before loading and check against the side slabs.
3. **Empty air.** In the lying-down arrangement there is 115 mm above the cabinets. This is
   deliberate — it is what buys the option — but if you settle on lying down, nothing is
   gained by it and the parent design (626 mm tall) would look tighter.
4. **Side stability.** The base tray is the parent's 566 mm wide with feet at ±249, so the
   side margin is the parent's 1.7 : 1 at a 100 N push; the wall strap is still supplied
   and still recommended.
5. **Cable access.** Lying down, the cabinets' rear faces are 194 mm deep in a 400 mm bay:
   about 180 mm of clear space behind them. Upright, the triangular plan leaves more. Both
   are open at the rear.

## 4. Why not a convertible *shelf*

A removable sub-shelf that raises the speakers into the middle of a tall bay was
considered and rejected: it would need two extra parts and two more joint sets, it would
put a second panel interface under the speaker load, and it would make the bay look like a
cabinet with a hole in it in both configurations. Sizing the bay for the union costs
nothing in parts and keeps one continuous shelf.
