from spirit_extras import import_spirit, post_processing, plotting
import matplotlib.pyplot as plt
import numpy as np
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
DELAUNAY_PATH = os.path.join(SCRIPT_DIR, "delaunay64.vtk")
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "plots")

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

import plot_util

def main(path):
    print(path)

    calculation = calculation_folder.calculation_folder(path)
    gamma   = calculation.descriptor["gamma"]
    l0      = calculation.descriptor["l0"]
    n_cells = calculation.descriptor["n_cells"]

    if calculation.descriptor["max_angle_between_neighbours"] < 1e-2:
        return

    chain_file = os.path.join(path, "initial_chain.ovf")

    plot_name  = f"initial_hopfion_gamma_{gamma:.3f}_r0_{l0:.3f}"
    plot_path = os.path.join(calculation.output_folder, plot_name)

    plotter = plot_util.get_pyvista_plotter(chain_file, n_cells, idx_image_infile=0)

    # plot_util.add_preimages(plotter)
    plotter.isosurface(0.0, "spins_z")
    # plotter.isosurface(0.9, "spins_x")
    # plotter.show( )

    plotter.render_to_png( plot_path )
    plot_util.annotate_params(plot_path + ".png", gamma = gamma, r0 = l0)

if __name__ == "__main__":

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True)[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    for f in args.paths:
        main(f)