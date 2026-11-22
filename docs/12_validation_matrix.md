# 12 — Final validation matrix

Evidence classes: **A** = analytically checked (calculation), **C** = CAD checked
(geometric/boolean, export re-import), **S** = supplier rule checked (published document
applied), **P** = physically tested (**none**), **R** = independent review.

Overall status: **provisional design, dimensionally checked (DXF and STEP feature
level), analytically validated, NOT assembly-validated and NOT supplier-accepted.**
Quote-ready only in the sense that the upload files exist and have been re-imported and
checked; the reviewer's finding that an earlier revision was not buildable is recorded
in `docs/11` along with the fixes. Not physically tested. Not fabrication-released:
equipment confirmation (E1–E4, S1) is still outstanding.

## A. Equipment and storage fit

| # | requirement | criterion | evidence | result | unresolved |
|---|---|---|---|---|---|
| A1 | turntable fits the top with a modest margin | ≥ 20 mm margin all round | C: 57.1 mm sides, 24.0 mm front/rear (`out/cad_checks.md` §5) | PASS (for the provisional deck) | deck identity unconfirmed (E1) |
| A2 | all turntable feet bear on a flat surface | no feature on the top face; feet inside the flat field | C: top tray has no holes/fixings on its top face; feet 55 mm inside the 3.3 mm bend tangent | PASS | foot positions assumed (E4); turntable's own feet do the final levelling |
| A3 | no interference between turntable and stand | 0 mm³ | C: §2 of `out/cad_checks.md` | PASS | dust-cover envelope is an assumption (E7) |
| A4 | dust cover can be removed / opened | clearance to wall | C: cover envelope inside the open top; 34 mm rear projection when hinged | PASS | cover geometry assumed |
| A5 | two horizontal speakers, grilles forward, side by side | bay ≥ 2 × W + gaps | C: 566.2 bay vs 534.0 pair | PASS | speaker width/variant unconfirmed (E8) |
| A6 | speakers on isolation with correct loaded height | bay ≥ speaker + compressed pad + handling | A/C: 190 ≥ 155 + 23 + 12; tolerance net +10.0 mm (`calc_report` §9.3) | PASS | pad compression is a manufacturer estimate |
| A7 | speaker connections, controls, ventilation accessible | ≥ 100 mm behind cabinets; front open | C: 206 mm behind each cabinet; controls on the open front strip | PASS | connector positions assumed from the manual's panel description |
| A8 | one removable record container with insertion and removal path | 0 interference over the whole path | C: 0.000 mm³ at 0–400 mm of forward travel (`cad_checks` §6) | PASS | container not chosen by the owner (S1) |
| A9 | upright LPs, browsable | crate fits with handles accessible | C: 99 mm clear each side, 41 mm above the rim; browse with the crate drawn out | PASS (with the stated browsing method) | — |
| A10 | two crates not silently assumed | explicitly evaluated | C: 2 × 368.3 = 736.6 vs 566.2 bay → does not fit; width would go to ≈752 | PASS (conflict surfaced) | 2-crate variant not modelled |
| A11 | footprint as close to the turntable as practical | explained minimum | A: width set by the speaker pair (570 vs 452 = +26 %), depth set by the crate (400 vs 352 = +14 %) | PASS with explanation | — |

## B. Geometry, structure and stability

