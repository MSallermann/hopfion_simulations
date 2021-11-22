import numpy as np
SC = 0
FCC = 1
BCC = 2

def ABC(J, lattice, lattice_constant=1):

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

    return mat.dot(J), mat # returns [A,B,C]


def get_degenerate_jij(J_old, lattice, lattice_constant, lam):
    ABC_old, mat = ABC(J_old, lattice, lattice_constant)

    bigger_mat = np.zeros( shape=(4,4) )
    bigger_mat[:3,:4] = mat
    bigger_mat[3,1] = lam
    J_new = np.linalg.inv(bigger_mat).dot( [*ABC_old,1] )

    ABC_new = ABC(J_new, lattice, lattice_constant)[0]

    print(ABC_old)
    print(ABC_new)

    assert( np.isclose(ABC_old, ABC_new).all() )
    return J_new


if __name__ == "__main__":
    J_old = [61,-10, 0, -5]
    ABC_old, mat = ABC( J_old, SC)

    J_new = get_degenerate_jij(J_old, SC, 1, -0.1)
    print(J_new)
    exit() 

    J1_list = []
    J2_list = []
    J3_list = []
    J4_list = []
    lam_list = np.linspace(-1,1,500)

    for lam in lam_list:
        J_new = get_degenerate_jij(J_old, SC, 1, lam)

        J1_list.append(J_new[0])
        J2_list.append(J_new[1])
        J3_list.append(J_new[2])
        J4_list.append(J_new[3])

        print(ABC(J_new, SC)[0])
        print(J_new)
        print("---")

    J1_list = np.array(J1_list)
    J2_list = np.array(J2_list)
    J3_list = np.array(J3_list)
    J4_list = np.array(J4_list)

    import matplotlib.pyplot as plt

    plt.plot(lam_list, J1_list, label="J1")
    plt.plot(lam_list, J2_list, label="J2")
    plt.plot(lam_list, J3_list, label="J3")
    plt.plot(lam_list, J4_list, label="J4")

    plt.legend()
    plt.xlabel(r"$\lambda$")
    plt.savefig("J.png", dpi=300)

    plt.close()
    plt.plot(lam_list, J2_list/J1_list, label="J2/J1" )
    plt.plot(lam_list, J3_list/J1_list, label="J3/J1" )
    plt.plot(lam_list, J4_list/J1_list, label="J4/J1" )
    plt.legend()
    plt.xlabel(r"$\lambda$")
    plt.savefig("J_ratio.png", dpi=300)