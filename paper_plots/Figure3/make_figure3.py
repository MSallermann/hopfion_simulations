import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

# print(mpl.rcParams.keys())

mpl.rcParams["font.size"]       = 8 #'dejavusans' (default),
mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 11.0 * cm # Full DIN A4 width
FIG_HEIGHT        = FIG_WIDTH * 4/5 * 0.9 #/ 1.6 # Golden ratio

NCOLS = 5
NROWS = 4

HORIZONTAL_MARGINS = [0.11, 0.0] # left right
VERTICAL_MARGINS   = [0.01, 0.01] # bottom top
WSPACE             = 0.02
HSPACE             = 0.01
WIDTH_RATIOS      = None
HEIGHT_RATIOS     = None

def annotate(ax, text, pos = [0,1], fontsize=8):
    ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

def image_to_ax(ax, path):
    image = plt.imread(path)
    ax.imshow(image)
    ax.axis("off")

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

p1 = plot_data()
p1.gamma = 0.857
p1.l0 = 2.5
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
        [0, offset_d],
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
    l0 = p.l0 
    annotate_idx    = p.annotations
    annotate_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    BASE_PATH = "/home/moritz/hopfion_simulations/all_sp"
    calculation_path = os.path.join(BASE_PATH, f"gamma_{gamma:.3f}_l0_{l0:.3f}")

    energies       = np.loadtxt(os.path.join(calculation_path, "energies.txt"))
    rx             = np.loadtxt(os.path.join(calculation_path, "rx.txt"))
    energies_inter = np.loadtxt(os.path.join(calculation_path, "energies_interpolated.txt"))
    rx_inter       = np.loadtxt(os.path.join(calculation_path, "rx_interpolated.txt"))

    fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))

    gs  = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 
    gs00 = GridSpecFromSubplotSpec(2, 2, subplot_spec=gs[0:-1,0:-1], hspace=0.1, wspace=0.0, height_ratios=[1,0.2], width_ratios=[1,0.1])
    a = fig.add_subplot(gs00[0,0])

    a.plot(rx_inter, energies_inter, color="C0", ls="-")
    a.plot(rx, energies, mec="black", mfc="C0", ls="None", marker=".")
    a.set_xlabel("Reaction coordinate [arb.]")
    a.set_ylabel("Energy [meV]")

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

    for col in range(0,NCOLS):
        a         = fig.add_subplot(gs[-1,col])
        idx       = annotate_idx[col][0]
        plot_name = f"{idx}_{NAME}.png"
        path = os.path.join(SCRIPT_DIR, "renderings", plot_name)
        annotate(a, annotate_letter[col])
        image_to_ax(a, path)

    for i,row in enumerate( range(0,NROWS-1)[::-1] ):
        a         = fig.add_subplot(gs[row,-1])
        idx       = annotate_idx[i + NCOLS][0]
        plot_name = f"{idx}_{NAME}.png"
        path = os.path.join(SCRIPT_DIR, "renderings", plot_name)
        annotate(a, annotate_letter[i + NCOLS])
        image_to_ax(a, path)

    # print(mpl.rcParams.keys())
    fig.savefig(f"plot3_{gamma}_{l0}.png", dpi=300)