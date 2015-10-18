import scipy
R_w = 0.6 # W/mk
R_f = 0.003 # W/mk
r = 0.2 # m
T_0 = 70 # C
T_a = 20 # C
dx = 0.001 # ft
L = 80 # ft

def heat_balance(T_1,T_2):
   heat_in = (T_1-T_2) * scipy.pi * r**2 * R_w
   heat_out = ( (T_1 + T_2) / 2 - T_a ) * 2 * r * scipy.pi * dx * R_f 
   return abs(heat_in-heat_out)

T = [T_0]
X = [0]

import numpy as np
from scipy.optimize import minimize
for x in np.arange(dx,L,dx):   
  X.append(x)
  fun = lambda s: heat_balance(T[-1],s)
  T.append(float(minimize(fun,T[-1]-dx,method="SLSQP")['x']))

from matplotlib import pyplot as plt
plt.plot(X,T)
plt.show()
