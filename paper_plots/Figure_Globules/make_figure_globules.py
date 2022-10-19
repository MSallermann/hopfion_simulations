import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))
import plot_util

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

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

p2 = plot_data()
p2.gamma = 0.857
p2.l0 = 5.0
p2.globule_idx = 32


for i, p in enumerate([p1,p2]):
    from spirit_extras.plotting import Paper_Plot
    pplot = Paper_Plot( 11 * Paper_Plot.cm  )
    pplot.nrows = 3
    pplot.ncols = 2
    pplot.vertical_margins   = [0.025, 0.025]
    pplot.horizontal_margins = [0.025, 0.025]
    pplot.height_ratios = [0.1, 1, 1]
    pplot.height_from_aspect_ratio( 1/1.1 )

    gamma = p.gamma 
    l0    = p.l0 

    BASE_PATH = "/home/moritz/hopfion_simulations/all_sp"
    calculation_path = os.path.join(BASE_PATH, f"gamma_{gamma:.3f}_l0_{l0:.3f}")

    # Render surfaces and copy data
    import render_surfaces
    # render_surfaces.render_globule(p.globule_idx, calculation_path)

    fig = pplot.fig()
    gs = pplot.gs()

    # a = fig.add_subplot(gs[0,:])

    # Draw some spines
    a = pplot.spine_axis(gs[1,0], color="lightgray")
    a = pplot.spine_axis(gs[1,1], color="lightgray")
    a = pplot.spine_axis(gs[2,0], color="lightgray")
    a = pplot.spine_axis(gs[2,1], color="lightgray")
    a = pplot.spine_axis(gs[:,:])
    a = pplot.spine_axis(gs[0,:])

    a.text(0.5, 0.5, plot_util.gamma_r0_string(gamma, l0), fontsize=8, horizontalalignment="center", verticalalignment="center" )

    # pplot.annotate(a, rf"$\gamma = {gamma:.3f}, r_0 = {l0:.3f} a$")

    # gs = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 

    NAME = f"{p.globule_idx}_{gamma:.3f}_{l0:.3f}"

    a = fig.add_subplot(gs[1,0])
    pplot.annotate(a, "(a)", pos=[0.025,1])
    plot_path = os.path.join(SCRIPT_DIR, "renderings", f"globule_iso_{NAME}.png")
    pplot.image_to_ax(a, plot_path)

    a = fig.add_subplot(gs[1,1])
    pplot.annotate(a, "(b)", pos=[0.025,1])
    plot_path = os.path.join(SCRIPT_DIR, "renderings", f"globule_oop_{NAME}.png")
    pplot.image_to_ax(a, plot_path)

    a = fig.add_subplot(gs[2,0])
    pplot.annotate(a, "(c)", pos=[0.025,1])
    plot_path = os.path.join(SCRIPT_DIR, "renderings", f"globule_schematic_{NAME}.png")
    pplot.image_to_ax(a, plot_path)

    a = fig.add_subplot(gs[2,1])
    pplot.annotate(a, "(d)", pos=[0.025,1])
    plot_path = os.path.join(SCRIPT_DIR, "renderings", f"globule_ip_{NAME}.png")
    pplot.image_to_ax(a, plot_path)

    # print(mpl.rcParams.keys())
    print( f"plot_globules_{gamma:.3f}_{l0:.3f}.png" )
    fig.savefig(f"plot_globules_{gamma:.3f}_{l0:.3f}.png", dpi=300)