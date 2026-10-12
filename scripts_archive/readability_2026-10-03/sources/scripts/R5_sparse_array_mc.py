"""R5_C10_part1 items 02 and 03: sparse-array Monte Carlo checks for report section C10.

Part A (item 03): re-runs the audit re-implementation (28 Sep 2026) of the report's
  sparse-array Monte Carlo with its exact inputs, and adds the analytic expectation.
  Inputs (from that script): N_spot given (1,140 for N = 128; 1,720 for N = 256);
  aperture L = N_spot / 2 wavelengths; N positions drawn independently and uniformly
  on [0, L] (no minimum spacing); isotropic elements; far field sampled in
  u = sin(theta) over the full visible space [-1, 1] at 40*N_spot + 1 points;
  main lobe |u| < 1/L (first nulls of the aperture envelope), sidelobes |u| > 1/L;
  numpy default_rng(seed 1); 20 trials.  A 200-trial run with another seed is added.

Part B (item 02): DTU ultra-sparse OPA geometry (Qiu et al., Laser Photonics Rev. 2024):
  N = 120 emitters across D = 6 mm (mean pitch 50 um) along one axis, lambda = 1.55 um.
  Main-lobe fraction under two conventions: power integrated uniformly in angle phi over
  +-90 deg (flat element pattern in phi, as the paper's simulation) and uniformly in u.
  Random uniform positions stand in for the paper's optimized aperiodic positions.

Part C (item 02): the same far field seen through a Gaussian instrument response of
  0.13 deg FWHM (the paper's camera-limited beam width): peak-to-mean-floor and
  peak-to-highest-floor ratios over -80..82 deg, with 0, 1 and 2 dB rms amplitude spread.

Run: python R5_sparse_array_mc.py   (no files read or written)
"""
import numpy as np


def af_power(x, u):
    """|array factor|^2 for element positions x (in wavelengths) at sine-space points u."""
    out = np.empty(u.size)
    step = 20000
    for i in range(0, u.size, step):
        out[i:i + step] = np.abs(np.exp(2j * np.pi * np.outer(u[i:i + step], x)).sum(1)) ** 2
    return out


def sinc2_int(a, n=200001):
    x = np.linspace(-a, a, n)
    return np.trapezoid(np.sinc(x) ** 2, x)


def part_a():
    print("Part A: sparse-array Monte Carlo (audit inputs)")
    for seed, trials in [(1, 20), (2, 200)]:
        rng = np.random.default_rng(seed)
        for N, M in [(128, 1140), (256, 1720)]:
            L = M / 2.0
            u = np.linspace(-1, 1, 40 * M + 1)
            main = np.abs(u) < 1.0 / L
            side = ~main
            fr, pk, mn = [], [], []
            for _ in range(trials):
                x = rng.uniform(0, L, N)
                af = af_power(x, u)
                fr.append(af[main].sum() / af.sum())
                pk.append(10 * np.log10(af[side].max() / N ** 2))
                mn.append(10 * np.log10(af[side].mean() / N ** 2))
            # analytic expectation: E|AF|^2 = N + N(N-1) sinc^2(uL)
            e_main = N * 2 / L + N * (N - 1) * sinc2_int(1.0) / L
            e_tot = 2 * N + N * (N - 1) * sinc2_int(L) / L
            print(f"  seed {seed}, {trials} trials, N={N}, N_spot={M}, L={L:.0f} lambda "
                  f"({L * 1.55e-3:.3f} mm at 1.55 um): main {np.mean(fr):.4f} (sd {np.std(fr):.4f}), "
                  f"peak SL {np.mean(pk):.2f} dB (sd {np.std(pk):.2f}), mean SL {np.mean(mn):.2f} dB; "
                  f"N/N_spot {N / M:.4f}; analytic main {e_main / e_tot:.4f}")


def part_bc():
    lam = 1.55e-6
    N, D = 120, 6e-3
    print("Part B/C: DTU geometry, N=120 over 6 mm")
    print(f"  N_spot (angle, pi D/lambda) = {np.pi * D / lam:.0f};  N_spot (sine, 2D/lambda) = {2 * D / lam:.0f}")
    print(f"  N/N_spot: angle {N / (np.pi * D / lam):.4f}, sine {N / (2 * D / lam):.4f}")
    rng = np.random.default_rng(3)
    dphi = 0.002                      # deg
    phi = np.arange(-90, 90 + dphi / 2, dphi)
    u = np.sin(np.radians(phi))
    Dl = D / lam
    sig = 0.13 / 2.3548 / dphi        # Gaussian sigma in samples
    k = np.arange(-int(5 * sig), int(5 * sig) + 1)
    ker = np.exp(-0.5 * (k / sig) ** 2)
    ker /= ker.sum()
    fov = (phi >= -80) & (phi <= 82)
    res = {0: [], 1: [], 2: []}
    frac_phi, frac_u = [], []
    for t in range(20):
        x = np.sort(rng.uniform(0, Dl, N))
        for amp_db in (0, 1, 2):
            a = 10 ** (rng.normal(0, amp_db, N) / 20) if amp_db else np.ones(N)
            af = np.abs(np.exp(2j * np.pi * np.outer(u, x)) @ a) ** 2
            if amp_db == 0:
                main = np.abs(u) < 1.0 / Dl
                frac_phi.append(af[main].sum() / af.sum())          # uniform in phi
                w = np.cos(np.radians(phi))                           # du = cos(phi) dphi
                frac_u.append((af * w)[main].sum() / (af * w).sum())  # uniform in u
            blur = np.convolve(af, ker, mode="same")
            pk = blur[np.abs(phi) < 0.02].max()
            floor = blur[fov & (np.abs(phi) > 0.4)]
            res[amp_db].append((10 * np.log10(pk / floor.mean()), 10 * np.log10(pk / floor.max())))
    print(f"  main-lobe fraction: uniform in phi {np.mean(frac_phi):.4f}; uniform in u {np.mean(frac_u):.4f}")
    for amp_db in (0, 1, 2):
        r = np.array(res[amp_db])
        print(f"  0.13 deg blur, {amp_db} dB rms amplitude spread: peak/mean floor {r[:, 0].mean():.1f} dB, "
              f"peak/highest floor {r[:, 1].mean():.1f} dB (range {r[:, 1].min():.1f}-{r[:, 1].max():.1f})")


if __name__ == "__main__":
    part_a()
    part_bc()
