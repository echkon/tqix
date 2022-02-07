"""
>>> this file is a part of tqix: a Toolbox for Quantum in X
                              x: quantum measurement, quantum metrology, 
                                 quantum tomography, and more.
________________________________
>>> copyright (c) 2019 and later
>>> authors: Binho Le
>>> contributors:
>>> all rights reserved
________________________________
"""

#from numpy import
import numpy as np
from tqix.qx import *


__all__ = ['get_Nds','get_dim','get_num_block','get_array_block',
           'get_jmin','get_jarray','get_marray',
           'get_vidx','get_midx','get_jmm1_idx','get_mm1_idx_max'
            ]
        
def get_Nds(d):
    """ to get numper of particle from dimension d
    
    Paramater:
    -------------
    d: dimension
    
    Return:
    -------------
    N: number of particle """
    
    d4 = d*4
    root = np.sqrt(d4)
    if int(root + 0.5)**2 == d4: #perfect quare number
        return int(root - 2)
    else:
        return int(np.sqrt(1+d4)-2)
        
def get_dim(N):
    """ to get dimension from number of particle N
    Paramater:
    -------------
    N: number of particle
    
    Return:
    -------------
    d: dimension """
    
    d = (N/2 + 1)**2 - (N % 2)/4
    return int(d)


def get_num_block(N):
    """ to get number of block
    
    Paramater:
    -------------
    N: number of particle
    
    Return:
    -------------
    Nbj: Number of block j """
    
    return int(N/2 + 1 -1/2*(N % 2))
    
def get_array_block(N):
    # an array of block
    num_block = get_num_block(N)
    array_block = [i * (N+2-i) for i in range(1, num_block+1)]
    return array_block

def get_jmin(N):
    """ to get j min

    Paramater:
    -------------
    N: number of particle

    Return:
    -------------
    jmin: min of j """

    if N % 2 == 0:
        return 0
    else:
        return 0.5
        
def get_jarray(N):
    """ to get array of j from N

    Paramater:
    -------------
    N: number of particle

    Return:
    -------------
    jarray: a array of j"""

    jarray = np.arange(get_jmin(N),N/2 + 1,1)
    return jarray
       
def get_marray(j):
    """ to get array of m from j

    Paramater:
    -------------
    j: number of j

    Return:
    -------------
    marray: a array of j"""

    marray = np.arange(-j,j+1,1)
    return marray
          
def get_vidx(j,m):
    # to get index in vector state from j,m
    return int(j-m)

def get_mm1_idx_max(N):
    # to get mm1 or ik

    ik = {}
    mm1 = {}
    j = N/2

    m_vary = get_marray(j)
    for m in m_vary:
        for m1 in m_vary:
            i, k = j - m, j - m1
            mm1[(i, k)] = (m, m1)
            ik[(m, m1)] = (i, k)
    return [mm1,ik]


def get_midx(N,j,m,m1,block):
    # to get index in density matrix
    # ref. qutip
    k = int(j-m1)
    kp = int(j-m)
    block_num = int(N/2 - j) #0,1,2,...
    offset = 0
    
    if block_num > 0:
        offset = block[block_num - 1]
    i = kp + offset
    k = k + offset
    return (i,k)
    
def get_jmm1_idx(N):
    # get index i,k of density matrix from j,m,m1
    # and revert j,m,m1 from i,k
    # ref. qutip
    
    ik = {}
    jmm1 = {}
    
    block = get_array_block(N)
    j_vary = get_jarray(N)
    for j in j_vary:
        m_vary = get_marray(j)
        for m in m_vary:
            for m1 in m_vary:
                i, k = get_midx(N,j,m,m1,block)
                jmm1[(i, k)] = (j, m, m1)
                ik[(j, m, m1)] = (i, k)
    return [jmm1,ik]