from spirit_extras.plotting import Paper_Plot
from spirit_extras.calculation_folder import Calculation_Folder
import numpy as np
import shutil

def main(paths, renderings_base_path, relative_input_path, idx_image, image_name="rendering.png", grid_image_output="grid.png"):

    data_list = []

    # First step is to go over all possible data paths, collect and render the images if necessary
    for path in paths:
        base_path  = os.path.basename(path)
        image_path = os.path.join( renderings_base_path, base_path, image_name )

        calc = Calculation_Folder(path, descriptor_file="params.json")
        chain_path = calc.format(relative_input_path)
        if type(idx_image) is int:
            idx_image_cur = idx_image
        elif type(idx_image) is str:
            idx_image_cur = int( calc.format(idx_image) )

        print(f"===")
        print(f"path                = {path}")
        print(f"base_path           = {base_path}")
        print(f"image_path          = {image_path}")
        print(f"relative_input_path = {relative_input_path}")
        print(f"chain_path          = {chain_path}")
        print(f"idx_image           = {idx_image}")
        print(f"idx_image_cur       = {idx_image_cur}")

        if not os.path.exists(image_path):
            import plot_spin_configuration
            if not os.path.exists( os.path.dirname(image_path) ):
                os.makedirs( os.path.dirname(image_path) )
            print(f"RENDERING new image for {image_path}")

            rendering_input_path  = chain_path
            rendering_output_path = calc.to_relpath(image_path)
            print(os.path.splitext(rendering_output_path)[0])

            # Have to remove the .png ending here since pyvista is stupid like that
            temp_path, ext = os.path.splitext(rendering_output_path)

            plot_spin_configuration.main(path, rendering_input_path, temp_path, idx_image_infile=idx_image_cur, annotate=0)
            print("... done")
        else:
            print("Rendering exists")

        data_list.append( [calc["gamma"], calc["l0"], image_path] )

    # Turn data list into array
    data_list = np.array(data_list)

    # Lists of uniqe gamma and l0 in increasing order, have to convert them to float since they are actually strings here
    gamma_list = np.sort( np.unique( [float(f) for f in data_list[:,0]]) )
    l0_list    = np.sort( np.unique( [float(f) for f in data_list[:,1]]) )

    shape_grid = (len(l0_list), len(gamma_list))

    pplot = Paper_Plot(Paper_Plot.cm * 17)
    pplot.nrows = shape_grid[0]
    pplot.ncols = shape_grid[1]
    pplot.vertical_margins   = [0.1, 0.05]
    pplot.horizontal_margins = [0.1, 0.05]

    pplot.height_from_aspect_ratio(pplot.ncols / pplot.nrows )

    fig = pplot.fig()
    gs  = pplot.gs()

    print(f"gamma_list = {gamma_list}, {len(gamma_list)}")
    print(f"l0_list    = {l0_list},    {len(l0_list)}")

    # We draw a coordinate frame around the image grid
    ax_frame = fig.add_subplot(gs[:,:])

    _max = np.max(l0_list)
    _min = np.min(l0_list)
    _range = _max - _min
    ax_frame.set_ylim( _min - 0.5*_range/(pplot.nrows), _max + 0.5*_range/(pplot.nrows) )
    ax_frame.set_ylabel( r"$r_0~[a]$" )

    _max = np.max(gamma_list)
    _min = np.min(gamma_list)
    _range = _max - _min
    ax_frame.set_xlim( _min - 0.5*_range/(pplot.ncols), _max + 0.5*_range/(pplot.ncols) )

    # nice labels for gamma
    xtick_labels = [ f"{i}/7" for i in range(8)]
    xtick_labels[0]  = "0"
    xtick_labels[-1] = "1"

    ax_frame.tick_params(right=True, top=True, labelright=True, labeltop=True, labelrotation=0)
    ax_frame.set_xticks( [ i/7.0 for i in range(8)] )
    ax_frame.set_xticklabels( xtick_labels )
    ax_frame.set_xlabel(r"$\gamma$")

    for d in data_list:
        if not os.path.exists(d[2]):
            continue

        gamma = float(d[0])
        l0    = float(d[1])

        col = np.argwhere( gamma_list == gamma )[0,0]
        row = pplot.nrows-1 - np.argwhere( l0_list == l0 )[0,0]

        ax = fig.add_subplot(gs[row, col])

        image = plt.imread(d[2])

        image_height = image.shape[0] # remember: height comes first
        image_cropped = pplot.crop(image, width=image_height) # Crop image to be square, by adjusting the width
        pplot.image_to_ax(ax, image_cropped)

    fig.savefig(grid_image_output, dpi=300)
    # plt.show()

import calculation_folder
import glob
import argparse, os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("paths",      type=str, nargs="+")
parser.add_argument("-o",         help = "base folder to output renderings to", required=True, type=str)
parser.add_argument("-i",         help = "relative path to input ovf file", required=True, type=str)
parser.add_argument("--idx_image", help = "idx of image in input ovf file", required=True, type=str)
parser.add_argument("-n",         help = "name of the rendered image file", required=True, type=str)
parser.add_argument("--output",    help = "name of the rendered image file", required=True, type=str)


args = parser.parse_args()

main(args.paths, renderings_base_path=args.o, relative_input_path=args.i, idx_image=args.idx_image, image_name=args.n, grid_image_output=args.output)