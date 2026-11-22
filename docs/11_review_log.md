# 11 — Independent review log

An independent reviewer agent was given the requirements (`prompt.md`) and the actual
files (CAD source, exports, calculations, drawings, renders, assembly sequence) and asked
to be adversarial: find impossible assembly paths, contradictions, arithmetic errors,
weak design, manufacturing incompatibilities and overclaims. Findings and resolutions
below. **Line numbers refer to revision R0.9 as reviewed; the fixes are in R0.9a.**

Overall verdict from the reviewer (verbatim): *"'Dimensionally checked, provisional,
quote-ready' is not accurate as written… provisional — yes, and honestly so…
quote-ready — no."* That verdict was accepted for the parts listed as fixed below, and
the status label was changed to **"provisional design, dimensionally checked, not
assembly-validated"** until a build exists.

## CRITICAL findings — all fixed

**R1. Six of the 22 locknuts could not be fitted or held: the base tray joint was
unassemblable.** The base tray's 20 mm skirt enclosed the nut pocket; the nut sat
between the deck underside, the end flange and the skirt, reachable only through a
10 × 33 mm slit.
*Fix:* reversed the fastener direction for all 22 joints — button head **inside** the
bay, flanged locknut **outside**. Every nut is now turned with a wrench from outside the
stand. Side benefits: the inboard protrusion drops from 5.0 mm (nut body) to 2.75 mm
(button head), which is what keeps the speaker envelope clear at the top tray; and the
part count of special operations is unchanged. Geometry updated in
`cad/model.py::make_bolt`, noted on drawing S1 and in `docs/05`.
*Verification:* `out/cad_checks.md` §3 now tests every bolt solid against P1–P4 **and**
against the turntable, both speakers, the crate and all eight isolators: 0.000 mm³
everywhere.

**R2. The P3 flat-pattern DXF had no foot holes** (`spec["foot_holes"]` was never
written, and the hole coordinates were off the blank).
*Fix:* `spec["foot_holes"]` is now set, the stray `w/2` removed. `out/dxf/…P3…dxf` now
contains 4 circles, and the export verification checks hole counts per part.

**R3. The tray slots in every DXF were corrupt open contours, rotated 90° relative to
the STEP.** The obround was assembled from arcs whose centres were offset diagonally,
giving an 11 × 6.8 open shape instead of a closed 6.8 × 5.5 slot with the long axis
along the flat's X (the direction that becomes vertical in the formed part).
*Fix:* new `add_obround()` that builds a closed slot for either orientation, and the
tray slot is now passed as 6.8 (X) × 5.5 (Y) in the flat. Feature-level verification
added: per part, hole count, bend count, arc radii, outline closure and "all holes
inside the outline" (`out/export_verification.json`, all five parts `ok: true`).

**R4. The anti-tip strap could not be attached, and existed in three different forms.**
No hole in any part for it; 1.5 mm thickness (not a stocked gauge); three different
flange depths between model, DXF and text.
*Fix:* one 6.6 hole through the top tray's rear margin (8 mm from the rear edge, 16 mm
behind the turntable, verified clear); P5 rebuilt as a single 1.88 mm "Z" strap
(foot 110 with a 6.6 × 40 slot, riser 250, wall flange 30) from the same stock; the BOM
now carries 23 M5 fasteners; drawing S6 and `docs/05` rewritten to match the model.

**R5. The "bolt group carries the moment in bearing" claim was wrong** — the three bolts
of a flange lie in one horizontal row and cannot form a couple about the sway axis.
*Fix:* removed the claim. The joint now carries moment the way a clamped joint does, by
redistributing contact pressure; the opening moment `M_sep = N·h/6` is **45 N·m per
flange against a 4.75 N·m demand (margin 9:1)**, and the report states explicitly that
this is preload-dependent, that the lower bay's rear panel is the friction-independent
element, and that the maintenance plan includes torque checks.

**R6. `docs/11` did not exist while the matrix scored it.** This file.

## MAJOR findings — fixed

**R7. "Cap trays with flanges outside the slabs" contradicted the CAD** (the trays sit
between the slabs, flanges against the inner faces, 566.2 mm apart, not 400 mm).
*Fix:* corrected in `docs/03`, `docs/05`, `docs/10`.

**R8. Record-bay and rear-panel numbers were wrong in every user-facing document**
(396.3 vs 393.8 clear depth; "400 mm" usable height; panel 398.5 vs 400).
*Fix:* the usable record-bay envelope is now stated everywhere as
**566 × 394 × 370 mm** (370 because the tray above hangs 30 mm into the bay), and the
depth chain in `docs/03` uses the model's 393.8 mm. The rear panel's height is 398.5 mm
(1.5 mm drop-in allowance) and matches its STEP.

**R9. The feet did not reach the floor in the model, and the nut face was in the wrong
place in the instructions.** The glide base floated 21 mm above the datum.
*Fix:* base on z = 0, stud 35 mm, locknut on the deck's **top** face (`make_foot`), and
`docs/05` step 8 corrected. The height chain from the floor is now modelled, not
assumed.

