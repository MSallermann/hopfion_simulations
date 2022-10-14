from spirit_extras import import_spirit
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(calculation_folder_path, relative_input_path, relative_output_path, idx_image_infile=0, mode="isosurface", view="auto", distance=80, annotate=22):
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

    # The saddle point
    plotter, center, normal = plot_util.get_pyvista_plotter(absolute_input_path, calculation.descriptor["n_cells"], idx_image_infile)
    plotter.background_color = "transparent"

    # Read in the forward and the backward image

    spins_forward  = np.empty((0,0))
    spins_backward = np.empty((0,0))
    spins_middle = np.empty((0,0))
    positions      = np.empty((0,0))

    from spirit import state, io, geometry, system

    with state.State(INPUT_FILE, quiet=True) as p_state:
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        io.image_read( p_state, absolute_input_path, idx_image_inchain=0, idx_image_infile = idx_image_infile-1 )
        spins_backward = np.array(system.get_spin_directions(p_state))

        io.image_read( p_state, absolute_input_path, idx_image_inchain=0, idx_image_infile = idx_image_infile )
        spins_middle = np.array(system.get_spin_directions(p_state))

        io.image_read( p_state, absolute_input_path, idx_image_inchain=0, idx_image_infile = idx_image_infile+1 )
        spins_forward = np.array(system.get_spin_directions(p_state))

        positions = np.array(geometry.get_positions(p_state))

    mode       = spins_forward - spins_backward
    mode_norm  = np.linalg.norm(mode, axis=1)
    mode_scale = 1/np.max(mode_norm) * mode_norm

    positions    = positions[mode_scale > 1e-2]
    mode         = mode[mode_scale > 1e-2]
    spins_middle = spins_middle[mode_scale > 1e-2]

    mode_scale   = mode_scale[mode_scale > 1e-2]

    point_cloud = pv.PolyData(positions)
    point_cloud["spins"]      = spins_middle
    point_cloud["mode"]       = mode
    point_cloud["mode_scale"] = mode_scale
    point_cloud["mode_rgba"]  = plotting.get_rgba_colors( [ m/s for m,s in zip(mode, mode_scale)  ] )

    mode_arrows = pyvista_plotting.arrows_from_point_cloud(point_cloud, factor=1, scale = "mode_scale", orient="mode", geom=pv.Sphere())
    plotter.add_mesh(mode_arrows, {"rgb" : "True", "scalars" : "mode_rgba"})


    clip_cube = pv.Cube(bounds = [32,64,32,64,-1,64] )
    # plotter.add_mesh(clip_cube, {"color":"red", "opacity":0.5})
    mesh_args = plotter.isosurface(0.0, "spins_z")
    mesh_args[0] = mesh_args[0].clip_box( clip_cube )
    mesh_args[1] = {"color" : "black", "opacity" : 0.5}

    plot_util.set_view(plotter, center, normal, distance, view)
    plotter.rotate_camera([0,0,1], -np.pi/4)
    plotter.align_camera_up(normal)

    if not os.path.exists(os.path.dirname(absolute_output_path)):
        os.makedirs(os.path.dirname(absolute_output_path))

    plotter.render_to_png( absolute_output_path )

    if annotate>0:
        plot_util.annotate_params(absolute_output_path + ".png", gamma = calculation.descriptor["gamma"], r0 = calculation.descriptor["l0"], fontsize=annotate)

    calculation.to_json()
    print(f"Output to: {absolute_output_path + '.png'}")


if __name__ == "__main__":
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    # parser.add_argument("-what", help = "what to plot. either 'hopfion' or 'sp'", required=True, type=str, default="sp")
    parser.add_argument("-mode", help = "what to plot. one of [isosurface, cross_section_ip, cross_section_oop]", required=True, type=str, default="isosurface")
    parser.add_argument("-view", help = "from which view to plot. one of [hopfion_normal, hopfion_inplane, hopfion_diagonal]", required=True, type=str, default="auto")
    parser.add_argument("-distance", help = "distance of camera to hopfion center", required=False, type=float, default=80)
    parser.add_argument('-annotate', help = "annotation fontsiye, 0 disables anntotation", required=False, type=int, default=18)


    args = parser.parse_args()
    print(args.mode)

    for f in args.paths:
        calc = calculation_folder.calculation_folder(f)
        if calc.descriptor["max_angle_between_neighbours"] < 1e-3:
            continue
        # if args.what.lower() == "sp":
        inputpath = calc.descriptor["saddlepoint_chain_file"]
        idx_image = calc.descriptor["idx_sp"]
        outputpath = f"mode_{args.mode}_{args.view}"
        # elif args.what.lower() == "hopfion":
        #     inputpath = calc.descriptor["initial_chain_file"]
        #     outputpath = f"{args.what}_{args.mode}_{args.view}"
        #     idx_image = 0
        # else:
        #     raise Exception("Unknown -what argument. Choose either 'sp' or 'hopfion'")

        main(f, inputpath, outputpath, idx_image, args.mode, args.view, args.distance, args.annotate)
