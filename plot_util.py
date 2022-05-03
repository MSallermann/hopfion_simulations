def annotate_params(path_to_png, gamma, r0, dpi=300):
    import matplotlib.pyplot as plt
    dpi = 300
    img = plt.imread(path_to_png)
    height, width, depth = img.shape
    figsize = width / float(dpi), height / float(dpi)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.text(0, 1, rf"$\gamma = {gamma:.2f}$  $r_0 = {r0:.2f}\,a$", fontsize = 18, bbox = dict(facecolor='white', edgecolor="white", alpha=0.80), horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    ax.axis('off')
    ax.imshow(img)
    fig.savefig(path_to_png, dpi=300, bbox_inches=0, pad_inches = 0)