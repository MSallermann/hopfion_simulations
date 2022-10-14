import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gradient_line

#define font family to use for all text
from urllib3 import Retry

matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
                               # 'dejavuserif', 'cm' (Computer Modern), 'stix',
                               # 'stixsans'

def get_norm(my_list, factor=0.5):
    _min = min(my_list)
    _max = max(my_list)
    _span = _max - _min
    norm = matplotlib.colors.Normalize(vmin = _min - factor*_span, vmax = _max + factor*_span)
    return norm

def main(data, ratio):
    if ratio:
        ylabel = r"$\Delta E~/~E_0$"
        name_prefix = "e_barrier_ratio"
    else:
        ylabel = r"$\Delta E~[\mathrm{meV}]$"
        name_prefix = "e_barrier"

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

    plt.ylabel(ylabel)
    plt.xlabel(r"$r_0~[a]$")

    plt.legend()
    plt.savefig(f"{name_prefix}_vs_r0.png", bbox_inches="tight", dpi=300)
    plt.show()
    plt.close()

    # Plot vs gamma
    for r0 in r0_list:
        tmp = data[ data[:,1] == r0 ]
        tmp = tmp[ np.argsort(tmp[:,0]) ]

        label_text = fr"$r_0 = {r0} a$"

        cmap = matplotlib.cm.get_cmap('Blues')
        norm = get_norm(r0_list)
        plt.plot(tmp[:,0], tmp[:,2], color = cmap(norm(r0)), mfc = cmap(norm(r0)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

    plt.ylabel(ylabel)
    plt.xlabel(r"$\gamma$")
    plt.gca().set_xticks( [i/7.0 for i in range(8)] )

    xtick_labels = [ f"{i}/7" for i in range(8)]
    xtick_labels[0]  = "0"
    xtick_labels[-1] = "1"

    plt.gca().set_xticks( [ i/7.0 for i in range(8)] )
    plt.gca().set_xticklabels( xtick_labels )

    plt.legend()
    plt.savefig(f"{name_prefix}_vs_gamma.png", bbox_inches="tight", dpi=300)
    plt.show()
    plt.close()

    # Plot vs angle
    for i in range(8):
        g = i/7.0
        tmp = data[ data[:,0] == g ]
        tmp = tmp[ np.argsort(tmp[:,3]) ] # Sort by angle

        if i==0:
            label_text = fr"$\gamma = 0$"
        elif i==7:
            label_text = fr"$\gamma = 1$"
        else:
            label_text = fr"$\gamma = {i:.0f}\,/\,7$"

        cmap = matplotlib.cm.get_cmap('Greens')
        norm = get_norm(gamma_list)
        plt.plot(tmp[:,3] / np.pi, tmp[:,2], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

    plt.gca().set_xticks( [0.25, 0.5] )
    plt.gca().set_xticklabels( [r"$\pi/4$", r"$3\pi/2$"] )
    plt.ylabel(ylabel)
    plt.xlabel(r"$\max( \angle (\mathbf{s}_i, \mathbf{s}_j) )$")
    plt.legend()
    plt.savefig(f"{name_prefix}_vs_angle.png", bbox_inches="tight", dpi=300)
    plt.close()

    # Plot vs criterion fulfilledness
    for i in range(8):
        g = i/7.0
        tmp = data[ data[:,0] == g ]
        tmp = tmp[ np.argsort(tmp[:,4]) ] # Sort by criterion

        if i==0:
            label_text = fr"$\gamma = 0$"
        elif i==7:
            label_text = fr"$\gamma = 1$"
        else:
            label_text = fr"$\gamma = {i:.0f}\,/\,7$"

        cmap = matplotlib.cm.get_cmap('Greens')
        norm = get_norm(gamma_list)
        plt.plot(tmp[:,4], tmp[:,2], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

    # plt.gca().set_xticks( [0.25, 0.5] )
    # plt.gca().set_xticklabels( [r"$\pi/4$", r"$3\pi/2$"] )
    plt.ylabel(ylabel)
    plt.xlabel(r"criterion")
    plt.legend()
    plt.savefig(f"{name_prefix}_vs_criterion.png", bbox_inches="tight", dpi=300)
    plt.close()

    # plt.legend()
    # plt.savefig("e_barrier_vs_r0.png", bbox_inches="tight", dpi=300)

    # plt.close()

    # # Plot vs max_angle
    # for r0 in r0_list:
    #     tmp = data[ np.argsort(data[:,3])]
    #     plt.plot(tmp[:,3], tmp[:,2])
    #     plt.show()
    #     tmp = data[ data[:,1] == r0 ]
    #     tmp = tmp[ np.argsort(tmp[:,0]) ]

    #     label_text = fr"$r_0 = {r0} a$"

    #     cmap = matplotlib.cm.get_cmap('Blues')
    #     norm = get_norm(r0_list)
    #     plt.plot(tmp[:,0], tmp[:,2], color = cmap(norm(r0)), mfc = cmap(norm(r0)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

    # plt.ylabel(r"$\Delta E~[\mathrm{meV}]$")
    # plt.xlabel(r"$\gamma$")
    # plt.gca().set_xticks( [i/7.0 for i in range(8)] )

    # xtick_labels = [ f"{i}/7" for i in range(8)]
    # xtick_labels[0]  = "0"
    # xtick_labels[-1] = "1"

    # plt.gca().set_xticks( [ i/7.0 for i in range(8)] )
    # plt.gca().set_xticklabels( xtick_labels )

    # plt.legend()

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

        if calculation.descriptor["max_angle_between_neighbours"] < 1e-3:
            continue

        data.append( [ calculation.descriptor["gamma"], calculation.descriptor["l0"], calculation.descriptor["energy_barrier_divided_by_E0"], calculation.descriptor["max_angle_between_neighbours"],  calculation.descriptor["criterion_fulfilledness"]  ] )
    main(data, ratio=True)

    data  = [] # angle > 0
    for f in args.paths:
        print(f)
        calculation = calculation_folder.calculation_folder(f)

        if calculation.descriptor["max_angle_between_neighbours"] < 1e-3:
            continue

        data.append( [ calculation.descriptor["gamma"], calculation.descriptor["l0"], calculation.descriptor["energy_barrier"], calculation.descriptor["max_angle_between_neighbours"], calculation.descriptor["criterion_fulfilledness"] ] )
    main(data, ratio=False)

