import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

import plot_util

import plot_template
# print(mpl.rcParams.keys())

mpl.rcParams["font.size"]        = 8 #'dejavusans' (default),
mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 7.5 * cm # Full DIN A4 width

NCOLS = 1
NROWS = 3
HORIZONTAL_MARGINS = [0.05, 0.0155]
VERTICAL_MARGINS   = [0.0125, 0.01]
WSPACE             = 0.0
HSPACE             = 0.3
WIDTH_RATIOS       = None
HEIGHT_RATIOS      = None

## target 
ASPECT_RATIO = 1.6/(1.6) # Width of subplots divided by height
# Compute height from desired aspect ratio and margins
FIG_HEIGHT = FIG_WIDTH * (1 - WSPACE - HORIZONTAL_MARGINS[0] - HORIZONTAL_MARGINS[1]) / (1 - VERTICAL_MARGINS[0] - HSPACE - VERTICAL_MARGINS[1]) / ASPECT_RATIO

def annotate(ax, text, pos = [0,1], fontsize=12):
    ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

def image_to_ax(ax, path):
    image = plt.imread(path)
    ax.imshow(image)
    ax.axis("off")

fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))
gs  = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=2*HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 
h = np.ones(gs.nrows)
h[-1] = 0.24
gs.set_height_ratios(h)

import plot_energy_barrier

ax_r0    = fig.add_subplot(gs[0, 0])
ax_gamma = None
ax_angle = fig.add_subplot(gs[1, 0])

data = np.loadtxt( os.path.join(SCRIPT_DIR, "barrier_data.txt") )

plot_energy_barrier.main(data, False, ax_r0, ax_gamma, ax_angle)

for a in [ax_angle, ax_r0]:
    a.get_legend().remove()

# Last axis is only for the legend
a = fig.add_subplot(gs[2,0])

import matplotlib as mpl

def get_norm(my_list, factor=0.5):
    _min = min(my_list)
    _max = max(my_list)
    _span = _max - _min
    norm = mpl.colors.Normalize(vmin = _min - factor*_span, vmax = _max + factor*_span)
    return norm

gamma_list = np.linspace(0,1,7)
cmap = mpl.cm.get_cmap('Greys')
norm = get_norm(gamma_list)

for g in gamma_list:
    label_text = plot_util.gamma_string(g)
    a.plot([], color = cmap(norm(g)), mfc = cmap(norm(g)), marker="o", markersize = 6, markeredgewidth = 1.0, lw=2.5, mec = "black", label = label_text)

# line, = a.plot([0,1],[0,1],'b')           #add some data
# a.legend((line,),('Test',),loc='center') #create legend on bottommost axis
a.legend(loc="lower center", ncol=4, prop={'size': 8},frameon=False)
a.axis("off")  

# fig.legend(loc="lower center", cols=4)
fig.savefig("plot_barriers_v2.png", dpi=300)