import scipy
R_w = 0.024# W/mk
R_f = 0.042 # W/mk
r = 0.2 # m
T_0 = 61 # C
T_a = 20 # C
dx = 0.0001 # m
L = 25 # m

def heat_balance(T_1,T_2):
   heat_in = (T_1-T_2) * scipy.pi * r**2 * R_w
   heat_out = ( (T_1 + T_2) / 2 - T_a ) * 2 * r * scipy.pi * dx * R_f 
   return abs(heat_in-heat_out)

def sim():
   T = [T_0]
   X = [0]
   print 'r is ',R_f
   import numpy as np
   from scipy.optimize import minimize
   for x in np.arange(dx,L,dx):   
     X.append(x)
     fun = lambda s: heat_balance(T[-1],s)
     T.append(float(minimize(fun,T[-1]-dx,method="SLSQP")['x']))
   return([T,X])

from matplotlib import pyplot as plt
typs = ['+','x','|','_','*']
#typs = ['D','s','8','p','^']
cols = ['red','blue','black','purple','brown']

for i, rf in enumerate([7,14,50,100,200]):
    R_f = 1.0/rf
    ans = sim()
    plt.scatter(ans[1],ans[0],c=cols[i],marker=typs[i],s = 100,label=rf,lw=3) 
#plt.plot(X,T)
plt.legend(fontsize=20,title='Pipe Insolation R Value')
plt.xlabel('Distance (m)',fontsize=20)
plt.ylabel('Average Temperature (C)',fontsize=20)
plt.show()

