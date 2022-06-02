import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

# print(mpl.rcParams.keys())

mpl.rcParams["font.size"]        = 8 #'dejavusans' (default),
mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 21.0 * cm # Full DIN A4 width
FIG_HEIGHT        = FIG_WIDTH / 3.418 # Golden ratio

NCOLS = 3
NROWS = 1
HORIZONTAL_MARGINS = [0.02, 0.01]
VERTICAL_MARGINS  = [0.2, 0.1]
WSPACE            = 0.25
HSPACE            = 0.1
WIDTH_RATIOS      = None
HEIGHT_RATIOS     = None

def annotate(ax, text, pos = [0,1], fontsize=12):
    ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

def image_to_ax(ax, path):
    image = plt.imread(path)
    ax.imshow(image)
    ax.axis("off")

fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))
gs  = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=2*HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 

import plot_energy_barrier

ax_r0    = fig.add_subplot(gs[0, 0])
ax_gamma = fig.add_subplot(gs[0, 1])
ax_angle = fig.add_subplot(gs[0, 2])

data = np.loadtxt( os.path.join(SCRIPT_DIR, "barrier_data.txt") )
# fig.add_axes(gs[0,1])
# fig.add_axes(gs[0,2])

plot_energy_barrier.main(data, ax_r0, ax_gamma, ax_angle)

fig.savefig("plot_barriers.png", dpi=300)