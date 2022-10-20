import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import gradient_line

#define font family to use for all text
from urllib3 import Retry

mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
mpl.rcParams["font.size"] = 8
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

cm                = 1/2.54
FIG_WIDTH         = 11.0 * cm # Full DIN A4 width
FIG_HEIGHT        = FIG_WIDTH  / 1.6 # Golden ratio

# matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
#                                # 'dejavuserif', 'cm' (Computer Modern), 'stix',
#                                # 'stixsans'

def get_norm(my_list, factor=0.5):
    _min = min(my_list)
    _max = max(my_list)
    _span = _max - _min
    norm = mpl.colors.Normalize(vmin = _min - factor*_span, vmax = _max + factor*_span)
    return norm

def main(data, ratio, ax_r0=None, ax_gamma=None, ax_angle=None):
    if ratio:
        ylabel = r"$\Delta E~/~E_0$"
        name_prefix = "e_barrier_ratio"
    else:
        ylabel = r"$\Delta E~[\mathrm{meV}]$"
        name_prefix = "e_barrier"

    data = np.asarray(data)

    r0_list    = np.unique(data[:,1])
    gamma_list = np.unique(data[:,0])

    # if ax_r0 is None:
    #     fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    # else:

    if not ax_r0 is None:
        print("R0")
        ax = ax_r0

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

            cmap = mpl.cm.get_cmap('Reds')
            norm = get_norm(gamma_list)
            ax.plot(tmp[:,1], tmp[:,2], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", mec = "black", label = label_text)
            # gradient_line.gradient_line(ax=plt.gca(), x=tmp[:,1], y=tmp[:,2], c=tmp[:,0])

        ax.set_ylabel(ylabel)
        ax.set_xlabel(r"$r_0~[a]$")

        ax.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5,-0.4,0,1))
    # fig.tight_layout()
    # if ax_r0 is None:
    #     plt.savefig(f"{name_prefix}_vs_r0.png", bbox_inches="tight", dpi=300)
        # plt.show()
        # plt.close()

    if not ax_gamma is None:
    #     fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    # else:
        print("gamma")
        ax = ax_gamma
        # Plot vs gamma
        for r0 in r0_list:
            tmp = data[ data[:,1] == r0 ]
            tmp = tmp[ np.argsort(tmp[:,0]) ]

            label_text = fr"$r_0 = {r0}~a$"

            cmap = mpl.cm.get_cmap('Blues')
            norm = get_norm(r0_list)
            ax.plot(tmp[:,0], tmp[:,2], color = cmap(norm(r0)), mfc = cmap(norm(r0)), marker="o", mec = "black", label = label_text)

        ax.set_ylabel(ylabel)
        ax.set_xlabel(r"$\gamma$")
        ax.set_xticks( [i/7.0 for i in range(8)] )

        xtick_labels = [ f"{i}/7" for i in range(8)]
        xtick_labels[0]  = "0"
        xtick_labels[-1] = "1"

        ax.set_xticks( [ i/7.0 for i in range(8)] )
        ax.set_xticklabels( xtick_labels )

        # ax.legend()
        ax.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5,-0.4,0,1))

    # if ax_r0 is None:
    #     fig.savefig(f"{name_prefix}_vs_gamma.png", bbox_inches="tight", dpi=300)
        # plt.show()
        # plt.close()

    # if ax_angle is None:
    #     fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    # else:

    if not ax_angle is None:
        print("angle")

        ax = ax_angle

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

            cmap = mpl.cm.get_cmap('Greens')
            norm = get_norm(gamma_list) 
            ax.plot(tmp[:,3] / np.pi, tmp[:,2], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", mec = "black", label = label_text)

        ax.set_xticks( [1/8, 2/8, 3/8, 0.5] )
        ax.set_xticklabels( [r"$1/8\pi$", r"$1/4\pi$", r"$3/8\pi$", r"$1/2\pi$"] )
        ax.set_ylabel(ylabel)
        ax.set_xlabel(r"$\max( \angle (\mathbf{n}_i, \mathbf{n}_j) )$")
        ax.set_xlim(1/16,0.5-1/16)
        # ax.legend()
        ax.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5,-0.4,0,1))

    # if ax_angle is None:
    #     fig.savefig(f"{name_prefix}_vs_angle.png", bbox_inches="tight", dpi=300)
        # plt.close()

    # fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    # # Plot vs criterion fulfilledness
    # for i in range(8):
    #     g = i/7.0
    #     tmp = data[ data[:,0] == g ]
    #     tmp = tmp[ np.argsort(tmp[:,4]) ] # Sort by criterion

    #     if i==0:
    #         label_text = fr"$\gamma = 0$"
    #     elif i==7:
    #         label_text = fr"$\gamma = 1$"
    #     else:
    #         label_text = fr"$\gamma = {i:.0f}\,/\,7$"

    #     cmap = mpl.cm.get_cmap('Greens')
    #     norm = get_norm(gamma_list)
    #     ax.plot(tmp[:,4], tmp[:,2], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

    # # plt.gca().set_xticks( [0.25, 0.5] )
    # # plt.gca().set_xticklabels( [r"$\pi/4$", r"$3\pi/2$"] )
    # ax.set_ylabel(ylabel)
    # ax.set_xlabel(r"criterion")
    # ax.legend()
    # fig.savefig(f"{name_prefix}_vs_criterion.png", bbox_inches="tight", dpi=300)

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
    parser.add_argument("-data", type=str, default=None)

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

    if args.data:
        np.savetxt(args.data, data, header="gamma,l0,energy_barrier,max_angle,criterion_fulfilledness")

    main(data, ratio=False)