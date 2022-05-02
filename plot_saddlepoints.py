from spirit_extras import import_spirit, post_processing
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
# OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "plots")

def annotate_params(path_to_png, gamma, r0, dpi=300):
    import matplotlib.pyplot as plt
    dpi = 300
    img = plt.imread(path_to_png)
    height, width, depth = img.shape
    figsize = width / float(dpi), height / float(dpi)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    # plt.text(0, 1, rf"$\gamma = {gamma:.2f}$  $r_0 = {r0:.2f}\;a$", fontsize = 8, bbox = dict(facecolor='white', edgecolor="white", alpha=0.5), horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    plt.text(0, 1, rf"$\gamma = {gamma:.2f}$  $r_0 = {r0:.2f}\;a$", fontsize = 18, bbox = dict(facecolor='white', edgecolor="white", alpha=0.8), horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    ax.axis('off')
    ax.imshow(img)
    fig.savefig(path_to_png, dpi=300, bbox_inches=0, pad_inches = 0)

def main(path):
    print(path)

    calculation = calculation_folder.calculation_folder(path)

    chain_file = os.path.join(path, "gneb_sp", "chain.ovf")

    try:
        history = np.loadtxt(os.path.join(calculation.output_folder, "gneb_sp", "history.txt"))
        if history[-1,1] > 1e-7:
            chain_file = os.path.join(path, "gneb_sp", "chain_before_lbfgs.ovf")
    except:
        pass

    gamma   = calculation.descriptor["gamma"]
    l0      = calculation.descriptor["l0"]
    n_cells = calculation.descriptor["n_cells"]

    if calculation.descriptor["max_angle_between_neighbours"] < 1e-2:
        return

    plot_name  = f"saddlepoint_gamma_{gamma:.3f}_r0_{l0:.3f}"

    from spirit import state, io, geometry
    from spirit_extras import data, pyvista_plotting

    with state.State(INPUT_FILE) as p_state:
        geometry.set_n_cells(p_state, n_cells)
        io.image_read(p_state, chain_file, idx_image_infile=1, idx_image_inchain=0)
        system = data.spin_system_from_p_state(p_state)

        # Create plotter
        plotter = pyvista_plotting.Spin_Plotter(system)

        if os.path.exists(DELAUNAY_PATH):
            plotter.load_delaunay(DELAUNAY_PATH)
        else:
            plotter.compute_delaunay()
            plotter.save_delaunay(DELAUNAY_PATH)

        plotter.isosurface(0, "spins_z")
        # plotter.show(save_camera_file="camera.json")

        # Compute camera positions
        distance = 80
        center, normal = post_processing.hopfion_normal(p_state)

        print(center, normal)

        plotter.camera_position    = center + distance * normal
        plotter.camera_focal_point = center
        plotter.camera_up          = np.cross(normal, [1,0,0])

        plot_path = os.path.join(calculation.output_folder, plot_name)
        plotter.render_to_png( plot_path )
        annotate_params(plot_path + ".png", gamma = gamma, r0 = l0)


if __name__ == "__main__":

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()



    for f in args.paths:
        main(f)