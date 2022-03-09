import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gradient_line

#define font family to use for all text
from urllib3 import Retry

matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
                               # 'dejavuserif', 'cm' (Computer Modern), 'stix',
                               # 'stixsans'

def main(data):
    data = np.asarray(data)

    # Plot vs r0
    for i in range(8):
        g = i/7.0
        tmp = data[ data[:,0] == g ]
        tmp = tmp[ np.argsort(tmp[:,1]) ]

        if i==0:
            label_text = fr"$\gamma = 0$"
        elif i==7:
            label_text = fr"$\gamma = 1$"
        else:
            label_text = fr"$\gamma = {i:.0f}\,/\,7$"

        plt.plot(tmp[:,1], tmp[:,2], marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)
        # gradient_line.gradient_line(ax=plt.gca(), x=tmp[:,1], y=tmp[:,2], c=tmp[:,0])

    plt.ylabel(r"$\Delta E~[\mathrm{meV}]$")
    plt.xlabel(r"$r_0$")

    plt.legend()
    plt.savefig("e_barrier_vs_r0.png", bbox_inches="tight", dpi=300)

    plt.close()
    r0_list= np.unique(data[:,1])
    # Plot vs gamma
    for r0 in r0_list:
        tmp = data[ data[:,1] == r0 ]
        tmp = tmp[ np.argsort(tmp[:,0]) ]

        label_text = fr"$r_0 = {r0} a$"

        plt.plot(tmp[:,0], tmp[:,2], marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

    plt.ylabel(r"$\Delta E~[\mathrm{meV}]$")
    plt.xlabel(r"$\gamma$")
    plt.gca().set_xticks( [i/7.0 for i in range(8)] )

    xtick_labels = [ f"{i}/7" for i in range(8)]
    xtick_labels[0]  = "0"
    xtick_labels[-1] = "1"

    plt.gca().set_xticks( [ i/7.0 for i in range(8)] )
    plt.gca().set_xticklabels( xtick_labels )

    plt.legend()
    plt.savefig("e_barrier_vs_gamma.png", bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    import calculation_folder
    import glob
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    data  = [] # angle > 0
    for f in args.paths:
        print(f)
        calculation = calculation_folder.calculation_folder(f)
        data.append( [ calculation.descriptor["gamma"], calculation.descriptor["l0"], calculation.descriptor["energy_barrier"]] )

    main(data)