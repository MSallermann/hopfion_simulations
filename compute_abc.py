import numpy as np
SC = 0
FCC = 1
BCC = 2

def ABC_Matrix(lattice, lattice_constant=1):

    if lattice == SC:
        a_s = 1/lattice_constant * np.array([1/2, 2, 2, 2])
        b_s = -lattice_constant * np.array([1/96, 1/24, 1/24, 1/6])
        c_s = -lattice_constant * np.array([1/48, 1/3, 7/12, 1/3])
        mat = np.array( [a_s,b_s,c_s] )

    elif lattice == FCC:
        a_s = 1/lattice_constant * np.array([2, 2, 12, 8])
        b_s = -lattice_constant * np.array([1/96, 1/24, 3/16, 1/6])
        c_s = -lattice_constant * np.array([1/12, 1/12, 3/2, 4/3])
        mat = np.array( [a_s,b_s,c_s] )


    elif lattice == BCC:
        a_s = 1/lattice_constant * np.array([1, 1, 4, 11])
        b_s = -lattice_constant * np.array([1/192, 1/48, 1/12, 83/192])
        c_s = -lattice_constant * np.array([7/96, 1/24, 2/3, 197/96])
        mat = np.array( [a_s,b_s,c_s] )

    return mat # returns [A,B,C]

def ABC(J):
    matrix = ABC_Matrix(lattice=SC, lattice_constant=1)
    return matrix.dot(J)

def get_l0(A,B,C):
    return np.sqrt((B+C)/A)

def get_E0(A,B,C):
    return np.sqrt(A * (B + C))

def get_gamma(A,B,C):
    return C/(C+B)

def ABC_from_reduced(E0, l0, gamma):
    A = E0 / l0
    B = E0*l0 * (1 - gamma)
    C = E0*l0 * gamma
    return [A,B,C]

def J_from_reduced(E0, l0, gamma, lam):
    [A,B,C] = ABC_from_reduced(E0, l0, gamma)
    J = invert_ABC([A, B, C], lattice=SC, lattice_constant=1, lam=lam)
    return J

def invert_ABC(ABC):
    """ Invert by fixing J1 to 1"""

    M_matrix = ABC_Matrix(lattice=SC, lattice_constant=1)
    first_column = M_matrix[:,0]
    sub_matrix   = M_matrix[:,1:]

    J = np.linalg.inv(sub_matrix).dot( np.asarray(ABC) - first_column )
    return np.array([1, *J])

def J_from_reduced(E0, l0, gamma):
    ABC = ABC_from_reduced(E0, l0, gamma)
    return invert_ABC(ABC)