**R10. `cad/check.py` reported checks it did not perform** (a hard-coded "0.000" cell,
a tautological alignment table, an unused variable, and no bolt-vs-equipment check —
the one that mattered, since a modelled nut cleared the speaker by 0.1 mm).
*Fix:* the fastener section is now a real boolean test of all 22 bolts against all
structural parts and all equipment envelopes; the tautological table is replaced by that
test (a bolt intersecting a plate *is* the misalignment test); the strap hole is checked
against the turntable footprint. All pass with 0.000 mm³.

**R11. "6 pieces" on every quote-facing document** (the data is 7).
*Fix:* 7 pieces / 5 part numbers everywhere; the editing artefact in `docs/08` removed.

**R12. `docs/07` cost figures had drifted from the generated model.**
*Fix:* regenerated figures pasted in (laser 141.41, bending 60.00, coating 73.57,
subtotal 288.97, total 517.66).

**R13. Racking: one formula was questioned, three numbers disagreed.**
*Partly rejected.* For a shear panel of width W (in the load direction), height H and
thickness t, the shear area at a horizontal section is `t·W` and the drift is
`V·H/(G·t·W)`, so `k = G·t·W/H` — the expression used. The reviewer's proposed
`k = G·t·H/W` would be right for a panel loaded along its *height*. The side-slab term
was however missing a factor 2 (two slabs), and the connection's clearance take-up was
absent.
*Fix:* side-slab stiffness doubled; connection slop (0.25 mm coated hole clearance)
added as the governing term; one number now used everywhere (front-to-back 0.001 mm
elastic, capped by 0.25 mm of connection take-up; side-to-side 0.65 mm including the
panel's bolted connections).

**R14. Dust-cover wall clearance appeared as 350 / 60 / 34 mm.**
*Fix:* one statement: **40 mm behind the stand plus 360 mm of headroom above the plinth**
if the cover is hinged open; removed-for-play needs only 80 mm.

**R15. Two orphan drawing sheets and a blank underside render.**
*Fix:* orphans deleted, underside render re-shot with the floor plane removed, and the
two "section" renders replaced by 25–50 mm sections viewed isometrically.

## MINOR findings — fixed or noted

| # | finding | action |
|---|---|---|
| R16 | docs quoted 0.72 mm as "the governing deflection"; the base tray's 1.94 mm governs | corrected in `docs/01`, `docs/04` |
| R17 | tolerance stacks under-count the joint-alignment contribution; the Y-locating margin is 0.04 mm after coating | noted in `docs/03` §9 and in the "provisional" status; the slot's Y clearance is left at 0.2 mm nominal deliberately (it is the locating direction) and the fit is verified by the four design checks, not by tolerance arithmetic alone |
| R18 | self weight not in the FE load cases | noted; adding 4 kg of tray to 15 kg of payload raises the top tray's deflection from 0.32 to ~0.35 mm — it does not change any verdict, and the payload assumptions already carry a 2× margin over the real equipment |
| R19 | `grillage.moments()` ignores the edge-beam EI override | noted in `calc/shelf.py` docstring; stresses reported are from the plate strips, i.e. conservative for the flanges (the edge beams carry more of the moment than the strip model assigns them) |
| R20 | test plan required "no coating in the slots", which is impossible | corrected to "no coating bridging the slot, ≤0.1 mm per face" |
| R21 | `docs/13` had two wrong dimensions (166 mm of clear deck, 40 mm baffle height) | corrected to 99 mm and 24 mm |
| R22 | tool list "3 mm hex key" with a torque figure | `docs/05` now says a hex key plus "firm hand-tight, then a quarter turn", with 3 N·m as the reference value if a torque driver is used; nut/head washers are not used and the 33 MPa contact pressure is stated |
| R23 | dead code, stale docstrings, render count | cleaned |

## What the review did not and could not establish

The reviewer had no shell, so nothing was executed; every finding was derived by reading
code and artefacts, and every fix above was verified by re-running the pipeline
(`cad/check.py`, `cad/export.py`, `calc/run_all.py`, `cad/drawings.py`, `cad/render.py`)
and reading the regenerated output. **No one has built this stand.** The status label
reflects that.

## Residual risks carried into R0.9a

1. **Equipment identity (E1, E8, E9).** Unchanged and still the top blocker.
2. **The clamped joint's preload.** Modelled, not measured; 27:1 slip margin and 9:1
   opening margin, with a maintenance check.
3. **Speaker clearance at the top tray.** 1.4 mm from the modelled envelope; a
   box-shaped cabinet (rather than the modelled wedge) would still clear, but a rough
   cast edge or a rear connector could not. Called out in `docs/03` §7.
4. **Powder coat thickness in the nesting clearances.** 0.3 mm/side allowance against a
   worst-case stack of 0.46 mm: the panel may have to be tapped in with a mallet.
5. **Datum sensitivity.** The stand's height chain assumes the glide base sits on the
   floor and the deck is 32 mm up; a heavily dished floor consumes the ±5 mm travel.
