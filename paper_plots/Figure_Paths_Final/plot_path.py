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

plt.margins(0.1)

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

import plot_spin_configuration
import calculation_folder
def render_from_annotations(annotation_list, xlist, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for xy, text in annotation_list:
        idx = np.argmin( np.abs(xlist - xy[0]) )

        print(xlist)
        print(xy[0])

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

        plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path=input_path, relative_output_path=plot_name, idx_image_infile=idx_infile, distance=48, annotate=-1, mode="isosurface", view="hopfion_diagonal", output_dir=output_directory, output_suffix="")

pplot = Paper_Plot(17.5 * Paper_Plot.cm)
pplot.nrows = 2
pplot.ncols = 2
pplot.wspace = 0.00
pplot.hspace = 0
pplot.horizontal_margins[0] = 0.065
pplot.horizontal_margins[1] = 0.065
pplot.vertical_margins[0]   = 0.12
pplot.vertical_margins[1]   = 0.01
pplot.height_ratios        = [1,1.8]

pplot.height_from_aspect_ratio(6/(sum(pplot.height_ratios)) - pplot.wspace)

fig = pplot.fig()
gs_all = pplot.gs()

gs_l = GridSpecFromSubplotSpec(1,1,gs_all[1,0], hspace=0, wspace=0)

# Left plot
ax_plot = fig.add_subplot(gs_l[0,0])
ax_plot.plot(rx_inter, energies_inter)

ax_plot.spines["top"].set_color("lightgrey")
ax_plot.spines["right"].set_visible(False)

ax_plot.set_xlabel("Reaction coordinate [arb.]")
ax_plot.set_ylabel("Energy [meV]")

ax_plot.set_xmargin(0.07)

# Shade under plot
fill_start = rx[12]
fill_end   = rx[92]
ax_plot.fill_between(rx_inter, energies_inter, y2=0, where = (rx_inter>fill_start) & (rx_inter<fill_end), color="lightsalmon" )

# Inset axes
axins = ax_plot.inset_axes([0.04, 0.04, 0.65, 0.35])
axins.plot(rx_inter, energies_inter)
axins.set_xlim(300, rx[92]+2)
axins.set_ylim(energies[92]-0.2, 14.5)
ax_plot.indicate_inset_zoom(axins, edgecolor="black")
axins.set_xticklabels([])
axins.set_yticklabels([])

# Right plot
gs_r = GridSpecFromSubplotSpec( 1, 1, gs_all[1,1], hspace=0, wspace=0)
ax_plot_r = fig.add_subplot( gs_r[:,:], zorder=0)
ax_plot_r.set_facecolor([0,0,0,0])
ax_plot_r.set_xlabel("Reaction coordinate [arb.]")
# ax_plot_r.fill_between(rx_inter, energies_inter, y2=0, where = (rx_inter>fill_start) & (rx_inter<fill_end), color=[0.7,0.8,1], edgecolor="None" )
ax_plot_r.fill_between(rx_inter, energies_inter, y2=0, where = (rx_inter>fill_start) & (rx_inter<fill_end), color="lightgrey", edgecolor="None" )

# ax_plot_r.plot(rx_inter, energies_inter, color=[0.7,0.8,1])
ax_plot_r.plot(rx_inter, energies_inter, color="lightgrey")


ax_plot_r.spines['left'].set_color('grey')
ax_plot_r.yaxis.label.set_color('grey')
ax_plot_r.tick_params(axis='y', colors='grey')
ax_plot_r.set_xmargin(0.07)

# Create twin axis
ax_twin = ax_plot_r.twinx()
ax_twin.set_xlim(ax_twin.get_xlim())

for k,s in ax_twin.spines.items():
    s.set_visible(False)

ax_twin.set_ylabel("Bloch point distance [a]")

BASE_PATH = "/home/moritz/hopfion_simulations/all_sp"
calculation_path = os.path.join(BASE_PATH, f"gamma_{gamma:.3f}_l0_{l0:.3f}")
bp_distance = np.loadtxt( os.path.join( calculation_path, "bp_distance.txt" ) )


rx_bp = rx[:len(bp_distance)][bp_distance[:,1]>0]
dist  = bp_distance[:,1][bp_distance[:,1]>0]
ax_twin.plot(rx_bp, dist, color="black", lw=2.4)
ax_twin.plot(rx_bp, dist, color="lightsalmon")

# Add spines
pplot.spine_axis(gs_all[0,:], color="grey")
pplot.spine_axis(gs_all[:,:])

# ax_twin.plot(rx_inter, energies_inter,zorder=-1)
# fill_start = rx[12]
# fill_end   = 383

# Annotations of energy plot
pplot.annotate_graph(ax_plot, (rx[12], energies[12]), "l", offset_scale=0.9)
pplot.annotate_graph(ax_plot, (rx[13], energies[13]), "ur", offset_scale=1.1)
pplot.annotate_graph(ax_plot, (rx[20], energies[20]), "u")
pplot.annotate_graph(ax_plot, (rx[28], energies[28]), "u")
pplot.annotate_graph(ax_plot, (rx[60], energies[60]), "u")
pplot.annotate_graph(ax_plot, (rx[92], energies[92]), "ur")
pplot.annotate_graph(axins, (rx[60], energies[60]), "d", text = "E", key=None)
pplot.annotate_graph(axins, (rx[92], energies[92]), "ul", text = "F", key=None)

annotation_list = pplot.annotation_dict["key1"]["annotation_list"]
print(annotation_list)

grad = np.gradient(dist, rx_bp)

for (rx_, e), t in annotation_list:
    idx = np.argmin( np.abs(rx_bp - rx_) )
    xy_text = pplot.xy_text_auto( ax = ax_twin, xy = (rx_bp[idx], dist[idx]), deriv=grad[idx] )
    pplot.annotate_graph( ax_twin, (rx_bp[idx], dist[idx] ), xy_text = xy_text, text=t, key=None)

# Surface renderings
gs_iso = GridSpecFromSubplotSpec( 1, 6, gs_all[0,:], hspace=0, wspace=0)

OUTPUT_DIR = "isosurface_renderings"
render_from_annotations(annotation_list, rx, OUTPUT_DIR)

####### Mark bloch point
idx = 28
plot_name = f"idx_{idx}"
plot_path = os.path.join(OUTPUT_DIR, f"idx_{idx}")
calculation_path = "/home/moritz/hopfion_simulations/all_sp/gamma_0.857_l0_5.000"
input_path = "./chain_file_total.ovf"
idx_infile = idx

if idx > 33:
    idx_infile = idx-34
    calculation_path = "/home/moritz/hopfion_simulations/second_sp_gamma_0.857_l0_5.000/"
    input_path = "./combined2/chain.ovf"

plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path=input_path, relative_output_path=plot_name, idx_image_infile=idx_infile, distance=48, annotate=-1, mode="mark_bloch_points", view="hopfion_diagonal", output_dir=OUTPUT_DIR, output_suffix="")


counter = 0
for a in pplot.row(0, gs=gs_iso):
    xy, text = annotation_list[counter]
    print(text)
    idx = np.argmin( np.abs(rx - xy[0]) )
    pplot.image_to_ax(a, os.path.join( OUTPUT_DIR, f"idx_{idx}.png" ))

    for k,s in a.spines.items():
        s.set_visible(True)
        s.set_color("lightgrey")

    pplot.annotate(a, text )
    counter += 1

fig.savefig("path.png", dpi=300)