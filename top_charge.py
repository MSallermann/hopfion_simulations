from curses import noraw
from spirit_extras import import_spirit, pyvista_plotting
import os
import calculation_folder
import plot_util
import pyvista 
import numpy as np


SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def fibonacci_sphere(radius, center, n=50):
    from numpy import arange, pi, sin, cos, arccos
    goldenRatio = (1 + 5**0.5)/2
    i = arange(0, n)
    theta = 2 *pi * i / goldenRatio
    phi = arccos(1 - 2*(i+0.5)/n)
    x, y, z = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)

    result = np.empty(shape=(n, 3))
    result[:,0] = radius * x + center[0]
    result[:,1] = radius * y + center[1]
    result[:,2] = radius * z + center[2]

    return result

def fibonacci_sphere2(radius, center, n):
    from numpy import arange, pi, sin, cos, arccos

    if n >= 600000:
        epsilon = 214
    elif n>= 400000:
        epsilon = 75
    elif n>= 11000:
        epsilon = 27
    elif n>= 890:
        epsilon = 10
    elif n>= 177:
        epsilon = 3.33
    elif n>= 24:
        epsilon = 1.33
    else:
     epsilon = 0.33

    goldenRatio = (1 + 5**0.5)/2
    i = arange(0, n) 
    theta = 2 *pi * i / goldenRatio
    phi = arccos(1 - 2*(i+epsilon)/(n-1+2*epsilon))
    x, y, z = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi);

    result = np.empty(shape=(n, 3))
    result[:,0] = radius * x + center[0]
    result[:,1] = radius * y + center[1]
    result[:,2] = radius * z + center[2]

    return result

def my_sphere(radius, center, n_theta, n_phi_equator):
    result = []
    for theta in np.linspace(0,np.pi,n_theta):
        circ = np.sqrt(1 - np.cos(theta)**2)
        n_phi = int(circ*n_phi_equator + 1)
        for phi in np.linspace(0, 2*np.pi, n_phi):
            result.append( radius * np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]) + center )
    return result

