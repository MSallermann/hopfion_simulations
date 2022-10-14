import os
import calculation_folder
import matplotlib
import matplotlib.pyplot as plt
import plot_spin_configuration

matplotlib.rcParams["font.family"] = "serif" #'dejavusans' (default),
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

def main(BASE_DIR):
    # Isosurface plots
    calculation          = calculation_folder.calculation_folder(BASE_DIR)
    gamma = calculation.descriptor["gamma"]
    l0 = calculation.descriptor["l0"]

    iso_hopfion = os.path.join(BASE_DIR, "hopfion_isosurface_hopfion_diagonal.png")
    iso_sp      = os.path.join(BASE_DIR, "sp_isosurface_hopfion_diagonal.png")

    cross_section_hopfion = os.path.join(BASE_DIR, "hopfion_cross_section_ip_hopfion_inplane.png")
    cross_section_sp      = os.path.join(BASE_DIR, "sp_cross_section_ip_hopfion_inplane.png")

    mode = os.path.join(BASE_DIR, "mode_isosurface_hopfion_diagonal.png")

    SHAPE    = (2, 3)

    fig = plt.figure()
    fig.suptitle(rf"$\gamma = {gamma:.2f}$  $r_0 = {l0:.2f}\,a$", fontsize=32)
    base_size = 10
    fig.set_figheight( base_size * 0.8 )
    fig.set_figwidth(  base_size * 1.25)

    def add_plot(path, loc, title="", rowspan=1, colspan=1):
        a     = plt.subplot2grid(shape=SHAPE, loc=loc, rowspan=rowspan, colspan=colspan )
        a.set_title(title, fontsize=22)
        image = plt.imread(path)
        a.imshow(image)
        a.axis("off")

    add_plot(iso_hopfion, (0,0), title="Hopfion")
    add_plot(iso_sp, (1,0), title="Saddlepoint")
    add_plot(cross_section_hopfion, (0,1))
    add_plot(cross_section_sp, (1,1))

    add_plot(mode, (0,2), rowspan=2, title="Collapse mode")

    plt.tight_layout()

    plt.savefig(f"plot2_gamma_{gamma:.3f}_l0_{l0:.3f}.png", dpi=300, bbox_inches=0, pad_inches=0)
    print(f"Output to: plot2_gamma_{gamma:.3f}_l0_{l0:.3f}.png")

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    args = parser.parse_args()

    for f in args.paths:
        main(f)