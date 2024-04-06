import numpy as np
from numpy.core.fromnumeric import put
#set parameters
K=100
S0=100
r=0.02
T=0.5
N=10
c=0.01
sigma=0.2
u=np.exp(sigma*np.sqrt(T/N))
d=1/u
print(u,d)
#define derivative type
type1=-1 #put(-1) or call(1)
type2="eu" #am or eu


#define function to calculate payoff of option based on type 2
def ameu(x,y,type2):
  if type2=="am":
    return np.maximum(x,y)
  if type2=="eu":
    return y

#create spot price calculation
def spot(S0,u,d,N):
  C = S0 * d ** (np.arange(N,-1,-1)) * u ** (np.arange(0,N+1,1)) 
  return C

# print(binomial_tree_slow(K,T,S0,r,N,u,d,opttype='C'))
def binomial_tree_fast(K,T,S0,r,N,u,d,type1,type2):
    #precompute constants
    dt = T/N
    q = (np.exp((r-c)*dt) - d) / (u-d)
    print(q)
    disc = np.exp(-r*dt)

    # initialise asset prices at maturity - Time step N
    C = spot(S0,u,d,N)

    # initialise option values at maturity
    C = np.maximum( type1*(C - K) , np.zeros(N+1) )

    # step backwards through tree
    for i in np.arange(N,0,-1):
        C = ameu(np.maximum( type1*(spot(S0,u,d,i-1) - K) , np.zeros(i) ),disc * ( q * C[1:i+1] + (1-q) * C[0:i] ),type2)

    return C[0]

print(binomial_tree_fast(K,T,S0,r,N,u,d,type1,type2))