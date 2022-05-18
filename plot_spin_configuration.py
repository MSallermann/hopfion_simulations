from spirit_extras import import_spirit
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(calculation_folder_path, relative_input_path, relative_output_path, idx_image_infile=0, mode="isosurface", view="auto"):
    # Read calculation folder from input path, and get the absolute input and output paths
    calculation          = calculation_folder.calculation_folder(calculation_folder_path)
    absolute_input_path  = calculation.to_abspath(relative_input_path)
    absolute_output_path = calculation.to_abspath(relative_output_path)

    print(f"Input:   {absolute_input_path}")
    print(f"Output:  {absolute_output_path}")

    # DO STUFF HERE
    print(mode.lower())
    known_modes = ["isosurface", "cross_section_ip", "cross_section_oop"]
    if mode.lower() not in known_modes:
        raise Exception(f"Unknown mode: {mode.lower()}\nKnown modes {known_modes}\n")

    known_views = ["hopfion_normal", "hopfion_inplane", "hopfion_diagonal", "auto"]
    if view.lower() not in known_views:
        raise Exception(f"Unknown view: {view.lower()}\nKnown views {known_views}\n")

    if view.lower() == "auto":
        if mode.lower() == "cross_section_ip":
            view = "hopfion_inplane"
        else:
            view = "hopfion_normal"

    from spirit_extras import import_spirit, post_processing, pyvista_plotting, plotting
    import plot_util
    import numpy as np
    import pyvista as pv

    plotter, center, normal = plot_util.get_pyvista_plotter(absolute_input_path, calculation.descriptor["n_cells"], idx_image_infile)
    plotter.background_color = "white"

    if mode.lower() == "isosurface":
        plotter.isosurface(0.0, "spins_z")

    elif mode.lower() == "cross_section_ip":
        plane_normal = np.cross(normal, [1,0,0])
        plane_normal /= np.linalg.norm(plane_normal)
        plane        = pv.Plane(center, plane_normal, 60, 60, 80, 80)
        plane        = plane.interpolate(plotter._point_cloud, radius=1.5)
        # plotter.add_mesh(plane.copy().translate(-0.5 * plane_normal), {**plotter.default_render_args, "opacity" : 0.25})

        plane_arrows = pyvista_plotting.arrows_from_point_cloud(plane, factor=0.6)
        plotter.add_mesh(plane_arrows, {**plotter.default_render_args})

        # Clipped black isosurface
        mesh_args       = plotter.isosurface(0.0, "spins_z")
        isosurface_copy = mesh_args[0].copy()
        mesh_args[0]    = mesh_args[0].clip(plane_normal, center, value=-0.5)
        mesh_args[1]    = {"color" : "black", "opacity" : 0.75}

        plotter.add_mesh(isosurface_copy.clip(plane_normal, center, value=-0.25, invert=False).clip(plane_normal, center, value=0.25, invert=True), {"color" : "black", "opacity" : 1, "line_width" : 20})

    elif mode.lower() == "cross_section_oop":
        plane_normal = normal
        plane_normal /= np.linalg.norm(plane_normal)

        plane        = pv.Plane(center, plane_normal, 60, 60, 80, 80)
        plane        = plane.interpolate(plotter._point_cloud, radius=1.5)

        # plotter.add_mesh(plane.copy().translate(-0.5 * plane_normal), {**plotter.default_render_args, "opacity" : 0.25})

        plane_arrows = pyvista_plotting.arrows_from_point_cloud(plane, factor=0.6)
        plotter.add_mesh(plane_arrows, {**plotter.default_render_args})

        # Clipped black isosurface
        mesh_args       = plotter.isosurface(0.0, "spins_z")
        isosurface_copy = mesh_args[0].copy()
        mesh_args[0]    = mesh_args[0].clip(plane_normal, center, value=-0.5)
        mesh_args[1]    = {"color" : "black", "opacity" : 0.75}
        plotter.add_mesh(isosurface_copy.clip(plane_normal, center, value=-0.25, invert=False).clip(plane_normal, center, value=0.25, invert=True), {"color" : "black", "opacity" : 1, "line_width" : 20})

    plot_util.set_view(plotter, center, normal, 80, view)

    if not os.path.exists(os.path.dirname(absolute_output_path)):
        os.makedirs(os.path.dirname(absolute_output_path))

    plotter.render_to_png( absolute_output_path )
    plot_util.annotate_params(absolute_output_path + ".png", gamma = calculation.descriptor["gamma"], r0 = calculation.descriptor["l0"])

    calculation.to_json()

if __name__ == "__main__":
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-i",    help = "input path, relative to calculation folder" , required=True, type=str)
    parser.add_argument("-o",    help = "output path, relative to calculation folder", required=True, type=str)
    parser.add_argument("-mode", help = "what to plot", required=True, type=str, default="isosurface")
    parser.add_argument("-view", help = "from which view to plot", required=True, type=str, default="auto")
    parser.add_argument("-idx_image", help = "idx of the image in the chain file that is plotted", required=True, type=int)
    parser.add_argument('-MPI',  help = "speed up loop over folders with MPI (useful when wildcards are used to specify multiple calculation folders)", action='store_true')

    args = parser.parse_args()
    print(args.mode)
    if not args.MPI:
        for f in args.paths:
            main(f, args.i, args.o, args.idx_image, args.mode, args.view)
    else:
        from mpi_loop import mpi_loop

        def callable(i):
            input_path = args.paths[i]
            main(input_path, args.i, args.o, args.idx_image, args.mode, args.view)

        mpi_loop(callable, len(args.paths))