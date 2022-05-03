def main(paths):
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import ImageGrid

    data_list = []

    for path in paths:
        print(path)
        calculation = calculation_folder.calculation_folder(path)
        gamma = calculation.descriptor["gamma"]
        l0    = calculation.descriptor["l0"]
        path_image = glob.glob(os.path.join(path, "saddlepoint*.png"))

        if len(path_image) < 1:
            continue
        else:
            path_image = path_image[0]

        # img = plt.imread(path_image)
        data_list.append([gamma, l0, path_image])

    data_list = np.array(data_list)

    gamma_list = np.sort( np.unique(data_list[:,0]) )
    l0_list = np.sort( np.unique(data_list[:,1]) )

    shape_grid = (len(gamma_list), len(l0_list))

    fig = plt.figure(figsize=(16., 16.))
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                    nrows_ncols=shape_grid,  # creates 2x2 grid of axes
                    axes_pad=0.1,  # pad between axes in inch.
                    share_all=True
                    )

    for a in grid:
        a.axis("off")
        a.axis("off")

    for d in data_list:
        row = len(l0_list)-1 - np.where(l0_list == d[1] )[0][0]
        col = np.where(gamma_list == d[0] )[0][0]
        idx_grid = row * len(gamma_list) + col
        image = plt.imread(d[2])
        ax = grid[idx_grid]
        ax.imshow(image)
        plt.gca().axis('off')

    plt.savefig("sp_grid.png", dpi=300)
    plt.show()

import calculation_folder
import glob
import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("paths", type=str, nargs="+")
args = parser.parse_args()

main(args.paths)