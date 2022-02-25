from spirit_extras.spirit_extras import plotting, pyvista_plotting, import_spirit, data
import matplotlib.pyplot as plt
import numpy as np
import json

def main(path, delaunay_mesh_path):
    from spirit import state, geometry, chain, simulation, io

    params_json = os.path.join( path, "params.json" )
    print(f"Trying to read from {params_json}")
    with open(params_json, "r") as f:
        params = json.load(f)

    with state.State("input.cfg", quiet=True) as p_state:
        geometry.set_n_cells(p_state, params["n_cells"])
        io.chain_read(p_state, os.path.join( path, params["initial_chain_file"]) )
        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP, n_iterations=1)
        # chain.update_data(p_state)
        energy_path = data.energy_path_from_p_state(p_state)

        plotting.plot_energy_path(energy_path, plt.gca(), kwargs_interpolated=dict(lw=2), kwargs_discrete = dict(marker="."))

        label_indices = [0]
        labels = ["A", "B", "C", "D", "E"]

        idx_sp = energy_path.idx_sp()
        if idx_sp >= 2:
            label_indices.append( int(idx_sp/2) )

        label_indices.append(idx_sp)

        if energy_path.noi()-1 - idx_sp >= 2:
            label_indices.append( int( (energy_path.noi()-1 + idx_sp)/2 ) )

        label_indices.append( energy_path.noi()-1 )

        for i, label_idx in enumerate(label_indices):
            r = energy_path.reaction_coordinate
            e = energy_path.total_energy

            xy = (r[label_idx], e[label_idx] - e[-1] )
            xytext = np.array(xy) + np.array([0, 150])
            plt.gca().annotate( labels[i], xy, xytext, horizontalalignment="center", verticalalignment="center")

        plt.savefig(os.path.join(path, "chain.png"))
        # plt.show()
        plt.close()

        spin_system = data.spin_system_from_p_state(p_state)
        point_cloud = pyvista_plotting.create_point_cloud(spin_system)

        if os.path.exists(delaunay_mesh_path):
            print(f"Using delaunay file {delaunay_mesh_path}")
            delaunay = pv.read(delaunay_mesh_path)
        else:
            delaunay = pyvista_plotting.delaunay(point_cloud)
            delaunay.save(delaunay_mesh_path)

        delaunay = pyvista_plotting.delaunay(point_cloud)

        for i, label_idx in enumerate(label_indices):
            spin_system = data.spin_system_from_p_state(p_state, idx_image=label_idx)
            point_cloud = pyvista_plotting.create_point_cloud(spin_system)
            delaunay.copy_attributes( point_cloud )
            isosurface  = pyvista_plotting.isosurface_from_delaunay(delaunay)
            pyvista_plotting.save_to_png( os.path.join(path, f"chain_image{labels[i]}"), [isosurface] )

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="input_folder", type=str, nargs='?', help='The input folder')
    parser.add_argument('-d', dest="delaunay", type=str, nargs='?', help='The input folder')

    args = parser.parse_args()

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import glob

    files = glob.glob( args.input_folder)

    for f in files:
        main(f, args.delaunay)