# Variant C — steel stand, **dual-mode speaker bay** (either way up)

**570 × 400 × 741 mm, 5 part numbers / 7 pieces of 1.88 mm CRS, ≈US$525 estimated.
Revision D0.9 — provisional, dimensionally checked, not built, not quoted.**

You asked whether a stand that still has room to lay the speakers down could work.
It can — and the honest answer is that it costs width, not money.

## The geometry that decides it

| arrangement | pair envelope | bay needed |
|---|---|---|
| upright (triangle on its base) | 282 W × 235 D × 270 H | 314 W × 305 H |
| lying down (wedge on its 194 mm face) | 534 W × 235 D × 155 H | 566 W × 190 H |
| **both possible** | — | **566 W × 305 H** |

So the bay has to be the *union*: the lying-down width (566) **and** the upright height
(305). There is no shortcut — a 482 mm interior (the upright-only stand) physically
cannot take the pair lying down, and a 190 mm bay cannot take them standing up.

This variant is therefore the parent design's width with the upright design's height:

| | parent (lying down) | A (upright) | **C (dual)** |
|---|---|---|---|
| overall | 570 × 400 × 626 | 486 × 400 × 741 | **570 × 400 × 741** |
| speaker bay clear | 566 × 400 × 190 | 482 × 400 × 305 | **566 × 400 × 305** |
| turntable margins | 57 mm | 15 mm | 57 mm |
| gap between cabinets: lying / upright | 20 / — | — / 188 | **20 / 272** |
| acoustic centres: lying / upright | 287 | — / 329 | **287 / 413** |
| footprint vs turntable | +43 % | +22 % | **+43 %** |
| cost estimate | ≈$518 | ≈$514 | **≈$525** |

Note the one thing that gets *better*: with the wider bay the upright arrangement spreads
to **413 mm** between acoustic centres (upright-only variant A: 329 mm), which is a real
improvement for stereo.

## What it costs you

You cannot have both compactness and the option. Specifically:

* **+43 % footprint over the turntable** — the width is set by the lying-down pair again.
* **+115 mm height** over the parent — the speaker bay is sized for the upright cabinet, so
  in the lying-down arrangement there is 115 mm of **visible empty air above the speakers**
  (see `out/renders/14_arrangement_B_lying_front.png`). It reads as a half-empty bay.
* In the upright arrangement there is 272 mm of gap between the cabinets. That is
  excellent for imaging and looks deliberate; it is also a lot of air.
* **US$7 more than the parent** — the parts are the same count, just bigger, and bigger
  parts cost only slightly more at this size. Cost is *not* the reason to choose between
  the three steel variants; layout is.

## Verification performed on this geometry

* `out/cad_checks.md` — **all checks pass, for BOTH arrangements**: 0 mm³ interference
  between every part pair; the structure against the turntable, the upright speakers,
  the lying-down speakers, both isolator layouts, and the crate; all 22 bolts against
  every part and every equipment envelope; the crate removal path at 50 mm steps; the
  strap hole clear of the turntable.
* `out/export_verification.json` — 5 STEP files re-imported (1 solid each, identical
  bounding boxes, 0.0000 % volume difference); 5 DXF flat patterns re-read with correct
  hole counts, bend counts, arc radii, closed outlines and all holes inside.
* `out/calc_report.md` — top tray 0.32 mm under 15 kg; **middle tray 0.27 mm with the
  upright isolator layout and 0.30 mm with the lying-down layout** (both reported);
  base tray 1.94 mm under 40 kg; racking 0.65 mm at 100 N; tip force 115 N loaded /
  73 N with the records out; joint slip margin 27:1, joint opening moment 45 N·m against
  a 4.75 N·m demand.
* `out/renders/` — **14 views**, including arrangement A (upright) and arrangement B
  (lying down) as separate isometrics and front elevations.
* `out/drawings/` — 6 A2 sheets; GA-01D carries both arrangements in the notes.
* `out/bom.csv`, `out/cost_model.md` — identical BOM to the parent except part sizes.

Not performed: build, supplier quote, independent review of this variant, acoustic test.

## Practical advice

If you genuinely do not yet know which orientation you prefer: **this variant is the only
one that lets you decide later without re-buying.** Buy it, try the upright arrangement
first (vertical baffles, 413 mm centres), and if you dislike the height of the object or
the look, lay the cabinets down on a second set of isolator positions — the bay and the
shelf are already right for it. The only thing you change is where the eight isolation
pads sit (both layouts are in `docs/NOTES.md`); the pad count differs, 3 per cabinet
upright and 4 lying down, so the box of eight ISO-PUCK minis covers either layout with
spares.

If you would rather have the smallest and best-aimed object, choose **A (upright)** —
it is 84 mm narrower and it looks designed rather than accommodating.

## Files

`cad/` (params, sheetmetal, model, check, export, drawings, render, bom), `calc/`,
`out/step/` (5 parts + multi-body), `out/dxf/`, `out/drawings/`, `out/renders/` (14),
`out/calc_report.md`, `out/cad_checks.md`, `out/bom.csv`, `out/cost_model.md`,
`UPRIGHT-DUAL-D09-package.zip`. Upload instructions are identical to
`../../docs/08_upload_guide.md` (same material, thickness, finish, counts).