if __name__ == "__main__":

    J = [1, -0.25, 0.0004, -0.0001] # B = 0
    matrix = ABC_Matrix( lattice=SC, lattice_constant=1 )
    ABC = matrix.dot(J)
    J_new = invert_ABC(ABC)
    print( f"E0 = {get_E0(*ABC)}" )
    print(f"J = {J}")
    print(f"ABC = {ABC}")
    print(f"J_new = {J_new}")

    J = [1, 0.3, 0.246, -0.793] # C = 0
    matrix = ABC_Matrix( lattice=SC, lattice_constant=1 )
    ABC = matrix.dot(J)
    J_new = invert_ABC(ABC)
    print( f"E0 = {get_E0(*ABC)}" )
    print(f"J = {J}")
    print(f"ABC = {ABC}")
    print(f"J_new = {J_new}")

    J = [1, 0.2, -0.273, -0.174] # C = 6B
    matrix = ABC_Matrix( lattice=SC, lattice_constant=1 )
    ABC = matrix.dot(J)
    J_new = invert_ABC(ABC)
    print( f"E0 = {get_E0(*ABC)}" )
    print(f"J = {J}")
    print(f"ABC = {ABC}")
    print(f"J_new = {J_new}")

    # ABC_old, mat = ABC( J_old, SC)
    # A_old, B_old, C_old = ABC_old

    # J_iso = get_isotropic_solutions(A_old, B_old, lam=1)
    # J_B0  = get_B0_solutions(A_old, 0.5*C_old, lam=1)
    # J_C0  = get_C0_solutions(A_old, 3*B_old, lam=1)

    # ABC_iso = ABC(J_iso, SC)[0]
    # ABC_B0  = ABC(J_B0, SC)[0]
    # ABC_C0  = ABC(J_C0, SC)[0]

    # print( "ABC_old", ABC_old )
    # print( "ABC_iso", ABC_iso )
    # print( "ABC_B0", ABC_B0 )
    # print( "ABC_C0", ABC_C0 )
    # print("---")
    # print("J_iso", J_iso)
    # print("J_B0",  J_B0)
    # print("J_C0",  J_C0)

    # print( ABC_iso[2], ABC_iso[1] * 6)


    # J = [61,-10, 0, -5]

    # [A,B,C] = ABC(J, SC)[0]

    # A_new = 0.5
    # B_new = A * B / A_new
    # C_new = A * C / A_new
    # ABC_new = [A_new, B_new, C_new]

    # J_new = invert_ABC(ABC_new, SC, lattice_constant = 1, lam = -1)
    # print("A,B,C = ", A,B,C)
    # print("A,B,C_new = ", *ABC_new)
    # print("J_new = ", J_new)
    # print( max(C_new, 6*B_new), 6.5*A_new )
    # print( max(C, 6*B), 6.5*A )

    # print(f"E0 = {get_E0(A,B,C)} meV")
    # print(f"l0 = {get_l0(A,B,C)} AA")
    # print(f"gamma = {get_gamma(A,B,C)}")

    # for i in range(8):
    #     gamma   = float(i)/7.0
    #     l0      = 3 # AA
    #     E0      = 1 # meV
    #     J       = J_from_reduced(E0, l0, gamma, lam=1)
    #     [A,B,C] = ABC_from_reduced(E0, l0, gamma)
    #     print(J)
    #     print(A, B, C)

    # J = [1, 0.2, -0.273, -0.174] # C = 6B
    # [A,B,C] = ABC(J, SC)[0]
    # print(A,B,C)

    # [A,B,C] = ABC(J, SC)[0]
    # print(A,B,C)

    # exit()

    # J_old = [61, -10, 0, -5]

    # J_new = get_degenerate_jij(J_old, SC, 1, 0.04)
    # print(J_new)

    # J1_list = []
    # J2_list = []
    # J3_list = []
    # J4_list = []
    # lam_list = np.linspace(-1,1,500)

    # for lam in lam_list:
    #     J_new = get_degenerate_jij(J_old, SC, 1, lam)

    #     J1_list.append(J_new[0])
    #     J2_list.append(J_new[1])
    #     J3_list.append(J_new[2])
    #     J4_list.append(J_new[3])
    #     print(lam)
    #     print(ABC(J_new, SC)[0])
    #     print(J_new)
    #     print("---")



    # J1_list = np.array(J1_list)
    # J2_list = np.array(J2_list)
    # J3_list = np.array(J3_list)
    # J4_list = np.array(J4_list)

    # import matplotlib.pyplot as plt

    # plt.plot(lam_list, J1_list, label="J1")
    # plt.plot(lam_list, J2_list, label="J2")
    # plt.plot(lam_list, J3_list, label="J3")
    # plt.plot(lam_list, J4_list, label="J4")

    # plt.legend()
    # plt.xlabel(r"$\lambda$")
    # plt.savefig("J.png", dpi=300)

    # plt.close()
    # plt.plot(lam_list, J2_list/J1_list, label="J2/J1" )
    # plt.plot(lam_list, J3_list/J1_list, label="J3/J1" )
    # plt.plot(lam_list, J4_list/J1_list, label="J4/J1" )
    # plt.legend()
    # plt.xlabel(r"$\lambda$")
    # plt.savefig("J_ratio.png", dpi=300)