# importing required library
import matplotlib.pyplot as plt
import numpy as np
import os

BASE_DIR = "all_sp"
NAME     = "hopfion_isosurface_hopfion_diagonal.png"
SHAPE    = (4, 8)

# creating grid for subplots
fig = plt.figure()
base_size = 6
fig.set_figheight( base_size )
fig.set_figwidth(  base_size * 1.40)

# axes = []
a =  plt.subplot2grid(shape=SHAPE, loc=(0, 0), rowspan=3, colspan=7 )
image = plt.imread("stability_criterion.png")
a.axis("off")
a.imshow(image)

# Bottom row
r0 = 3.0
row = SHAPE[0] - 1
for i,gamma in enumerate(np.arange(0,1+1/7,1/7)):
    file = os.path.join(BASE_DIR, f"gamma_{gamma:.3f}_l0_{r0:.3f}", NAME)
    a = plt.subplot2grid(shape=SHAPE, loc=(row, i), rowspan=1, colspan=1 )
    image = plt.imread(file)
    a.axis("off")
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)
    a.imshow(image)

# right column
gamma = 1.0
col = SHAPE[1] - 1
for i,r0 in enumerate(np.arange(3.0, 5.0, 0.5)[::-1]):
    file = os.path.join(BASE_DIR, f"gamma_{gamma:.3f}_l0_{r0:.3f}", NAME)
    a = plt.subplot2grid(shape=SHAPE, loc=(i, col), rowspan=1, colspan=1 )
    image = plt.imread(file)
    a.axis("off")
    a.imshow(image)



# ax2 = plt.subplot2grid(shape=(6,6), loc=(1, 0), colspan=1)
# ax3 = plt.subplot2grid(shape=(6,6), loc=(1, 2), rowspan=2)
# ax4 = plt.subplot2grid(shape=(6,6), loc=(2, 0))
# ax5 = plt.subplot2grid(shape=(6,6), loc=(2, 1), colspan=1)

# plotting subplots
# ax1.plot(x, y)
# ax1.set_title('ax1')
# ax2.plot(x, y)
# ax2.set_title('ax2')
# ax3.plot(x, y)
# ax3.set_title('ax3')
# ax4.plot(x, y)
# ax4.set_title('ax4')
# ax5.plot(x, y)
# ax5.set_title('ax5')

# automatically adjust padding horizontally
# as well as vertically.
# plt.gcf().subplots_adjust(bottom=0, top=1, left=0, right=1)

plt.tight_layout()

plt.savefig("plot1.png", dpi=500, bbox_inches="tight", pad_inches=0)