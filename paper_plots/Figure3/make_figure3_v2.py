import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

import plot_util

# print(mpl.rcParams.keys())

mpl.rcParams["font.size"]       = 8 #'dejavusans' (default),
mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 11 * cm # Full DIN A4 width

NCOLS = 5
NROWS = 4

HORIZONTAL_MARGINS = [0.1, 0.05] # left right
VERTICAL_MARGINS   = [0.15, 0.05] # bottom top
WSPACE             = 0.02
HSPACE             = 0.02
WIDTH_RATIOS      = None
HEIGHT_RATIOS     = None

## target 
ASPECT_RATIO = 5/4 # Width of subplots divided by height
# Compute height from desired aspect ratio and margins
FIG_HEIGHT = FIG_WIDTH * (1 - HORIZONTAL_MARGINS[0] - HORIZONTAL_MARGINS[1]) / (1 - VERTICAL_MARGINS[0] - VERTICAL_MARGINS[1]) / ASPECT_RATIO

def annotate(ax, text, pos = [0,0.95], fontsize=8):
    ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

def image_to_ax(ax, path):
    image = plt.imread(path)
    ax.imshow(image)
    # ax.axis("off")
    ax.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)
    a.spines["right"].set_visible(False)
    a.spines["left"].set_visible(False)
    a.spines["top"].set_visible(False)
    a.spines["bottom"].set_visible(False)


# Need these to place the annotations
annotate_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
offset_u = 1.5*np.array([0,10])
offset_r = 1.5*np.array([10,0])
offset_l = -1.5*offset_r
offset_d = -1.5*offset_u
offset_ur = (offset_r + offset_u) / np.sqrt(2)
offset_ul = (offset_l + offset_u) / np.sqrt(2)
offset_dr = (offset_r + offset_d) / np.sqrt(2)
offset_dl = (offset_l + offset_d) / np.sqrt(2)

class plot_data:
    def __init__(self):
        self.gamma = 0
        self.l0 = 0
        self.annotations = []
        self.globule_idx = 0

p1             = plot_data()
p1.gamma       = 0.857
p1.l0          = 2.5
p1.globule_idx = 24
p1.annotations = [
        [0, offset_d],
        # [5, "down"],
        [14, offset_dl],
        [15, offset_d],
        [16, offset_r],
        [24, offset_ur],
        [32, offset_ur],
        [37, offset_ur],
        [56, offset_u],
    ]

p2 = plot_data()
p2.gamma = 0.857
p2.l0 = 5.0
p2.globule_idx = 32
p2.annotations = [
        [0, offset_u],
        [11, offset_ul],
        [12, offset_r],
        [13, offset_r],
        [32, offset_u],
        [39, offset_u],
        [42, offset_u],
        [46, offset_u]
    ]

for i, p in enumerate([p1,p2]):
    gamma = p.gamma 
    l0    = p.l0 
    annotate_idx = p.annotations

    BASE_PATH = "/home/moritz/hopfion_simulations/all_sp"
    calculation_path = os.path.join(BASE_PATH, f"gamma_{gamma:.3f}_l0_{l0:.3f}")

    energies       = np.loadtxt(os.path.join(calculation_path, "energies.txt"))
    rx             = np.loadtxt(os.path.join(calculation_path, "rx.txt"))
    energies_inter = np.loadtxt(os.path.join(calculation_path, "energies_interpolated.txt"))
    rx_inter       = np.loadtxt(os.path.join(calculation_path, "rx_interpolated.txt"))

    fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))

    # fig.suptitle(rf"$\gamma = {gamma:.3f}, r_0 = {l0:.3f} a$")
    # fig.suptitle(plot_util.gamma_r0_string(gamma, l0))

    # Overall gridspec
    gs = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 

    # Gridspec with margins to contain plot of path
    # gs00 = GridSpecFromSubplotSpec(2, 2, subplot_spec=gs[1:,0:-1], hspace=0.1, wspace=0.0, height_ratios=[1,0.2], width_ratios=[1,0.1])

    # Throwaway axis that just draws a frame around the grid spec

    a = fig.add_subplot(gs[1:,0:-1])
    a.spines["top"].set_color("lightgray")
    a.spines["right"].set_color("lightgray")
    a.plot(rx_inter, energies_inter, color="C0", ls="-")
    a.plot(rx, energies, mec="black", mfc="C0", ls="None", marker=".")
    a.set_xlabel("Reaction coordinate [arb.]")
    a.set_ylabel("Energy [meV]")

    a.text(*[0.25,0.25], plot_util.r0_string(l0), fontsize=8, horizontalalignment='right', verticalalignment='top', transform=a.transAxes, bbox=dict(facecolor='none', edgecolor='black'))

    for i,(idx,anno) in enumerate(annotate_idx):
        xy  = (rx[idx], energies[idx])
        arrowprops = dict(arrowstyle="-")
        xy_text = anno
        a.annotate(annotate_letter[i], xy , xy_text, arrowprops = arrowprops, verticalalignment="center", horizontalalignment="center", textcoords="offset points")

    # Render surfaces and copy data
    import render_surfaces

    # render_surfaces.run(annotate_idx, calculation_path)
    # render_surfaces.render_globule(p.globule_idx, calculation_path)

    NAME = f"{gamma:.3f}_{l0:.3f}"

    import render_charge_dists
    render_charge_dists.run(annotate_idx, calculation_path)
    # NAME = f"{gamma:.3f}_{l0:.3f}_charge"

    # for i in range(len(rx)):
    #     render_charge_dists.run([[i,""]], calculation_path)

    for col in range(0,NCOLS):
        a         = fig.add_subplot(gs[0,col])
        idx       = annotate_idx[col][0]
        plot_name = f"{idx}_{NAME}.png"
        path = os.path.join(SCRIPT_DIR, "renderings", plot_name)
        annotate(a, annotate_letter[col])
        image_to_ax(a, path)
        a.spines["right"].set_visible(True)
        a.spines["right"].set_color("lightgray")

    for i,row in enumerate( range(1,NROWS) ):
        a         = fig.add_subplot(gs[row,-1])
        idx       = annotate_idx[i + NCOLS][0]
        plot_name = f"{idx}_{NAME}.png"
        path = os.path.join(SCRIPT_DIR, "renderings", plot_name)
        annotate(a, annotate_letter[i + NCOLS])
        image_to_ax(a, path)
        a.spines["top"].set_visible(True)
        a.spines["top"].set_color("lightgray")

    a = fig.add_axes( gs[:,:].get_position(fig) )
    a.set_facecolor([0,0,0,0])
    a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)

    # print(mpl.rcParams.keys())
    fig.savefig(f"plot3_{gamma}_{l0}_v2.png", dpi=300)