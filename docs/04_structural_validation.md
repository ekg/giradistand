# 04 — Structural validation: what was checked, how, and what it means

The full numbers are in `out/calc_report.md` (generated) and `out/cad_checks.md`.
This document is the engineer's reading of them: method, limits, governing modes and
the honest gaps.

## 1. Method summary

| check | method | file |
|---|---|---|
| shelf bending, deflection, stress | 3-DOF grillage FE (self-written), validated against two closed-form plate solutions | `calc/grillage.py`, `calc/shelf.py` |
| folded edge-beam participation | eccentric edge beam on the plate boundary, EI = E[t h³/12 + (t h)(h/2)²] | `calc/shelf.py` |
| joint slip, bearing, tear-out, preload | EC3-style design formulae, allowable values | `calc/joints.py` |
| racking both directions | separate stiffness models per mechanism + "friction lost" case | `calc/racking.py` |
| mass, centre of mass | computed from the CAD solids | `calc/stability.py` |
| tipping / sliding / rocking | overturning vs restoring moment about the real support polygon | `calc/stability.py` |
| tolerances | arithmetic worst case + RSS | `calc/tolerances.py` |
| interference, alignment, equipment fit | boolean CAD checks (22 pairs, 25 equipment-structure pairs) | `cad/check.py` |

No commercial FEA was used. The grillage model was written for this job because a
plate-bending problem had to be solved honestly at zero tooling cost; it is validated
against classical solutions rather than asserted.

## 2. Shelf results

Acceptance limits were set before the numbers were computed: 1.5 mm deflection for the
top and middle trays, 2.5 mm for the base tray, σ ≤ fy/2 = 102.5 MPa, and ≤ 0.5 mm
differential between turntable feet.

| shelf | governing load case | deflection | σ_max | factor on fy |
|---|---|---|---|---|
| top tray (15 kg) | uniform 15 kg | 0.72 mm | 16.8 MPa | 12.2 |
| top tray | 4 turntable feet, 40/30 eccentric | 0.37 mm | 16.5 MPa | 12.4 |
| top tray | 15 kg on one foot (overload) | 0.59 mm | 46.8 MPa | 4.4 |
| middle tray (10 kg) | 8 isolator pads | 0.48 mm | 11.6 MPa | 17.7 |
| base tray (40 kg) | uniform over the tray | 1.94 mm | 45.1 MPa | 4.5 |
| base tray | 40 kg on crate corners | 0.32 mm | 25.7 MPa | 8.0 |

Everything passes. Two results deserve comment because they are the reason the design
looks the way it does:

* **A flat 1.88 mm plate spanning 566 mm would deflect ≈7 mm** under 15 kg — six times
  the limit. The design does not rely on plate action. The 30 mm front and rear flanges
  turn the shelf into a shallow box with edge beams: the plate then spans 400 mm
  between the beams, clamped at the beams and at the two bolted end edges. That single
  change takes 7 mm to 0.72 mm. This is the "effective section shape instead of
  thickness" argument in numbers: going from 1.88 to 3.0 mm sheet would have
  quadrupled the weight and the cost to buy a factor of 4.1 in stiffness.
* **The 190 mm speaker bay is the least redundant part of the frame**, because the rear
  panel stops below it. The top tray's joints therefore carry a moment. `docs/04 §4`
  and `out/calc_report.md §7.2` show the two cases: clamped (0.65 mm drift at 100 N,
  passes) and pinned (2.58 mm, fails). The clamped condition is verified with a 27:1
  slip margin and the bolt group carries the moment in bearing as a backstop.

## 3. Where the model is optimistic, and by how much

| idealisation | direction of error | estimate |
|---|---|---|
| grillage reproduces closed-form plates 8–15 % flexible | conservative | — |
| plate edge treated as fully clamped at the tray end flanges | **optimistic** if the joint rotates; bounded by the "pinned" run (0.69 mm vs 0.32 mm for the top tray) | ≈0.4 mm |
| corner panels and corner reliefs not modelled (the front/rear edge beam is modelled as continuous from slab to slab) | optimistic, small: the beam ends 32 mm short of the support and load crosses the corner panels, which are stiff (33 × 30 mm L-plates) | <0.1 mm |
| local dishing of the 1.88 mm plate under a bolt head or a foot pad not modelled | optimistic | <0.05 mm |
| no residual stress, no flat-panel imperfections, no long-term creep | optimistic | qualitative |
| payloads are assumptions (15/10/40 kg) | — | utilisation scales linearly; the design has a factor of 4.4 at the assumed loads |

