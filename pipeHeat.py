import numpy as np
import scipy
from scipy.optimize import minimize
from matplotlib import pyplot as plt
typs = ['+','x','|','_','*']
cols = ['red','blue','black','purple','brown']
class pipeSimulator:
   R_w = 0.654# W/mk water heat loss ocefficient
   # R_w = 0.028# W/mk air heat loss ocefficient
   R_f = 0.042 # W/mk pipe heat loss coefficient
   r = 0.2 # m pipe radius
   T_0 = 50 # C initial temperature
   T_a = 20 # C ambiant temperature
   dx = 0.01 # m differential distance
   L = 25 # m length of pipe

   def heat_balance(self,T_1,T_2):
      heat_in = (T_1-T_2) * scipy.pi * self.r**2 * self.R_w
      heat_out = ( (T_1 + T_2) / 2 - self.T_a ) * 2 * self.r * scipy.pi * self.dx * self.R_f 
      return abs(heat_in-heat_out)

   def simulation(self):
      T = [self.T_0]
      X = [0]
      print 'r is ',self.R_f
      for x in np.arange(self.dx,self.L,self.dx):   
        X.append(x)
        fun = lambda s: self.heat_balance(T[-1],s)
        T.append(float(minimize(fun,T[-1]-self.dx,method="SLSQP")['x']))
      return([T,X])
   
pipe = pipeSimulator()
for i, rf in enumerate([7,14,50,100,200]):
    pipe.R_f = 1.0/rf
    ans = pipe.simulation()
    plt.scatter(ans[1],ans[0],c=cols[i],marker=typs[i],s = 10,label=rf,lw=3) 

plt.legend(fontsize=20,title='Pipe Insolation R Value')
plt.xlabel('Distance (m)',fontsize=20)
plt.ylabel('Average Temperature (C)',fontsize=20)
plt.show()

