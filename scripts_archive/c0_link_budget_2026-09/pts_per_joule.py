import numpy as np
h=6.62607015e-34; c=2.99792458e8
R=200.0; rho=0.1
Eph=lambda lam: h*c/lam
def amode(R,D=20e-3,lam=1550e-9):
    w0=0.45*D; t=1-np.exp(-2*(0.5/0.45)**2); zr=np.pi*w0**2/lam
    w=w0*np.sqrt(1+(R/zr)**2); return t**2*lam**2*R**2/(2*np.pi*w**2), w, t
# ToF central 2026
A_tof=np.pi*(12.5e-3)**2; eta_tof=0.5*0.37; n_tof=25
E_tof=n_tof*Eph(940e-9)*np.pi*R**2/(rho*A_tof*eta_tof)
Am,w,t=amode(R); eta_f=0.25; n_f=30
E_f=n_f*Eph(1550e-9)*np.pi*R**2/(rho*Am*eta_f)
print("A_tof mm2",A_tof*1e6,"eta_tof",eta_tof,"E_tof nJ",E_tof*1e9)
print("A_mode mm2",Am*1e6,"w mm",w*1e3,"t",t,"t^2",t**2,"E_f uJ",E_f*1e6)
print("ratio",E_f/E_tof)
fa=A_tof/Am; fn=n_f/n_tof; fe=Eph(1550e-9)/Eph(940e-9); fh=eta_tof/eta_f
print("factors area",fa,"n",fn,"Eph",fe,"eta",fh,"prod",fa*fn*fe*fh)
print("geom 20mm",np.pi*0.01**2*1e6,"geom/Amode",np.pi*0.01**2/Am,"aperture 25/20 sq",(25/20)**2)
# max A_mode collimated
Amax=t**2*1550e-9*R/4; w0opt=np.sqrt(1550e-9*R/np.pi)
print("Amax mm2",Amax*1e6,"w0opt mm",w0opt*1e3,"Dopt mm",w0opt/0.45*1e3)
for D in [10e-3,20e-3,25e-3,40e-3,80e-3]:
    print(" D",D*1e3,"A_mode mm2",amode(R,D)[0]*1e6)
# coverage and full-cell
th=np.deg2rad(0.05); Acell=(th*R)**2; Aspot=np.pi*w**2
print("Acell m2",Acell,"Aspot m2",Aspot,"coverage",Aspot/Acell,"tiles",Acell/Aspot)
Am_full=t**2*(1550e-9)**2*R**2/(2*Acell)
print("A_mode full mm2",Am_full*1e6,"lam2/Omega mm2",(1550e-9)**2/th**2*1e6, "diam of 3.15",2*np.sqrt(3.15/np.pi),"diam 1.32",2*np.sqrt(Am_full*1e6/np.pi))
E_full=E_f*Am/Am_full
print("E_full uJ",E_full*1e6,"ratio to tof",E_full/E_tof)
# points per joule
for name,E in [("tof",E_tof),("fmcw",E_f),("fmcw0.15",0.15e-6),("fmcw_full",E_full)]:
    print(name,"pts/J",1/E)
# 1550 linear APD ToF illustrative
i_n=2e-12*np.sqrt(250e6); M=10; QE=0.8; q=1.602e-19; tp=4e-9; SNR=7
Nph=SNR*i_n*tp/(QE*q*M)
E_apd=Nph*Eph(1550e-9)*np.pi*R**2/(rho*A_tof*0.5)
print("i_n nA",i_n*1e9,"N_ph at detector",Nph,"E_apd uJ",E_apd*1e6,"ratio tof",E_apd/E_tof,"spad photons at det",n_tof/0.37)
# sunlight into coherent mode
Esun=0.25 # W/m2/nm at 1550 approx
L=rho*Esun/np.pi; dl=(1550e-9)**2*1e9/c*1e9 # nm
P=L*(1550e-9)**2*dl*0.5
print("coherent sun: dlambda nm",dl,"P W",P,"ph/s",P/Eph(1550e-9),"in 10us",P/Eph(1550e-9)*10e-6)
# direct detection background
B=3e8
print("bg per 1ns bin single shot",B*1e-9,"100 shots",B*1e-9*100,"CW 10us",B*10e-6,"5sqrt",5*np.sqrt(B*10e-6))
# channel counts
tau=2*R/c; Nd=15e6
for Eo,Pc in [(0.30e-6,30e-3),(0.30e-6,16e-3),(0.15e-6,30e-3),(0.15e-6,15e-3)]:
    Popt=Eo*Nd; print("Eo",Eo,"Pc",Pc,"Popt W",Popt,"Popt/Pc",Popt/Pc,"2tauN",2*tau*Nd,"Nch",Popt/Pc+2*tau*Nd)
print("tof Popt W",E_tof*Nd,"tof min listening pixels",tau*Nd)
# coherence cap
for Pc in [30e-3,16e-3]:
    print("Pc",Pc,"per ramp nJ",Pc/(2*100e3)*1e9,"per pair nJ",2*Pc/(2*100e3)*1e9)
# range scaling
print("E_tof at 10 m nJ",E_tof*(10/200)**2*1e9,"factor",(200/10)**2)