The "pinned joint" runs in `out/calc_report.md §6.2` are the honest bound for the
clamped-joint assumption, and even in that state every shelf deflection stays inside
1.5 mm. That is the useful conclusion: the shelves do not depend on joint friction;
only the 190 mm top bay's lateral racking does, and it has an independent backstop.

## 4. Joints

* M5 button head + DIN 6923 flanged locknut, 22 off, torque 3.0 N·m with a 3 mm hex key
  (bolt tension 3.0 kN, 42 % of the A2-70 capacity).
* Joint capacity per flange (3 bolts): bearing governs at 19.2 kN; bolt shear 14.3 kN;
  friction at μ = 0.30 with 9 kN of clamp = 2.7 kN.
* Slip margin against the 100 N handling disturbance: **27:1**. Bolt tension
  utilisation 42 %. Bearing utilisation at the same 100 N: 0.5 %.
* The joint carries moment the way a clamped joint does — by redistributing contact
  pressure, not through a bolt couple (the three bolts of a flange lie in one
  horizontal row). The moment at which the joint begins to open is
  `M_sep = N·h/6 = 45 N·m` per flange against a demand of 4.75 N·m: **margin 9:1**.
  This is preload-dependent, which is why the maintenance plan includes a torque
  check and why the lower bay has a friction-independent panel.
* Tear-out: nearest slot edge is 14.6 mm from the flange free edge, capacity
  7.8 kN/bolt.
* Powder coat is *not* protected by polymer washers in the structural stack (that would
  creep); the joint is steel-on-coated-steel and does not slip, so there is no fretting.
* The 6.8 mm slot is 5.5 mm wide: it gives ±0.65 mm of vertical adjustment and only
  0.25 mm of horizontal play, so the shelf cannot wander in the plane.

## 5. Feet

* 4 × M6 stud glides, 145 N each at full load, capacity ≈10 kN each in tension.
* Deck local pressure under the M6 flange nut: 1.44 MPa against 205 MPa yield.
* Level travel ≈ ±5 mm; the glides are replaceable with a twist and cost ≈$1.85.
* Non-marking polymer base (specified); felt pads are an acceptable substitute if the
  floor is delicate, with the levelling done by shims instead.

## 6. Stability — the number that matters

Unrestrained, the stand tips when a sustained horizontal force at 900 mm reaches:

| configuration | front/rear | side |
|---|---|---|
| fully loaded (59.4 kg) | 116 N | 170 N |
| records removed (37.4 kg) | 74 N | 108 N |
| empty stand (23.1 kg) | 38 N | 55 N |

A 100 N (10 kgf) sustained push at bench height does **not** tip the loaded stand
(margin 1.2), but a 74 N push does tip it with the records removed. That is normal for
a 37 kg piece of furniture with a 400 mm deep base, and it is not something a different
sheet-metal layout can fix — it is physics (`mg·b/2 / h`). The consequence is stated
rather than hidden:

> **The wall strap (P5) is part of the standard kit.** With it fitted, tipping is not a
> credible failure mode and the stand satisfies the brief's stability requirement in
> the restrained condition. Unrestrained, it satisfies a 60 N bump criterion in every
> stationary configuration except the empty stand (which is a moving condition).

Sliding: 175 N at μ = 0.30, 291 N at μ = 0.50 — 1.7–2.9× the 100 N disturbance.

## 7. What this does not establish

* **No physical test.** Nothing has been built, loaded or measured. Every statement
  above is analytical or geometric.
* **No supplier review.** SendCutSend has not seen or priced these files.
* **No dynamic analysis.** The first natural frequency of the frame is not computed.
  Masses, clamped joints and a 400 mm deep slab side make a stiff, damped structure
  likely, but "likely" is not evidence; the home test plan is how it gets established
  (`docs/06`).
* **No acoustic analysis.** See `docs/13`.
* **No long-term behaviour.** No creep data for the isolation pads, no fatigue check
  for 22 bolts that never see more than 0.5 % of their bearing capacity, no coating
  durability data.
* **Buckling** is not formally checked. At the computed stress levels (≤47 MPa,
  t/b = 1.88/400) plate buckling is far from governing, and the shelves are supported
  on all four edges; a formal check would be needed if payloads were doubled.
