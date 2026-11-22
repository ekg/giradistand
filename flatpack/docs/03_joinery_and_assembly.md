# 03 — Joinery, assembly and disassembly

## 1. How each joint locates, carries load and resists withdrawal

| direction | mechanism | positive or friction? |
|---|---|---|
| vertical load | the tab bears on the slot's lower face, 150 × 18 = 2700 mm² per end (0.03 MPa at the design load, vs 8 MPa bearing) | **positive** |
| fore-aft (Y) | the slot is 150.2 long for a 150.0 tab: the tab ends bear on the slot ends (±0.1 mm) | **positive** |
| lateral (X) inward | the tab shoulder bears on the side panel's inner face | **positive** |
| lateral (X) outward | the 8 mm dowel through the protruding tab bears on the side panel's outer face, 4 mm of free play away | **positive, gravity-retained** |
| rotation about X | the 18 mm tab in an 18.2 mm slot: ±0.1 mm of play over 150 mm = 0.076° | positive, near-rigid |
| rotation about Y | same, over the 18 mm thickness in the slot, plus the second tab at the other end | positive |
| racking (X) | the shelves act as diaphragms plus the panels' own out-of-plane stiffness (EI = 1.41 kN·m² per panel) | positive; `docs/04` shows it passes even with pinned joints |
| racking (Y) | the side panels are in-plane shear panels | positive |

No glue, no fastener, no press fit is load-bearing in the shelf joints. The only
friction-sensitive element is the dowel, and it is retained by gravity: it stands 11 mm
proud in a vertical hole and cannot fall out.

## 2. Joint dimensions (the numbers that must be right)

| parameter | value | why |
|---|---|---|
| tab length × thickness | 150.0 × 18.0 | matches the shelf's own thickness |
| slot | 150.2 × 18.2 (nominal t + 0.20) | **the slot width is set from the fit coupon** |
| dogbone reliefs | R4 at each slot corner | a Ø6.35 cutter cannot cut a sharp internal corner; without relief the tab's square corners collide |
| tab protrusion | 18.0 past the panel's outer face | room for the dowel hole and the dowel's bearing face |
| dowel hole | Ø8.4, 22 mm from the shoulder (4 mm past the outer face) | 4 mm of play, then the dowel stops withdrawal; 14 mm of material to the tab end (1.75 d) |
| dowel | Ø8 × 40 birch, 11 mm proud each side | gravity-retained, liftable by hand |

## 3. Assembly sequence (checked for insertion direction and access)

**Tools: a rubber mallet. Nothing else. 20–25 minutes, one person.**

1. **Identify.** P1 side panels (2, identical — the slot pattern is symmetric in Y so
   there is no left/right). P2 shelves (2, identical), P3 base shelf (the one with four
   6.6 foot holes), P4 strap, P5 coupon, bag of 6 dowels. Ink or a pencil mark on the
   *inner* faces: "IN" and an arrow to the front.
2. **Feet.** Screw the four M6 glides into P3 from below (they are the only threaded
   items in the kit apart from their nuts). Nothing else goes into P3.
3. **First side down.** Lay one P1 flat on a rug, **outer face down**, front edge toward
   you.
4. **Shelves in.** Insert the base shelf (P3) into the *lowest* slot, then the two
   shelves into the middle and top slots. Each slides in from the side and stops when its
   tab shoulder meets the panel — a light tap with the mallet, never a hard blow.
   *Check:* all three shelves now stand up like a ladder, all projecting 18 mm past the
   panel, all with their dowel holes on the same side.
5. **Second side on — the only step that wants care.** Lift the second P1 over the three
   protruding tabs, front edge aligned, and lower it so all three tabs enter the three
   slots together. Tap it down with the heel of your hand, then the mallet. One person can
   do this; two make it easier because the tabs can be guided.
6. **Dowel it.** Drop one dowel into each of the six tab holes (both ends of all three
   shelves). Push it through with a thumb; it should pass with light hand pressure.
   *Check:* with the dowels in, no shelf can be pulled out by hand.
7. **Stand it up** and check the four feet carry load. Adjust the glides until the top
   shelf is level within ~1 mm per 300 mm; lock the M6 nuts on the deck's top face.
8. **Wall strap.** Bolt the strap's foot down through the 6.6 hole at the top shelf's
   rear margin (one M5 bolt + locknut, in the kit). Hold the strap's wall flange against
   the wall with **no tension**, mark the hole, drill a 3 mm pilot and drive the fixing
   for your wall type. Re-check the feet afterwards.
9. **Isolators and equipment.** Eight isolation pads on the middle shelf at the four
   marked positions per speaker; speakers in from the front, grilles forward; record
   crate in from the front; turntable on top, platter levelled with the turntable's own
   feet.

**Do not**: sand a joint to make it fit (change the cut), force a visibly misaligned
joint, glue anything (it can all come apart), or put the dowels in before both sides are
on.

## 4. Disassembly (2 minutes)

1. Equipment and crate out. 2. Strap off the wall. 3. Pull the six dowels out. 4. Slide
the second side panel off the three tabs. 5. Lift the shelves out. 6. Glides out.
The kit re-packs as six flat panels, 638 × 394 the largest — it fits in a car boot.

## 5. Where the parts come from and what "ready to assemble" means here

* Every hole, slot, dogbone and profile is CNC-cut. **No drilling, sawing, chiselling or
  routing at home.** The single exception is the 3 mm pilot for the wall fixing, which no
  shop can do for you.
* The kit is **sanded, unfinished**. If you want a finish, it goes on before assembly
  (and the slots will be that much tighter — see `docs/05` §4).
* **Holding tabs.** A router may leave small tabs or onion-skin holding the parts in the
  sheet. This kit must arrive with them removed: they cannot be on mating faces (tab
  ends, slot walls) or on visible faces. Confirm this when you order; if tabs are
  unavoidable, they must be on an underside and the shop must remove them. A kit with
  tabs still attached is not ready to assemble.
* Labels: pencil on the inner faces, or a printed sheet in the box. **Never laser-engrave
  labels into visible faces** — they read as cuts and they spoil the finish.

## 6. If a joint does not go together

| symptom | cause | action |
|---|---|---|
| shelf will not enter a slot | slot too tight for the actual thickness | stop; re-cut the slot (or use the coupon's larger clearance next time) |
| shelf rattles in the slot | slot too loose | the dowel still locks it; note the measurement for the next kit |
| second side will not go on | one shelf is not fully seated, or a tab is damaged | lift off, re-seat all three, try again |
| dowel will not enter | hole fouled by a holding tab or a burr | clear it with a 8 mm drill bit **by hand** (twist, not a power drill) and re-check |
| stand rocks | floor or feet | adjust the glides; check nothing is under a foot |
