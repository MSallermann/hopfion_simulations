import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gradient_line

#define font family to use for all text
from urllib3 import Retry

matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
                               # 'dejavuserif', 'cm' (Computer Modern), 'stix',
                               # 'stixsans'

def get_norm(my_list, factor=0.25):
    _min = min(my_list)
    _max = max(my_list)
    _span = _max - _min
    norm = matplotlib.colors.Normalize(vmin = _min - factor*_span, vmax = _max + factor*_span)
    return norm

def main(data):
    data = np.asarray(data)

    r0_list = np.unique(data[:,1])
    gamma_list = np.unique(data[:,0])

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

        cmap = matplotlib.cm.get_cmap('Reds')
        norm = get_norm(gamma_list)
        plt.plot(tmp[:,1], tmp[:,2], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)
        # gradient_line.gradient_line(ax=plt.gca(), x=tmp[:,1], y=tmp[:,2], c=tmp[:,0])

    plt.ylabel(r"$\Delta E~[\mathrm{meV}]$")
    plt.xlabel(r"$r_0$")

    plt.legend()
    plt.savefig("e_barrier_vs_r0.png", bbox_inches="tight", dpi=300)

    plt.close()
    # Plot vs gamma
    for r0 in r0_list:
        tmp = data[ data[:,1] == r0 ]
        tmp = tmp[ np.argsort(tmp[:,0]) ]

        label_text = fr"$r_0 = {r0} a$"

        cmap = matplotlib.cm.get_cmap('Blues')
        norm = get_norm(r0_list)
        plt.plot(tmp[:,0], tmp[:,2], color = cmap(norm(r0)), mfc = cmap(norm(r0)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

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