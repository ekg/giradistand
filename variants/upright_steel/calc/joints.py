"""
Joints: M5 clamped tray-to-slab connections and M6 levelling feet.

Approach
  * The tray end-flange joint is a CLAMPED (friction-grip) connection: the bolt
    preload presses the 30 mm flange against the side slab over a large area.
    Capacity is checked three ways: friction, bolt bearing on the 1.88 mm
    sheets, and local crushing of the slot.  Friction is used for *stiffness*
    (no slip under service load); the bolts in bearing are the positive
    backstop, so loosening friction cannot turn the frame into a mechanism.
  * Bolt preload from a realistic hand torque with a 3 mm hex key.
      T = K F d,  K = 0.20 (as-received zinc/A2 threads, no lubricant)
      F = T / (K d) = 3.0 N.m / (0.20 x 5 mm) = 3.0 kN
    (A2-70 M5 is good for ~5.5 N.m; 3 N.m is a deliberately mild, repeatable
    hand torque and leaves margin on the bolt.)
"""

import math, sys, os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
sys.path.insert(0, os.path.join(os.path.dirname(_here), "cad"))
import params as P
from materials import STEEL, M5

MU = 0.30
T_TORQUE = 3.0
K_NUT = 0.20
D = M5["d"]
AS_ = M5["As"]
N_BOLTS = len(P.TRAY_BOLT_Y)
N_JOINTS = 3      # one per tray per side


def main():
    Fp = T_TORQUE * 1000.0 / (K_NUT * D)          # N
    Ft_rd = 0.9 * M5["fu_b"] * AS_ / 1.25          # N
    Fv_rd = 0.6 * M5["fu_b"] * AS_ / 1.25
    Fb_rd = 2.5 * D * STEEL["t"] * STEEL["fu"] / 1.25
    e_edge = 14.6                                  # slot to flange free edge, mm
    Ftear = 2 * e_edge * STEEL["t"] * STEEL["fu"] / 1.25
    inter_press = Fp / (math.pi * (5.9 ** 2 - 2.5 ** 2))   # MPa under flanged nut

    lateral = 100.0            # N, handling disturbance (same as racking check)
    H_shelf = 15 * 9.81        # N per shelf end (top tray governs)
    # A clamped joint carries moment by redistributing contact pressure, not by
    # a bolt couple: the three bolts of a flange lie in one horizontal row, so
    # they cannot form a couple about the sway axis.  The moment at which the
    # joint starts to open is M_sep = N*h/6 for a contact band of depth h.
    n_flange = 3 * Fp                              # clamp per flange
    h_flange = P.FLANGE
    M_sep = n_flange * h_flange / 6.0              # N.mm per flange, before separation
    M_portal = lateral * P.H_SPK / 2.0             # N.mm, top joint, whole bay
    M_demand = M_portal / 2.0                       # N.mm per flange

    lines = ["## 5. Joints", "",
             "### 5.1 M5 clamped flange joint (22 bolts, 11 per side)", "",
             "| quantity | value | basis |", "|---|---|---|",
             f"| preload per bolt Fp | {Fp/1000:.2f} kN | T=3.0 N.m, K=0.20, d=5 mm |",
             f"| bolt tension utilisation | {100*Fp/Ft_rd:.0f} % of {Ft_rd/1000:.2f} kN | "
             f"0.9 fu As / 1.25 (A2-70) |",
             f"| bolt shear capacity Fv,Rd | {Fv_rd/1000:.2f} kN | 0.6 fu As / 1.25 |",
             f"| sheet bearing Fb,Rd | {Fb_rd/1000:.2f} kN per bolt | 2.5 d t fu / 1.25 |",
             f"| tear-out (edge {e_edge:.1f} mm) | {Ftear/1000:.2f} kN per bolt | 2 e t fu / 1.25 |",
             f"| joint clamp (3 bolts) | {3*Fp/1000:.1f} kN | |",
             f"| joint friction capacity (mu=0.30) | {3*Fp*MU/1000:.2f} kN | clamped joint, both faces coated |",
             f"| contact pressure under the flanged nut | {inter_press:.1f} MPa | vs 205 MPa yield |",
             "", "Load cases on one tray-to-slab joint:", "",
             "| action | demand | capacity | utilisation |", "|---|---|---|---|"]
    for label, dem, cap in [
        ("vertical shelf reaction, top tray (15 kg / 2 sides)", H_shelf / 2,
         3 * Fv_rd),
        ("pure slip (friction) at 100 N lateral", lateral, 3 * Fp * MU),
        ("slot bearing at 100 N lateral", lateral, 3 * Fb_rd),
    ]:
        lines.append(f"| {label} | {dem:.1f} N | {cap/1000:.2f} kN | {100*dem/cap:.2f} % |")

    lines += ["", f"Joint moment at first opening: M_sep = N.h/6 = "
              f"{M_sep/1000:.1f} N.m per flange; demand {M_demand/1000:.2f} N.m -> "
              f"margin {M_sep/M_demand:.0f}:1.", "",
              "Slip margin against the 100 N handling disturbance: "
              f"{3*Fp*MU/lateral:.0f}:1 - the joint stays metal-to-metal, so the frame",
              "behaves as rigid-jointed for racking (see 7.2).", "",
              "Caveat, stated plainly: this joint's moment capacity is preload-",
              "dependent. If the bolts were ever allowed to slacken completely the",
              "joint would become a pin and the 190 mm speaker bay would rely on the",
              "panel below and on the tray's own plate bending. The maintenance plan",
              "therefore includes a torque check at one week, one month and annually.", "",
              "Loosening: nylon-insert locknuts (DIN 6923) plus a preloaded clamped",
              "joint; no spring washers, no polymer washers in the structural stack.",
              "Because the joint does not slip in service there is no fretting of the",
              "powder coat at the interface. Torque is checked at assembly and the",
              "locknuts are visible for re-torque during the annual inspection.", "",
              "### 5.2 M6 levelling feet (4 off)", ""]
    W = 59.1 * 9.81
    lines += ["| quantity | value | basis |", "|---|---|---|",
              f"| load per foot | {W/4:.0f} N | 59.1 kg total / 4 |",
              f"| M6 stud tension capacity | {0.9*700*20.1/1.25/1000:.2f} kN | A2-70, As=20.1 mm2 |",
              f"| deck local pressure under M6 flange nut | {W/4/(math.pi*(6.4**2-3.0**2)):.2f} MPa | vs 205 MPa |",
              f"| footprint per foot | {math.pi*P.FOOT['base_dia']**2/4:.0f} mm2 | {P.FOOT['base_dia']:.0f} mm base |"]
    return "\n".join(lines)


if __name__ == "__main__":
    print(main())
