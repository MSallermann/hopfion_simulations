import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))
sys.path.insert(0, os.path.join(SCRIPT_DIR, ".."))

import plot_template

cm                = 1/2.54
FIG_WIDTH         = 17.5 * cm # Full DIN A4 width

pplot = plot_template.Paper_Plot(FIG_WIDTH)
pplot.ncols              = 3
pplot.nrows              = 2
pplot.horizontal_margins = [0.055, 0.0]
pplot.vertical_margins   = [0.14, 0.05]
pplot.wspace             = 0.05
pplot.hspace             = 0.0
pplot.width_ratios       = [4,1,1]
pplot.height_ratios      = None

pplot.height_from_aspect_ratio(12/4)

fig = pplot.fig()
gs  = pplot.gs()

# Criterion gridspec
gs0 = GridSpecFromSubplotSpec(5, 8, subplot_spec=gs[:,0], hspace=0.0, wspace=0.0)

# Frame around plot and isosurfaces
a = pplot.spine_axis( gs0[:,:] )
pplot.annotate(a, "(a)", pos=(-0.05, 1.0))

NAME = "hopfion_isosurface_hopfion_normal"
SUFFIX = "80"

# Surfaces top
for col,a in enumerate(pplot.row(0, gs=gs0)):
    gamma = float(1/7*col)
    l0    = float(5.00)
    file = os.path.join(SCRIPT_DIR, "renderings", NAME +  f"_{gamma:.3f}_{l0:.3f}_{SUFFIX}.png")
    pplot.image_to_ax(a, file)

# # Surfaces right
for row,a in enumerate(pplot.col(-1, slice(1,None,None), gs=gs0)):
    gamma = float( 1 )
    l0    = float( 5 - (row+1) * 0.5 )
    file = os.path.join(SCRIPT_DIR, "renderings", NAME +  f"_{gamma:.3f}_{l0:.3f}_{SUFFIX}.png")
    print(file)
    pplot.image_to_ax(a, file)
    # a.axis("off")

# Criteron plot
a = fig.add_subplot(gs0[1:,0:-1], zorder=999)
a.spines["top"].set_visible(False)
a.spines["right"].set_visible(False)
a.set_xmargin(0.03)
a.set_ymargin(0.028)
import plot_criterion
plot_criterion.main(np.loadtxt("criterion_data.txt"), a)

a = fig.add_subplot(gs[0,1])
pplot.annotate(a, "(b)")
path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_cross_section_ip_hopfion_inplane_0.857_5.000.png")
pplot.image_to_ax(a, path)

a = fig.add_subplot(gs[0,2])
pplot.annotate(a, "(c)")
path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_cross_section_oop_hopfion_normal_0.857_5.000.png")
pplot.image_to_ax(a, path)

a = fig.add_subplot(gs[1,1])
pplot.annotate(a, "(d)")
path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_preimages_hopfion_diagonal_0.857_5.000.png")
pplot.image_to_ax(a, path)

a = fig.add_subplot(gs[1,2])
pplot.annotate(a, "(e)")
path = os.path.join(SCRIPT_DIR, "renderings", "color_sphere.png")
pplot.image_to_ax(a, path)

fig.savefig("plot1_v4.png", dpi=300)