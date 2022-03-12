from tqix.pis.util import *
from tqix.pis import *
import numpy as np 

__all__ = ['get_xi_2_H','get_xi_2_S','get_xi_2_R','get_xi_2_D','get_xi_2_E']

def get_xi_2_H(alpha,gamma,qc):
    var_alpha = qc.var(alpha)
    mean_gamma = qc.expval(gamma)
    return (2*var_alpha)/np.abs(mean_gamma) 

def get_xi_2_S(qc):
    N = qc.N
    mean_Jx2_Jy2 = qc.expval(type="x2y2")
    mean_J_2_minus = qc.expval(type="-2")
    return 2/N*(mean_Jx2_Jy2-np.abs(mean_J_2_minus))

def get_xi_2_R(qc):
    xi_2_S = get_xi_2_S(qc)
    N = qc.N
    mean_Jz = qc.expval(type="z")
    return (N**2/(4*np.abs(mean_Jz)**2))*xi_2_S

def get_xi_2_D(qc,n):
    var = qc.var(type="xyz",use_vector=True,n=n)
    mean = qc.expval(type="xyz",use_vector=True,n=n)
    N = qc.N
    return (N*var)/(N**2/4-mean**2)

def get_xi_2_E(qc,n):
    var_Jvec = qc.var(type="xyz",use_vector=True,n=n)
    mean_Jvec = qc.expval(type="xyz",use_vector=True,n=n)
    N = qc.N
    mean_J_2 = qc.expval(type="J2")
    return (N*var_Jvec)/(mean_J_2-N/2-mean_Jvec)