| # | requirement | criterion | evidence | result | unresolved |
|---|---|---|---|---|---|
| B1 | shelf deflection acceptable | ≤1.5 mm top/mid, ≤2.5 mm base | A: 0.72 / 0.48 / 1.94 mm worst cases (`calc_report` §6) | PASS | payloads are assumptions (C10) |
| B2 | turntable stays level | foot differential ≤0.5 mm | A: 0.0–0.08 mm; 0.50 mm only under a 15 kg single-foot overload | PASS | — |
| B3 | shelf stress within a factor of 2 on yield | σ ≤ 102.5 MPa | A: max 46.8 MPa (factor 4.4) | PASS | factor 2 objective exceeded |
| B4 | load path from every shelf to the floor | explicit | A: shelf → flange clamp → bolt group → slab in-plane → feet | PASS | — |
| B5 | racking, side-to-side | ≤2.0 mm at 100 N | A: 0.65 mm with clamped joints; 2.58 mm if the upper joints were pins (`calc_report` §7.2) | PASS, conditional on the clamped joint (slip margin 27:1, opening moment 9:1) | joint preload is modelled, not measured; the claim that bolts form a bearing couple was withdrawn (review R5) |
| B6 | racking, front-to-back | ≤2.0 mm at 100 N | A: 0.001 mm elastic (side slabs act as shear panels) | PASS | — |
| B7 | positive (non-friction) racking mechanism | required | C/A: P4 rear panel is a bolted shear diaphragm in the lower bay | PASS for the lower 400 mm | the upper 190 mm bay is friction-dependent by design, with a documented margin and a torque check |
| B8 | tipping, unrestrained | ≥60 N tip force at 900 mm in every stationary case | A: 116 N (loaded), 74 N (records removed), 38 N (empty) (`calc_report` §8) | PASS except the empty stand | empty stand is a moving condition; **wall strap supplied as standard** |
| B9 | tipping, restrained | not a credible mode | A + design: P5 strap specified in the standard kit | PASS (by design) | requires 2 wall fixings — the only home operation outside the kit |
| B10 | sliding | ≥2× the disturbance | A: 175 N at μ=0.30, 291 N at μ=0.50 | PASS | floor friction is assumed |
| B11 | rocking | eliminated by levelling | A/C: 4-point support, ±5 mm travel, deck local flexibility 0.3 mm at 40 kg | PASS | — |
| B12 | asymmetric / partly withdrawn storage | evaluated | A: CoM shifts to y=+70 with the crate 200 mm out; tip force 73 N | PASS (restrained) | — |

## C. Manufacturability (supplier rules)

| # | requirement | criterion | evidence | result | unresolved |
|---|---|---|---|---|---|
| C1 | material and thickness in stock | .074 in CRS listed | S [5] | PASS | — |
| C2 | bend parameters are the supplier's, not invented | R 1.60 / K 0.40 / BD 3.277 | S [6]; every flat pattern derived from them | PASS | re-check if another supplier is used |
| C3 | min flange length | ≥ 8.13 mm formed | S: smallest flange 20 mm; P5 stub 18 mm to the bend line | PASS | P5 is the only part near the limit |
| C4 | hole/slot to bend clearance | ≥ half the die width (6 mm) | S: slots 8.6 mm from the bend centre line | PASS | — |
| C5 | part size limits | ≤762 × 1117 cut, ≤762 × 914 coated | S/C: largest 619.7 × 453.5 flat | PASS | — |
| C6 | bend length limit | ≤1117 mm | S: longest bend 619 mm | PASS | — |
| C7 | no hems / 180° folds assumed | max bend angle 130° | S [7]; the design uses no hems | PASS (hems rejected, not assumed) | exposed edges are deburred + coated, not hemmed |
| C8 | corner reliefs square (not rounded) | supplier warning on assembly uploads | S [8]; flat patterns use square notches | PASS | — |
| C9 | uniform thickness solids, one body per part | required for STEP upload | C: each STEP re-imports as 1 valid solid, uniform 1.88 mm, dimensions matching to <0.02 mm (`out/export_verification.json`) | PASS | not uploaded, so not confirmed by the supplier |
| C10 | no threads on parts | no tapping, no thread chasing | S [10] ("tapped holes are not plugged — expect to chase threads") + design: zero threads on parts | PASS | — |
| C11 | hardware insertion not needed | — | design: through-bolts + locknuts | PASS | — |
| C12 | DXF flat patterns valid | closed contours, mm, 1:1, CUT/BEND layers, correct feature counts and slot orientation | C: re-read with ezdxf; hole counts, bend counts, arc radii, outline closure and hole containment all checked per part — all five `ok: true` (`out/export_verification.json`) | PASS (after fixing review R2/R3) | — |
| C13 | editable parametric source | one parameter set | `cad/params.py` drives CAD, DXF, drawings, renders, BOM, calculations | PASS | — |

## D. Joints, tolerances and assembly