def main(calculation_folder_path, relative_input_path, relative_output_path, idx_image_infile=0, mode="isosurface", view="auto", background_color="transparent", distance=80, annotate=22, output_dir=None, output_suffix="", only_center=False):
    # Read calculation folder from input path, and get the absolute input and output paths
    calculation = calculation_folder.calculation_folder(calculation_folder_path)
    gamma       = calculation.descriptor["gamma"]
    l0          = calculation.descriptor["l0"]

    if not output_suffix is None:
        output_suffix = calculation.format(output_suffix)
    if not output_dir is None:
        output_dir = calculation.format(output_dir)

    # Input is always relative to calculation folder
    absolute_input_path = calculation.to_abspath(relative_input_path)

    relative_output_path += output_suffix
    if output_dir is None:
        absolute_output_path = calculation.to_abspath(relative_output_path)
    else:
        absolute_output_path = os.path.join(output_dir, relative_output_path)

    if not os.path.exists(os.path.dirname(absolute_output_path)):
        os.makedirs(absolute_output_path)

    print(f"Input:   {absolute_input_path}")
    print(f"Output:  {absolute_output_path}")

    # DO STUFF HERE
    plotter, center, normal  = plot_util.get_pyvista_plotter(absolute_input_path, calculation.descriptor["n_cells"], idx_image_infile, DELAUNAY_PATH="/home/moritz/hopfion_simulations/delaunay64.vtk", INPUT_FILE=INPUT_FILE)
    plotter.resolution = (1024, 1024)

    plot_util.set_view(plotter, center, normal, distance, "hopfion_inplane")
    plotter.align_camera_up(normal)
    plotter.align_camera_position(axis = normal, align_direction=[1,1,0])
    print(center, normal)

    mesh_args = plotter.isosurface(0.0, "spins_z")
    iso = mesh_args[0]
    mesh_args[1]["color"]   = 0
    mesh_args[1]["opacity"] = 0.0

    if not iso:
        print("No BP found")
        plotter.render_to_png( absolute_output_path )
        return

    bp_centers, bp_cells = iso.ray_trace( center-20*normal, center + 20*normal)

    for p in bp_centers:
        print( f'Intersected at {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}' )

    # my_mesh = mesh_args[0]
    # Find center of bloch point

    if only_center:
        with open("bp_centers.txt", "a") as f:
            if len(bp_centers) == 2:
                f.write(f"{idx_image_infile} {np.linalg.norm(bp_centers[0] - bp_centers[1])}\n")
            else:
                f.write(f"{idx_image_infile} -1\n")
        return

    if len(bp_centers) != 2:
        print("No BP found")
        plotter.render_to_png( absolute_output_path )
        return

    bp_radius = np.linalg.norm( bp_centers[1] - bp_centers[0] ) / 3

    for idx_bp,bp_center in enumerate(bp_centers):
        print(f"===== BP {idx_bp} =====")
        my_mesh = pyvista.Sphere(radius=bp_radius, center = bp_center, theta_resolution=15, phi_resolution=15 )

        # my_mesh = pyvista.PolyData(fibonacci_sphere2(radius=bp_radius, center=bp_center, n=300))
        # my_mesh = pyvista.PolyData(my_sphere(radius=bp_radius, center=bp_center, n_theta=15, n_phi_equator=30))
        # my_mesh = my_mesh.reconstruct_surface()

        my_mesh = my_mesh.interpolate( plotter._point_cloud, radius=1.5)

        # arrows = pyvista_plotting.arrows_from_point_cloud(my_mesh, factor=0.5)
        # plotter.add_mesh(arrows, {})
        # plotter.add_mesh(my_mesh, {"color" : "lightgrey"})

        faces = np.reshape(my_mesh.faces, ( my_mesh.n_faces, 4 ) )

        def solid_angle(v1t,v2t,v3t):
            v1  = v1t / np.linalg.norm(v1t)
            v2  = v2t / np.linalg.norm(v2t)
            v3  = v3t / np.linalg.norm(v3t)

            x = v1.dot( np.cross(v2, v3 ) )
            y = 1 + v1.dot( v2 ) + v1.dot( v3 ) + v2.dot( v3 )
            solid_angle = 2 * np.arctan2( x, y )
            return solid_angle

        spins = my_mesh["spins"]
        solid_angles         = []
        solid_angles_spatial = []

        for i,f in enumerate(faces):
            if(f[0] != 3):
                raise Exception("Not a triangular face")

            solid_angles.append( solid_angle( spins[f[1]], spins[f[2]], spins[f[3]] ) / (4*np.pi) )
            solid_angles_spatial.append( solid_angle( my_mesh.points[f[1]] - bp_center, my_mesh.points[f[2]] - bp_center, my_mesh.points[f[3]] - bp_center ) / (4*np.pi) )

        solid_angles         = np.asarray(solid_angles)
        solid_angles_spatial = np.asarray(solid_angles_spatial)
        solid_angle_density  = solid_angles/solid_angles_spatial

        np.savetxt(f"solid_angles_{idx_bp}.txt", solid_angles)
        np.savetxt(f"solid_angles_spatial_{idx_bp}.txt", solid_angles_spatial)
        np.savetxt(f"solid_angle_density_{idx_bp}.txt", solid_angle_density)

        s = np.abs(solid_angle_density)
        # s = np.abs(solid_angles_spatial)

        print(f"mean(s) {np.mean(s)}")
        print(f"std(s) {np.std(s)}")

        factor = 1.5e-1/np.std(s)
        mean_s = np.mean(s)
        warp_factors = []
        for i in range(len(s)):
            wf = 1 + factor * (s[i] - mean_s)
            if wf < 1.0:
                wf = 1/(2-wf)
            warp_factors.append(wf)
        warp_factors = np.asarray(warp_factors)
        print(f"min wf {np.min(warp_factors)}")
        print(f"max wf {np.max(warp_factors)}")
        my_mesh.cell_data["warp_factors"] = warp_factors

        my_mesh = my_mesh.cell_data_to_point_data()

        vis_radius = 0.75
        vis_center = center + 2*normal
        if idx_bp==1:
            vis_center -= 4*normal

        warped_mesh = pyvista.Sphere(radius=vis_radius, center=vis_center, theta_resolution=15, phi_resolution=15)
        warped_mesh.copy_attributes(my_mesh)
        warped_mesh = warped_mesh.warp_by_scalar(scalars="warp_factors", factor=1)

        plotter.add_mesh(warped_mesh, {"color" : "lightgray", "smooth_shading":True})

    # plotter.show()
    plotter.render_to_png( absolute_output_path )
    print(f"Output to: {absolute_output_path}.png")


if __name__ == "__main__":
    from spirit_extras import import_spirit
    spirit_info = import_spirit.find_and_insert("~", stop_on_first_viable=True )[0]
    print(spirit_info)

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths",       help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-i",          help = "relative input path", required=True, type=str, default="sp")
    parser.add_argument("-o",          help = "relative output path", required=True, type=str, default="sp")
    parser.add_argument("-idx",        help = "relative input path", required=True, type=int, default="sp")
    parser.add_argument("-view",       help = "from which view to plot. one of [hopfion_normal, hopfion_inplane, hopfion_diagonal]", type=str, default="hopfion_diagonal")
    parser.add_argument("-distance",   help = "distance of camera to hopfion center", required=False, type=float, default=80)
    parser.add_argument("-annotate",   help = "annotation fontsiye, 0 disables anntotation", required=False, type=int, default=18)
    parser.add_argument("-output_dir", help = "absolute output_directory, if not specified defaults to calculation folder", required=False, type=str, default=None)
    parser.add_argument("-output_suffix", help = "suffix for output files", required=False, type=str, default="")
    parser.add_argument("-background_color", help = "background_color", required=False, type=str, default="transparent")
    parser.add_argument("-only_center", action="store_true")

    args = parser.parse_args()
    # print(args.mode)

    for f in args.paths:
        calc = calculation_folder.calculation_folder(f)
        main(calculation_folder_path=f, relative_input_path=args.i, relative_output_path=args.o, idx_image_infile=args.idx, view=args.view, distance=args.distance, background_color=args.background_color, annotate=args.annotate, output_dir=args.output_dir, output_suffix=args.output_suffix, only_center=args.only_center)
