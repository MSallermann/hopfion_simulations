def annotate_params(path_to_png, gamma, r0, dpi=300, fontsize=15):
    import matplotlib.pyplot as plt
    dpi = 300
    img = plt.imread(path_to_png)
    height, width, depth = img.shape
    figsize = width / float(dpi), height / float(dpi)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    plt.text(0, 1, rf"$\gamma = {gamma:.2f}$  $r_0 = {r0:.2f}\,a$", fontsize = fontsize, bbox = dict(facecolor='white', edgecolor="white", alpha=0.80), horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    ax.axis('off')
    ax.imshow(img)
    fig.savefig(path_to_png, dpi=300, bbox_inches=0, pad_inches = 0)

def get_pyvista_plotter(chain_file, n_cells, idx_image_infile, DELAUNAY_PATH="delaunay64.vtk", INPUT_FILE="input.cfg"):
    import os
    from spirit_extras import import_spirit, post_processing, plotting
    import numpy as np
    from spirit import state, io, geometry
    from spirit_extras import data, pyvista_plotting

    plotter = None
    system = None
    with state.State(INPUT_FILE, quiet=True) as p_state:
        geometry.set_n_cells(p_state, n_cells)
        io.image_read(p_state, chain_file, idx_image_infile=idx_image_infile, idx_image_inchain=0)
        system = data.spin_system_from_p_state(p_state, copy=True)

        # Create plotter
        plotter = pyvista_plotting.Spin_Plotter(system)

        if os.path.exists(DELAUNAY_PATH):
            plotter.load_delaunay(DELAUNAY_PATH)
        else:
            plotter.compute_delaunay()
            plotter.save_delaunay(DELAUNAY_PATH)

        # Compute camera positions
        distance = 80
        center, normal = post_processing.hopfion_normal(system)

        plotter.camera_position    = center + distance * normal
        plotter.camera_focal_point = center
        plotter.camera_up          = np.cross(normal, [1,0,0])

    return plotter, center, normal

def set_view(plotter, hopfion_center, hopfion_normal, distance = 80, view="hopfion_normal"):
    import numpy as np
    if view.lower() == "hopfion_normal":
        plotter.camera_position    = hopfion_center + distance * hopfion_normal
        plotter.camera_focal_point = hopfion_center
        plotter.camera_up          = np.cross(hopfion_normal, [1,0,0])
    elif view.lower() == "hopfion_inplane":
        plane_normal = np.cross(hopfion_normal, [1,0,0])
        plane_normal /= np.linalg.norm(plane_normal)
        plotter.camera_position = hopfion_center + distance * plane_normal
        plotter.camera_up = hopfion_normal
    elif view.lower() == "hopfion_diagonal":
        plane_normal = np.cross(hopfion_normal, [1,0,0])
        diagonal_normal = plane_normal + hopfion_normal
        diagonal_normal /= np.linalg.norm(diagonal_normal)
        plotter.camera_position = hopfion_center + distance * diagonal_normal
        plotter.camera_up = hopfion_normal
    else:
        raise Exception(f"Unknown mode {view}")

def add_preimages(plotter, N=16, sz=0.2):
    from spirit_extras import import_spirit, post_processing, plotting
    import numpy as np
    for i in range(N):
        phi = 2 * np.pi / N * i
        spin = [np.sin(phi),np.cos(phi),sz]
        colors = plotting.get_rgba_colors( [spin] )
        plotter.add_preimage(spin, tol=0.15, n_neighbours=24, render_args={"color" : colors[0][:3]})

def clip_cube(center, normal, cube_type, infinity=100, zero=1):
    import numpy as np
    import pyvista as pv

    axis  = np.cross(normal, [0,0,1])
    angle = -np.arccos(normal[2]) * 180/np.pi

    if cube_type.lower() == "normal":
        bounds = (center[0], center[0]+infinity, center[1]-infinity, center[1]+infinity, center[2]-infinity, center[2]+infinity)
    elif cube_type.lower() == "plane":
        bounds = (center[0]-infinity, center[0]+infinity, center[1]-infinity, center[1]+infinity, center[2], center[2]+infinity)
    elif cube_type.lower() == "slice_normal":
        bounds = (center[0]-zero, center[0]+zero, center[1]-infinity, center[1]+infinity, center[2]-infinity, center[2]+infinity)
    elif cube_type.lower() == "slice_plane":
        bounds = (center[0]-infinity, center[0]+infinity, center[1]-infinity, center[1]+infinity, center[2]-zero, center[2]+zero)
    else:
        raise Exception("Invalid type")

    clip_cube = pv.Cube(bounds=bounds).rotate_vector( vector = axis, angle = angle, point=center, inplace=True )

    return clip_cube