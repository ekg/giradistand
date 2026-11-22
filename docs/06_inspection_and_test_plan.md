# 06 — Inspection and home test plan

**Status: proposed. None of it has been performed on a physical build.**
This plan is written so that the first build produces evidence rather than impressions.
Do the steps in order; stop at any row that fails and correct before continuing.

## 0. Parts inspection, before assembly (10 min)

| # | check | accept | record |
|---|---|---|---|
| 0.1 | part count and IDs | 2 × P1, 2 × P2, 1 × P3, 1 × P4, 1 × P5, bags A/B/C complete | ☐ |
| 0.2 | flat pattern of each tray | outline matches `out/dxf/*.dxf` at 1:1; no burr on any edge (run a finger **along** edges, not across) | ☐ |
| 0.3 | bend angles | both end flanges of each tray at 90° ± 1°, checked with a square | ☐ |
| 0.4 | slot/hole alignment | drop a tray onto a slab on the bench, all 3 screws per side pass through by hand | ☐ |
| 0.5 | coating | no bare metal, no coated threads (there are none), no coating in the 6.8 mm slots | ☐ |
| 0.6 | rear panel drop-in | panel slides between the slabs without force | ☐ |
| 0.7 | tray top flatness | straightedge across the top tray: ≤ 0.3 mm gap anywhere inside the flat field | ☐ |

If 0.4 or 0.6 fails, **stop** — that is a tolerance or nesting problem, and the
correct response is to tell the fabricator, not to file the part.

## 1. Assemble and level the empty stand (as `docs/05`, steps 1–9)

| # | check | accept | record |
|---|---|---|---|
| 1.1 | all four feet carry load | feeler gauge or paper under each foot; none slides out freely | ☐ |
| 1.2 | top tray level | ≤ 1 mm per 300 mm both ways | ☐ |
| 1.3 | rigidity, empty | push/pull side-to-side and front-to-back with about 50 N (5 kgf) at the top: no creak, no visible relative movement at the joints | ☐ |
| 1.4 | no rocking | stand on a hard floor, press each corner: no movement | ☐ |

## 2. Fit check with the equipment, unpowered (15 min)

| # | check | accept | record |
|---|---|---|---|
| 2.1 | turntable feet | all four on the flat top face, none touching a bend or an edge; platter levels with the turntable's own feet | ☐ |
| 2.2 | turntable connectors | RCA/USB/DC plugs fit with ≥ 20 mm of space behind the plug body | ☐ |
| 2.3 | dust cover | lifts off and refits without touching the stand; if used hinged, opens fully with ≥ 60 mm wall clearance | ☐ |
| 2.4 | speakers | both sit on four isolators, no rocking, 6 mm to each side, 20 mm gap, grilles unobstructed and clear of the tray above (≥ 10 mm) | ☐ |
| 2.5 | speaker controls | volume/bass/treble reachable without moving the speaker | ☐ |
| 2.6 | speaker cables | both RCA plugs and the AC/DC connections make with the cable not touching the frame or the tray edge | ☐ |
| 2.7 | record crate | slides in and out with one hand, no scraping, 400 mm of clear floor in front | ☐ |
| 2.8 | crate loaded | with a full crate, the stand does not move when the crate is drawn out | ☐ |

## 3. Progressive load test — **inert weights only, no electronics** (15 min)

Use bags of rice/sand or dumbbells. Never test with the turntable installed.

| # | load | check | accept |
|---|---|---|---|
| 3.1 | 10 kg on the top tray (centre) | deflection at the centre | ≤ 1.0 mm (design 0.7 mm) |
| 3.2 | 15 kg on the top tray, all on one corner | local deflection, no permanent set after removal | ≤ 1.0 mm; 0 mm set |
| 3.3 | 40 kg on the base tray (or the loaded crate) | deflection mid-span, front and rear edge | ≤ 2.5 mm (design 1.9 mm) |
| 3.4 | everything loaded (15 + 10 + 40) | any creak, any joint movement, any coating damage at the clamped faces | none |
| 3.5 | same, push 100 N sideways at the top tray | movement at the top tray | ≤ 2 mm and returns to zero |
| 3.6 | remove all load | any permanent deflection at the top tray | ≤ 0.2 mm |

Record the measured deflection. A 1 mm feeler gauge and a straightedge are enough — the
point is a number, not a machine.

## 4. Acoustic test, in stages (as long as you like)

Rules: **do not** provoke feedback deliberately, do not strike the turntable, do not run
the stylus on a record while thumping the stand, and never leave the room at high volume
during the first test.

1. **Silent check.** Everything connected, volume at zero, stylus up. Listen for
   transformer hum from the speakers and any buzz from the stand. Wiggle each cable
   gently — no crackle.
2. **Low level.** A record you do not care about, volume low, stylus down. Listen for
   howl at moderate level. Stop immediately if it starts.
3. **Normal level.** Increase slowly to your usual listening level over several tracks.
   Between tracks, listen for ringing or buzz.
4. **Handling test.** With a record playing at low volume (or better, with the stylus
   up), tap the top tray lightly with a fingernail and then the middle tray. Note
   whether either rings audibly. If the top tray rings, fit the optional damping tape
   to its underside (25 mm strip along the centre, 3M 2552 or equivalent, 4 strips
   across the width — it does not interfere with anything).
5. **Walking test.** With music at normal level, walk past the stand and touch nothing.
   Does it move? Rock?

**Stop-and-adjust criteria** (any of these means fix it before continuing):
* audible feedback at or below your normal listening level;
* any rattle or buzz that changes when you touch the frame (that is a loose fastener);
* visible movement of the turntable when you walk past;
* any joint that has loosened after a week (re-torque and re-check the cause).

## 5. After one week and after one month

| # | check | accept |
|---|---|---|
| 5.1 | re-torque all 23 M5 locknuts (incl. the strap) | none moves more than 1/8 turn |
| 5.2 | feet | still carrying load, no floor marks |
| 5.3 | platter level | still level (a shelf may have settled in its slots) |
| 5.4 | coating at clamped faces | no fretting dust, no rust |
| 5.5 | isolation pads | no permanent compression set, no cracking |

Log the results. If a check fails, the correct fix is in the "what to check" table in
`docs/05`, and the failure belongs in the change log (`docs/10`) so the design can be
corrected for the next build.
