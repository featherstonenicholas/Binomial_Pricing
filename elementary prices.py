import numpy as np
#initialise parameters
r0=0.06
u=1.25
d=0.9
T=10
q=0.5
p0=1
#create rate lattice calculation, array for time T
def rate(r0,u,d,T):
  C = r0 * d ** (np.arange(T,-1,-1)) * u ** (np.arange(0,T+1,1)) 
  return C

P=[np.ones(1)] # initialise P_0,0
for i in range(T):
    #add dummy values for top and bottom values
    p=np.hstack([0,P[i],0]) 
    r=np.hstack([0,rate(r0,u,d,i),0])
    #use forward formulae
    P.append(q * p[1:i+3]/(1+r[1:i+3]) + (1-q) * p[0:i+2]/(1+r[0:i+2]))
    

F=100 #face value
c=0.1 #coupon rate
def bond(F,r0,q,u,d,t,T,c):
    c=F*c # initialise coupon payment value
    #initialise final payment array
    F=(F+c)*np.ones(T+1)
    
    for i in np.arange(T,t,-1):
        disc= 1/(1+rate(r0,u,d,i-1))
        F = disc * ( q * F[1:i+1] + (1-q) * F[0:i] )
        F+=c*np.ones(i)
        
    return F
#compare elementary value price to previous lattice price of zero coupon bond
z1=float(bond(F,r0,q,u,d,0,6,0))
z2=100*np.sum(P[6])
print(z1,z2)