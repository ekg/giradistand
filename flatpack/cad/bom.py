"""BOM + cost model for the flat-pack kit (ESTIMATE, not a quotation)."""
import os, csv, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(_here)), "cad"))
sys.path.insert(0, _here)
import params as P, model as M, export as X

OUT = os.path.join(os.path.dirname(_here), "out")

PURCHASED = [
    ("Birch dowel 8 mm x 1000", "cut to 6 x 40 mm", 1, 4.50),
    ("M6 levelling glide, male stud, 23 mm base", "M6x40, polymer base", 4, 1.85),
    ("M6 flanged nylon-insert locknut DIN 6923", "M6, 10 mm AF", 4, 0.38),
    ("Sorbothane isolation pad 50 x 50 x 6 mm, 30 duro",
     "8 off, 1 per speaker corner (or ISO-PUCK mini upgrade)", 8, 2.20),
    ("Wall fixing for P4 strap", "4.0 x 40 screw or anchor", 2, 0.30),
]
RATES = dict(sheet=110.0, routing=95.0, sanding=35.0, ship=32.0, tax=0.09)

def main():
    geo, sheets, ap = X.export_all()
    parts = M.build()
    rows = []
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        pts = geo[pid]["pts"]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        w = max(xs) - min(xs); h = max(ys) - min(ys)
        rows.append((pid, geo[pid].get("step") is not None and 1 or 1, w, h,
                     w * h, geo[pid]["qty"]))
    used = sum(r[4] * r[5] for r in rows)
    material = RATES["sheet"] * len(sheets)
    fab = material + RATES["routing"] + RATES["sanding"]
    purch = sum(q * u for (_, _, q, u) in PURCHASED)
    sub = fab + purch + RATES["ship"]
    tax = sub * RATES["tax"]
    total = sub + tax
    with open(os.path.join(OUT, "bom.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["part", "description", "qty", "material", "thickness_mm",
                     "length_mm", "width_mm", "area_mm2", "grain", "finish"])
        names = {"P1": "SIDE PANEL", "P2": "SHELF", "P3": "BASE SHELF",
                 "P4": "WALL STRAP", "P5": "FIT COUPON"}
        for (pid, _, w, h, a, q) in rows:
            wr.writerow([pid, names[pid], q, "18 mm Baltic birch ply B/BB",
                         P.T, f"{w:.0f}", f"{h:.0f}", f"{a:.0f}",
                         "long axis along sheet X", "sanded, unfinished"])
        wr.writerow([])
        wr.writerow(["PURCHASED", "", "qty", "spec", "", "", "", "", "", "unit_est_usd"])
        for (it, spec, q, u) in PURCHASED:
            wr.writerow(["", it, q, spec, "", "", "", "", "", f"{u:.2f}"])
        wr.writerow([])
        for label, val in (("plywood sheets", material), ("CNC routing", RATES["routing"]),
                           ("edge/face sanding", RATES["sanding"]),
                           ("purchased items", purch), ("shipping", RATES["ship"]),
                           (f"tax {RATES['tax']*100:.0f}%", tax),
                           ("TOTAL ESTIMATE", total)):
            wr.writerow(["", label, "", "", "", "", "", "", "", f"{val:.2f}"])
    L = ["## Cost model (ESTIMATE - not a quotation)", "",
         f"| line | USD | basis |", "|---|---|---|",
         f"| plywood, {len(sheets)} sheet(s) 1525x1525x18 Baltic birch | {material:.0f} | "
         f"supplier list price, verify locally |",
         f"| CNC routing (one sheet, 2 setups: outlines + slot/dogbone pass) | "
         f"{RATES['routing']:.0f} | shop rate ~$80/h, ~1.2 h, quote required |",
         f"| edge + face sanding | {RATES['sanding']:.0f} | shop operation, per sheet |",
         f"| dowels, feet, isolation, wall fixings | {purch:.0f} | itemised in bom.csv |",
         f"| shipping (sheet-sized parcel) | {RATES['ship']:.0f} | estimate |",
         f"| sales tax {RATES['tax']*100:.0f}% | {tax:.0f} | assumption |",
         f"| **TOTAL ESTIMATE** | **{total:.0f}** | |", "",
         f"Material + CNC = **${fab:.0f}**, against the brief's $220-250 allowance.",
         f"Utilisation: {used/1e6:.2f} m2 of parts on {len(sheets)*P.PLY['sheet'][0]*P.PLY['sheet'][1]/1e6:.2f} m2 "
         f"of sheet = {100*used/(len(sheets)*P.PLY['sheet'][0]*P.PLY['sheet'][1]):.0f} %.",
         "", "Levers if the quote comes back high:",
         "* birch-faced poplar-core ply instead of Baltic birch: -$35, acceptable for",
         "  an indoor stand but with more voids and a weaker edge;",
         "* no shop sanding (buy the parts raw and sand at home): -$35, but breaks the",
         "  'ready to assemble' promise;",
         "* collect in person instead of shipping: -$32.",
         "All three together would land it near $250, at the cost of the finished-kit",
         "promise. None is recommended as the default."]
    with open(os.path.join(OUT, "cost_model.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
