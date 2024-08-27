import numpy as np

#initialise parameters
r0=0.05
u=1.2
d=0.9
T=10
q=0.5
F=100 #face value
c=0.0 #coupon rate
R=0.2 #recovery rate
a=0.01 #parameters for hazard rates
b=1.01

#create rate lattice calculation
def rate(r0,u,d,T):
  C = r0 * d ** (np.arange(T,-1,-1)) * u ** (np.arange(0,T+1,1)) 
  return C
#add in hazard rate calculations. For non defaultable, set a=0

def hazard(a,b,T):
    h=a*b**(np.arange(0,T+1,1)-T/2)
    return h

#pricing a bond following lattice term structure for risk free rate


def bond(F,r0,q,u,d,a,b,R,t,T,c):
    c=F*c # initialise coupon payment value
    rec=R*F
    #initialise final payment array
    F=(F+c)*np.ones(T+1)
    
    for i in np.arange(T,t,-1):
        disc= 1/(1+rate(r0,u,d,i-1))
        F = disc * ( (1-hazard(a,b,i-1)) *(q* F[1:i+1] + (1-q) * F[0:i] )+hazard(a,b,i-1)*rec)
        F+=c*np.ones(i)
        
    return F



#find forward price of a coupon bearing bond

Z_4=bond(F,r0,q,u,d,a,b,R,4,T,c)-(F*c)*np.ones(len(bond(F,r0,q,u,d,a,b,R,4,T,c))) #value of a 2 year bond at t=4

#define a discounted expectation of an array
def disc_exp(F,r0,q,u,d):
    #precompute constants
    N=len(F)-1
    
    for i in np.arange(N,0,-1):
        disc= 1/(1+rate(r0,u,d,i-1))
        F = disc * ( q * F[1:i+1] + (1-q) * F[0:i] )
        
    return F
#forward price of a 2 year coupon paying bond at t=4
forward=100*disc_exp(Z_4,r0,q,u,d)/bond(F,r0,q,u,d,a,b,R,0,4,0)
print(forward)

#define non discounted exp
def undisc_exp(F,q,u,d):
  #precompute constants
  N=len(F)-1
  
  for i in np.arange(N,0,-1):
      
      F =  ( q * F[1:i+1] + (1-q) * F[0:i] )
  return F

#future price of above contract
future=undisc_exp(Z_4,q,u,d)
print(future)
