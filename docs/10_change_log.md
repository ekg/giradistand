# 10 — Change log and revision history

## R0.9 — 2026-11-22 — first complete package (provisional)

Everything below is the first issued revision. The history records the decisions that
changed during the work, because several of them changed the geometry.

### Layout decisions and why they changed

| # | decision | alternative considered | reason |
|---|---|---|---|
| 1 | 570 mm overall width | deeper retry at a narrower top over a wider speaker bay | the speaker pair is 534 mm and sets the width; a stepped top saves no footprint and adds a third part number |
| 2 | 400 mm overall depth | 380 mm (tighter around the crate) | the crate is 368.3 mm and needs front clearance to slide out; 400 also keeps the turntable's 24 mm rear margin |
| 3 | record bay 400 mm high | 372 mm (crate + 13) | the middle tray's 30 mm front flange hangs into the top of the bay; below ≈390 mm the crate cannot slide out under it. This was found by the crate-path check, not by inspection |
| 4 | speaker bay 190 mm high | 175 mm | the ISO-PUCK mini is 24 mm high, not 8 mm; 175 would have crushed the pad or the cabinet |
| 5 | shelf trays *between* the side slabs | trays between the slabs | gains 3.8 mm of interior width, removes a corner-relief conflict between the tray's front flange and the slab, and puts the bolt heads on the outside where they are reachable |
| 6 | through-bolts + flanged locknuts | PEM self-clinching nuts | removes every thread from every part, so powder coating cannot damage a thread and there is nothing to chase; also avoids an insertion service charge |
| 7 | P4 rear panel as a shear diaphragm | rear X-brace straps | a panel is one flat part with two bends, keeps cables and vents clear of the speaker bay, and gives a *positive* racking path; a diagonal in the rear plane would have collided with the crate |
| 8 | 1.88 mm CRS, stiffness from folded flanges | 3.0 mm CRS, or 3.17 mm aluminium | a flat 1.88 mm plate deflects 7 mm over the 566 mm span; the 30 mm flanges take that to 0.72 mm at a fraction of the weight and cost |
| 9 | feet at ±262 / ±183 | ±255 / ±160 | 16 % more restoring moment for free, still inside the base tray's flange |
| 10 | wall strap moved from "optional" to "standard kit" | leave it optional | with the records removed the unrestrained tip force is 74 N at bench height; that is not a margin to rely on in a house with children |

### Engineering corrections made during the work

| # | finding | correction |
|---|---|---|
| 11 | P2 tray interfered with P4 rear panel by 3.4 mm³ at the bay ceiling | rear panel height reduced to `H_REC − 1.5` |
| 12 | dust-cover envelope was modelled rotating the wrong way (below the hinge) and intersected the top tray by 18 000 mm³ | hinge moved to the rear top and the rotation direction corrected; the open cover now sits entirely in free air |
| 13 | nested rear panel had only 0.30 mm of clearance against a 0.46 mm worst-case stack | `PAINT_CLR` raised to 0.30 mm/side |
| 14 | grille FE initially validated with the wrong boundary condition (rotations fixed on the "simply supported" case) | validation separated into w-only and fully fixed cases; both now reproduce the closed-form plate solutions to +15 % / +8 % |
| 15 | turntable "foot differential" metric sampled the tray corners (always 0) | probe points moved to the actual turntable foot positions |
| 16 | tray flat-pattern outline was missing its left tab and had the front tabs at the wrong depth | outline rebuilt from the same spans as the folded model; flat area now matches the folded volume to 1 % |
| 17 | side slabs were initially given inward folded returns | removed: they would have reduced the speaker bay below 534 mm at the front opening |

### Deliberately not done

* No hem on the exposed edges: the supplier's maximum bend angle is 130°, so a 180° hem
  is not available. Exposed edges are deburred and powder coated instead, with R3
  external corners.
* No hardware inserts, no tapping, no countersinking: none is needed, and each would add
  a service, a failure mode and a lead time.
* No aluminium variant developed: it would be lighter and more expensive; documented as
  an alternative with the stiffness comparison, not engineered.
* No two-crate variant: the width consequence is computed and stated, but the variant is
  not drawn.

## Planned for R1.0 (blocked on equipment confirmation)

1. Confirm E9 (which speaker face rests on the shelf). If it is the 155 mm face, change
   `SPK_H` to 194 and regenerate: P1 (+39 mm), P4 (+39 mm), `H_OVER` +39 mm, all flat
   patterns and drawings.
2. Confirm E1/E8. If the turntable depth > 400 mm, change `D_OVER`; if the speaker width
   ≠ 267 mm, change `SPK_W` (this moves `W_OVER`, P1, P2, P3, P4).
3. Confirm S1 (container) and adjust `CRATE_*` / `H_REC` if needed.
4. After the first build: replace the assumed pad compression, torque figures and
   joint stiffness with measured values; add the measured deflections to
   `docs/06` and re-issue as R1.0 with a "physically tested" column in the matrix.
