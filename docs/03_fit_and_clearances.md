# 03 — Fit, dimension chains and the envelopes used

All values mm unless stated. CAD units are mm; inches given for review (1 in = 25.4 mm).
Every number here is produced by `cad/params.py` (`python3 cad/params.py` prints the
same chain) and checked geometrically by `cad/check.py` (results in
`out/cad_checks.md`).

## 1. The width conflict, resolved explicitly

The brief warns that two 10.5 in (267 mm) speakers side by side need 534 mm before
anything else. That is correct, and it is what sets the stand's width:

```
speaker pair                2 x 267.0            = 534.0
central gap between cabinets                     =  20.2   (minimum useful separation)
side clearance, each side   2 x 6.0              =  12.0   (hand access, isolation pads)
-----------------------------------------------------------
speaker bay clear width                          = 566.2
+ 2 x side slab 1.88                             =   3.8
-----------------------------------------------------------
overall width                                    = 570.0
```

Consequences, stated plainly:

* The turntable (452 mm) is **not** the width driver. It sits on a 566.2 mm shelf with
  **57.1 mm margins each side**, which is a generous margin for a 570 mm stand.
* There is no credible way to reduce the width while keeping both speakers horizontal
  and side by side. Reducing the central gap to zero saves 20 mm; reducing the side
  clearance to 2 mm saves 8 mm — and then the speakers cannot be lifted in.
* Asking for "a footprint close to the turntable's" (452 × 352 = 0.159 m²) is
  therefore satisfied only to 570 × 400 = 0.228 m², **+43 %**. The stand is as close
  to the turntable as the speaker pair allows, and no closer.

### Is a narrower top over a wider speaker bay worth it?

A stepped side slab (narrow at the top, wide at the speaker level) was assessed and
rejected:

* it saves nothing on the **footprint**, because the footprint is set by the widest
  level (the speaker bay), which still has to exist;
* it would make the speaker bay's shear path eccentric and add a 60 mm cantilever at
  the joint that carries the turntable, i.e. it makes the top *less* level;
* it needs a third tray width (the top tray would be 452 + margins = ~500 mm against
  566 mm), i.e. a third unique part number and a second set of bend settings.

The top tray is therefore the same part as the speaker tray — one part number, two
pieces, and a 1.88 mm shadow gap between the tray edge and the slab face at every
level.

## 2. Speaker bay clear width chain

```
left slab inner face                              = -283.12
left cabinet outer edge            -277.12   (6.00 side clearance)
left cabinet inner edge             -10.12
central gap                                       =   20.24
right cabinet inner edge            +10.12
right cabinet outer edge           +277.12   (6.00 side clearance)
right slab inner face                             = +283.12
```

Nothing intrudes horizontally: the tray end flanges sit *outside* the interior (they are
lapped onto the slab outer faces, x = 281.24…283.12) and the locknuts protrude 5 mm
further inboard, but they are all at the *shelf levels* (z = 20.0, 421.9, 613.8), i.e.
below the speakers' underside (457.9) or above their top (612.9). Verified as 0 mm³ of
interference between the bolt envelopes and every equipment envelope in
`out/cad_checks.md` §2–3. The bay is 566.24 wide against 534.0 of equipment.

## 3. Overall height chain

```
floor                                              0.0
levelling glide base (9.0 high, M6 x 40 stud)      -> 32.0   deck top surface (nominal, +/-5 adjustable)
base tray plate 1.88                               -> 32.0
record bay clear height                           400.0     (crate 358.8 + 41.2 spare)
middle tray plate 1.88                             -> 433.88 (top surface)
speaker bay clear height                          190.0     (155 speaker + 23 compressed pad + 12 handling)
top tray plate 1.88                                -> 625.76 = turntable support surface
turntable body 141.6                               -> 767.36 = plinth top in use
```

The record bay is 400 rather than 372 because the middle tray's 30 mm front flange
hangs into the top of the bay; the crate (358.8) must pass *under* it while being slid
out, and 400 − 30 = 370 > 358.8 leaves 11.2 mm. That is the whole reason for the
extra height, and it is not decoration: it is the difference between a crate that
slides out and one that cannot.

## 4. Depth chain

```
rear face of the body                            -200.0
side slab / tray depth                           400.0
rear panel web (1.2 clearance + 1.88)            -196.9 … -195.0
record bay clear depth (to crate rear face)      393.8
crate depth                                      368.3   (25.5 spare)
front face of the body                           +200.0
```

The record bay's **usable height** is 370 mm, not 400: the middle tray's 30 mm
front flange hangs into the top of the bay and the crate must pass under it.
That is the dimension to compare a container against (see §8).

