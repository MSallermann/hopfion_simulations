import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np
from matplotlib.patches import Rectangle, ConnectionPatch

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

from plot_template import Paper_Plot

gamma = 0.857
l0    = 5.00
BASE_PATH = "/home/moritz/hopfion_simulations/all_sp"
calculation_path = os.path.join(BASE_PATH, f"gamma_{gamma:.3f}_l0_{l0:.3f}")

energies       = np.loadtxt(os.path.join(calculation_path, "energies.txt"))[:34]
rx             = np.loadtxt(os.path.join(calculation_path, "rx.txt"))[:34]
energies_inter = np.loadtxt(os.path.join(calculation_path, "energies_interpolated.txt"))[:330]
rx_inter       = np.loadtxt(os.path.join(calculation_path, "rx_interpolated.txt"))[:330]

PATH_PLATEAU = "/home/moritz/hopfion_simulations/second_sp_gamma_0.857_l0_5.000/combined2"

energies_2       = np.loadtxt(os.path.join(PATH_PLATEAU, "energies.txt"))[::1]
rx_2             = np.loadtxt(os.path.join(PATH_PLATEAU, "rx.txt"))[::1] + rx[-1]
energies_inter_2 = np.loadtxt(os.path.join(PATH_PLATEAU, "energies_interpolated.txt"))
rx_inter_2       = np.loadtxt(os.path.join(PATH_PLATEAU, "rx_interpolated.txt")) + rx[-1]

rx = np.array( [*rx, *rx_2] )
rx_inter = np.array( [*rx_inter, *rx_inter_2] )
energies = np.array( [*energies, *energies_2] )
energies_inter = np.array( [*energies_inter, *energies_inter_2] )

def render_from_annotations(annotation_list, xlist, output_directory):
    import plot_spin_configuration
    import calculation_folder

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for xy, text in annotation_list:
        idx = np.argmin( np.abs(xlist - xy[0]) )

        plot_name = f"idx_{idx}"
        plot_path = os.path.join(output_directory, f"idx_{idx}")

        if os.path.exists(plot_path + ".png"):
            print(f"Skipping idx {idx}")
            continue
        print(f"Rendering idx {idx}")

        calculation_path = "/home/moritz/hopfion_simulations/all_sp/gamma_0.857_l0_5.000"
        input_path = "./chain_file_total.ovf"
        idx_infile = idx

        if idx > 33:
            idx_infile = idx-34
            calculation_path = "/home/moritz/hopfion_simulations/second_sp_gamma_0.857_l0_5.000/"
            input_path = "./combined2/chain.ovf"

        plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path=input_path, relative_output_path=plot_name, idx_image_infile=idx_infile, distance=60, annotate=-1, mode="isosurface", view="hopfion_diagonal", output_dir=output_directory, output_suffix="")

pplot = Paper_Plot(11 * Paper_Plot.cm)
pplot.nrows = 4
pplot.ncols = 5
pplot.horizontal_margins[0] = 0.15
pplot.vertical_margins[0]   = 0.125

pplot.height_from_aspect_ratio(5/4)

fig = pplot.fig()
gs  = pplot.gs()

# Main plot
ax_plot = fig.add_subplot(gs[1:,:-1])
ax_plot.plot(rx_inter, energies_inter)
ax_plot.spines["top"].set_color("lightgrey")
ax_plot.spines["right"].set_color("lightgrey")
ax_plot.set_xlabel("Reaction coordinate [arb.]")
ax_plot.set_ylabel("Energy [meV]")

fill_start = rx[12]
fill_end   = 383

ax_plot.fill_between(rx_inter, energies_inter, y2=0, where = (rx_inter>fill_start) & (rx_inter<fill_end), color="lightsalmon" )

axins = ax_plot.inset_axes([0.1, 0.1, 0.6, 0.3])
axins.plot(rx_inter, energies_inter)
axins.set_xlim(300, 383)
axins.set_ylim(12.5, 14.35)
ax_plot.indicate_inset_zoom(axins, edgecolor="black")
axins.set_xticklabels([])
axins.set_yticklabels([])

pplot.annotate_graph(ax_plot, (rx[0],  energies[0]),  "d")
pplot.annotate_graph(ax_plot, (rx[11], energies[11]), "d")
pplot.annotate_graph(ax_plot, (rx[12], energies[12]), "l", offset_scale=0.9)
pplot.annotate_graph(ax_plot, (rx[13], energies[13]), "ur", offset_scale=1.1)
pplot.annotate_graph(ax_plot, (rx[24], energies[24]), "u")

pplot.annotate_graph(axins, (rx[33], energies[33]), "d")
pplot.annotate_graph(axins, (rx[60], energies[60]), "d", offset_scale=0.8)
pplot.annotate_graph(axins, (rx[83], energies[80]), "u")

annotation_list = pplot.annotation_dict["key1"]["annotation_list"]

print(annotation_list)

OUTPUT_DIR = "isosurface_renderings"
render_from_annotations(annotation_list, rx, OUTPUT_DIR)

counter = 0
for a in pplot.row(0):
    xy, text = annotation_list[counter]
    print(text)
    idx = np.argmin( np.abs(rx - xy[0]) )
    pplot.image_to_ax(a, os.path.join( OUTPUT_DIR, f"idx_{idx}.png" ))

    a.spines["left"].set_visible(True)
    a.spines["left"].set_color("lightgrey")
    pplot.annotate(a, text )
    counter += 1

for a in pplot.col(-1, slice(1,None,1)):
    xy, text = annotation_list[counter]
    idx = np.argmin( np.abs(rx - xy[0]) )
    pplot.image_to_ax(a, os.path.join( OUTPUT_DIR, f"idx_{idx}.png" ))

    a.spines["top"].set_visible(True)
    a.spines["top"].set_color("lightgrey")
    pplot.annotate(a, annotation_list[counter][1] )
    counter += 1

pplot.spine_axis(gs[:,:])

fig.savefig("test_path_template.png", dpi=300)