| # | requirement | criterion | evidence | result | unresolved |
|---|---|---|---|---|---|
| D1 | small consistent fastener family | 1 size for structure | design: M5 throughout; M6 only for the feet | PASS | — |
| D2 | joint does not slip in service | margin ≥5 | A: 27:1 at 100 N (`calc_report` §5.1) | PASS | preload from an assumed torque |
| D3 | positive backstop if friction is lost | required | A/C: bolts bear in 5.5 mm holes (slot is vertical only) | PASS | — |
| D4 | no force-fitting | worst stack ≤ available movement | A: ±0.58 vs ±0.65 mm (`calc_report` §9.1) | PASS | bend tolerance is a published figure |
| D5 | coating and production tolerances in clearances | included | A: `calc_report` §9.2–9.5 | PASS | — |
| D6 | fastener envelopes and tool access modelled | no interference; every nut reachable | C: all 22 bolts vs P1–P4 **and** vs turntable/speakers/crate/pads = 0 mm³; button head inside, locknut outside for wrench access (`out/cad_checks.md` §3) | PASS (after fixing review R1) | — |
| D7 | assembly order is physically possible | sequence checked, no trapped part | C + `docs/05`: every bolt is inserted from inside the open bay and every nut turned from outside; the base tray's closed skirt was found to block the old arrangement and the fastener direction was reversed (review R1) | PASS (reasoned + geometric) | not built |
| D8 | one-person assembly | stated | `docs/05`: 35–45 min, one person (a second is optional for the tilt-up in step 4) | PASS (claimed) | not performed |
| D9 | replaceable floor-protecting feet + levelling | required | design: M6 glides + locknuts, ±5 mm; polymer base | PASS | floor protection of the specific base material unverified |
| D10 | no polymer in structural joints | required | design: no washers of any kind in the clamped stack | PASS | — |
| D11 | safe exposed edges | deburred, R3 corners, no hems available | S [7] + drawing notes | PASS (as far as the process allows) | — |
| D12 | disassembly | reversible | design: all locknuts, no adhesive, no press fits | PASS | — |

## E. Documentation and process

| # | requirement | evidence | result |
|---|---|---|---|
| E1 | reproducible calculations with sources, formulas, units, assumptions | `out/calc_report.md`, `calc/*.py` | PASS |
| E2 | FEA used only if credible, else honest analytical checks | self-written grillage FE + validation vs 2 closed-form solutions; limits stated | PASS |
| E3 | exports re-opened and compared | `out/export_verification.json` (5 STEP + 1 assembly + 5 DXF) | PASS |
| E4 | dimensioned drawings | `out/drawings/` S1–S6, A2, PNG + PDF | PASS |
| E5 | rendered views + exploded | `out/renders/` 01–10 | PASS |
| E6 | BOM + cost, labelled as estimate | `out/bom.csv`, `out/cost_model.md`, `docs/07` | PASS (estimate only) |
| E7 | upload guide, exact files | `docs/08` | PASS |
| E8 | independent review + log | `docs/11` — 6 critical, 9 major, 8 minor findings; all critical and major fixed, one rejected with reasoning | PASS (review performed; fixes verified by re-running the pipeline) |
| E9 | change log | `docs/10` | PASS |
| E10 | input register with verification status | `docs/02`, `out/input_register.csv` | PASS |
| E11 | assembly instructions + test plan | `docs/05`, `docs/06` | PASS (proposed) |
| E12 | sources | `docs/09` | PASS |

## E2. Review-derived checks added

| check | evidence | result |
|---|---|---|
| every fastener clears every part and every equipment envelope | `out/cad_checks.md` §3 | PASS, 0.000 mm³ |
| DXF feature counts / arc radii / closure / containment | `out/export_verification.json` | PASS, 5/5 parts |
| strap attachment hole exists in the top tray and clears the turntable | `out/cad_checks.md` §3b | PASS |
| feet reach the floor datum in the model | `cad/model.py::make_foot`, `out/cad_checks.md` | PASS |

## F. Physically tested

| # | item | status |
|---|---|---|
| F1 | shelf deflection measured under load | **NOT RUN** |
| F2 | joint slip / loosening after a week | **NOT RUN** |
| F3 | assembly time measured | **NOT RUN** |
| F4 | racking drift measured | **NOT RUN** |
| F5 | acoustic feedback / rattles | **NOT RUN** |
| F6 | coating durability at clamped faces | **NOT RUN** |

## G. The three things that would block a manufacturing release

1. **E9 — which face of the speaker rests on the shelf.** If it is the 155 mm face, the
   speaker bay must be 194 mm high and *P1, P2, P4 all change size* (all three part
   numbers, and the flat patterns).
2. **E1/E8 — equipment identity.** A different turntable depth or speaker width changes
   `D_OVER` or `W_OVER`, which changes P1, P2, P3, P4 and the rear panel width.
3. **S1 — record container.** A taller crate than 358.8 mm changes `H_REC`, therefore
   P1's height and P4's height.

Everything else is a documented default that can be changed in `cad/params.py` and
regenerated in about three minutes.
