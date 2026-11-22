# 13 — Vibration, acoustics, damping and real-world use

This document separates what the design *does* from what remains unknown. Nothing here
is measured. The stand was designed to give the turntable and the speakers the best
mechanical arrangement the brief's constraints allow, and to make the remaining
problems testable rather than hidden.

## 1. The unavoidable compromise, stated up front

The brief requires one stand carrying a turntable *above* two powered speakers. That is
the single worst arrangement for vinyl playback: the speakers' acoustic output drives
the same structure the stylus reads, and the turntable's own manual says do not place it
near loudspeakers [1]. The design mitigates the three coupling paths it can:

| path | mitigation | residual |
|---|---|---|
| **structure-borne** (speaker cabinet → shelf → frame → platter) | 4 elastomer isolators per speaker, loaded at ~29 % of their rated capacity so they are compliant rather than bottomed out; the speakers sit on the tray, not on a rigid bracket, and the speaker's own mounting holes are deliberately *not* used | low-frequency transfer is unavoidable; a 3.16 kg cabinet on 24 mm pucks still couples below ~40 Hz |
| **airborne** (speaker output → plinth/cover → stylus) | speakers are 190 mm below the plinth, in a bay with an open front and rear, and the top tray is a solid plate between them | the plinth is exposed to the speakers' upper output; the dust cover should be off during play |
| **frame resonance** (sheet-metal panels ringing) | 1.88 mm plates with folded flanges; every joint is clamped at ≈9 kN per flange; the trays are bolted at 3 points, not 1 | thin steel panels *do* ring; the optional damping tape exists for this reason and is specified as a retrofit if the home test hears it |

The honest statement: **a shared stand is a compromise and no claim of isolation is
made.** The design makes it as good as the arrangement allows, and the test plan
(`docs/06`) is how you find out whether your particular combination is quiet enough.

## 2. Isolation selection, with numbers

* Speaker: 3.16 kg. Four ISO-PUCK mini per speaker: 4 × 2.75 kg = 11 kg of capacity, so
  each unit carries 29 % of its rating. That is inside the manufacturer's guidance to
  stay at least 10 % away from the limit, and loaded height is ~23 mm of the 24 mm
  free height, i.e. the pad barely compresses.
* Loaded height 23 mm is what the 190 mm speaker bay is sized for: 155 + 23 + 12 mm of
  handling clearance.
* **Any thinner isolator is safe** (more clearance). Anything *taller* than 24 mm needs
  `H_SPK` raised — e.g. the full-size ISO-PUCK (26 mm) would still fit only if the
  handling clearance is reduced, so it is not recommended.
* Sorbothane hemispheres or 6 mm cork/rubber pads are acceptable substitutes with the
  same or lower height; they will not have published load ratings, so they are a
  judgement call, not an equivalent.
* Contact: the pads sit on the flat middle tray and under the cabinet's base face,
  inset 32 mm from the cabinet's footprint corners. If the cabinet bottom is not flat
  (register item E10), use three pads or a 6 mm plywood shoe.

## 3. Damping, if you need it

* Symptom: a metallic ring when you tap the top tray with the stylus up, or a buzz on
  bass-heavy passages that disappears when you press on the tray.
* Fix (optional, ≈$22): 3M 2552 aluminium-foil constraining-layer tape, 25 mm wide,
  four strips across the *underside* of the top tray (between the flanges, avoiding the
  bolt heads) and two strips on the underside of the middle tray. It is 0.25 mm thick,
  tolerates ~65 °C, does not interfere with any clearance, and can be removed.
* Do not put anything soft between the clamped steel faces: that would trade a real
  stiffness loss (creep, loss of the friction grip) for a cosmetic gain.

## 4. Cables, connectors and ventilation

* The record bay is closed at the rear by the shear panel; the speaker bay and the
  turntable level are open at the rear. All connections — turntable RCA/USB/DC, speaker
  RCA/DC/AC — are made in free air with ≥20 mm behind each plug and 206 mm behind each
  speaker cabinet.
* No cable has to pass through a hole, a gap under 10 mm, or a slot. Cables drop off the
  rear edge; a hook-and-loop tie around the rear panel's edge is enough to dress them.
* The speakers are sealed acoustic suspension cabinets with no ports; the "ventilation"
  in their manual is about not smothering the amplifier in an enclosed space. An open
  front and rear, 206 mm of space behind, and 20 mm between the cabinets is
  conservative.
* The turntable's power supply sits on the floor or on the record bay's deck beside the
  crate; 166 mm of clear deck is left at one side of the crate for it.

## 5. Ergonomics and listening geometry

* Turntable support at 626 mm, plinth top at 767 mm: a low-console height. Cueing is
  comfortable from a chair and workable standing. Raising it is a one-parameter change
  (`H_SPK`) with a described visual cost (`docs/01 §5`).
* Speaker acoustic centres end up **287 mm apart**. That is very close. Stereo imaging
  will be narrow and the pair will behave almost as a single source unless you sit
  close: at 1.0–1.5 m the geometry is defensible; at 3 m it will sound like one wide
  speaker. This is inherent to "two horizontal speakers side by side on a compact
  stand" and cannot be fixed without widening the stand (the parameter is `SPK_GAP`;
  a 120 mm gap adds 100 mm to the width).
* The baffle in the documented horizontal orientation is tilted up by the product's own
  38.6°. With the baffle's bottom edge ~40 mm above the shelf, the axis crosses a seated
  ear height at ≈1.5 m. If you listen further away, a pair of small wedges under the
  front of each cabinet (not supplied — a 40 × 20 × 194 mm hardwood wedge lifts the
  front 20 mm and removes about 6° of tilt) is a sensible accessory.
* Turntable margins: 57 mm each side, 24 mm front/rear. Cueing and record handling are
  clear on all four sides; the open top means the dust cover can be lifted off
  vertically without touching anything.

## 6. Care

* Powder coat: wipe with a damp cloth. No solvents, no abrasives. Wrinkle/textured
  finishes trap dust in the texture; a soft brush works better than a cloth.
* Annual: re-torque the 23 M5 locknuts (1/8 turn check), check the feet, re-check the
  platter with a bubble level, look for white corrosion at any clamped edge.
* Do not drag the stand with the crate loaded: lift it, or unload first. Dragging on a
  hard floor wears the polymer glides and can walk a locknut loose.
* The record crate should be drawn forward, not levered; it is not a structural part.
* Moving house: disassemble (reverse of `docs/05`), and keep the turntable's own
  packaging for the platter and counterweight — the stand does not need any.
