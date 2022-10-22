import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
matplotlib.rcParams.update({'font.size': 16})
                               # 'dejavuserif', 'cm' (Computer Modern), 'stix',
                               # 'stixsans'

def main(data, ax):
    data = np.asarray(data)
    # print(data)

    d  = 1 #AA
    l0 = 3.5 #AA

    gamma_list = np.linspace(0,1)

    def r0_min(gamma, d):
        return np.sqrt( 6.5 * d**2 / (max(gamma, 6.0 * (1.0 - gamma))) )

    # l0_approx = 0.5 * l0 * np.sqrt( np.array([ max(g, 6.0 * (1.0 - g)) for g in gamma_list]) )

    mask_greater_than_zero = data[:,2] > 1e-5

    fig = plt.figure(figsize = (8.5,5))

    ax.fill_between( gamma_list, [r0_min(g, d) for g in gamma_list], 5, color = "royalblue", alpha=0.45 )
    ax.fill_between( gamma_list, 0, [r0_min(g, d) for g in gamma_list], color = "lightsalmon", alpha=0.45 )
    ax.plot( data[mask_greater_than_zero,0], data[mask_greater_than_zero,1],   marker="o", markersize = 6, markeredgewidth = 1.0, mec = "black", markerfacecolor="royalblue", ls="None" )
    ax.plot( data[~mask_greater_than_zero,0], data[~mask_greater_than_zero,1], marker="X", markersize = 7, markeredgewidth = 1.0, mec = "black", markerfacecolor="lightsalmon", ls="None" )

    # Include whtie dots to highlight rendered surfaces
    mask_highlight = data[:,1] == 5.00
    mask_highlight = np.logical_or(mask_highlight, np.logical_and( data[:,1] >= 3.00, data[:,0] == 1.00 ))
    ax.plot( data[mask_highlight,0], data[mask_highlight,1],   marker=".", markersize = 3, markeredgewidth = 1.0, mec = "white", markerfacecolor="white", ls="None" )

    # plt.plot( data[mask_highlight,0], data[mask_highlight,1],   marker="o", markersize = 7, markeredgewidth = 2.0, mec = "black", markerfacecolor="royalblue", ls="None" )

    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel(r"$r_0~[a]$")

    xtick_labels = [ f"{i}/7" for i in range(8)]
    xtick_labels[0]  = "0"
    xtick_labels[-1] = "1"
    ax.set_xticks( [ i/7.0 for i in range(8)] )
    ax.set_xticklabels( xtick_labels )

if __name__ == "__main__":
    import calculation_folder
    import glob
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    parser.add_argument("-data", type=str, default=None)

    args = parser.parse_args()

    paths = []
    smallest_r0 = dict()

    data  = []
    for f in args.paths:
        calculation = calculation_folder.calculation_folder(f)
        gamma = calculation.descriptor["gamma"]
        r0    = calculation.descriptor["l0"]
        angle = calculation.descriptor["max_angle_between_neighbours"]

        if angle < 1e-2:
            if not gamma in smallest_r0.keys():
                smallest_r0[gamma] = [gamma, r0, angle]
            else:
                if r0 > smallest_r0[gamma][1]:
                    smallest_r0[gamma] = [gamma, r0, angle]
        else:
            data.append( [gamma, r0, angle] )

    data.extend( smallest_r0.values() )

    if not args.data is None:
        print(f"Saving data in {args.data}")
        np.savetxt(args.data, data)

    print(data)
    fig, ax = plt.subplots()
    main(data, ax)
    fig.savefig("stability_criterion.png", dpi=300, bbox_inches="tight", pad_inches=0.1 )
    print("Output to: ./stability_criterion.png")
    # plt.show()
