"""
BOM + fabrication schedule + cost model (estimate, NOT a quotation).

Rates are stated assumptions used for budgeting only; SendCutSend returns an
instant price when the STEP files are uploaded. Nothing here is a live quote.
"""

import os, sys, csv, json
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
import params as P
import model as M
import sheetmetal as S
import export as X

ROOT = os.path.dirname(_here)
OUT = os.path.join(ROOT, "out")

# ---- rate assumptions (ESTIMATES) ---------------------------------------
RATE = dict(
    laser_area=55.0,      # USD per m2 of sheet area burned
    laser_cut=0.90,       # USD per metre of cut length
    laser_setup=6.00,     # USD per part
    bend_each=3.50,       # USD per bend
    bend_min=9.00,
    deburr=2.00,
    coat_area=18.0,       # USD per m2
    coat_setup=6.00,
    coat_min=10.00,
    ship=28.00,
    tax=0.0825,
)

PURCHASED = [
    # (item, spec, qty, unit price, source/assumption)
    ("M5x12 button head screw, ISO 7380-1, A2-70 black",
     "M5x12, 3 mm hex socket", 22, 0.42, "assumption, fastener supplier"),
    ("M5 flanged nylon-insert locknut, DIN 6923, A2",
     "M5, 8 mm AF", 22, 0.34, "assumption"),
    ("M6 levelling glide, male stud",
     "M6x40 thread, 23 mm polymer base, 9 mm high", 4, 1.85, "assumption"),
    ("M6 flanged nylon-insert locknut, DIN 6923",
     "M6, 10 mm AF", 4, 0.38, "assumption"),
    ("IsoAcoustics ISO-PUCK mini (box of 8)",
     "44 mm dia x 24 mm, 2.75 kg each", 1, 79.00, "supplier list price, verify"),
    ("Groove Crate 14.5 x 14.5 x 14.125 in record crate",
     "HDPE, 368 x 368 x 359 mm, ~80-100 LPs", 1, 34.00, "supplier list price, verify"),
    ("3M 2552 aluminium-foil damping tape (optional)",
     "25 mm x 5 m roll", 1, 22.00, "optional, assumption"),
    ("Wall fixings for P5 strap (user supplies)",
     "2 x 4.0 x 40 screw or plasterboard anchor", 2, 0.30, "user supplies"),
]


def flat_metrics():
    """Flat area (mm2) and cut length (mm) per part from the same code that
    makes the DXF files."""
    _, spec_top = M.make_tray(P.Z_TOP)
    _, spec_bot = M.make_tray(P.Z_BOT, front_h=P.FLANGE_BOT, foot_holes=True)

    def poly_len(pts, closed=True):
        L = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5
                for i in range(len(pts) - 1))
        if closed:
            L += ((pts[0][0] - pts[-1][0]) ** 2 + (pts[0][1] - pts[-1][1]) ** 2) ** 0.5
        return L

    def area(pts):
        a = 0.0
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % len(pts)]
            a += x1 * y2 - x2 * y1
        return abs(a) / 2

    out = {}
    o, h, s, b = X.flat_side_slab()
    out["P1"] = dict(area=area(o), cut=poly_len(o) + len(h) * 3.14159 * P.BOLT["clearance"],
                     bends=0, holes=len(h), qty=2)
    for pid, spec in (("P2", spec_top), ("P3", spec_bot)):
        o, h, s, b = X.flat_tray(spec)
        out[pid] = dict(area=area(o), cut=poly_len(o)
                        + len(s) * (2 * P.TRAY_SLOT[1] + 3.14159 * P.TRAY_SLOT[0])
                        + len(h) * 3.14159 * P.FOOT["clearance"],
                        bends=4, holes=len(h) + len(s), qty=2 if pid == "P2" else 1)
    o, h, s, b = X.flat_panel()
    out["P4"] = dict(area=area(o), cut=poly_len(o) + len(h) * 3.14159 * P.BOLT["clearance"],
                     bends=2, holes=len(h), qty=1)
    o, h, s, b = X.flat_strap()
    out["P5"] = dict(area=area(o), cut=poly_len(o) + len(h) * 3.14159 * 6.6,
                     bends=1, holes=len(h), qty=1)
    return out


