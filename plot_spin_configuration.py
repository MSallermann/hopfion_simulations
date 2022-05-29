from spirit_extras import import_spirit
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(calculation_folder_path, relative_input_path, relative_output_path, idx_image_infile=0, mode="isosurface", view="auto", distance=80, annotate=22, absolute_paths=False):

    # Read calculation folder from input path, and get the absolute input and output paths
    calculation          = calculation_folder.calculation_folder(calculation_folder_path)

    if absolute_paths:
        absolute_input_path  = relative_input_path
        absolute_output_path = relative_output_path
    else:
        absolute_input_path  = calculation.to_abspath(relative_input_path)
        absolute_output_path = calculation.to_abspath(relative_output_path)

    print(f"Input:   {absolute_input_path}")
    print(f"Output:  {absolute_output_path}")

    # DO STUFF HERE
    print(mode.lower())
    known_modes = ["isosurface", "cross_section_ip", "cross_section_oop", "schematic"]
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

    plotter, center, normal  = plot_util.get_pyvista_plotter(absolute_input_path, calculation.descriptor["n_cells"], idx_image_infile)
    plotter.background_color = "transparent"

    if mode.lower() == "isosurface":
        plotter.isosurface(0.0, "spins_z")

    elif mode.lower() == "cross_section_ip":
        plane_normal = np.cross(normal, [1,0,0])
        plane_normal /= np.linalg.norm(plane_normal)
        plane        = pv.Plane(center, plane_normal, 60, 60, 80, 80)
        plane        = plane.interpolate(plotter._point_cloud, radius=1.5)
        # plotter.add_mesh(plane.copy().translate(-0.5 * plane_normal), {**plotter.default_render_args, "opacity" : 0.25})

        plane_arrows = pyvista_plotting.arrows_from_point_cloud(plane, factor=0.6)

        from spirit_extras import plotting

        # Have to recompute colors after interpolating
        spins = np.zeros(shape=(len( plane_arrows["spins_x"] ), 3))
        spins[:,0] = plane_arrows["spins_x"]
        spins[:,1] = plane_arrows["spins_y"]
        spins[:,2] = plane_arrows["spins_z"]
        plane_arrows["spins_rgba"] = plotting.get_rgba_colors( spins, opacity=1.0 )

        plotter.add_mesh(plane_arrows, {**plotter.default_render_args})
        # plotter.add_mesh(plane_arrows)

        # Clipped black isosurface
        mesh_args       = plotter.isosurface(0.0, "spins_z")
        isosurface_copy = mesh_args[0].copy()
        mesh_args[0]    = mesh_args[0].clip(plane_normal, center, value=-0.5)
        mesh_args[1]    = {"color" : "black", "opacity" : 0.25}

        # plotter.add_mesh(isosurface_copy.clip(plane_normal, center, value=-0.25, invert=False).clip(plane_normal, center, value=0.25, invert=True), {"color" : "black", "opacity" : 1, "line_width" : 20})

    elif mode.lower() == "cross_section_oop":
        plane_normal = normal
        plane_normal /= np.linalg.norm(plane_normal)

        plane        = pv.Plane(center, plane_normal, 60, 60, 80, 80)
        plane        = plane.interpolate(plotter._point_cloud, radius=1.5)

        # plotter.add_mesh(plane.copy().translate(-0.5 * plane_normal), {**plotter.default_render_args, "opacity" : 0.25})

        plane_arrows = pyvista_plotting.arrows_from_point_cloud(plane, factor=0.6)

        spins = np.zeros(shape=(len( plane_arrows["spins_x"] ), 3))
        spins[:,0] = plane_arrows["spins_x"]
        spins[:,1] = plane_arrows["spins_y"]
        spins[:,2] = plane_arrows["spins_z"]
        plane_arrows["spins_rgba"] = plotting.get_rgba_colors( spins, opacity=1.0 )

        plotter.add_mesh(plane_arrows, {**plotter.default_render_args})

        # Clipped black isosurface
        mesh_args       = plotter.isosurface(0.0, "spins_z")
        isosurface_copy = mesh_args[0].copy()
        mesh_args[0]    = mesh_args[0].clip(plane_normal, center, value=-0.25)
        mesh_args[1]    = {"color" : "black", "opacity" : 0.75}

    elif mode.lower() == "schematic":
        mesh_args = plotter.arrows()
        clip_cube = pv.Cube(bounds = [32,64,32,64,-1,64] )
        # plotter.add_mesh(clip_cube, {"color":"red", "opacity":0.5})
        mesh_args[0] = mesh_args[0].clip_box( clip_cube )
        mesh_args = plotter.isosurface(0.0, "spins_z")
        mesh_args[1] = {"color" : "black", "opacity" : 0.75}

        # normal = np.array([1,1,1])

        # # Clipped black isosurface
        # mesh_args       = plotter.isosurface(0.0, "spins_z")
        # isosurface_copy = mesh_args[0].copy()
        # mesh_args[0]    = mesh_args[0].clip(plane_normal, center, value=-0.5)
        # mesh_args[1]    = {"color" : "black", "opacity" : 0.75}

        # plotter.add_mesh(isosurface_copy.clip(plane_normal, center, value=-0.25, invert=False).clip(plane_normal, center, value=0.25, invert=True), {"color" : "black", "opacity" : 1, "line_width" : 20})

    plot_util.set_view(plotter, center, normal, distance, view)

    if mode.lower() == "schematic":
        plotter.rotate_camera([0,0,1], -np.pi/4)

    if view.lower() != "hopfion_normal":
        plotter.align_camera_up(normal)
    else:
        plotter.align_camera_up([1,0,0])

    if not os.path.exists(os.path.dirname(absolute_output_path)):
        os.makedirs(os.path.dirname(absolute_output_path))

    plotter.render_to_png( absolute_output_path )

    if annotate >= 1:
        plot_util.annotate_params(absolute_output_path + ".png", gamma = calculation.descriptor["gamma"], r0 = calculation.descriptor["l0"], fontsize=annotate)

    calculation.to_json()
    print(f"Output to: {absolute_output_path + '.png'}")

if __name__ == "__main__":
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths",     help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-what",     help = "what to plot. either 'hopfion' or 'sp'", required=True, type=str, default="sp")
    parser.add_argument("-mode",     help = "what to plot. one of [isosurface, cross_section_ip, cross_section_oop]", type=str, default="isosurface")
    parser.add_argument("-view",     help = "from which view to plot. one of [hopfion_normal, hopfion_inplane, hopfion_diagonal]", type=str, default="auto")
    parser.add_argument("-distance", help = "distance of camera to hopfion center", required=False, type=float, default=80)
    parser.add_argument('-annotate', help = "annotation fontsiye, 0 disables anntotation", required=False, type=int, default=18)

    args = parser.parse_args()
    print(args.mode)

    for f in args.paths:
        calc = calculation_folder.calculation_folder(f)
        if calc.descriptor["max_angle_between_neighbours"] < 1e-3:
            continue
        if args.what.lower() == "sp":
            inputpath = calc.descriptor["saddlepoint_chain_file"]
            idx_image = calc.descriptor["idx_sp"]
            outputpath = f"{args.what}_{args.mode}_{args.view}"
        elif args.what.lower() == "hopfion":
            inputpath = calc.descriptor["initial_chain_file"]
            outputpath = f"{args.what}_{args.mode}_{args.view}"
            idx_image = 0
        else:
            raise Exception("Unknown -what argument. Choose either 'sp' or 'hopfion'")

        main(f, inputpath, outputpath, idx_image, args.mode, args.view, args.distance, args.annotate)
