import numpy as np

# Initialise parameters
S0 = 4     # initial stock price
K = 5     # strike price
T = 1         # time to maturity in years
r = 0.25      # annual risk-free rate
N = 3        # number of time steps
u = 2       # up-factor in binomial models
d = 1/u       # ensure recombining tree
    
# define function to zipper merge 2 arrays
def zipmerge(a,b):
    return np.stack([a,b], axis=-1).flatten()

# create function to generate array of all outcomes
def maxtodate(S0,u,d,n):
    S=np.array([S0])
    maxtodate=np.array([S0])
    for i in range(n):
        S=np.array(zipmerge(d*S,u*S))
        maxtodate=np.maximum(np.array(zipmerge(maxtodate,maxtodate)),S)
    return maxtodate
#create function for full list of S at time n
def end_S(S0,u,d,n):
    S=np.array([S0])
    for i in range(n):
        S=np.array(zipmerge(d*S,u*S))
    return S
#function to unzipper
def unzipper(S):
    S = S.reshape(-1,2)
    return S[:,0], S[:,1]

   
# print(binomial_tree_slow(K,T,S0,r,N,u,d,opttype='C'))
def binomial_tree_fast(K,T,S0,r,N,u,d,opttype='C'):
    #precompute constants
    dt = T/N
    #q = (np.exp(r*dt) - d) / (u-d)
    #disc = np.exp(-r*dt)
    q = (1 + r - d) / (u-d)
    disc = 1/(1+r)
    # initialise asset prices at maturity - Time step N
    C = np.array(maxtodate(S0,u,d,N))
    
    # initialise option values at maturity
    C = C - np.array(end_S(S0,u,d,N) )
    
    # step backwards through tree
    for i in np.arange(N,0,-1):
        C_low , C_high = unzipper(C)
        C = disc * ( q * C_high + (1-q) * C_low )
        

    return C[0]
C=binomial_tree_fast(K,T,S0,r,N,u,d,opttype='C')

print(C)


