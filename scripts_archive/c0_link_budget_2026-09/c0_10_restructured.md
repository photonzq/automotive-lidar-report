### 10. Link budget: loss versus range, the detection level, and how range scales

How far can a lidar see with a given laser energy per point and a given lens, and how much of that range survives a darker target, a dirty window or bad weather? This subsection answers both questions with one model. The model is built in three steps and then applied in three ways.

**The three steps.**
1. **How much light comes back** (10.2). The link loss $\mathcal{L}(R)$ is the fraction of the transmitted light that the receiver can use from a target at range $R$. It is derived for direct detection (the ToF receivers) and for coherent detection (FMCW), and plotted against range in Figure C0.10a.
2. **How much light is needed** (10.3). Detection statistics give $n_{\rm req}$, the mean number of signal photoelectrons per point that each receiver needs for a required detection probability at a fixed false-alarm rate (Figure C0.10b).
3. **Where the two meet** (10.4). Converting $n_{\rm req}$ into a detection level $\mathcal{L}_{\rm det}$, the smallest usable fraction, gives the maximum range as the crossing $\mathcal{L}(R_{\max})=\mathcal{L}_{\rm det}$. These are the dashed lines and dots of Figure C0.10a.

**The three applications.** 10.5 shows what more energy per point, or a larger aperture, buys in range (Figure C0.10c). 10.6 asks how much margin each design keeps at shorter ranges, and what a darker target, a dirty or wet window, fog and rain then do to its range (Figure C0.10d). 10.7 lists what the model leaves out. Before all of this, 10.1 states the assumptions and defines the symbols.

| Part | Question it answers | Figure |
|---|---|---|
| 10.1 Model, assumptions and symbols | What is assumed, and what does each symbol mean? | — |
| 10.2 Link loss | How much of the transmitted light can the receiver use? | C0.10a (the curves) |
| 10.3 Detection statistics | How many photoelectrons does a reliable detection need? | C0.10b |
| 10.4 Detection level and maximum range | Where does the returned light fall below what is needed? | C0.10a (dashed lines and dots) |
| 10.5 Range scaling | What does more energy per point, or a larger aperture, buy? | C0.10c |
| 10.6 Margin at short range | What do dark targets, dirty windows, fog and rain cost? | C0.10d |
| 10.7 Limits of the model | What is left out? | — |

**Main results** [E]:
- **Direct detection loses signal as $D^2/R^2$ at every range** (10.2). A coherent (FMCW) receiver collects only the light in one spatial mode, so its loss is flat out to the beam's Rayleigh range and falls beyond it.
- **Equal apertures, constant gap** (10.5). When both receivers use the same aperture, sized optimally for the coherent beam at each range, FMCW needs about three times the energy per sample of SPAD ToF, whatever the range. This underlies the energy-per-point comparisons between ToF and FMCW in §C7a and §C10.
- **The flat near field leaves FMCW little margin at short range** (10.6). A direct-detection design that just reaches 200 m on a 10% target has 26 dB to spare at 10 m, while the best FMCW design has 3 dB. An extra 3 dB of loss, from a dirty window or a 5% target, therefore blinds that FMCW design at every range. In fog of 200 m visibility its reach falls to 18 m, against 61 m for ToF. In heavy rain behind a wet window it falls to 50 m, against 147 m.
- **A smaller aperture buys the margin back with energy** (10.6). An FMCW design that tolerates dark targets and fog as well as ToF does (a 7 mm aperture) needs five times the energy of the best FMCW design, i.e. twenty times ToF's. A wet window still costs it range, because water absorbs at 1,550 nm. What FMCW keeps in fog is its rejection of the backscatter from droplets near the sensor.

**Figures and data.** The script `build/figures/link_budget_scaling.py` draws the four figures and writes the numbers quoted here to `link_budget_scaling_tables.txt`. All numbers are [E], for a Lambertian target that fills the illuminated spot, at normal incidence and in clear air unless stated otherwise. The subsection joins subsections 1 (photon budget), 2 (FMCW), 7 (detection statistics) and 8 (weather) into one picture.

#### 10.1 Model, assumptions and symbols

**Assumptions.** Every result below rests on the following conditions; 10.7 notes what changes when they fail.
- **Lambertian target.** The target is perfectly diffuse, with a bidirectional reflectance distribution function (BRDF, the ratio of reflected radiance to incident irradiance) of $\rho/\pi$ in every direction. This is invalid for glossy paint and for retroreflectors (signs, number plates), which return far more or far less toward the sensor, depending on angle.
- **Exponential (Rayleigh) speckle statistics.** For coherent detection, the power in a single spatial mode is exponentially distributed from one look to the next (Rayleigh amplitude). Summing $N_{\rm sp}$ independent speckles narrows the distribution (10.3).
- **Shot-noise-limited LO receiver.** The coherent receiver's noise is the shot noise of its local oscillator, with thermal (amplifier) noise and dark current neglected. This holds only approximately at the 105–125 °C of automotive temperature ratings; §C4c gives 82–94% of the shot-noise limit for Ge photodiodes at 125 °C. A receiver below the limit needs correspondingly more signal photoelectrons, which 10.6 treats as a fixed extra loss.
- **Ideal Gaussian beams.** Transmit beam and LO are ideal TEM00 Gaussians (the fundamental, single-lobed transverse mode; $M^2=1$, where $M^2$ is the beam-quality factor, not the APD gain), with perfect mode matching and alignment between them. Real beams and misalignment lower the coherent signal below the computed value (10.7).
- **No turbulence.** Atmospheric turbulence would distort the wavefront and lower heterodyne efficiency at long range (Frehlich and Kavaya 1991).
- **Depolarizing target.** The factor ½ in the coherent result assumes the target scrambles polarization, so only half its return lies in the LO's polarization. A retroreflector largely preserves polarization, so the factor then differs.
- **Clear air and normal incidence.** The target faces the sensor and fills the illuminated spot. The air is clear, except in 10.6, which adds fog and rain (subsection 8 treats weather for direct detection alone).

**Symbols.** Each symbol is also defined again where it is first used.
- $R$: range to the target. $\lambda$: wavelength. $E_{\rm ph}=h\nu=hc/\lambda$: photon energy, with $h$ Planck's constant and $\nu$ the optical frequency ($2.11\times10^{-19}$ J at 940 nm, $1.28\times10^{-19}$ J at 1,550 nm).
- $E_{\rm tx}$: optical energy transmitted per point, summed over all shots of a point (ToF) or over the up–down chirp pair (FMCW).
- $\rho$: Lambertian reflectance, here 0.1. A Lambertian surface that intercepts power $P$ radiates $\rho P/\pi$ per steradian along its normal.
- $D$: diameter of the receive lens (direct detection), or of the shared transmit–receive aperture (monostatic coherent). $A_{\rm rx}=\pi D^2/4$.
- $P_{\rm tx}$: transmitted optical power. $P_{\rm het}$: the signal a coherent receiver collects in its local oscillator's (LO's) spatial mode and polarization, expressed as an equivalent optical power.
- $A_{\rm mode}$: the *mode-equivalent collecting area* of a coherent receiver (m²).
  - **Definition.** It is the area of an ideal direct-detection lens that would collect, from the same Lambertian target, the same signal power as the coherent receiver collects in its single LO mode. It takes the place of $A_{\rm rx}$ in the link budget: $P_{\rm het}=P_{\rm tx}\,\rho A_{\rm mode}/(\pi R^2)$ before atmospheric loss.
  - **Not a physical area.** It depends on the range and on the beam, and is usually much smaller than the aperture: 63 mm² against the 491 mm² of a 25 mm aperture at 200 m. 10.2 derives it (Eqs. (31)–(33)).
