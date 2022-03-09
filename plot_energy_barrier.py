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

    for i in range(8):
        g = i/7.0
        tmp = data[ data[:,0] == g ]
        tmp = tmp[ np.argsort(tmp[:,1]) ]

        if i==0:
            label_text = fr"$\gamma = 0$"
        elif i==7:
            label_text = fr"$\gamma = 1$"
        else:
            label_text = fr"$\gamma = {i:.0f}/7$"

        plt.plot(tmp[:,1], tmp[:,2], marker="o", markersize = 6, markeredgewidth = 1.0, mec = "black", label = label_text)

    plt.ylabel(r"$\Delta E~[\mathrm{meV}]$")
    plt.xlabel(r"$r_0$")

    plt.legend()
    plt.savefig("e_barrier.png")

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