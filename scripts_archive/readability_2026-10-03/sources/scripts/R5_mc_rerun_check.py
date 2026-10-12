"""R5_C10_part1 item 03: exact re-run of the sparse-array block of the 28 Sep 2026 audit script.
Inputs: N_spot given (1,140 for N = 128; 1,720 for N = 256); aperture L = N_spot/2 wavelengths;
uniform random positions on [0, L]; u = sin(theta) over [-1, 1] at 40*N_spot+1 points; main lobe |u| < 1/L;
numpy default_rng(1); 20 trials. Run: python R5_mc_rerun_check.py (no files read or written)."""
import numpy as np
# exact re-run of the sparse-array block of the earlier audit script (seed 1, 20 trials)
rng = np.random.default_rng(1)
for N, M in [(128, 1140), (256, 1720)]:
    fr=[]; pk=[]; mn=[]
    for trial in range(20):
        L = M/2.0
        x = rng.uniform(0, L, N)
        u = np.linspace(-1, 1, 40*M+1)
        AF = np.abs(np.exp(2j*np.pi*np.outer(u, x)).sum(1))**2
        main = np.abs(u) < 1.0/L
        fr.append(AF[main].sum()/AF.sum())
        side = np.abs(u) > 1.0/L
        pk.append(10*np.log10(AF[side].max()/N**2)); mn.append(10*np.log10(AF[side].mean()/N**2))
    print(N, M, "L(lambda)=%.0f" % L, "main=%.4f" % np.mean(fr), "sd=%.4f" % np.std(fr), "peakSL=%.2f dB" % np.mean(pk), "meanSL=%.2f dB" % np.mean(mn), "N/M=%.4f" % (N/M))
