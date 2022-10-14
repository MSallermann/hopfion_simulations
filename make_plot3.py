import matplotlib
import matplotlib.pyplot as plt
import os, shutil
import numpy as np 
import calculation_folder

matplotlib.rcParams["font.family"] = "serif" #'dejavusans' (default),
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

# if os.path.exists(OUTPUT_DIR):
    # shutil.rmtree(OUTPUT_DIR)
# os.makedirs(OUTPUT_DIR)

def main(calculation_path):
    calculation = calculation_folder.calculation_folder(calculation_path)
    gamma = calculation.descriptor["gamma"]
    l0 = calculation.descriptor["l0"]

    OUTPUT_DIR = f"./fig3_gamma_{gamma:.3f}_l0_{l0:.3f}"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    rx             = np.loadtxt( calculation.to_abspath("rx.txt") )
    energies       = np.loadtxt( calculation.to_abspath("energies.txt") )
    rx_inter       = np.loadtxt( calculation.to_abspath("rx_interpolated.txt") )
    energies_inter = np.loadtxt( calculation.to_abspath("energies_interpolated.txt") )

    annotate_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # annotate_idx_pre    = [
    #     [0, "down"],
    #     # [5, "down"],
    #     [14, "left_down"],
    #     [15, "down"],
    #     [16, "right"],
    #     [24, "right_up"],
    #     [32, "right_up"],
    #     [37, "right_up"],
    #     [56, "up"],
    # ]

    annotate_idx_pre    = [
        [0, "down"],
        # [5, "down"],
        [11, "left_up"],
        [12, "down"],
        [13, "right"],
        [14, "right_up"],
        [20, "up"],
        [25, "up"],
        [32, "up"]
]

    # Filter out the annotations that are out of scope
    annotate_idx = []
    for i,(idx,anno) in enumerate(annotate_idx_pre):
        if idx not in range(len(rx)):
            continue
        annotate_idx.append([idx, anno])

    # Plot the path
    fig, ax = plt.subplots()


    def plot_path(ax):
        ax.plot(rx_inter, energies_inter, color="C0", ls="-")
        ax.plot(rx, energies, mec="black", mfc="C0", ls="None", marker="o")

        # Plot the annotations
        for i,(idx,anno) in enumerate(annotate_idx):
            xy      = (rx[idx], energies[idx])

            offset_horizontal = 20
            offset_vertical = 1.75

            if anno == "left":
                xy_text = (rx[idx]-offset_horizontal, energies[idx])
            elif anno == "right":
                xy_text = (rx[idx]+offset_horizontal, energies[idx])
            elif anno == "up":
                xy_text = (rx[idx], energies[idx]+offset_vertical)
            elif anno == "down":
                xy_text = (rx[idx], energies[idx]-offset_vertical)
            elif anno == "left_down":
                xy_text = (rx[idx]-offset_horizontal, energies[idx]-offset_vertical)
            elif anno == "right_down":
                xy_text = (rx[idx]+offset_horizontal, energies[idx]-offset_vertical)
            elif anno == "left_up":
                xy_text = (rx[idx]-offset_horizontal, energies[idx]+offset_vertical)
            elif anno == "right_up":
                xy_text = (rx[idx]+offset_horizontal, energies[idx]+offset_vertical)

            arrowprops = dict(arrowstyle="-")
            ax.annotate(annotate_letter[i], xy , xy_text, arrowprops = arrowprops, verticalalignment="center", horizontalalignment="center")

        ax.set_xlabel("Reaction coordinate [arb.]")
        ax.set_ylabel("Energy [meV]")

    plot_path(ax)
    base_size = 1e-3 * 1.5
    rendering_width = 768
    rendering_height = 1024
    plt.gcf().set_figheight( int(base_size * 3.5 * rendering_width ) )
    plt.gcf().set_figwidth(  int(base_size * 4 * rendering_height) )
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "path.png"), dpi=300, pad_inches=0, bbox_inches=0)
    plt.close()

    import plot_spin_configuration, plot_util

    # Render the isosurfaces
    for i,(idx,anno) in enumerate(annotate_idx):
        plot_path = os.path.join(OUTPUT_DIR, str(idx))
        if not os.path.exists(plot_path + ".png"):
            plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=calculation.to_relpath(plot_path), idx_image_infile=idx, distance=60, annotate=-1, mode="isosurface", view="hopfion_normal")
        plot_util.annotate_text(plot_path + ".png", annotate_letter[i], fontsize=20)

    # Start making the complete figure

    fig = plt.figure()
    SHAPE = (4, 5)
    fig.suptitle(rf"$\gamma = {gamma:.2f}$  $r_0 = {l0:.2f}\,a$", fontsize=15)
    base_size = 10
    # fig.set_figheight( base_size * 0.8 )
    # fig.set_figwidth(  base_size * 1.25)

    def add_plot(path, loc, title="", rowspan=1, colspan=1):
        a     = plt.subplot2grid(shape=SHAPE, loc=loc, rowspan=rowspan, colspan=colspan )
        a.set_title(title, fontsize=22)
        image = plt.imread(path)
        print(image.shape)
        a.imshow(image)
        a.axis("off")

    add_plot(os.path.join(OUTPUT_DIR, "path.png"), loc=(0,0), rowspan=SHAPE[0]-1, colspan=SHAPE[1]-1)

    # Place 5 at bottom row
    for i,(idx,anno) in enumerate(annotate_idx[:5]):
        plot_path = os.path.join(OUTPUT_DIR, str(idx)) + ".png"
        loc = (SHAPE[0]-1,i)
        print(i, idx)
        print(loc)
        add_plot(plot_path, loc, rowspan=1, colspan=1)

    # Place 3 at right column
    for i,(idx,anno) in enumerate(annotate_idx[5:]):
        plot_path = os.path.join(OUTPUT_DIR, str(idx)) + ".png"
        loc = (SHAPE[0]-2-i, SHAPE[1]-1)
        print(i, idx)
        print(loc)
        add_plot(plot_path, loc, rowspan=1, colspan=1)

    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "fig3.png")
    plt.savefig(plot_path, dpi=300, bbox_inches=0, pad_inches=0)
    print(f"Output to: {plot_path}")

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")

    args = parser.parse_args()
    for f in args.paths:
        main(f)