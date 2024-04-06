import numpy as np
#initialise parameters
r0=0.06
u=1.25
d=0.9
T=6
q=0.5
type=1 # caplet =1, floorlet =-1
K=0.02 #Strike of caplet/floorlet
#create rate lattice calculation
def rate(r0,u,d,T):
  C = r0 * d ** (np.arange(T,-1,-1)) * u ** (np.arange(0,T+1,1)) 
  return C

#define a discounted expectation of an array
def disc_exp(F,r0,q,u,d):
    #precompute constants
    N=len(F)-1
    
    for i in np.arange(N,0,-1):
        disc= 1/(1+rate(r0,u,d,i-1))
        F = disc * ( q * F[1:i+1] + (1-q) * F[0:i] )
        
    return F

#initialise final payoff array

r=rate(r0,u,d,T-1)
r=np.maximum(0,type*(r-K))/(1+r)
value=disc_exp(r,r0,q,u,d)
print(value)