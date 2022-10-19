import os
import sys
import calculation_folder
import numpy as np
### Import Spirit modules


INPUT_FILE = "input.cfg"
quiet      = True

def main(calculation_folder_path, path_to_dimer=None, output_chain=None, delta_Rx=1, convergence_energy=1, min_iter=10, max_iter=-1, forward=True, backward=True, absolute_paths=False, relax_ends=False, prefix=""):

    calculation = calculation_folder.calculation_folder(calculation_folder_path)

    if path_to_dimer is None:
        path_to_dimer = calculation.to_abspath( calculation.descriptor["saddlepoint_chain_file"] )
    else: 
        path_to_dimer = calculation.to_abspath(path_to_dimer)

    if not absolute_paths:
        output_chain  = calculation.to_abspath(output_chain)

    # Write state prepare callback
    def state_prepare_cb(p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    from spirit import state
    from spirit import system
    from spirit import geometry
    from spirit import chain
    from spirit import configuration
    from spirit import transition
    from spirit import simulation
    from spirit import parameters
    from spirit import io
    from spirit import log

    import matplotlib.pyplot as plt

    if os.path.exists(output_chain):
        os.remove(output_chain)

    OUTPUT_DIR = os.path.dirname(output_chain)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # helper functions
    def read_dimer(p_state):
        noi_file = io.n_images_in_file(p_state, path_to_dimer)
        chain.set_length(p_state, 2)
        if noi_file > 2:
            print("WARNING: file does contain more than 2 images, reading last 2")
        io.image_read(p_state, path_to_dimer, idx_image_infile=noi_file-2, idx_image_inchain=0)
        io.image_read(p_state, path_to_dimer, idx_image_infile=noi_file-1, idx_image_inchain=1)

    noi_bf = [0,0] # noi backward and noi forward
    def append(p_state, idx_image, noi):
        if not output_chain is None:
            io.image_append(p_state, output_chain, idx_image=idx_image)
            noi[idx_image] += 1

    with state.State(INPUT_FILE, quiet) as p_state:
        state_prepare_cb(p_state)
        read_dimer(p_state)
        NOISE_SCALE = 1e-4

        if backward:
            print("Backward chain")
            read_dimer(p_state)
            # In the backward chain we include image 0 of the dimer
            append(p_state, 0, noi_bf)

            parameters.gneb.set_moving_endpoints(p_state, True, fix_left=False, fix_right=True)
            parameters.gneb.set_equilibrium_delta_Rx(p_state, delta_Rx, delta_Rx)

            converged = False
            iteration = 0

            while not converged:
                transition.dimer_shift(p_state, True)
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=0)

                simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_LBFGS_OSO)
                energies = chain.get_energy(p_state)

                # Backward chain, therefore delta_E > 0
                delta_E  = energies[-1] - energies[0]

                print(f"delta_E = {delta_E:.5f}, delta_E > {convergence_energy*delta_Rx:.5f}")
                append(p_state, 0, noi_bf)

                iteration += 1
                if iteration >= min_iter:
                    converged = delta_E < convergence_energy*delta_Rx
                    if max_iter > 0 and iteration >= max_iter:
                        break

            if relax_ends:
                print("Relaxing endpoint")
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=1)
                simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=0)
                append(p_state, 0, noi_bf)
               
        if forward:
            print("Forward chain")
            read_dimer(p_state)

            # Push dimer from saddle point to final state
            parameters.gneb.set_moving_endpoints(p_state, True, fix_left=True, fix_right=False)
            parameters.gneb.set_equilibrium_delta_Rx(p_state, delta_Rx, delta_Rx)
            parameters.gneb.set_convergence(p_state, 1e-6)

            converged = False
            iteration = 0
            while not converged:
                simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_LBFGS_OSO)
                energies = chain.get_energy(p_state)

                # Forward chain, therefore delta_E < 0
                delta_E = energies[-1] - energies[0]

                print(f"delta_E = {delta_E:.5f}, delta_E < {-convergence_energy*delta_Rx:.5f}")
                append(p_state, 1, noi_bf)
               
                transition.dimer_shift(p_state, False)
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=1)

                iteration += 1
                if iteration >= min_iter:
                    converged = energies[-1] - energies[0] > -convergence_energy*delta_Rx
                    if max_iter > 0 and iteration >= max_iter:
                        break

            if relax_ends:
                print("Relaxing endpoint")
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=1)
                simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=1)
                append(p_state, 1, noi_bf)

        # Combine chains
        print("Combining chains")
        from spirit_extras import chain_io, data, plotting

        chain.set_length(p_state, 1)
        io.chain_read(p_state, output_chain)
        print(f"noi_backward = {noi_bf[0]}, noi_forward = {noi_bf[1]}")

        print("Inverting backward chain")
        chain_io.invert_chain(p_state, 0, noi_bf[0] - 1)
        io.chain_write(p_state, output_chain)

        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP, n_iterations=1)
        energy_path = data.energy_path_from_p_state(p_state)

        plot_path = os.path.join(OUTPUT_DIR, "total_path.png")
        plotting.plot_energy_path(energy_path, plt.gca())
        print(f"Output plot to: {plot_path}")
        plt.savefig( plot_path )
        np.savetxt(  os.path.join(OUTPUT_DIR, "rx_interpolated.txt"), energy_path.interpolated_reaction_coordinate)
        np.savetxt(  os.path.join(OUTPUT_DIR, "energies_interpolated.txt"), energy_path.interpolated_total_energy)
        np.savetxt(  os.path.join(OUTPUT_DIR, "rx.txt"), energy_path.reaction_coordinate)
        np.savetxt(  os.path.join(OUTPUT_DIR, "energies.txt"), energy_path.total_energy)

if __name__ == "__main__":
    from spirit_extras import import_spirit
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths",        help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-i",           help = "input path, relative to calculation folder" , required=False, type=str, default=None)
    parser.add_argument("-o",           help = "output path, relative to calculation folder", required=False, type=str, default="chain_file_total.ovf")
    parser.add_argument("-Rx",          help = "delta Rx between chain images", required=False, type=float, default = 1)
    parser.add_argument("-convergence", help = "convergence parameterr", required=False, type=float, default = 1)
    parser.add_argument("-min_iter",    help = "minimum number of iterations", required=False, type=int, default = 10)
    parser.add_argument("-max_iter",    help = "maximum number of iterations", required=False, type=int, default = -1)
    parser.add_argument("-backward",    help = "build the backward chain", action="store_true", required=False)
    parser.add_argument("-forward",     help = "build the forward chain",  action="store_true", required=False)
    parser.add_argument("-relax_ends",  help = "if the endpoints should be relaxed",  action="store_true", required=False)
    parser.add_argument("-prefix",      help = "prefix for outputfiles", type=str, required=False, default="")

    args = parser.parse_args()

    for f in args.paths:
        main(f, args.i, args.o, delta_Rx=args.Rx, convergence_energy=args.convergence, min_iter=args.min_iter, max_iter=args.max_iter, forward=args.forward, backward=args.backward, relax_ends=args.relax_ends, prefix=args.prefix)