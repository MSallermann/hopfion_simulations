import numpy as np
import matplotlib.pyplot as plt
import matplotlib

#define font family to use for all text
from urllib3 import Retry

matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
                               # 'dejavuserif', 'cm' (Computer Modern), 'stix',
                               # 'stixsans'

def main(data):
    data = np.asarray(data)
    # print(data)

    d  = 1 #AA
    l0 = 3.5 #AA

    gamma_list = np.linspace(0,1)

    def r0_min(gamma, d):
        return np.sqrt( 6.5 * d**2 / (max(gamma, 6.0 * (1.0 - gamma))) )

    # l0_list    = np.linspace(0,1)
    # plt.contourf( gamma_list, l0_list, lhs(gamma_list) - rhs(d,l0_list) )

    l0_approx = 0.5 * l0 * np.sqrt( np.array([ max(g, 6.0 * (1.0 - g)) for g in gamma_list]) )

    # plt.plot( gamma_list, l0_approx, color="r" )

    mask_greater_than_zero = data[:,2] > 1e-5
    plt.fill_between( gamma_list, [r0_min(g, d) for g in gamma_list], 5, color = "royalblue", alpha=0.45 )
    plt.fill_between( gamma_list, 0, [r0_min(g, d) for g in gamma_list], color = "lightsalmon", alpha=0.45 )

    plt.plot( data[mask_greater_than_zero,0], data[mask_greater_than_zero,1],   marker="o", markersize = 6, markeredgewidth = 1.0, mec = "black", markerfacecolor="royalblue", ls="None" )
    plt.plot( data[~mask_greater_than_zero,0], data[~mask_greater_than_zero,1], marker="X", markersize = 7, markeredgewidth = 1.0, mec = "black", markerfacecolor="lightsalmon", ls="None" )
    plt.xlabel(r"$\gamma$")
    plt.ylabel(r"$r_0~[a]$")
    plt.savefig("stability_criterion.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    import calculation_folder
    import glob
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="input_folder", type=str, nargs='?', help='The input folder')

    args = parser.parse_args()

    files = glob.glob( args.input_folder)

    data  = [] # angle > 0
    for f in files:
        calculation = calculation_folder.calculation_folder(f)
        data.append( [ calculation.descriptor["gamma"], calculation.descriptor["l0"], calculation.descriptor["max_angle_between_neighbours"]] )

    main(data)