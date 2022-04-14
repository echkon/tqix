from tqix.pis import *
from tqix import *
import numpy as np
from matplotlib import pyplot as plt
import time 
N=100
angles = np.linspace(0,0.1,30).tolist()
# OAT
noise = 0.05
def find_mean_xi_s(noise):
      OAT_xi_2_S = []
      min_xi_s = np.inf 
      min_theta = None
      for theta in angles:
            qc = circuit(N)
            qc.RN(np.pi/2,0)
            start = time.time()
            qc.OAT(theta,"Z",noise=0.05,num_processes=25)
            end = time.time()-start 
            print("time:",end)
            xi_2_s = np.real(get_xi_2_S(qc))
            if xi_2_s < min_xi_s:
                  min_xi_s = xi_2_s
                  min_theta = theta
            elif xi_2_s > min_xi_s:
                  break 

      print("noise,xi_2_s,theta:",noise,min_xi_s,min_theta)

find_mean_xi_s(0.05)
find_mean_xi_s(0.1)
find_mean_xi_s(0.15)
find_mean_xi_s(0.2)

