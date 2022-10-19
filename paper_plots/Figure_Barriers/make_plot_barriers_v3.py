import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))
sys.path.insert(0, os.path.join(SCRIPT_DIR, ".."))


import plot_util

import plot_template
# print(mpl.rcParams.keys())

# Settings
cm                = 1/2.54
FIG_WIDTH         = 7.5 * cm # Full DIN A4 width

pplot = plot_template.Paper_Plot(FIG_WIDTH)
pplot.ncols = 1
pplot.nrows = 3
pplot.horizontal_margins = [0.175, 0.01]
pplot.vertical_margins   = [0.01, 0.01]
pplot.wspace = 0
pplot.hspace = 0.4
pplot.height_ratios = [1, 1, 0.4]

pplot.height_from_aspect_ratio(1.4/(2+pplot.height_ratios[-1]))

fig = pplot.fig()
gs  = pplot.gs()

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
a.legend(loc="lower center", ncol=3, prop={'size': 7},frameon=False)
a.axis("off")  

# fig.legend(loc="lower center", cols=4)
fig.savefig("plot_barriers_v3.png", dpi=300)