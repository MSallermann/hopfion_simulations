from spirit_extras import import_spirit
import matplotlib.pyplot as plt
import numpy as np
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
DELAUNAY_PATH = os.path.join(SCRIPT_DIR, "delaunay32.vtk")
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "plots")

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
# OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "plots")

def main(path):

    calculation = calculation_folder.calculation_folder(path)
    chain_file  = calculation.to_abspath( "initial_chain.ovf" )

    gamma = calculation.descriptor["gamma"]
    l0    = calculation.descriptor["l0"]
    n_cells    = calculation.descriptor["n_cells"]


    plot_name  = f"initial_hopfion_gamma_{gamma:.3f}_r0_{l0:.3f}"

    from spirit import state, io, geometry
    from spirit_extras import data, pyvista_plotting

    with state.State(INPUT_FILE) as p_state:
        geometry.set_n_cells(p_state, n_cells)
        io.image_read(p_state, chain_file, idx_image_infile=0, idx_image_inchain=0)
        system = data.spin_system_from_p_state(p_state)

        # Create plotter
        plotter = pyvista_plotting.Spin_Plotter(system)

        # plotter.camera_position = 'xy'
        # plotter.camera_azimuth   = 45
        # plotter.camera_elevation = 50

        if os.path.exists(DELAUNAY_PATH):
            plotter.load_delaunay(DELAUNAY_PATH)
        else:
            plotter.compute_delaunay()
            plotter.save_delaunay(DELAUNAY_PATH)

        plotter.isosurface(0, "spins_z")
        # plotter.show(save_camera_file="camera.json")
        plotter.camera_from_json("camera.json")
        plotter.render_to_png(os.path.join(OUTPUT_FOLDER, plot_name) )

if __name__ == "__main__":

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_3img", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()



    for f in args.paths:
        main(f)