* **Cabinet depth 400 mm** versus **space to the wall**: with the dust cover removed
  for play (Audio-Technica's own recommendation) 80 mm behind the stand is enough for
  RCA, USB and DC plugs plus a cable bend. With the cover *hinged and open* it
  projects 34 mm beyond the stand and leans up to 1099 mm high, so about 40 mm behind the stand plus 360 mm of headroom is then needed — either is a small fraction of a typical 400 mm console gap.
* The turntable's rear connectors sit at y ≈ −176 (24 mm inside the shelf edge), so
  cables leave the plinth and fall into open air behind the top tray. Nothing touches a
  cable.

## 5. Shelf surface vs clear opening vs operating clearance

These are different quantities and are listed separately:

| quantity | value |
|---|---|
| shelf **surface** (top tray, usable flat area) | 566.2 × 400.0 mm, no holes, no fixings |
| shelf surface **flat field** (inboard of the bend tangents) | 562.9 × 396.7 mm |
| **clear opening** of the speaker bay | 566.2 W × 400 D × 190 H |
| **clear opening** of the record bay | 566.2 W × 393.8 D × 400 H (370 usable) (open front) |
| operating clearance: cueing hand above the platter | open above the stand — no limit |
| operating clearance: speaker controls | front-left strip of each baffle, reachable from the open front |
| operating clearance: speaker connectors | 206 mm free behind each cabinet |
| operating clearance: crate sliding out | 400 mm of floor in front of the stand |

## 6. Turntable support — the flatness requirements that matter

* All four turntable feet bear on a **single flat plate**: the top tray has no holes,
  no screw heads, no keys and no lip on its top face. The only features on the top face
  are the 3.3 mm bend tangent zones at the perimeter, and the feet (42/45 mm inboard)
  are 55 mm inside those.
* The tray is levelled by the four M6 glides at the base (≈±5 mm travel), and the
  platter is levelled on the turntable's own adjustable feet (±8 mm), which is the
  manufacturer's intended method. Two independent levelling stages is deliberate: the
  stand gets the shelf roughly level, the turntable gets the platter exact.
* Computed differential deflection between the four turntable feet under the design
  load is 0.0 mm (symmetric) to 0.08 mm (40/30 mm eccentric) and 0.50 mm for a 15 kg
  single-foot overload. A 0.5 mm differential across 264 mm of foot spacing is a
  0.11° tilt of the plinth — invisible to playback and inside the turntable's own
  levelling range.

## 7. Speaker fit — what is and is not checked

Checked geometrically (`out/cad_checks.md`):
speaker envelope vs every structural part (0 mm³ interference), pads vs shelf and
cabinet, bay height (190 vs 178 required), cabinet-to-slab clearance (6 mm), and the
0 mm³ result for the dust-cover envelope everywhere except open air.

Not checked, and stated as such: the location of the speaker's own connector cut-outs,
the exact silhouette of the die-cast end caps, the grille's protrusion beyond the
modelled envelope, and whether the cabinet's bottom face is flat over the four pad
positions (E10). All four are inside the modelled envelope by inspection of the
photographs and are listed as measurement requests in `docs/02`.

## 8. Record container — insertion, removal and browsing

* Insertion: the crate is lowered onto the base tray between the slabs (99 mm clear
  each side) and pushed back until it touches the rear panel. Nothing has to pass a
  lip, a rail or a key.
* Removal: `out/cad_checks.md` §6 evaluates the crate translated forward in 50 mm steps
  to 400 mm — **0.000 mm³ interference at every position**, including under the middle
  tray's front flange.
* Browsing: with the crate in place there is 41 mm above its rim, deliberately not
  enough to flick through records. The intended use is to draw the crate forward onto
  the floor (or lift it out by its side handles through the 99 mm gaps) and browse
  there. This is stated in the instructions so it is not a surprise.
* Capacity: one 14.5 in crate (80–100 LPs). Two will not fit — 736.6 mm of crate
  against a 566.2 mm bay. If two crates are required the stand becomes ≈752 mm wide,
  which is a parameter change, not a redesign.

## 9. Tolerance and assembly reality

* Worst-case joint misalignment in the bending direction is **±0.58 mm** (bend-to-edge
  ±0.38, two laser positions ±0.10) against **±0.65 mm** of movement in the 6.8 mm
  slots, so no part has to be forced. Derivation in `out/calc_report.md` §9.1.
* In the locating (Y) direction the stack is ±0.20 mm against a 0.5 mm hole clearance.
* Coating adds 0.05–0.13 mm per side: included in every clearance, in the nested rear
  panel (0.6 mm total allowance) and in the 5.5 mm bolt holes (5.24 mm effective hole
  against a 5.0 mm shank).
* Nothing relies on nominal CAD alignment: the trays are free in Z by ±0.65 mm and are
  set level by the assembler before final tightening (procedure in `docs/05`).
