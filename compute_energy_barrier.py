from spirit_extras import plotting, pyvista_plotting, import_spirit, data
import matplotlib.pyplot as plt
import numpy as np
import calculation_folder
import json
import os

def main(path):
    from spirit import state, geometry, chain, simulation, io, configuration
    print(path)
    calculation = calculation_folder.calculation_folder(path)
    params = calculation.descriptor
    # print(params)
    if params["max_angle_between_neighbours"] < 1e-2:
        return

    def state_prepare_cb(p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    with state.State("input.cfg", quiet=False) as p_state:
        state_prepare_cb(p_state)
        chain.set_length(p_state, 3)

        io.image_read(p_state, calculation.to_abspath(params["initial_chain_file"]),     idx_image_infile=0,  idx_image_inchain=0)
        io.image_read(p_state, calculation.to_abspath(params["saddlepoint_chain_file"]), idx_image_infile=int(params["idx_sp"]),  idx_image_inchain=1)
        configuration.plus_z(p_state, idx_image=2)
        chain.update_data(p_state)

        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP, n_iterations=1)

        epath = data.energy_path_from_p_state(p_state)

        calculation.descriptor["energy_barrier"]               = epath.barrier()
        calculation.descriptor["energy_barrier_reduced"]       = epath.barrier() / params["E0"]
        calculation.descriptor["energy_barrier_divided_by_E0"] = epath.barrier() / (epath.total_energy[0] - epath.total_energy[2])

    calculation.to_json()

if __name__ == "__main__":
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    for f in args.paths:
        main(f)