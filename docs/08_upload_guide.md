# 08 — Supplier upload guide (SendCutSend)

Verified against the supplier's published pages on the date of this package (see
`docs/09` for the exact sources). **Nothing was uploaded; these instructions have not
been executed.** If the checkout behaves differently, the supplier's live rules win.

## Before you start

* The authoritative geometry for every bent part is the **folded STEP** file. SendCutSend
  accepts STEP for bent parts, unfolds with its own tooling, and asks you to confirm
  bend angles and flange directions in its 3D preview. The DXF flat patterns in
  `out/dxf/` are a checked reference (and useful for a second quote) — upload them only
  if a supplier asks for flat files, and upload only the `CUT` and `BEND` layers.
* The models were built with SendCutSend's own parameters for 0.074 in mild steel:
  inside radius 1.60 mm, K factor 0.40, bend deduction 3.277 mm per 90°. Do not let
  anyone re-model them with a different rule without re-issuing the flat patterns.
* Files are in millimetres, 1:1, and each contains exactly one solid body of uniform
  thickness.
* No part carries a thread, so **no hardware insertion and no tapping** are required.

## Step by step

1. Go to `app.sendcutsend.com`, start a new quote.
2. Upload, one at a time (each file is a single part):
   `P1_SIDE_SLAB.step` → quantity **2**
   `P2_SHELF_TRAY.step` → quantity **2**
   `P3_BASE_TRAY.step` → quantity **1**
   `P4_REAR_PANEL.step` → quantity **1**
   `P5_WALL_STRAP.step` → quantity **1**
3. For each part set:
   * **Material:** Mild Steel (CRS) 1008/1010
   * **Thickness:** 0.074 in (1.875 mm)
   * **Cutting:** Laser
   * **Deburring:** ON
   * **Bending:** ON for P2, P3, P4, P5; OFF for P1
   * **Powder coating:** ON, colour **Textured Black (BK01)**
   * **Hardware insertion / tapping / countersinking:** OFF
4. In the 3D preview, confirm for each bent part:
   * P2: four flanges, all bent the same way, **90°**, flanges pointing **away from the
     top face**;
   * P3: same as P2 (the front/rear flanges are 20 mm, the end flanges 30 mm);
   * P4: two flanges, 90°, both pointing to the same side;
   * P5: one flange, 90°.
   If the preview shows a flange folding the wrong way, stop and re-check — do not
   approve it.
5. Check the checkout summary against `out/bom.csv`: 7 pieces across 5 line items,
   15 bends total (0 + 8 + 4 + 2 + 1), one finish.
6. Compare the total with the estimate in `docs/07`. If it is more than about $400 for
   fabrication, get a second quote from OSH Cut with the same files before ordering.
7. Order the purchased items separately (`docs/07`).

## What to expect in the box

* Deburred, bent, powder-coated parts. SendCutSend applies coating *after* bending, and
  caps/plugs any hardware (there is none here).
* Witness marks from bending are normal and are coated over.
* Bend-to-edge tolerance ±0.38 mm and bend angle ±1°. The design absorbs both: the
  trays' 6.8 mm slots take the vertical component, and the rear panel is 0.6 mm
  narrower than the opening.
* **No** edge sealing, **no** thread chasing, **no** fitting of inserts — none is
  needed.

## If the supplier comes back with a problem

| message | cause | response |
|---|---|---|
| "open contours" | a flat DXF was uploaded with open polylines | upload the STEP instead |
| "bend radius does not match our specs" | model not built with 1.60 mm / K 0.40 | the STEPs here already use these; ask them to confirm before changing the model |
| "flange length below minimum" | only possible on P5 (18 mm stub) | P5's foot/riser bend lines are 110 mm and 360 mm from the end, well inside the minimum — if flagged, order P5 unbent and bend it by hand in a vise; it is a strap, not a structural part |
| "hole too close to bend" | the tray slots are 8.6 mm from the bend centre line, limit 6 mm | should not occur; ask for the specific feature |
| "part too large for coating" | the coating limit is 30 × 36 in | the largest part is 24.4 × 17.8 in; not applicable |
| quoted price far above estimate | one-off setup on five parts | get the OSH Cut comparison, or consider the plywood package |