- $T_{\rm atm}=e^{-\alpha R}$: one-way atmospheric transmission with extinction coefficient $\alpha$ (subsection 8; fog and rain in 10.6).
  - In clear air (Kim model, visibility 23 km, where the model's exponent is $q_{\rm K}=1.3$), $\alpha=0.085$ /km at 940 nm and 0.044 /km at 1,550 nm.
  - $T_{\rm atm}^2$ then costs only 0.15 and 0.08 dB at 200 m.
- $\eta$: end-to-end efficiency from photons at the aperture to signal photoelectrons: optics × detector, and for coherent detection also × mixing. The coherent receiver's mode and polarization factors are kept out of $\eta$ and put into $A_{\rm mode}$.
- $n_{\rm req}$: mean signal photoelectrons per point needed for the required detection probability (10.3).
- $\bar n$: the mean number of signal photoelectrons actually obtained per point.
- Coherent beam parameters:
  - $w_0$: the 1/e² intensity radius of the Gaussian beam at the aperture, its waist for a collimated beam; here $w_0=0.45D$ (10.2 explains the choice).
  - $w(R)$: the 1/e² radius at the target.
  - $z_R=\pi w_0^2/\lambda$: the Rayleigh range, the distance over which a collimated Gaussian beam stays roughly its launched size before spreading.
  - $t=1-e^{-2(D/2)^2/w_0^2}=1-e^{-2\times1.235}=0.915$: the aperture-truncation factor, the fraction of the Gaussian's power that passes a hard aperture of diameter $D$. With $w_0=0.45D$, $(D/2)^2/w_0^2=0.25/0.2025=1.235$. §C10.3b uses the same factor.

#### 10.2 How much light comes back: the link loss (Figure C0.10a)

This step computes, for each receiver, the share of the transmitted light that it can use. Direct detection is simple: the lens collects whatever light from the lit spot falls on it. Coherent detection is subtler, because the receiver responds only to light in one spatial mode; the mode-equivalent area $A_{\rm mode}$ puts the two receivers on the same footing. Figure C0.10a, at the end of this part, plots the results.

**Definition of the link loss.** The link loss $\mathcal{L}$ is the fraction of the transmitted energy that reaches the receiver in a form it can use, before the detector efficiency. The mean signal per point is then
$$\bar n=\frac{\eta\,E_{\rm tx}}{E_{\rm ph}}\,\mathcal{L}(R), \tag{29}$$
where $E_{\rm tx}/E_{\rm ph}$ is the number of photons transmitted per point, $\mathcal{L}(R)$ the share of them the receiver can use and $\eta$ the share of those that become photoelectrons. The link loss in dB is $-10\log_{10}\mathcal{L}$, so a larger number of dB means less light.

**Direct detection: the lens collects the whole spot.** The lit spot intercepts all the transmitted light and radiates $\rho E_{\rm tx}/\pi$ per steradian toward the sensor. A lens of area $A_{\rm rx}$ subtends $A_{\rm rx}/R^2$ sr, so
$$\mathcal{L}_{\rm DD}(R)=\frac{\rho\,A_{\rm rx}}{\pi R^2}\,T_{\rm atm}^2=\frac{\rho\,D^2}{4R^2}\,T_{\rm atm}^2 . \tag{30}$$
This is Eq. (23) of subsection 1 written as a fraction, with $A_{\rm rx}=\pi D^2/4$.
- **Scope.** This holds whatever the spot size, as long as the pixel sees the whole spot. It depends on wavelength only through $T_{\rm atm}$.
- **Worked example:** $D=25$ mm and $R=200$ m give $0.1\times0.025^2/(4\times200^2)=3.9\times10^{-10}$, i.e. 94.1 dB. Clear air adds 0.15 dB, for 94.2 dB.

**Coherent detection: one spatial mode and the mode-equivalent area.** A heterodyne receiver responds only to light in the spatial mode (and polarization) of its local oscillator (LO). Three standard results give its effective collecting area.
1. **Antenna theorem** [I: A. E. Siegman, *Appl. Opt.* 5, 1588 (1966)]. A single-mode receiver has an effective area $A_{\rm eff}(\Omega)$ for light arriving from direction $\Omega$, with $d\Omega$ an element of solid angle (sr). It obeys $\int A_{\rm eff}\,d\Omega=\lambda^2$ per polarization: a single-mode receiver can have a large area or a wide field of view, but not both. This is the $A\Omega\approx\lambda^2$ rule of §C7.
2. **Back-propagated LO** [I: Siegman 1966; B. J. Rye, *Appl. Opt.* 18, 1390 (1979); R. G. Frehlich and M. J. Kavaya, *Appl. Opt.* 30, 5325 (1991)]. The angular pattern of $A_{\rm eff}$ is the LO mode propagated backwards from the detector, through the optics, to the target.
   - Let $\tilde I_B(\mathbf r)$ be that back-propagated irradiance in the target plane, normalized so that $\int\tilde I_B\,d^2r=1$ (units m⁻²). Here $\mathbf r$ is the position in the target plane, measured from the beam axis, and $d^2r$ an element of target area.
   - Light from target point $\mathbf r$ arrives within a solid angle $d\Omega=d^2r/R^2$ and sees $A_{\rm eff}(\mathbf r)=\lambda^2R^2\,\tilde I_B(\mathbf r)$.
   - This is consistent with result 1: $\int A_{\rm eff}\,d\Omega=\lambda^2\int\tilde I_B\,d^2r=\lambda^2$.
3. **Diffuse target: patches add in power.** A rough surface randomizes the optical phase from patch to patch, so on average over speckle their heterodyne powers add.
   - A patch $d^2r$ lit by irradiance $I_T(\mathbf r)$ (the transmitted power per unit area arriving at the target, W/m²) radiates $(\rho/\pi)\,I_T\,d^2r$ per steradian.
   - The receiver collects this over the area $A_{\rm eff}(\mathbf r)$ at distance $R$, i.e. over $A_{\rm eff}/R^2$ steradians.
   - Summing all patches, with $A_{\rm eff}/R^2=\lambda^2\tilde I_B$ from result 2:
$$P_{\rm het}=\frac{\rho}{\pi}\,\lambda^2\int I_T(\mathbf r)\,\tilde I_B(\mathbf r)\,d^2r . \tag{31}$$

Eq. (31) says that the coherent signal is the overlap of the transmitted spot with the receiver's back-propagated mode. Writing the result in the direct-detection form, $P_{\rm het}=P_{\rm tx}\,\rho A_{\rm mode}/(\pi R^2)$, defines the mode-equivalent collecting area
$$A_{\rm mode}=\lambda^2R^2\int\frac{I_T(\mathbf r)}{P_{\rm tx}}\,\tilde I_B(\mathbf r)\,d^2r . \tag{32}$$
In a monostatic system (one aperture shared by transmitter and receiver) the transmitted beam and the back-propagated LO are the same Gaussian at the target, $g(r)=\frac{2}{\pi w^2}e^{-2r^2/w^2}$ (normalized to unit power), where $r=\lvert\mathbf r\rvert$ and $w=w(R)$ is the beam's 1/e² radius at the target. Then $\int g^2\,d^2r=\frac{4}{\pi^2w^4}\cdot\frac{\pi w^2}{4}=\frac{1}{\pi w^2}$. Two further factors complete the result:
- the aperture passes a fraction $t$ of the Gaussian on transmit and again on receive, $t^2$ in all;
- a depolarizing target sends only half its light into the LO's polarization, a factor ½.

$$\boxed{A_{\rm mode}(R)=\frac{t^2\,\lambda^2R^2}{2\pi\,w(R)^2}},\qquad \mathcal{L}_{\rm coh}(R)=\frac{\rho\,A_{\rm mode}}{\pi R^2}\,T_{\rm atm}^2=\frac{\rho\,t^2\lambda^2}{2\pi^2\,w(R)^2}\,T_{\rm atm}^2 . \tag{33}$$

This is the monostatic link equation of Piggott et al. (Waymo) [P], written as an area; the report's scripts use it throughout (§C10.3b).
- **What it assumes** (see the assumptions in 10.1): perfect alignment and mode matching, truncation treated to first order as a power factor on each pass, no atmospheric turbulence (which reduces heterodyne efficiency at long range; Frehlich and Kavaya 1991), and a fully depolarizing Lambertian target.
- **Physical reading.** The single-mode receiver collects the target's radiance times $\lambda^2$. Concentrating the light on a smaller spot raises the radiance, and with it the signal.

**A collimated beam: flat near field, $D^2/R^2$ far field and a best aperture.** A collimated beam (waist at the aperture) spreads as
$$w(R)^2=w_0^2\,[1+(R/z_R)^2] . \tag{34}$$
With Eq. (34), $\mathcal{L}_{\rm coh}$ in Eq. (33) has three regimes:
- **Near field** ($R\ll z_R$): $w\approx w_0$, so $\mathcal{L}_{\rm coh}\to\rho t^2\lambda^2/(2\pi^2w_0^2)$, *independent of range*. The spot does not grow, so its radiance, and what one mode collects, stays constant. Here a larger aperture is worse ($\propto1/D^2$) and a longer wavelength better ($\propto\lambda^2$).
- **Far field** ($R\gg z_R$): $w\to\lambda R/(\pi w_0)$, so $\mathcal{L}_{\rm coh}\to\rho t^2w_0^2/(2R^2)$. This is the direct-detection $D^2/R^2$ law, reduced by a factor $2t^2(0.45)^2=0.34$ (−4.7 dB). The factor is the ratio of $\rho t^2w_0^2/(2R^2)$ to $\rho D^2/(4R^2)$ from Eq. (30), with $w_0=0.45D$.
- **Best collimated aperture at each range.** $w^2=w_0^2+(\lambda R/\pi w_0)^2$ is smallest, at $2\lambda R/\pi$, when $w_0^2=\lambda R/\pi$, i.e. when the Rayleigh range equals the target range. Hence
$$\mathcal{L}_{\rm env}(R)=\frac{\rho\,t^2\lambda}{4\pi R}\,T_{\rm atm}^2,\qquad D_{\rm opt}(R)=\frac{\sqrt{\lambda R/\pi}}{0.45}. \tag{35}$$
  Here $\mathcal{L}_{\rm env}$ is the envelope, the best link loss any collimated aperture can reach at range $R$, and $D_{\rm opt}$ the aperture that reaches it; dividing the optimal waist $\sqrt{\lambda R/\pi}$ by 0.45 converts it into a diameter, because $w_0=0.45D$.
  - This envelope falls only as $1/R$.
  - At the optimum, $A_{\rm mode}=t^2\lambda R/4=t^2(0.45)^2A_{\rm rx}=0.17\,A_{\rm rx}$.

**Why the beam is launched with $w_0=0.45D$.** A Gaussian beam launched through a circular aperture of radius $a=D/2$ faces a trade-off. A wide beam fills the aperture and diffracts least, but its edges are clipped; a narrow beam passes whole but spreads faster. The standard way to settle this is to maximize the far-field on-axis intensity at a fixed launched power. The launched field is $E_0e^{-r^2/w_0^2}$, where $r$ is the distance from the beam axis and $E_0\propto\sqrt{P}/w_0$ for a beam of power $P$. The far-field on-axis amplitude is the integral of this field over the aperture: $\int_0^aE_0e^{-r^2/w_0^2}\,2\pi r\,dr=\pi w_0^2E_0\,(1-e^{-a^2/w_0^2})$. At fixed $P$ it therefore scales as $w_0\,(1-e^{-a^2/w_0^2})$. Setting its derivative with respect to $w_0$ to zero gives $e^{x^2}=1+2x^2$ with $x=a/w_0$. The solution is $a/w_0=1.12$, i.e. $w_0=0.89a\approx0.45D$. At the optimum the aperture passes $1-e^{-2(a/w_0)^2}\approx92\%$ of the power, or 91.5% ($t=0.915$) at exactly $0.45D$. By reciprocity the same choice maximizes the on-axis response of the matched single-mode receiver, so one value serves transmit and receive.

**Worked numbers at 1,550 nm, $D=25$ mm:**
- $w_0=0.45\times25\ {\rm mm}=11.25$ mm and $z_R=\pi(0.01125)^2/1.55\times10^{-6}=257$ m. The factor 0.838 below is $t^2=0.915^2$.
- The near-field level is $0.1\times0.838\times(1.55\times10^{-6})^2/(2\pi^2\times0.01125^2)=8.1\times10^{-11}$, i.e. 100.9 dB.
- At 200 m, $w=11.25\sqrt{1+(200/257)^2}=14.3$ mm, so $A_{\rm mode}=63$ mm² and $\mathcal{L}_{\rm coh}=0.1\times6.3\times10^{-5}/(\pi\times200^2)=5.0\times10^{-11}$: 103.0 dB, or 103.1 dB with clear air.
- **Envelope at 200 m:** $0.1\times0.838\times1.55\times10^{-6}/(4\pi\times200)=5.2\times10^{-11}$ (102.9 dB), with $D_{\rm opt}=\sqrt{1.55\times10^{-6}\times200/\pi}/0.45=22$ mm.

![Link loss versus range for direct detection and coherent detection, with detection levels](automotive_perception_report_figures/link_budget_loss_vs_range.png)

*Figure C0.10a.* Link loss versus range for a 10% Lambertian target in clear air; a larger number of dB means less light. The shaded band is 200–300 m.
- *(a)* Direct detection with 10, 25 and 50 mm lenses.
- *(b)* Coherent detection with collimated monostatic beams of 10, 25 and 50 mm at 1,550 nm, and 25 mm at 1,310 nm. The dash-dot curve is the best collimated aperture at each range, and the grey line the 25 mm direct-detection reference.
- In both panels the dashed horizontal lines are the detection levels derived in 10.4 (Eq. (36)), and the dots mark where the curves cross them, i.e. the maximum ranges. 10.4 reads the crossings.

**Reading Figure C0.10a: the shapes of the curves** [E]:
- **Direct detection is a straight line** on these axes, falling 20 dB per decade of range for every lens. Doubling the lens diameter lowers the loss by 6 dB at every range; going from 10 to 25 mm gains $20\log_{10}2.5=8.0$ dB (at 10 m, 76.0 against 68.1 dB).
- **Coherent detection is flat, then falls.** Each curve is level out to about its Rayleigh range (41, 257 and 1,026 m for 10, 25 and 50 mm) and falls 20 dB per decade beyond it, 4.7 dB below the direct-detection line of the same aperture.
- **In the near field a smaller aperture collects more.** The plateaus lie at 93.0, 100.9 and 107.0 dB for 10, 25 and 50 mm: the loss grows as $D^2$. Two collimated apertures collect equally where their beams have the same radius, which by Eq. (34) happens at $R=\pi w_{0,1}w_{0,2}/\lambda=\sqrt{z_{R,1}z_{R,2}}$. That is 103 m for 10 and 25 mm, and 513 m for 25 and 50 mm, just beyond the plot. Below that range the smaller aperture wins.
- **The envelope touches each curve at that aperture's Rayleigh range,** where the aperture is optimal. It falls only 10 dB per decade ($1/R$), because the best aperture grows as $\sqrt R$.
- **At 1,310 nm** the 25 mm plateau is 1.5 dB higher (102.4 dB), because the near-field level scales as $\lambda^2$.

#### 10.3 How much light is needed: detection statistics (Figure C0.10b)

A detection is a decision made in one range bin (ToF) or one frequency bin (FMCW): the signal there must cross a threshold that noise alone crosses only rarely. This part finds how many signal photoelectrons per point, on average, make that decision succeed with a given probability. The threshold is set for a false-alarm probability $P_{FA}=10^{-6}$ per bin (subsection 7). The detection probability $P_D$ then depends on the mean signal $\bar n$ and on how the signal fluctuates, which differs by receiver.

*Photon counting (SPAD histogram).* A pixel that sums hundreds of speckles sees a non-fading signal, so signal and background counts are Poisson.
- **Rule:** with background mean $b$ per bin, the threshold $n_{\rm th}$ is the smallest count with $P(N\ge n_{\rm th}\mid b)\le P_{FA}$. Here $P(N\ge n\mid\mu)$ is the probability that a Poisson count $N$ of mean $\mu$ is at least $n$, and $s$ is the mean signal count in the echo's bin. Then
$$P_D=P(N\ge n_{\rm th}\mid s+b)=\frac{\gamma(n_{\rm th},\,s+b)}{\Gamma(n_{\rm th})}. \tag{37}$$
  The special functions are:
  - $\Gamma(n)=\int_0^\infty u^{n-1}e^{-u}\,du$, the gamma function, which equals $(n-1)!$ for a whole number $n$;
  - $\gamma(n,x)=\int_0^x u^{n-1}e^{-u}\,du$, the lower incomplete gamma function, the same integral stopped at $x$;
  - their ratio $\gamma(n,x)/\Gamma(n)$, the regularized lower incomplete gamma function, which rises from 0 to 1 as $x$ grows. It equals the Poisson tail $P(N\ge n\mid x)$, which is why it appears here.
- **Night, $b=0.01$:** $P(N\ge2\mid0.01)=5.0\times10^{-5}$ is too high and $P(N\ge3\mid0.01)=1.7\times10^{-7}$ passes, so $n_{\rm th}=3$.
- **Bright sun, $b=2.2$** (the §C7a model's 4,430 background counts over ≈2,000 bins, §C7b subsection 1(a)): $P(N\ge12\mid2.2)=3.6\times10^{-6}$ fails and $P(N\ge13\mid2.2)=6.0\times10^{-7}$ passes, so $n_{\rm th}=13$.

*Coherent detection (FMCW).* After the FFT, the power in one frequency bin is compared with a threshold.
- **Normalization:** the noise (LO shot noise) is set to unit mean, so noise-only power is exponential and the threshold is $x_{\rm th}=-\ln P_{FA}=13.8$. (An exponential variable of unit mean exceeds $x$ with probability $e^{-x}$, and $-\ln10^{-6}=13.8$.) In a shot-noise-limited receiver the mean signal-to-noise ratio equals $\bar n$ (subsection 2), so $\bar n$ is also the signal power in these units.
- **Steady, non-fading target:**
$$P_D=Q_1\!\left(\sqrt{2\bar n},\sqrt{2x_{\rm th}}\right), \tag{38}$$
  where $Q_1(u,v)$ is Marcum's Q function: the probability that the envelope of a steady tone of amplitude $u$ plus Gaussian noise (unit variance per quadrature) exceeds a threshold $v$. The factors of 2 convert the unit-mean power scale into that amplitude scale.
- **One speckle** (Rayleigh amplitude, exponential intensity; Swerling I, Eq. (27) of subsection 7 with $\overline{\rm SNR}=\bar n$):
$$P_D=P_{FA}^{1/(1+\bar n)} . \tag{39}$$
- **$N_{\rm sp}$ independent speckles summed incoherently** (polarization, wavelength or spatial diversity), with $\bar n$ split equally among them:
  - the noise-only sum is Gamma-distributed, so the threshold $x_{N_{\rm sp}}$ solves $Q(N_{\rm sp},x_{N_{\rm sp}})=P_{FA}$, where $Q(n,x)=1-\gamma(n,x)/\Gamma(n)$ is the regularized upper incomplete gamma function, the probability that a sum of $n$ independent unit-mean exponential variables exceeds $x$;
  - each speckle's power, signal plus noise, is then exponential with mean $1+\bar n/N_{\rm sp}$, so
$$P_D=Q\!\left(N_{\rm sp},\,\frac{x_{N_{\rm sp}}}{1+\bar n/N_{\rm sp}}\right); \tag{40}$$
  - for $N_{\rm sp}=4$, $x_4=21.4$.

| Receiver statistics | $\bar n$ for $P_D=0.5$ | $\bar n$ for $P_D=0.9$ | $P_D$ at $\bar n=25$ | $P_D$ at $\bar n=30$ | $P_D$ at $\bar n=50$ |
|---|---|---|---|---|---|
| Photon counting, night ($b=0.01$, $n_{\rm th}=3$) | 2.7 | 5.3 | 1.00 | 1.00 | 1.00 |
| Photon counting, bright sun ($b=2.2$, $n_{\rm th}=13$) | 10.5 | 15.6 | 0.999 | 1.00 | 1.00 |
| Coherent, steady target | 13.3 | 20.8 | 0.97 | 0.995 | 1.00 |
| Coherent, 4 speckles summed | 19.3 | 44.9 | 0.66 | 0.76 | 0.92 |
| Coherent, 1 speckle | 18.9 | 130 | 0.59 | 0.64 | 0.76 |

*How the numbers are derived* [E]:
- **Method:** each entry solves the matching $P_D$ expression numerically (script): Eq. (37) for photon counting, with $\bar n=s$, and Eqs. (38), (40) and (39) for the three coherent rows.
- **Worked check, one speckle,** from Eq. (39):
  - at 90%, $1+\bar n=\ln P_{FA}/\ln P_D=(-13.82)/(-0.1054)=131$;
  - at $\bar n=30$, $P_D=(10^{-6})^{1/31}=e^{-13.82/31}=0.64$.

![Detection probability versus mean signal photoelectrons for photon counting and coherent detection](automotive_perception_report_figures/link_budget_detection_statistics.png)

*Figure C0.10b.* Detection probability versus mean signal photoelectrons per point at $P_{FA}=10^{-6}$ per range bin.
- Solid: photon counting at night and in bright sun. Dashed: coherent detection of a steady target, of four summed speckles and of one speckle.
- Dots and numbers mark $P_D=0.9$. The dotted verticals are the photoelectron counts used in the §C7a model (25 for ToF, 30 for FMCW).

**Reading Figure C0.10b** [E]:
- **ToF:** the model's 25 counts are 1.6× the 15.6 that an ideal single-bin counter needs in bright sun. The margin covers a return spread over two or three bins, dead time and pile-up (§C6).
- **FMCW:** the model's 30 photoelectrons give $P_D\approx0.64$ with one speckle and 0.76 with four. A 90% requirement needs 45 with four speckles (close to Waymo's 50 [P]), or 130 with one. The §C7a energy per point is therefore, if anything, generous to FMCW.
- **Curve shapes:** photon counting has the steepest curves. Once the mean clears the threshold, a non-fading Poisson signal almost always crosses it. Speckle fading makes the coherent curves shallow, so the last few percent of $P_D$ cost the most photons.
- **What this means for the comparison:** a SPAD ToF receiver in bright sun needs about 16–25 photoelectrons per point, and an FMCW receiver about 45 (four speckles) to 130 (one speckle) for the same 90% detection. The coherent receiver's freedom from background therefore does not translate into a lower photon requirement: even a steady coherent target needs more (20.8) than an ideal photon counter in bright sun (15.6), and speckle fading adds to that.
- **Next step:** 10.4 turns the model's photoelectron counts, 25 for SPAD ToF and 30 for FMCW (the dotted verticals), into detection levels.

#### 10.4 Where they meet: the detection level and the maximum range (Figure C0.10a)

This step turns the photoelectron requirement of 10.3 into a level on the link-loss axis of Figure C0.10a. The maximum range can then be read off the figure as the range where a loss curve crosses that level.

**The detection level.** Setting the mean signal $\bar n$ equal to the required $n_{\rm req}$ in Eq. (29) gives the largest loss a point can tolerate,
$$\mathcal{L}_{\rm det}=\frac{n_{\rm req}\,E_{\rm ph}}{\eta\,E_{\rm tx}}, \tag{36}$$
and the maximum range $R_{\max}$ solves $\mathcal{L}(R_{\max})=\mathcal{L}_{\rm det}$. "Largest loss" means the smallest usable fraction: a link with $\mathcal{L}$ below $\mathcal{L}_{\rm det}$ delivers fewer than $n_{\rm req}$ photoelectrons. The level moves by 10 dB for every factor of 10 in $E_{\rm tx}$. The table gives it for the three receivers compared in this report; these are the dashed lines of Figure C0.10a.

| Receiver | $\lambda$ | $n_{\rm req}$ | $\eta$ | $E_{\rm tx}$ per point | $\mathcal{L}_{\rm det}$ | Tolerable loss |
|---|---|---|---|---|---|---|
| SPAD dToF, bright sun | 940 nm | 25 | 0.185 | 0.1 µJ (e.g. ≈10 shots of 10 nJ) | $2.9\times10^{-10}$ | 95.4 dB |
| Linear InGaAs APD ToF | 1,550 nm | ≈890 | 0.40 | 2 µJ (one fibre-laser pulse) | $1.4\times10^{-10}$ | 98.5 dB |
| FMCW | 1,550 nm | 30 | 0.25 | 0.3 µJ (30 mW × 10 µs) | $5.1\times10^{-11}$ | 102.9 dB |

*How the numbers are derived* [E]:
- **$n_{\rm req}$ and $\eta$** are the §C7a values, with the APD's photoelectron count taken from the amplifier-noise calculation of §C7b subsection 1(a):
  - SPAD: optics 0.5 × photon detection efficiency 0.37;
  - APD: optics 0.5 × quantum efficiency 0.8;
  - FMCW: the §C7a(a) efficiency.
- **Worked (SPAD),** from Eq. (36): $25\times2.11\times10^{-19}/(0.185\times10^{-7})=2.86\times10^{-10}$, and $-10\log_{10}(2.86\times10^{-10})=95.4$ dB.
- **Worked (FMCW):** $30\times1.28\times10^{-19}/(0.25\times3\times10^{-7})=5.13\times10^{-11}$, i.e. 102.9 dB.

**Reading Figure C0.10a: where the curves cross the detection levels** [E]:
- **Direct detection falls as $D^2/R^2$ at every range.** Setting $\rho D^2/(4R^2)=\mathcal{L}_{\rm det}$ (Eq. (30) with $T_{\rm atm}=1$) gives $R_{\max}=\tfrac{D}{2}\sqrt{\rho/\mathcal{L}_{\rm det}}$.
  - SPAD case, $D=25$ mm: $0.0125\times\sqrt{0.1/2.86\times10^{-10}}=234$ m, or 229 m with clear air. The 10 and 50 mm lenses reach 93 and 450 m.
  - The APD case reaches 326 m with 25 mm. Its per-point need $n_{\rm req}E_{\rm ph}/\eta$ is 10× the SPAD's, but its 20× larger energy leaves a 2× margin, i.e. $\sqrt2\times$ the range.
- **Coherent detection is flat, then falls.** With 0.3 µJ, $D=10$ mm reaches 121 m and $D=25$ mm reaches 189 m.
  - The 50 mm aperture reaches *no* range: its near-field level, 107.0 dB, already exceeds the 102.9 dB budget.
  - At 1,310 nm the 25 mm aperture also fails, narrowly. Its near field is $10\log_{10}(1310/1550)^2=-1.5$ dB weaker, at 102.4 dB, and its 18% more energetic photons lower the budget to 102.2 dB.
- **Near the plateau, range is hypersensitive to the budget.**
  - For a fixed aperture, ignoring $T_{\rm atm}$, Eqs. (33) and (34) give $\mathcal{L}_{\rm coh}(R)=\mathcal{L}_{\rm coh}(0)/[1+(R/z_R)^2]$, where $\mathcal{L}_{\rm coh}(0)$ is the near-field plateau. So $R_{\max}=z_R\sqrt{\mathcal{L}_{\rm coh}(0)/\mathcal{L}_{\rm det}-1}$.
  - For 25 mm: $257\times\sqrt{8.06/5.13-1}=194$ m, or 189 m with clear air.
  - Requiring $P_D=0.9$ with four speckles ($n_{\rm req}=45$, 10.3) raises the level by $10\log_{10}(45/30)=1.8$ dB and cuts the 25 mm range to **54 m**.
  - The best collimated aperture degrades gracefully instead, as $R_{\max}\propto1/n_{\rm req}$: from 198 m to 133 m.
  - 10.6 follows this sensitivity to its practical consequences: dark targets, dirty windows and weather.
- **At 200 m, the 20–25 mm apertures of §C7a are close to the optimum** ($D_{\rm opt}=22$ mm). A bigger collimated aperture helps only beyond its own Rayleigh range; at 500 m the optimum is 35 mm.

#### 10.5 How range scales with energy per point and aperture (Figure C0.10c)

Solve $\mathcal{L}(R_{\max})=\mathcal{L}_{\rm det}(E_{\rm tx})$, i.e. set the link loss of 10.2 equal to the detection level of Eq. (36), with $T_{\rm atm}\approx1$ in the closed forms. The answer tells a designer what an extra joule per point, or a larger lens, buys in range.

- **Direct detection:** from Eqs. (30) and (36),
$$R_{\max}=\frac{D}{2}\sqrt{\frac{\rho\,\eta\,E_{\rm tx}}{n_{\rm req}\,E_{\rm ph}}}\ \propto\sqrt{A_{\rm rx}E_{\rm tx}} . \tag{41}$$
  At fixed average optical power $P_{\rm opt}$ (W), the point rate is $\dot N=P_{\rm opt}/E_{\rm tx}$ points per second. So $\dot N R_{\max}^2=\rho\,\eta\,D^2P_{\rm opt}/(4n_{\rm req}E_{\rm ph})$ is constant: this is the range-weighted point-rate figure of merit of §C3b. A lidar can trade points per second for range, but not raise both, without more power or a larger lens.
- **Coherent, fixed collimated aperture:** nothing is detected below a minimum energy per point $E_{\min}$, the energy at which even the near-field plateau $\mathcal{L}_{\rm coh}(0)$ just reaches the detection level:
$$E_{\min}=\frac{n_{\rm req}E_{\rm ph}}{\eta\,\mathcal{L}_{\rm coh}(0)}=\frac{2\pi^2\,n_{\rm req}\,E_{\rm ph}\,w_0^2}{\eta\,\rho\,t^2\lambda^2}. \tag{42}$$
  - This is 0.031, 0.19 and 0.76 µJ for $D=10$, 25 and 50 mm.
  - Above it, $R_{\max}=z_R\sqrt{E_{\rm tx}/E_{\min}-1}$, which becomes the $\sqrt{E_{\rm tx}}$ law once $R_{\max}\gg z_R$.
  - Worked (25 mm): $2\pi^2\times30\times1.28\times10^{-19}\times0.01125^2/(0.25\times0.1\times0.838\times(1.55\times10^{-6})^2)=9.6\times10^{-21}/5.0\times10^{-14}=1.9\times10^{-7}$ J.
- **Coherent, best collimated aperture at each range:** setting the envelope of Eq. (35) equal to the detection level gives
$$R_{\max}=\frac{\rho\,t^2\lambda\,\eta\,E_{\rm tx}}{4\pi\,n_{\rm req}E_{\rm ph}}\ \propto E_{\rm tx},\qquad \dot N\,R_{\max}=\text{const}. \tag{43}$$
  - Worked: $0.1\times0.838\times1.55\times10^{-6}\times0.25\times3\times10^{-7}/(4\pi\times30\times1.28\times10^{-19})=9.7\times10^{-15}/4.8\times10^{-17}=202$ m (198 m with clear air).
  - Doubling the energy doubles the range, but only if the aperture grows as $\sqrt R$, while the footprint's share of a fixed angular cell shrinks as $1/R$ (§C10.3a).
- **Equal apertures, constant gap.** At $D=D_{\rm opt}(R)$, the ratio of the energies per sample needed by FMCW and SPAD ToF does not depend on range:
$$\frac{E_{\rm FMCW}}{E_{\rm SPAD}}=\frac{n_{\rm c}E_{\rm ph,c}/\eta_{\rm c}}{n_{\rm d}E_{\rm ph,d}/\eta_{\rm d}}\cdot\frac{A_{\rm rx}}{A_{\rm mode}}=0.54\times\frac{1}{t^2(0.45)^2}=0.54\times5.9=3.2 . \tag{44}$$
  - The subscripts c and d mark the coherent and direct-detection cases: $n_{\rm c}$ and $n_{\rm d}$ are their values of $n_{\rm req}$, $E_{\rm ph,c}$ and $E_{\rm ph,d}$ their photon energies (1,550 and 940 nm), and $\eta_{\rm c}$, $\eta_{\rm d}$ their efficiencies.
  - The second factor is the ratio of the direct-detection lens area to the coherent mode-equivalent area at the optimum, $A_{\rm mode}=t^2(0.45)^2A_{\rm rx}$ from 10.2; 0.45 is again the ratio $w_0/D$.
  - The first factor is $(30\times1.28\times10^{-19}/0.25)/(25\times2.11\times10^{-19}/0.185)=1.54\times10^{-17}/2.86\times10^{-17}=0.54$.
  - With clear-air loss the ratio is 3.1 at 100–500 m.
- **Against a fixed 25 mm SPAD receiver**, the gap per sample closes as $1/R$, because the optimal coherent aperture grows: 8.1× at 100 m, 4.0× at 200 m, 2.6× at 300 m and 1.6× at 500 m.
- **Linear APD against SPAD with the same lens:** $(890\times1.28\times10^{-19}/0.40)/(25\times2.11\times10^{-19}/0.185)=10.0$. That is ten times the energy per point at every range, which the 1,550 nm eye-safety limits can pay for at low point rates (§C4c).

![Maximum range versus transmitted energy per point for direct and coherent detection](automotive_perception_report_figures/link_budget_range_scaling.png)

*Figure C0.10c.* Maximum range at 10% reflectance versus transmitted optical energy per point, for the detection levels of 10.4.
- The top axis converts energy per point into points per second per watt of light, $1/E_{\rm tx}$ (1 µJ per point is 1 Mpts/s per W).
- *(a)* Direct detection: SPAD at 940 nm with 10, 25 and 50 mm lenses, and a linear APD at 1,550 nm with 25 mm.
- *(b)* FMCW at 1,550 nm with collimated 10, 25 and 50 mm apertures, the best collimated aperture (dash-dot), and the 25 mm SPAD reference (grey).
- The dotted lines mark 200 and 300 m.

#### 10.6 Margin at short range: dark targets, dirty windows, fog and rain (Figure C0.10d)

The crossings of 10.4 say how far a sensor sees one 10% target in clear air, through a clean window. In service it also meets darker targets, dirty or wet windows, fog and rain. Each of these multiplies the returned light by a factor below one. This part asks what that factor costs in range. The answer depends on the *shape* of the loss curve (10.2). Direct detection gains signal steeply as the target comes closer, so a design sized for 200 m has light to spare at short range. A collimated coherent beam does not gain signal, so it has almost none to spare.

**The designs compared.** To compare like with like, each design gets just enough energy per point to reach $R_0=200$ m on a 10% target in clear air: its detection level equals its own link loss at 200 m, $\mathcal{L}_{\rm det}=\mathcal{L}(R_0)$. By Eq. (36) that energy is $E_{\rm tx}=n_{\rm req}E_{\rm ph}/[\eta\,\mathcal{L}(R_0)]$, with $n_{\rm req}$ and $\eta$ from the table in 10.4.
- **SPAD ToF at 940 nm with a 25 mm lens** needs 76 nJ per point: the 0.1 µJ of 10.4, which reaches 229 m, scaled by $(200/229)^2=0.76$. Without the 0.15 dB of clear-air loss this is the ≈73 nJ of §C7b subsection 1.
- **FMCW at 1,550 nm with the best collimated aperture for 200 m** ($D_{\rm opt}=22$ mm, Eq. (35)) needs 303 nJ. This is close to the ≈0.30 µJ of §C7b subsection 1, which uses a 20 mm beam and no atmospheric loss. With a 25 mm aperture it needs 312 nJ.
- **FMCW with smaller apertures** (16, 13, 10 and 7 mm) needs more energy, because at 200 m these beams are in their far field and collect less (10.2). Eq. (903) below gives the price.

**Margin.** The margin $M(R)$ of a design at range $R$ is the extra loss, in dB, that it can absorb there and still detect the target:
$$M(R)=10\log_{10}\frac{\mathcal{L}(R)}{\mathcal{L}_{\rm det}},\qquad M_{\rm DD}(R)=20\log_{10}\frac{R_0}{R},\qquad M_{\rm coh}(R)=10\log_{10}\frac{1+(R_0/z_R)^2}{1+(R/z_R)^2} . \tag{901}$$
The direct-detection form follows from Eq. (30), and the coherent form from Eqs. (33) and (34), both with $\mathcal{L}_{\rm det}=\mathcal{L}(R_0)$. Both neglect clear-air extinction, which changes the margins by at most 0.15 dB here.
- **Direct detection gains 6 dB for every halving of range.** At 10 m the margin is $20\log_{10}(200/10)=26.0$ dB, or 26.2 dB with clear air: the design receives 400 times the light it needs.
- **The coherent margin saturates.** As $R\to0$, $M_{\rm coh}$ rises only to the *plateau margin* $M_0=10\log_{10}[1+(R_0/z_R)^2]$, because the near-field loss is flat. For the best aperture $z_R=R_0$, so $M_0=10\log_{10}2=3.0$ dB: at 10 m the design receives only twice the light it needs. For 25 mm, $z_R=257$ m and $M_0=10\log_{10}[1+(200/257)^2]=2.1$ dB.

**A fixed extra loss: darker targets and dirty or wet windows.** Let $X$ be an extra two-way loss, in dB, that does not depend on range. Examples:
- **A darker target.** Both link losses are proportional to the reflectance (Eqs. (30) and (33)). A target of reflectance $\rho$ instead of $\rho_0=10\%$ therefore acts as $X=10\log_{10}(\rho_0/\rho)$: 3.0 dB for a 5% target and 7.0 dB for a 2% target.
- **A water film on the window,** crossed on the way out and again on the way back. Liquid water costs 9.4 dB per millimetre round trip at 1,550 nm (§C4c), so a 0.2 mm film costs $0.2\times9.4=1.9$ dB. At 940 nm water absorbs tens of times more weakly, and the film is neglected.
- **Dust, mud, salt or droplets on the window,** which scatter light out of the beam at every wavelength.
- **A receiver below its design point,** for example a Ge photodiode at 125 °C that reaches only 82–94% of the shot-noise limit (§C4c; 0.3–0.9 dB), or a stricter detection requirement than the model assumes (10.3).

A target is still detected wherever $M(R)\ge X$. Solving Eq. (901) for the range gives the maximum range with the extra loss:
$$R_{\max,{\rm DD}}(X)=R_0\,10^{-X/20},\qquad R_{\max,{\rm coh}}(X)=z_R\sqrt{\left[1+(R_0/z_R)^2\right]10^{-X/10}-1}\quad\text{for }X<M_0 . \tag{902}$$
- **Direct detection degrades gracefully.** A 3 dB loss costs 29% of the range ($200\times10^{-3/20}=142$ m), 6 dB halves it (101 m), and 10 dB still leaves 64 m.
- **A coherent design falls off a cliff at $X=M_0$.** Beyond it the square root has no real value: the design detects nothing *at any range*, because even its near-field plateau no longer reaches the detection level. The best-aperture design reaches 110 m behind a 0.2 mm water film ($X=1.9$ dB), 27 m with $X=3$ dB and nothing beyond 3.1 dB. The 25 mm design reaches 58 m behind the film and nothing beyond 2.1 dB.
- **The darkest target detectable at any range** follows from $X=M_0$. For a coherent design it is $\rho_{\min}=\rho_0/[1+(R_0/z_R)^2]$: 4.9% for the best aperture and 6.1% for 25 mm (with clear air). Direct detection has no such floor, since $\rho_{\min}(R)=\rho_0(R/R_0)^2$ keeps falling as the target comes closer: 0.024% at 10 m.

**What margin costs a coherent design.** Shrinking the aperture shortens the Rayleigh range and raises the plateau margin. But the narrower beam spreads more by 200 m, so more energy is needed to get there. Write $u=z_R/R_0$ for the Rayleigh range in units of the design range. The energy needed is proportional to $1/\mathcal{L}_{\rm coh}(R_0)$, i.e. to $w(R_0)^2$ (Eq. (33)). Eq. (34) with $w_0^2=\lambda z_R/\pi$ gives $w(R_0)^2=w_0^2+(\lambda R_0/\pi w_0)^2=(\lambda R_0/\pi)(u+1/u)$. The best aperture has $u=1$, so relative to it
$$\frac{E_{\rm tx}}{E_{\rm opt}}=\frac12\left(u+\frac1u\right),\qquad M_0=10\log_{10}\left(1+\frac1{u^2}\right),\quad\text{i.e.}\quad u=\left(10^{M_0/10}-1\right)^{-1/2} . \tag{903}$$
- Plateau margins of 6.7, 9.7, 13.9 and 20.0 dB (apertures of 16, 13, 10 and 7 mm) cost 1.21, 1.61, 2.54 and 5.02 times the energy.
- For large margins $E_{\rm tx}/E_{\rm opt}\approx\tfrac12\,10^{M_0/20}$, so every further 6 dB of margin doubles the energy. Direct detection gets its short-range margin free.

The table collects these results. Energies are per point, with multiples relative to the best FMCW design; "blind" means no detection at any range.

| Design (each reaches 200 m at 10% in clear air) | $z_R$ | Energy per point | Margin at 10 m | Darkest target at any range | $R_{\max}$ at $X=3$ dB (≈5% target) | $R_{\max}$ at $X=6$ dB | $R_{\max}$ at $X=10$ dB |
|---|---|---|---|---|---|---|---|
| SPAD ToF, 940 nm, 25 mm lens | — | 76 nJ (0.25×) | 26.2 dB | no floor (0.024% at 10 m) | 142 m | 101 m | 64 m |
| FMCW, 1,550 nm, 25 mm | 257 m | 312 nJ (1.03×) | 2.1 dB | 6.1% | blind | blind | blind |
| FMCW, 22 mm (best for 200 m) | 200 m | 303 nJ (1×) | 3.1 dB | 4.9% | 27 m | blind | blind |
| FMCW, 16 mm | 105 m | 368 nJ (1.21×) | 6.7 dB | 2.1% | 121 m | 44 m | blind |
| FMCW, 13 mm | 69 m | 489 nJ (1.61×) | 9.7 dB | 1.05% | 133 m | 81 m | blind |
| FMCW, 10 mm | 41 m | 769 nJ (2.54×) | 13.8 dB | 0.40% | 139 m | 94 m | 50 m |
| FMCW, 7 mm | 20 m | 1,522 nJ (5.02×) | 19.1 dB | 0.10% | 141 m | 99 m | 61 m |

**Fog.** Fog multiplies the link loss by $e^{-2\alpha R}$, where $\alpha$ is the extinction coefficient of the Kim model of subsection 8, $\alpha=(3.912/V)(\lambda/550\ {\rm nm})^{-q_{\rm K}}$ for meteorological visibility $V$. Below 500 m visibility $q_{\rm K}=0$, so fog then attenuates 940 and 1,550 nm equally. Unlike a dirty window, this loss grows with range: it is $10\log_{10}e^{2\alpha R}=8.686\,\alpha R$ dB, where $8.686=20/\ln10$. A design therefore detects out to the range at which its margin just pays for the fog:
$$M(R_{\max})=8.686\,\alpha\,R_{\max}\quad({\rm dB}) . \tag{904}$$
- **For direct detection** this is the condition $R^2e^{2\alpha R}=R_0^2$ of subsection 8.
- **For a coherent design** the left side never exceeds $M_0$, so the reach can never exceed $M_0/(8.686\,\alpha)$. In fog of 200 m visibility ($\alpha=19.6$ /km) the best-aperture design is limited to $3.1/(8.686\times0.0196\ {\rm m^{-1}})=18$ m, which is the reach the script finds.

| Design | $V=5$ km | 2 km | 1 km | 500 m | 200 m | 100 m | 50 m |
|---|---|---|---|---|---|---|---|
| SPAD ToF, 25 mm | 188 m | 163 m | 136 m | 96 m | 61 m | 41 m | 26 m |
| FMCW, 25 mm | 181 m | 131 m | 84 m | 31 m | 13 m | 6 m | 3 m |
| FMCW, 22 mm (best) | 186 m | 145 m | 102 m | 43 m | 18 m | 9 m | 5 m |
| FMCW, 16 mm | 191 m | 163 m | 131 m | 74 m | 37 m | 19 m | 10 m |
| FMCW, 13 mm | 192 m | 167 m | 138 m | 85 m | 48 m | 27 m | 14 m |
| FMCW, 10 mm | 192 m | 169 m | 142 m | 92 m | 56 m | 34 m | 19 m |
| FMCW, 7 mm | 193 m | 170 m | 144 m | 95 m | 60 m | 39 m | 24 m |

- **In haze** (visibility of 1 km or more) the smaller-aperture FMCW designs reach slightly farther than ToF. The reason is that the Kim model gives 1,550 nm less extinction than 940 nm there: at 1 km, $q_{\rm K}=0.5$ and $\alpha_{1550}/\alpha_{940}=(1550/940)^{-0.5}=0.78$.
- **In fog** (below 500 m visibility), where extinction no longer depends on wavelength, the best-aperture FMCW design keeps 18 m at 200 m visibility and 5 m at 50 m, against 61 and 26 m for ToF. The 7 mm design matches ToF to within 2 m, at twenty times its energy.
- **The kinks** in Figure C0.10d(b) at 0.5 and 1 km visibility come from the Kim model, whose exponent $q_{\rm K}$ changes form at those visibilities (subsection 8), not from the receivers.

**Rain and a wet window.** Raindrops are much larger than the wavelength, so rain extinguishes 940 and 1,550 nm almost equally. Subsection 8's empirical law gives the specific attenuation $\gamma_{\rm rain}=1.076\,R_r^{0.67}$ dB/km for a rain rate $R_r$ in mm/h: 3.2, 9.3 and 23.5 dB/km at 5, 25 and 100 mm/h. The light crosses range $R$ twice, so the loss is $2\gamma_{\rm rain}R$ with $R$ in km, e.g. 1.9 dB at 100 m in 25 mm/h rain. Like fog, rain is a loss that grows with range, so Eq. (904) applies with $8.686\,\alpha R$ replaced by $2\gamma_{\rm rain}R$. In rain the window is usually wet as well, which adds a fixed loss (Eq. (902)) at 1,550 nm only.

| Design | 5 mm/h | 25 mm/h | 100 mm/h | 25 mm/h + 0.1 mm film | 25 mm/h + 0.2 mm film | 100 mm/h + 0.2 mm film |
|---|---|---|---|---|---|---|
| SPAD ToF, 25 mm | 176 m | 147 m | 111 m | 147 m | 147 m | 111 m |
| FMCW, 25 mm | 143 m | 88 m | 43 m | 53 m | 13 m | 5 m |
| FMCW, 22 mm (best) | 155 m | 106 m | 58 m | 80 m | 50 m | 24 m |
| FMCW, 16 mm | 170 m | 134 m | 91 m | 118 m | 102 m | 69 m |
| FMCW, 13 mm | 173 m | 141 m | 101 m | 127 m | 115 m | 84 m |
| FMCW, 10 mm | 175 m | 144 m | 107 m | 132 m | 121 m | 92 m |
| FMCW, 7 mm | 176 m | 146 m | 110 m | 134 m | 123 m | 95 m |

- **Rain alone costs every design range, and the large-aperture FMCW designs the most.** Heavy rain of 25 mm/h leaves ToF 147 m and the best FMCW design 106 m.
- **A wet window then hits FMCW a second time.** With a 0.2 mm film in 25 mm/h rain, the best-aperture FMCW design reaches 50 m and the 25 mm design 13 m. The ToF design keeps its 147 m, because water barely absorbs at 940 nm. Even the 7 mm FMCW design loses 23 m to the film (146 → 123 m).
- **Film thickness is the uncertain input.** It depends on the window's tilt, coating, heating and wiping, none of which is modelled here. Figure C0.10d(d) therefore plots range against film thickness at a fixed 25 mm/h.
- **Rain is often not the worst of it.** Spray and splash from other vehicles, and wet, mirror-like roads, affect both receivers and are not modelled (subsection 8).

**Fog also sends light back: backscatter clutter.** Fog droplets scatter some of the light back toward the sensor, from every range. Two numbers decide whether this matters: how strong the fog return is in the target's own range bin, and how strong it is close to the sensor.
- **Symbols.** $\beta$ is the fog's volume backscatter coefficient (m⁻¹ sr⁻¹). A slab of fog of thickness $\Delta R$ sends $\beta\,\Delta R$ per steradian back toward the sensor, per unit of power crossing it. It is tied to the extinction by the lidar ratio $S=\alpha/\beta$, here 18 sr; O'Connor et al. (2004) give 18.8 sr for water clouds at 905 nm [I]. $\Delta R$ is the range-bin length, here 0.15 m: a 1 ns ToF bin, or the $c/2B$ resolution of an FMCW chirp of bandwidth $B=1$ GHz.
- **In the target's own bin.** The Lambertian target returns $\rho/\pi$ per steradian, and both returns reach the receiver through the same geometry. So
$$\frac{P_{\rm fog}}{P_{\rm tgt}}=\frac{\pi\beta\,\Delta R}{\rho}\ \ \text{(direct detection)},\qquad \frac{P_{\rm fog}}{P_{\rm tgt}}=\frac{2\pi\beta\,\Delta R}{\rho}\ \ \text{(coherent)} . \tag{905}$$
  - The factor 2 for the coherent receiver arises because spherical droplets keep the polarization: all of their return lies in the LO's polarization, while the model's depolarizing target puts only half of its return there (the ½ in Eq. (33)).
  - In fog of 200 m visibility, $\beta=19.6\ {\rm km^{-1}}/18\ {\rm sr}=1.09\times10^{-3}$ m⁻¹ sr⁻¹. Then $\pi\beta\Delta R/\rho=\pi\times1.09\times10^{-3}\times0.15/0.1=5.1\times10^{-3}$, i.e. −22.9 dB, and −19.9 dB for coherent detection. At 50 m visibility the ratios are −16.9 and −13.9 dB.
  - So in the target's own bin the fog is weak for both receivers.
- **Near the sensor.** Here the receivers differ, because they collect nearby light differently. A direct-detection lens collects $A_{\rm rx}/r^2$ from range $r$, so fog a few metres away returns far more per bin than fog near the target. A coherent receiver collects $A_{\rm mode}(r)/r^2=t^2\lambda^2/[2\pi w(r)^2]$ (Eq. (33)), which is flat inside the Rayleigh range. Relative to the echo of a 10% target at range $R_t$, the fog in the bin at range $r$ returns
$$\frac{P_{\rm fog}(r)}{P_{\rm tgt}(R_t)}=\frac{\pi\beta\,\Delta R}{\rho}\left(\frac{R_t}{r}\right)^2e^{2\alpha(R_t-r)}\ \ \text{(DD)},\qquad \frac{2\pi\beta\,\Delta R}{\rho}\,\frac{w(R_t)^2}{w(r)^2}\,e^{2\alpha(R_t-r)}\ \ \text{(coherent)}, \tag{906}$$
  where the exponential is the extra extinction on the target's longer path. The direct-detection form assumes that the receiver sees the whole beam from $r$ onward (full overlap); a biaxial design, with separate transmit and receive apertures, sees less of the first metres.

| Fog in the bin at | SPAD ToF, 25 mm (reach 61 m) | FMCW, 7 mm (reach 60 m) | FMCW, 13 mm (reach 48 m) | FMCW, 25 mm (reach 13 m) |
|---|---|---|---|---|
| 2 m | +13.2 dB | −3.2 dB | −9.9 dB | −11.6 dB |
| 5 m | +4.7 dB | −3.9 dB | −10.5 dB | −12.1 dB |
| 10 m | −2.1 dB | −5.5 dB | −11.4 dB | −12.9 dB |
| 20 m | −9.9 dB | −9.2 dB | −13.3 dB | −14.7 dB |

*The table* gives the fog return in one bin relative to the echo of a 10% target at 50 m, in fog of 200 m visibility, from Eq. (906). The reach in each column heading is that design's maximum range in this fog, from the fog table above; the 13 and 25 mm designs would not detect the 50 m target at all. Worked examples [E]:
- **Direct detection, 2 m:** $-22.9\ {\rm dB}+20\log_{10}(50/2)+8.686\times0.0196\times48=-22.9+28.0+8.2=+13.2$ dB.
- **FMCW 7 mm, 2 m:** $z_R=20$ m, so $w(50)^2/w(2)^2=[1+(50/20.1)^2]/[1+(2/20.1)^2]=7.19/1.01=7.1$, i.e. 8.5 dB, and $-19.9+8.5+8.2=-3.2$ dB.

**What the clutter means** [E]:
- **Direct detection.** The fog in the first metres returns more light per bin than the target itself (+13 dB at 2 m). Summed over the 200 bins between 20 and 50 m, it returns 5.8 times the target's photons.
  - The target echo still arrives later, so a linear receiver can reject the fog by its arrival time, provided the fog does not saturate its front end.
  - A SPAD, however, is dead for a few nanoseconds after each count, and a first-photon design records only one count per shot. The early fog counts then block part of the target echo (pile-up, §C6). This is the SPAD saturation noted in subsection 8.
  - Range gating and a biaxial layout cut the near fog, at the price of a blind zone near the car.
- **Coherent detection.** Fog near the sensor is no brighter per bin than the target, even for the 7 mm design (−3 dB at 2 m), and it arrives at other beat frequencies. The strong LO keeps the receiver linear, so the fog adds a weak noise floor in the near-range bins and nothing at the target's frequency. This is FMCW's real advantage in fog: it rejects the clutter, although it gains no signal.
- **Doppler** separates moving targets from fog, but not static ones: the droplets drift with the air, so they share the Doppler shift of the road and of parked cars.
- **Multiple scattering.** A single-mode receiver accepts light only within about $\lambda/(\pi w_0)$ of its axis (44 µrad for 25 mm at 1,550 nm), whereas a direct-detection pixel typically accepts a milliradian or more. The coherent receiver therefore rejects multiply scattered light, which arrives from wider angles. That removes clutter, but also the small gain in real reach that subsection 8 notes for direct detection.

![Maximum range of designs that all reach 200 m, versus an extra fixed loss, fog visibility, rain rate, and a water film on the window in heavy rain](automotive_perception_report_figures/link_budget_margin_weather.png)

*Figure C0.10d.* Maximum range on a 10% target for five designs that all reach 200 m in clear air. The designs are SPAD ToF at 940 nm with a 25 mm lens (red, dashed) and FMCW at 1,550 nm with collimated apertures of 25, 22 (the best for 200 m), 13 and 7 mm (cool colours). Each design's energy per point, given in the legend, is set to reach exactly 200 m.
- *(a)* Range versus an extra fixed two-way loss $X$ (Eq. (902)). The top axis gives the equivalent target reflectance behind a clean window, and the dotted line marks a 0.2 mm water film at 1,550 nm. A range of zero means no detection at any range.
- *(b)* Range versus meteorological visibility, with fog extinction from the Kim model (Eq. (904)). Fog is visibility below 1 km; the shaded band is 200 m to 1 km, and thick fog is 50–200 m (international visibility code; Kim et al. 2001).
- *(c)* Range versus rain rate, with a clean window (Carbonneau law, subsection 8). The rain classes are those of the Canadian observing manual MANOBS (light below 2.5 mm/h, moderate to 7.6, heavy, shaded, to 50, violent above); WMO notes that there is no agreed international definition.
- *(d)* Range in 25 mm/h rain versus the thickness of a water film on the window. The top axis gives the film's two-way loss at 1,550 nm; the film is neglected at 940 nm.

**Reading Figure C0.10d** [E]:
- **Panel (a) is Eq. (902).** The ToF curve falls smoothly. Each FMCW curve drops to zero at its plateau margin $M_0$: 2.1 dB for 25 mm, 3.1 dB for 22 mm and 9.7 dB for 13 mm.
- **Only the 7 mm design follows the ToF curve.** Its Rayleigh range (20 m) is far below 200 m, so over most of the range it is in its far field, where its loss falls as $1/R^2$ like direct detection.
- **Panel (b)** shows the same ordering in fog, where the loss grows with range. ToF and the 7 mm FMCW design keep about 60 m at 200 m visibility.
- **Panels (c) and (d)** show rain costing every design range. The water film then adds a fixed loss for FMCW only, which pushes the large-aperture designs over their cliff.

**What this means for design** [E]:
- **A range specification at 10% in clear air says little about robustness.** The same "200 m at 10%" describes a ToF design with 26 dB to spare at 10 m and an FMCW design with 3 dB. A coherent sensor's datasheet should therefore also give its plateau margin, or equivalently the darkest target it detects at any range, $\rho_0/[1+(R_0/z_R)^2]$, together with its range at 5% and in 200 m fog.
- **Robustness costs a coherent design energy, not a ToF design.**
  - A 13 mm aperture (1.6× the best FMCW energy) gives 9.7 dB of plateau margin: 133 m on a 5% target, 48 m in 200 m fog, and 115 m in heavy rain behind a 0.2 mm film.
  - A 7 mm aperture matches ToF's tolerance of dark targets and fog. It needs 5.0× the best FMCW energy, i.e. 1.5 µJ per point, twenty times ToF's 76 nJ.
  - The eye-safety limits at 1,550 nm leave room for that energy (§C4c), but the laser power and channel count of §C7b subsection 1 grow in proportion.
- **The wet window remains a 1,550 nm problem at any aperture,** because water absorbs there (§C4c). Window heating, water-repellent coatings and wiping matter more for FMCW than for 905 or 940 nm ToF.

#### 10.7 What the model leaves out

- **Small objects.** An object smaller than the footprint intercepts a fraction of the light that falls as $1/R^2$, so its loss grows as $R^{-4}$ (subsection 1; §E12). A narrow coherent beam is filled by smaller objects, but it must hit them (§C10.3a).
- **Background-limited direct detection.** When sunlight dominates, range scales as $A_{\rm rx}^{1/4}$ rather than $A_{\rm rx}^{1/2}$ (subsection 1).
- **Eye safety** caps $E_{\rm tx}$ per direction and per unit time (subsection 5, §C4c). It would appear as a wavelength-dependent vertical limit in Figure C0.10c.
- **Focusing.** Focusing a coherent beam at a set range $R_f$ gives the far-field level $\rho t^2w_0^2/(2R_f^2)$ there, restoring $D^2$ scaling at that range only. A focus at a short range would also restore short-range margin (10.6), but only by giving up the long range: one beam cannot be focused at both at once.
- **Turbulence, misalignment and non-Lambertian targets** lower $\mathcal{L}_{\rm coh}$ further (Frehlich and Kavaya 1991).
- **Weather beyond extinction.** 10.6 treats fog and rain as extinction, plus single-scattering backscatter for fog. It leaves out multiple scattering, snow, spray and splash (subsection 8), and it treats a wet window as a uniform film. Real droplets and smears on a window also scatter light out of the beam at every wavelength and distort the wavefront, which lowers the coherent receiver's mode overlap further.

Sources: https://doi.org/10.1364/AO.5.001588 (Siegman 1966) ; https://doi.org/10.1364/AO.18.001390 (Rye 1979) ; https://doi.org/10.1364/AO.30.005325 (Frehlich and Kavaya 1991) ; https://arxiv.org/pdf/2502.09736 (Piggott et al. 2025) ; https://doi.org/10.1117/12.417512 (Kim, McArthur and Korevaar 2001, fog model and visibility classes) ; https://journals.ametsoc.org/view/journals/atot/21/5/1520-0426_2004_021_0777_atfaoc_2_0_co_2.xml (O'Connor, Illingworth and Hogan 2004, lidar ratio of water clouds) ; https://www.baranidesign.com/faq-articles/2020/1/19/rain-rate-intensity-classification (MANOBS rain-rate classes) ; https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/aviation/aviation-hazards-precipitation (WMO: no agreed international definition of rain intensity)
