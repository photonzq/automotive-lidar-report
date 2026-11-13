# Simple arithmetic on published scatter-function fits (no simulation).
# B(theta) in sr^-1 (= cd m^-2 lx^-1), theta in degrees.
import numpy as np

def padmos_nominal(th):
    # Padmos & Alferdinck 1983, Eqs. (23a,b): 85th-percentile dry in-use windscreen
    th = np.asarray(th, float)
    return np.where(th < 9.0, 6.6 * th**-1.73, 44.0 * th**-2.6)

def powerlaw(k, n):
    return lambda th: k * np.asarray(th, float)**n

fits = {
    "Padmos nominal (85th pct, dry, in-use)": padmos_nominal,
    "Padmos mean car (nominal x 0.035/0.057)": lambda th: padmos_nominal(th) * 0.035 / 0.057,
    "Toet new clean 0.067 th^-1.50": powerlaw(0.067, -1.50),
    "Toet used clean 0.494 th^-1.81": powerlaw(0.494, -1.81),
    "Toet new dirty(salt) 17.456 th^-2.29": powerlaw(17.456, -2.29),
    "Toet used dirty(salt) 17.448 th^-2.18": powerlaw(17.448, -2.18),
    "Williamson lowest (lam. glass clean) 0.08 th^-1.07": powerlaw(0.08, -1.07),
    "Williamson highest (acrylic dirty) 6.24 th^-1.59": powerlaw(6.24, -1.59),
    "Williamson lam. glass day-of-test 532nm 4.330 th^-1.487": powerlaw(4.330, -1.487),
    "Stiles-Holladay eye 10 th^-2": powerlaw(10.0, -2.0),
}

angles = [1, 2, 5, 10, 20, 30, 40, 60]

def g_integral(func, t1, t2, npts=20000):
    # g(t1,t2) = int f dOmega = 2*pi * int f(theta) sin(theta) dtheta (theta in rad)
    th = np.linspace(t1, t2, npts)
    y = func(th) * np.sin(np.radians(th))
    return 2 * np.pi * np.trapezoid(y, np.radians(th))

print("B(theta) [sr^-1] and s = theta^2 B [deg^2/sr]")
for name, f in fits.items():
    B = f(np.array(angles))
    print(name)
    print("   B :", " ".join(f"{a:>3}deg={b:.3g}" for a, b in zip(angles, B)))
    print("   s :", " ".join(f"{a:>3}deg={a*a*b:.3g}" for a, b in zip(angles, B)))

print()
print("Integrated scatter fractions g(t1,t2) = int B dOmega")
for name in ["Padmos nominal (85th pct, dry, in-use)", "Padmos mean car (nominal x 0.035/0.057)"]:
    f = fits[name]
    print(name, " g(1,20)=%.4f g(2.5,90)=%.4f g(20,50)=%.4f g(50,90)=%.4f g(1,90)=%.4f"
          % (g_integral(f, 1, 20), g_integral(f, 2.5, 90), g_integral(f, 20, 50), g_integral(f, 50, 90), g_integral(f, 1, 90)))
for name in ["Williamson lowest (lam. glass clean) 0.08 th^-1.07", "Williamson highest (acrylic dirty) 6.24 th^-1.59",
             "Toet new dirty(salt) 17.456 th^-2.29", "Toet new clean 0.067 th^-1.50"]:
    f = fits[name]
    print(name, " g(1,40)=%.4f g(2.5,40)=%.4f g(10,40)=%.4f" % (g_integral(f, 1, 40), g_integral(f, 2.5, 40), g_integral(f, 10, 40)))

# Haze-equivalent from Padmos table values (g relative to incident light); windscreen T ~0.84 (Table I mean, read by eye)
T = 0.84
for label, g120, g2050, g50110 in [("mean", 0.035, 0.0058, 0.0026), ("85th", 0.057, 0.0097, 0.0045), ("clean mean", 0.0073, None, None)]:
    if g2050 is None:
        print(label, "g(1,20)=%.4f" % g120)
        continue
    tot = g120 + g2050 + g50110
    print(f"Padmos {label}: g(1,110) = {tot:.4f}; fraction beyond 20 deg = {(g2050+g50110)/tot:.2f}; ")

# Equivalent uniform-hemisphere f needed to match B at angle theta: f_eq = pi*B
f = fits["Padmos mean car (nominal x 0.035/0.057)"]
print("Padmos mean car: pi*B(theta) =", " ".join(f"{a}deg={np.pi*f(a):.3g}" for a in angles))
print("Uniform model with f = g(1,110)=0.043 gives B =", 0.043/np.pi)

# DXOMARK flare attenuation (dB) -> B_cam = 10^(-A/10)/pi
for A in [10, 20, 27, 31, 40, 50]:
    print(f"Flare attenuation {A} dB -> E_flare/E_source = {10**(-A/10):.2e}; B_cam = {10**(-A/10)/np.pi:.2e} sr^-1")

# Bellmann 2020 slopes (fraction lost per g/m^2): mirror (double pass) 0.259-0.538 (weekly fits), glass 0.0190-0.0700
for m in [0.259, 0.290, 0.429, 0.538]:
    single = 1 - np.sqrt(1 - m * 1.0)  # loss for 1 g/m^2 (linear range assumed)
    print(f"mirror slope {m}: single-pass loss at 1 g/m^2 = {single:.3f}; small-loss approx m/2 = {m/2:.3f}")

# Golden CO coupon 3 (Smestad/Micheli/Germer NIST slide 16, read by eye)
for wk, Td, Th in [(0, 0.902, 0.912), (5, 0.834, 0.892), (6, 0.843, 0.897)]:
    print(f"week {wk}: direct {Td}, hemispherical {Th}, (Th-Td)/Th = {(Th-Td)/Th:.3f}")

# McCann & Rizzi glare-limited ranges
for r in [141, 77, 6345, 343, 340, 11021]:
    print(f"range {r}:1 = {np.log10(r):.2f} log10 units")
