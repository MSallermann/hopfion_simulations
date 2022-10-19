import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np
from matplotlib.patches import Rectangle, ConnectionPatch

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))
import plot_util

from plot_template import Paper_Plot

def render(output_directory):
    pass

pplot = Paper_Plot(17.5 * Paper_Plot.cm)
pplot.nrows = 1
pplot.ncols = 3
pplot.wspace = 0.05
pplot.horizontal_margins[0] = 0.01
pplot.horizontal_margins[1] = 0.01
pplot.vertical_margins[0]   = 0.01
pplot.vertical_margins[1]   = 0.01

RATIO_SUPTITLE = 0.15
pplot.height_from_aspect_ratio(6 / (2 + RATIO_SUPTITLE))

fig    = pplot.fig()
gs_all = pplot.gs()

gamma_l0_list =  [
    [0, 3.0],
    [0.857, 5.00],
    [1, 5.00]
]

for col,(gamma,l0) in enumerate(gamma_l0_list):
    SUFFIX = f"_{gamma:.3f}_{l0:.3f}.png"
    gs = GridSpecFromSubplotSpec(3,2,gs_all[0,col], hspace=0.0, wspace=0.0)
    height_ratios = np.ones(gs.nrows)
    height_ratios[0] = RATIO_SUPTITLE
    gs.set_height_ratios(height_ratios)

    a = fig.add_subplot(gs[0,:])
    a.text(0.5, 0.5, plot_util.gamma_r0_string(gamma, l0), fontsize=8, horizontalalignment="center", verticalalignment="center" )
    a.axis("off")

    NAME = "hopfion_isosurface_hopfion_diagonal"
    a = fig.add_subplot(gs[1,0])
    pplot.annotate(a, "Hopfion", pos=[0.03, 0.98], fontsize=8)
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    pplot.image_to_ax(a, path)

    NAME = "sp_isosurface_hopfion_diagonal"
    a = fig.add_subplot(gs[1,1])
    pplot.annotate(a, "Saddle point", pos=[0.03, 0.98], fontsize=8)
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    pplot.image_to_ax(a, path)

    NAME = "hopfion_cross_section_ip_hopfion_inplane"
    a = fig.add_subplot(gs[2,0])
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    pplot.image_to_ax(a, path)

    NAME = "sp_cross_section_ip_hopfion_inplane"
    a = fig.add_subplot(gs[2,1])
    path = os.path.join(SCRIPT_DIR, "renderings", NAME + f"_{gamma:.3f}_{l0:.3f}.png")
    pplot.image_to_ax(a, path)

    pplot.spine_axis(gs[0,:], color="black", which=["bottom"])
    pplot.spine_axis(gs[1:,0], color="lightgray", which=["right"])
    pplot.spine_axis(gs[:,:])

fig.savefig("plot2_v3.png", dpi=300)