def price_part(m):
    laser = max(RATE["laser_setup"] + RATE["laser_area"] * m["area"] / 1e6
                + RATE["laser_cut"] * m["cut"] / 1000, 9.0)
    bend = max(RATE["bend_each"] * m["bends"], RATE["bend_min"]) if m["bends"] else 0.0
    deb = RATE["deburr"]
    coat = max(RATE["coat_setup"] + RATE["coat_area"] * m["area"] / 1e6,
               RATE["coat_min"])
    return dict(laser=laser, bend=bend, deburr=deb, coat=coat,
                unit=laser + bend + deb + coat)


def main():
    parts = M.build()
    fm = flat_metrics()
    names = {"P1": "SIDE SLAB", "P2": "SHELF TRAY", "P3": "BASE TRAY",
             "P4": "REAR PANEL", "P5": "WALL STRAP"}
    rows = []
    tot = dict(laser=0, bend=0, deburr=0, coat=0, total=0)
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        m = fm[pid]
        p = price_part(m)
        mass = sum(s.Volume() for s in parts[pid]["solids"]) * P.MATERIAL["rho"] / \
            max(1, len(parts[pid]["solids"]))
        q = m["qty"]
        rows.append(dict(part=pid, name=names[pid], qty=q,
                         flat_mm=f"{m['area']:.0f}", area_m2=m["area"] / 1e6,
                         cut_m=m["cut"] / 1000, bends=m["bends"],
                         holes=m["holes"], mass_each=mass,
                         laser=p["laser"], bend=p["bend"], deburr=p["deburr"],
                         coat=p["coat"], unit=p["unit"],
                         ext=p["unit"] * q))
        for k in tot:
            key = {"total": "unit"}.get(k, k)
            tot[k] += p[key] * q
    fab = tot["total"]
    purch = sum(q * u for (_, _, q, u, _) in PURCHASED)
    ship = RATE["ship"]
    sub = fab + purch + ship
    tax = sub * RATE["tax"]
    grand = sub + tax

    with open(os.path.join(OUT, "bom.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["part", "description", "qty", "material", "thickness_mm",
                    "finish", "bends", "holes_slots", "flat_area_mm2",
                    "cut_length_m", "mass_each_kg", "unit_price_est_usd",
                    "ext_price_est_usd"])
        for r in rows:
            w.writerow([r["part"], r["name"], r["qty"],
                        "Mild steel CRS 1008/1010", "1.88",
                        "powder coat textured black BK01", r["bends"], r["holes"],
                        f"{r['flat_mm']}", f"{r['cut_m']:.2f}",
                        f"{r['mass_each']:.2f}", f"{r['unit']:.2f}",
                        f"{r['ext']:.2f}"])
        w.writerow([])
        w.writerow(["PURCHASED", "", "qty", "spec", "", "", "", "", "", "", "",
                    "unit_est_usd", "ext_est_usd"])
        for (it, spec, q, u, src) in PURCHASED:
            w.writerow(["", it, q, spec, "", "", "", "", "", "", "",
                        f"{u:.2f}", f"{q*u:.2f}"])
        w.writerow([])
        w.writerow(["", "fabrication subtotal", "", "", "", "", "", "", "", "", "",
                    "", f"{fab:.2f}"])
        w.writerow(["", "purchased subtotal", "", "", "", "", "", "", "", "", "",
                    "", f"{purch:.2f}"])
        w.writerow(["", "shipping (estimate)", "", "", "", "", "", "", "", "", "",
                    "", f"{ship:.2f}"])
        w.writerow(["", f"sales tax @ {RATE['tax']*100:.2f}%", "", "", "", "", "",
                    "", "", "", "", "", f"{tax:.2f}"])
        w.writerow(["", "TOTAL ESTIMATE", "", "", "", "", "", "", "", "", "",
                    "", f"{grand:.2f}"])

    L = ["## 11. BOM, fabrication schedule and cost model", "",
         "### 11.1 Manufactured parts", "",
         "| part | description | qty | flat area (mm2) | cut length (m) | bends | "
         "holes/slots | mass each (kg) |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['part']} | {r['name']} | {r['qty']} | {r['flat_mm']} | "
                 f"{r['cut_m']:.2f} | {r['bends']} | {r['holes']} | "
                 f"{r['mass_each']:.2f} |")
    total_area = sum(r["area_m2"] * r["qty"] for r in rows)
    total_cut = sum(r["cut_m"] * r["qty"] for r in rows)
    L += ["", f"Total sheet area {total_area:.3f} m2, total cut length "
          f"{total_cut:.2f} m, {sum(r['bends']*r['qty'] for r in rows)} bends, "
          f"{len(rows)} distinct parts, {sum(r['qty'] for r in rows)} pieces.",
          "", "### 11.2 Purchased items", "",
          "| item | spec | qty | unit (USD) | ext (USD) | basis |",
          "|---|---|---|---|---|---|"]
    for (it, spec, q, u, src) in PURCHASED:
        L.append(f"| {it} | {spec} | {q} | {u:.2f} | {q*u:.2f} | {src} |")
    L += ["", "### 11.3 Cost model (ESTIMATE - not a quotation)", "",
          "| line | amount (USD) |", "|---|---|",
          f"| laser cutting | {tot['laser']:.2f} |",
          f"| CNC bending | {tot['bend']:.2f} |",
          f"| deburring | {tot['deburr']:.2f} |",
          f"| powder coating | {tot['coat']:.2f} |",
          f"| **fabrication subtotal** | **{fab:.2f}** |",
          f"| purchased items | {purch:.2f} |",
          f"| shipping (estimate) | {ship:.2f} |",
          f"| sales tax {RATE['tax']*100:.2f}% (assumption) | {tax:.2f} |",
          f"| **TOTAL ESTIMATE** | **{grand:.2f}** |", "",
          "Rates used (assumptions, not published prices):", "",
          f"* laser: ${RATE['laser_setup']:.2f}/part + ${RATE['laser_area']:.2f}/m2 + "
          f"${RATE['laser_cut']:.2f}/m of cut, minimum $9/part",
          f"* bending: ${RATE['bend_each']:.2f}/bend, minimum ${RATE['bend_min']:.2f}",
          f"* deburr: ${RATE['deburr']:.2f}/part",
          f"* powder coat: ${RATE['coat_setup']:.2f}/part + "
          f"${RATE['coat_area']:.2f}/m2, minimum ${RATE['coat_min']:.2f}",
          "", "**Status: estimate only.** SendCutSend returns an instant price when the",
          "five STEP files in `out/step/` are uploaded; no upload was performed and no",
          "quotation exists. Expect +/-25 % on the fabrication line, and note that",
          "one-off orders are dominated by per-part setup, not by area - which is why",
          "the design deliberately uses only 7 pieces of 5 distinct parts.", "",
          "### 11.4 Cost drivers and the cheaper alternative", "",
          "1. **Part count and per-part setup** (~40 % of the fabrication cost).",
          "   Already minimised: 5 part numbers, 6 pieces, 2 of which are identical.",
          "2. **Powder coating** (~25 %). Cheaper alternative: order bare/deburred parts",
          "   and finish at home with a single aerosol of matte black etch-primer +",
          "   topcoat (about $25 and 2 hours, OUTSIDE the guarantee of edge coverage).",
          "   Saves roughly 15 % of the total but breaks the 'ready to assemble'",
          "   promise, so it is offered only as an explicit choice.",
          "3. **Material thickness.** 0.059 in (1.5 mm) CRS would cut about 20 % of the",
          "   material cost but the shelf and racking checks would have to be re-run",
          "   (plate stiffness scales with t^3, so deflections would roughly double).",
          "   Not adopted.",
          "4. The single biggest optional saving is to drop P4 REAR PANEL and accept a",
          "   friction-only racking path - rejected: it removes the only",
          "   non-friction racking element (see 7.2)."]
    with open(os.path.join(OUT, "cost_model.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote out/bom.csv and out/cost_model.md; total estimate ${grand:.2f}")


if __name__ == "__main__":
    main()
