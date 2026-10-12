import numpy as np
from scipy.optimize import brentq
q=1.602e-19; h=6.62607015e-34; c=2.99792458e8
Eph=h*c/1550e-9; R=200; rho=0.1; A=np.pi*0.0125**2
def snr(npe,M=10,k=0.45,B=250e6,tp=4e-9,iin=2e-12):
    F=k*M+(1-k)*(2-1/M)
    I=npe*q/tp
    shot=np.sqrt(2*q*M**2*F*I*B); th=iin*np.sqrt(B)
    return M*I/np.sqrt(shot**2+th**2), F
for iin in [1.5e-12,2e-12,3e-12]:
  for M in [10,15]:
    n=brentq(lambda x: snr(x,M=M,iin=iin)[0]-7,1,1e5)
    E=n*Eph*np.pi*R**2/(rho*A*0.5*0.8)
    print("iin",iin,"M",M,"F",round(snr(n,M=M)[1],2),"npe",round(n),"E uJ",round(E*1e6,3))
# ToF model background per bin
bg=3e8*20.8e-6*(1-0.29); print("bg events",bg,"per 1ns bin",bg/1333,"shots",20.8/1.3333)
print("5sqrt(bg)",5*np.sqrt(bg),"ratio to 25",5*np.sqrt(bg)/25)
# per-channel budgets at 15 Mpts/s
N=15e6
print("ToF channels (20.8us occupancy)",N*20.8e-6,"rx W",N*60e-9,"per ch mW",N*60e-9/(N*20.8e-6)*1e3,"laser el W",N*0.37e-6,"per ch mW",N*0.37e-6/(N*20.8e-6)*1e3)
print("FMCW channels",190,"rx W",N*0.56e-6,"per ch mW",N*0.56e-6/190*1e3,"laser el W",N*2.0e-6,"per ch mW",N*2e-6/190*1e3,"optical per ch mW",4.5/190*1e3)
print("tof total W",3+N*0.43e-6,"fmcw",3+N*2.56e-6)
