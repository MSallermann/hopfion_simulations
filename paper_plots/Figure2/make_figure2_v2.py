import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np


import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))
import plot_util

# print(mpl.rcParams.keys())

# mpl.rcParams["font.size"]       = 12 #'dejavusans' (default),
mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 21.0 * cm # Full DIN A4 width
FIG_HEIGHT        = FIG_WIDTH * 2.3/6 #/ 1.6 # Golden ratio

NCOLS = 6
NROWS = 2
HORIZONTAL_MARGINS = [0.005, 0.005]
VERTICAL_MARGINS  = [0.02, 0.1]
WSPACE            = 0.0
HSPACE            = 0.0
WIDTH_RATIOS      = None #[2,2,1,1]
HEIGHT_RATIOS     = None

ASPECT_RATIO = 6/2 # Width of subplots divided by height
# Compute height from desired aspect ratio and margins
FIG_HEIGHT = FIG_WIDTH * (1 - HORIZONTAL_MARGINS[0] - HORIZONTAL_MARGINS[1]) / (1 - VERTICAL_MARGINS[0] - VERTICAL_MARGINS[1]) / ASPECT_RATIO

# HEIGHT_RATIOS     = [1,1,.15,1,1,.15,1,1,.15]

def annotate(ax, text, pos = [0.025,0.975], fontsize=12):
    ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

def image_to_ax(ax, path):
    image = plt.imread(path)
    ax.imshow(image)
    ax.axis("off")

# gamma = 0.000
# l0    = 3.000
# gamma = 0.857
# l0    = 5.000
# gamma = 1.000
# l0    = 5.000

gamma_l0_list =  [
    [0, 3.0],
    [0.857, 5.00],
    [1, 5.00]
]

fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))
gs  = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 

for i,(gamma,l0) in enumerate(gamma_l0_list):
    row = 0
    col = 2*i

    NAME = "hopfion_isosurface_hopfion_diagonal"
    a    = fig.add_subplot(gs[row, col])
    a.set_title( plot_util.gamma_r0_string(gamma, l0), fontsize=8, loc="left" )
    # a.set_title(f"$\gamma = {gamma:.3f}, r_0 = {l0:.3f}~a$", fontsize=8, loc="left")
    annotate(a, "Hopfion", fontsize=8, pos=[0.08, 0.98])
    # annotate(a, "A")
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    image_to_ax(a, path)

    NAME = "sp_isosurface_hopfion_diagonal"
    a    = fig.add_subplot(gs[row, col+1])
    annotate(a, "Saddle point", fontsize=8)
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    image_to_ax(a, path)

    NAME = "hopfion_cross_section_ip_hopfion_inplane"
    a    = fig.add_subplot(gs[row+1, col])
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    image_to_ax(a, path)

    NAME = "sp_cross_section_ip_hopfion_inplane"
    a    = fig.add_subplot(gs[row+1, col+1])
    # annotate(a, "")
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    image_to_ax(a, path)

    # NAME = "mode_isosurface_hopfion_diagonal"
    # a    = fig.add_subplot(gs[row, col+2])
    # annotate(a, "Collapse mode", fontsize=8)
    # # annotate(a, "A")
    # path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    # image_to_ax(a, path)


a = fig.add_axes( gs[:,:2].get_position(fig) )
a.set_facecolor([0,0,0,0])
a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)

a = fig.add_axes( gs[:,2:4].get_position(fig) )
a.set_facecolor([0,0,0,0])
a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)

a = fig.add_axes( gs[:,4:6].get_position(fig) )
a.set_facecolor([0,0,0,0])
a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)


fig.savefig(f"plot2_v2.png", dpi=300)