import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

# print(mpl.rcParams.keys())

# mpl.rcParams["font.size"]       = 12 #'dejavusans' (default),
mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 17.5 * cm # Full DIN A4 width
FIG_HEIGHT        = FIG_WIDTH / 2.218 # Golden ratio

NCOLS = 4
NROWS = 2
HORIZONTAL_MARGINS = [0.055, 0.0]
VERTICAL_MARGINS  = [0.12, 0.05]
WSPACE            = 0.05
HSPACE            = 0.05
WIDTH_RATIOS      = [2,2,1,1]
HEIGHT_RATIOS     = None

def annotate(ax, text, pos = [0,1], fontsize=8):
    ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

def image_to_ax(ax, path):
    image = plt.imread(path)
    ax.imshow(image)
    # a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)
    ax.axis("off")

fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))
gs  = GridSpec(figure=fig, nrows=NROWS, ncols=NCOLS, left=HORIZONTAL_MARGINS[0], bottom=VERTICAL_MARGINS[0], right=1-HORIZONTAL_MARGINS[1], top=1-VERTICAL_MARGINS[1], hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 
# gs.set_width_ratios([2, 1])

# Criterion gridspec
gs0 = GridSpecFromSubplotSpec(5, 8, subplot_spec=gs[0:,0:2], hspace=0.0, wspace=0.0)

# Frame around plot and isosurfaces
a = fig.add_axes( gs0[:,:].get_position(fig) )
a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)
annotate(a, "(a)", pos=(-0.05, 1.0))

# a = fig.add_axes(outer_gs[0,0])

# Criteron plot
a = fig.add_subplot(gs0[1:,0:-1])
a.spines["top"].set_visible(False)
a.spines["right"].set_visible(False)
a.set_xmargin(0.035)
a.set_ymargin(0.025)
import plot_criterion
plot_criterion.main(np.loadtxt("criterion_data.txt"), a)

NAME = "hopfion_isosurface_hopfion_normal"
SUFFIX = "80"

# Surfaces top
for col in range(gs0.ncols):
    a = fig.add_subplot(gs0[0,col])
    gamma = float(1/7*col)
    l0    = float(5.00)
    file = os.path.join(SCRIPT_DIR, "renderings", NAME +  f"_{gamma:.3f}_{l0:.3f}_{SUFFIX}.png")
    image_to_ax(a, file)

# Surfaces right
for row in range(1,5):
    a = fig.add_subplot(gs0[row, gs0.ncols-1])
    gamma = float( 1 )
    l0    = float( 5 - (row) * 0.5 )
    file = os.path.join(SCRIPT_DIR, "renderings", NAME +  f"_{gamma:.3f}_{l0:.3f}_{SUFFIX}.png")
    image_to_ax(a, file)
    # a.axis("off")

a = fig.add_subplot(gs[0,2])
annotate(a, "(b)")
path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_cross_section_ip_hopfion_inplane_0.857_5.000.png")
image_to_ax(a, path)

a = fig.add_subplot(gs[0,3])
annotate(a, "(c)")
path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_cross_section_oop_hopfion_normal_0.857_5.000.png")
image_to_ax(a, path)

a = fig.add_subplot(gs[1,2])
annotate(a, "(d)")
path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_preimages_hopfion_diagonal_0.857_5.000.png")
image_to_ax(a, path)

a = fig.add_subplot(gs[1,3])
annotate(a, "(e)")
path = os.path.join(SCRIPT_DIR, "renderings", "color_sphere.png")
image_to_ax(a, path)

# #################################
# # Colorsphere
# #################################
# print(gs[1:,.1:])

# a = fig.add_axes([0.2,-0.1,0.6,0.6], label="sdd")



#################################
# Plot of stability criterion
#################################
# height_ratios = [1,1,1,1,0.3,1]

# gs00 = GridSpecFromSubplotSpec(6, 8, subplot_spec=gs[0:2,0:2], hspace=0.25, wspace=0.0, height_ratios=height_ratios)

# ax0 = fig.add_subplot(gs00[:-2, :-1])
# import plot_criterion
# annotate(ax0, "(a)", [-0.1,1.00])
# plot_criterion.main(np.loadtxt("criterion_data.txt"), ax0)

# NAME = "hopfion_isosurface_hopfion_normal"

# # Left column
# for i in range(4):
#     a = fig.add_subplot(gs00[i,-1])
#     gamma = float(1.00)
#     l0    = float(5.00 - 0.5*i)
#     file = os.path.join(SCRIPT_DIR, "renderings", NAME +  f"_{gamma:.3f}_{l0:.3f}.png")
#     image_to_ax(a, file)

# # Bottom row
# for i in range(8):
#     a = fig.add_subplot(gs00[-1,i])
#     gamma = float(i*1/7)
#     l0    = float(3.00)
#     file = os.path.join(SCRIPT_DIR, "renderings", NAME +  f"_{gamma:.3f}_{l0:.3f}.png")
#     image_to_ax(a, file)

# #################################
# # Plot schematic
# #################################
# a    = fig.add_subplot(gs[0, 3])
# annotate(a, "(c)")
# path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_schematic_hopfion_diagonal_0.857_5.000.png")
# image_to_ax(a, path)
# # ax1.plot(x,y)

# #################################
# # Plot cross section ip
# #################################
# a = fig.add_subplot(gs[1, 3])
# annotate(a, "(e)")
# path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_cross_section_ip_hopfion_inplane_0.857_5.000.png")
# image_to_ax(a, path)

# #################################
# # Plot cross section oop
# #################################
# a = fig.add_subplot(gs[1, 2])
# annotate(a, "(d)")
# path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_cross_section_oop_hopfion_normal_0.857_5.000.png")
# image_to_ax(a, path)

# #################################
# # Plot cross section oop
# #################################
# a = fig.add_subplot(gs[0, 2])
# annotate(a, "(b)")
# path = os.path.join(SCRIPT_DIR, "renderings", "hopfion_preimages_hopfion_diagonal_0.857_5.000.png")
# image_to_ax(a, path)

fig.savefig("plot1_v3.png", dpi=300)