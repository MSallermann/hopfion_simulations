from spirit_extras import plotting, pyvista_plotting, import_spirit, data
import matplotlib.pyplot as plt
import numpy as np
import calculation_folder
import json
import os


def main(path):
    from spirit import state, geometry, chain, simulation, io

    calculation = calculation_folder.calculation_folder(path)
    params = calculation.descriptor

    if params["max_angle_between_neighbours"] < 1e-2:
        return

    def state_prepare_cb(p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    with state.State("input.cfg", quiet=True) as p_state:
        state_prepare_cb(p_state)
        chain.set_length(p_state, 2)

        io.image_read(p_state, os.path.join(path, params["initial_chain_file"]), idx_image_infile=0,  idx_image_inchain=0)
        io.image_read(p_state, os.path.join(path, "gneb_sp3", "chain.ovf"),      idx_image_infile=1,  idx_image_inchain=1)
        chain.update_data(p_state)

        epath = data.energy_path_from_p_state(p_state)

        calculation.descriptor["energy_barrier"] = epath.barrier()

    calculation.to_json()

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    for f in args.paths:
        main(f)