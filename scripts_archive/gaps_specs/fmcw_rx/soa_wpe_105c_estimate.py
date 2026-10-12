"""Order-of-magnitude estimate [E] of the wall-plug efficiency (WPE) of an InP
CW laser or semiconductor optical amplifier (SOA) at 105 degC, scaled from the
hottest published anchor points with the usual characteristic temperatures.

Model (standard empirical laser scaling, applied to the SOA via its
transparency current):
    P_out(T)  = eta_d(T) * (I - I_th(T))           (optical power, W)
    eta_d(T)  = eta_d(T_ref) * exp(-(T - T_ref) / T1)   (slope, W/A)
    I_th(T)   = I_th(T_ref)  * exp(+(T - T_ref) / T0)   (threshold or
                                                          transparency, A)
    WPE(T)    = P_out(T) / (I * V)   with I and V held fixed
so that
    WPE(T) / WPE(T_ref) = exp(-dT/T1) * (I - I_th(T)) / (I - I_th(T_ref)).
Holding V fixed slightly overstates the loss (the junction voltage falls as the
bandgap shrinks), and holding I fixed ignores thermal rollover (which makes the
real loss larger); the two errors partly cancel.

Anchors (sources in the accompanying report text):
  A. 1310 nm SSC/SOA-integrated DFB: WPE 20 % at >100 mW, 400 mA, 75 degC
     (Opt. Eng. 62(4) 046102, 2023). T0 = 75 K, T1 = 294 K from a 1300 nm
     InP SOA material study (IEEE Photonics J. 2022). I_th(75 degC) unknown:
     40-80 mA assumed.
  B. 1550 nm high-power SOA: WPE >20 % at <=50 degC (Aeva, >28 dBm).
     Transparency current assumed 10-20 % of the drive current at 50 degC;
     T0 = 50-70 K and T1 = 200-300 K assumed for InGaAsP/InGaAlAs wells.

Usage : python soa_wpe_105c_estimate.py
Output: printed table of WPE at 105 degC for each assumption set.
"""
import math


def ratio(dT, T0, T1, ith_frac):
    """WPE(T)/WPE(Tref) for drive I=1 (normalized) and Ith/I = ith_frac at Tref."""
    ith_hot = ith_frac * math.exp(dT / T0)
    if ith_hot >= 1.0:
        return 0.0
    return math.exp(-dT / T1) * (1.0 - ith_hot) / (1.0 - ith_frac)


print("A. 1310 nm, anchor 20 % at 75 degC, I = 400 mA, T0 = 75 K, T1 = 294 K")
for ith_ma in (40, 60, 80):
    r = ratio(105 - 75, 75.0, 294.0, ith_ma / 400.0)
    print(f"   Ith(75C) = {ith_ma:3d} mA -> WPE(105C) = {20 * r:4.1f} %  (x{r:.2f})")

print("B. 1550 nm, anchor 20 % at 50 degC")
for T0 in (50.0, 70.0):
    for T1 in (200.0, 300.0):
        for f in (0.10, 0.20):
            r = ratio(105 - 50, T0, T1, f)
            print(f"   T0={T0:4.0f} K T1={T1:4.0f} K Itr/I={f:.2f} -> "
                  f"WPE(105C) = {20 * r:4.1f} %  (x{r:.2f})")
