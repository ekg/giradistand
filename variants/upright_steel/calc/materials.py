"""
Material data used by the calculations, with the source of every number.

Steel (sheet, cold rolled mild steel, SendCutSend ".074in Mild Steel"):
  E = 200 GPa  - conservative floor for cold-rolled sheet (textbook 200-210 GPa)
  fy= 205 MPa  - 0.2% proof for CRS 1008/1010 (ASTM A1008 CS Type B min yields
                 170-205 MPa depending on grade; 205 MPa used)
  fu= 340 MPa  - typical UTS for CRS
  rho = 7850 kg/m3
E is deliberately 200 GPa rather than 210 GPa: deflection results are then ~5%
conservative.
"""

STEEL = dict(E=200_000.0, G=79_000.0, fy=205.0, fu=340.0, rho=7.85e-6,
             nu=0.30, t=1.88, name="CRS 1.88 mm (0.074 in)")

# Fasteners  ISO 7380-1 A2-70 button head + DIN 6923 flanged locknut
M5 = dict(d=5.0, As=14.2, At=14.2, Sp=0.8, grade="A2-70 (70 = 700 MPa UTS)",
          fu_b=700.0, fy_b=450.0, nut_h=5.0, head_d=9.5)

# bolt capacities, allowable (not ultimate) - simple working-stress approach
def bolt_capacities(d=5.0, As=14.2, fu_b=700.0, t_sheet=1.88, fu_sheet=340.0,
                    fy_sheet=205.0):
    Fv = 0.6 * fu_b * As / 1.25          # shear, ultimate / 1.25 (EC3 style)
    Ft = 0.9 * fu_b * As / 1.25          # tension
    Fb = 2.5 * d * t_sheet * fu_sheet / 1.25   # bearing on sheet
    tear = 2 * (e := 8.0) * t_sheet * fu_sheet / 1.25   # tear-out with e=8 mm
    return dict(shear=Fv, tension=Ft, bearing=Fb, tearout=tear,
                slip_mu03=0.30 * 4200.0)

FOOT = dict(d_m6=6.0, base_d=23.0, capacity_N=1500.0)

# Sound / isolation references kept deliberately factual
ISOLATION = dict(puck="IsoAcoustics ISO-PUCK mini: 44 mm dia x 24 mm, 2.75 kg per unit")
