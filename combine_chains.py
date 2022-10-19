import calculation_folder
import numpy as np
import matplotlib.pyplot as plt

def main(calculation_folder_path, input_paths, output_chain, compute_energy=True, relative_input=True, relative_output=True):
    from spirit import state, simulation, chain, io

    if calculation_folder_path is None:
        calculation = None
    else:
        calculation = calculation_folder.calculation_folder(calculation_folder_path)

    # Write state prepare callback
    def state_prepare_cb(p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    if relative_output:
        output_chain = calculation.to_abspath(output_chain)

    if os.path.exists(output_chain):
        os.remove(output_chain)
    OUTPUT_DIR = os.path.dirname(output_chain)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Check if all files exist and fail early
    for p in input_paths:
        if relative_input:
            p = calculation.to_abspath(p)
        if not os.path.exists(p):
            raise Exception(f"The file {p} does not exist!")

    with state.State("input.cfg") as p_state:
        state_prepare_cb(p_state)
        for p in input_paths:
            if relative_input:
                p = calculation.to_abspath(p)
            chain_io.chain_append_to_file_from_file(p_state, output_chain, p)  

        if compute_energy:
            chain.set_length(p_state, 1)
            io.chain_read(p_state, output_chain)
            simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP, n_iterations=1)
            energy_path = data.energy_path_from_p_state(p_state)

            plotting.plot_energy_path(energy_path, plt.gca())

            np.savetxt(  os.path.join(OUTPUT_DIR, "rx_interpolated.txt"), energy_path.interpolated_reaction_coordinate)
            np.savetxt(  os.path.join(OUTPUT_DIR, "energies_interpolated.txt"), energy_path.interpolated_total_energy)
            np.savetxt(  os.path.join(OUTPUT_DIR, "rx.txt"), energy_path.reaction_coordinate)
            np.savetxt(  os.path.join(OUTPUT_DIR, "energies.txt"), energy_path.total_energy)

            plt.savefig( os.path.join(OUTPUT_DIR, "combined_path.png"))

if __name__ == "__main__":
    from spirit_extras import import_spirit, chain_io, data, plotting
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-i", nargs='+', help = "input paths, relative to calculation folder", type=str, required=True, default=None)
    parser.add_argument("-o", help = "output path, relative to calculation folder", required=True, type=str)

    args = parser.parse_args()

    for f in args.paths:
        main(f, args.i, args.o)