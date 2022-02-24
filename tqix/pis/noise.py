import numpy as np
from sympy import gamma
from tqix.qx import *
from tqix.pis.util import *
from tqix.pis import *
from scipy.sparse import csc_matrix,lil_matrix

__all__ =['add_noise']

def add_noise(qc,noise=0.3):
    state = qc.state
    d_in = shapex(state)[0]
    N_in = qc.N
    d_dicke = get_dim(N_in)

    if d_in != d_dicke:
        state = lil_matrix(np.pad(state.toarray(),((0,d_dicke-d_in),(0,d_dicke-d_in))))
    new_Nds = get_Nds(shapex(state)[0])

    assert N_in == new_Nds, "not full block"

    non_zero_arrays = state.nonzero()   
    iks = list(zip(non_zero_arrays[0],non_zero_arrays[1]))
    jmm1 = get_jmm1_idx(N_in)[0]
    rho_0 = csc_matrix((d_dicke, d_dicke), dtype=np.complex)
    rho = state
    j_min = get_jmin(N_in)
    j_max = N_in/2

    for ik in iks:
        j,m,m1 = jmm1[ik]
        i,k = ik
        first_term = 0
        second_term = 0
        third_term = 0
        gamma_1 = 0; gamma_2 = 0; gamma_3 = 0; gamma_4 = 0; gamma_5 = 0; gamma_6 = 0
        gamma_7 = 0; gamma_8 = 0; gamma_9 = 0
        p_jmm1 = state[i,k]

        if j >= j_min and j <= j_max and m > -j and m1 > -j and m < j and m1 < j:
            Lambda_a = get_Lambda(N_in,j,type="a")
            gamma_1 = m*m1*Lambda_a*dicke_bx(N_in,{(j,m,m1):1})

        if (j-1) >= j_min and (j-1) <= j_max and (m >= -(j-1) and m1 >= -(j-1)) and (m <= (j-1) and m1 <= (j-1)):
            B_jm_z = get_B(j,m,type="z")
            B_jm1_z = get_B(j,m1,type="z")
            Lambda_b = get_Lambda(N_in,j,type="b")
            gamma_2 = B_jm_z*B_jm1_z*Lambda_b*dicke_bx(N_in,{(j-1,m,m1):1}) 

        if (j+1) <= j_max and (j+1) >= j_min and (m >= -(j+1) and m1 >= -(j+1)) and (m <= (j+1) and m1 <= (j+1)):
            D_jm_z = get_D(j,m,type="z")
            D_jm1_z = get_D(j,m1,type="z")
            Lambda_d = get_Lambda(N_in,j,type="d")
            gamma_3 = D_jm_z*D_jm1_z*Lambda_d*dicke_bx(N_in,{(j+1,m,m1):1})
        
        first_term = (gamma_1+gamma_2+gamma_3)
        
        if j >= j_min and j <= j_max  and (m-1) >= -j and (m1-1) >= -j and (m-1) <= j and (m1-1) <= j:
            A_jm_minus = get_A(j,m,type="-")
            A_jm1_minus = get_A(j,m1,type="-")
            Lambda_a = get_Lambda(N_in,j,type="a")
            gamma_4 = A_jm_minus*A_jm1_minus*Lambda_a*dicke_bx(N_in,{(j,m-1,m1-1):1})
        
        if (j-1) >= j_min and (j-1) <= j_max and (m-1) >= -(j-1) and (m1-1) >= -(j-1) and (m-1) <= (j-1) and  (m1-1) <= (j-1):
            B_jm_minus = get_B(j,m,type="-")
            B_jm1_minus = get_B(j,m1,type="-")
            Lambda_b = get_Lambda(N_in,j,type="b")
            gamma_5 = B_jm_minus*B_jm1_minus*Lambda_b*dicke_bx(N_in,{(j-1,m-1,m1-1):1})
        
        if  (j+1) >= j_min and (j+1) <= j_max and (m-1) >= -(j+1) and (m1-1) >= -(j+1) and (m-1) <= (j+1) and (m1-1)  <= (j+1):
            D_jm_minus = get_D(j,m,type="-")
            D_jm1_minus = get_D(j,m1,type="-")
            Lambda_d = get_Lambda(N_in,j,type="d")
            gamma_6 = D_jm_minus*D_jm1_minus*Lambda_d*dicke_bx(N_in,{(j+1,m-1,m1-1):1})
        
        second_term = (gamma_4+gamma_5+gamma_6)/2
        
        if j >= j_min and j <= j_max and (m+1) <= j and (m1+1) <= j and (m+1) >= -j and (m1+1) >= -j:
            A_jm_plus = get_A(j,m,type="+")
            A_jm1_plus = get_A(j,m1,type="+")
            Lambda_a = get_Lambda(N_in,j,type="a")
            gamma_7 = A_jm_plus*A_jm1_plus*Lambda_a*dicke_bx(N_in,{(j,m+1,m1+1):1})
        
        if (j-1) >= j_min and (j-1) <= j_max and (m+1) >= -(j-1) and (m1+1) >= -(j-1) and (m+1) <= (j-1) and (m1+1) <= (j-1):
            B_jm_plus = get_B(j,m,type="+")
            B_jm1_plus = get_B(j,m1,type="+")
            Lambda_b = get_Lambda(N_in,j,type="b")
            gamma_8 = B_jm_plus*B_jm1_plus*Lambda_b*dicke_bx(N_in,{(j-1,m+1,m1+1):1})
        
        if (j+1) >= j_min and (j+1) <= j_max and  (m+1) >= -(j+1) and (m1+1) >= -(j+1) and (m+1) <= (j+1) and (m1+1) <= (j+1):
            D_jm_plus = get_D(j,m,type="+")
            D_jm1_plus = get_D(j,m1,type="+")
            Lambda_d = get_Lambda(N_in,j,type="d")
            gamma_9 = D_jm_plus*D_jm1_plus*Lambda_d*dicke_bx(N_in,{(j+1,m+1,m1+1):1})

        third_term = (gamma_7+gamma_8+gamma_9)/2

        rho_0 += p_jmm1*(first_term+second_term+third_term)
    normalized_rho_0 = daggx(rho_0).dot(rho_0)/((daggx(rho_0).dot(rho_0)).diagonal().sum())
    new_state = (1-noise)*rho + noise*normalized_rho_0             
    return new_state



        










        




        










        



