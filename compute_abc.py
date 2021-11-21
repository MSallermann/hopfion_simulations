import numpy as np
SC = 0
FCC = 1
BCC = 2

def ABC(J, lattice):

    if lattice == SC:
        a_s = np.array([1/2, 2, 2, 2])
        b_s = np.array([1/96, 1/24, 1/24, 1/6])
        c_s = np.array([1/48, 1/3, 7/12, 1/3])

    elif lattice == FCC:
        a_s = np.array([2, 2, 12, 8])
        b_s = np.array([1/96, 1/24, 3/16, 1/6])
        c_s = np.array([1/12, 1/12, 3/2, 4/3])

    elif lattice == BCC:
        a_s = np.array([1, 1, 4, 11])
        b_s = np.array([1/192, 1/48, 1/12, 83/192])
        c_s = np.array([7/96, 1/24, 2/3, 197/96])

    A = np.asarray(J).dot(a_s)
    B = np.asarray(J).dot(b_s)
    C = np.asarray(J).dot(c_s)

    return [A, B, C]

if __name__ == "__main__":
    J = [61,-10, 0, -5]
    print(ABC( J , SC))