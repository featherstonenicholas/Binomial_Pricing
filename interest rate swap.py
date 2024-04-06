import numpy as np
#initialise parameters
r0=0.06
u=1.25
d=0.9
T=6
q=0.5
K=0.05 #fixed swap value
#create rate lattice calculation
def rate(r0,u,d,T):
  C = r0 * d ** (np.arange(T,-1,-1)) * u ** (np.arange(0,T+1,1)) 
  return C

#define a discounted expectation of a swap
def disc_swap(r,r0,q,u,d,K):
    #precompute constants
    N=len(r)-1
    
    for i in np.arange(N,0,-1):
        disc= 1/(1+rate(r0,u,d,i-1))
        r = disc * ( rate(r0,u,d,i-1)-K+q * r[1:i+1] + (1-q) * r[0:i] )
        
    return r

#initialise final payoff array

r=rate(r0,u,d,T-1)
r=(r-K)/(1+r)
print(r)
print(disc_swap(r,r0,q,u,d,K))

