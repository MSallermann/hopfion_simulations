import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec
import matplotlib as mpl
import numpy as np

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

print(mpl.rcParams.keys())

mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),

plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes',  labelsize=8)

# Settings
cm                = 1/2.54
FIG_WIDTH         = 21.0 * cm # Full DIN A4 width
FIG_HEIGHT        = FIG_WIDTH / 1.618 # Golden ratio
HORIZONTAL_MARGIN = 0.1
VERTICAL_MARGIN   = 0.1
WSPACE            = 0.2
HSPACE            = 0.3
WIDTH_RATIOS      = [2, 1]
HEIGHT_RATIOS     = [2, 1]

x = np.linspace(0, 100, 100)
y = x**2

fig = plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))
gs  = GridSpec(nrows=2, ncols=2, left=HORIZONTAL_MARGIN, bottom=VERTICAL_MARGIN, right=1-HORIZONTAL_MARGIN, top=1-VERTICAL_MARGIN, hspace=HSPACE, wspace=WSPACE, width_ratios=WIDTH_RATIOS, height_ratios=HEIGHT_RATIOS) 

ax0 = fig.add_subplot(gs[0, 0])
ax0.set_xlabel("x")
ax0.plot(x,y)

# Second axes
ax1 = fig.add_subplot(gs[1, 0])
ax1.plot(x,y)

ax2 = fig.add_subplot(gs[:, 1])
ax2.plot(x,y)

# ax2 = fig.add_axes([0.7, 0.5, 0.5, 0.1])
# ax2.plot(x,y)

fig.savefig("test_plot.png")