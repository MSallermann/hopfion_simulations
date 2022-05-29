import os
import sys
import calculation_folder
import numpy as np
### Import Spirit modules


INPUT_FILE = "input.cfg"
quiet = False

def main(calculation_folder_path, path_to_dimer=None, output_chain_forward=None, output_chain_backward=None, delta_Rx=1, convergence_energy=1, min_iter=10, max_iter=-1, forward=True, backward=True, absolute_paths=False, relax_ends=False):

    calculation = calculation_folder.calculation_folder(calculation_folder_path)
    path_to_dimer = calculation.to_abspath(path_to_dimer)

    if path_to_dimer is None:
        path_to_dimer = calculation.to_abspath( calculation.descriptor["saddlepoint_chain_file"] )

    if not absolute_paths:
        output_chain_forward  = calculation.to_abspath(output_chain_forward)
        output_chain_backward = calculation.to_abspath(output_chain_backward)

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

    energies_forward  = []
    energies_backward = []

    def read_dimer(p_state):
        noi_file = io.n_images_in_file(p_state, path_to_dimer)
        chain.set_length(p_state, 2)
        if noi_file > 2:
            print("WARNING: file does contain more than 2 images, reading last 2")
        io.image_read(p_state, path_to_dimer, idx_image_infile=noi_file-2, idx_image_inchain=0)
        io.image_read(p_state, path_to_dimer, idx_image_infile=noi_file-1, idx_image_inchain=1)

    with state.State(INPUT_FILE, quiet) as p_state:
        state_prepare_cb(p_state)
        read_dimer(p_state)
        NOISE_SCALE = 1e-4
        if forward:
            print("Forward chain")
            if os.path.exists(output_chain_forward):
                os.remove(output_chain_forward)

            # Push dimer from saddle point to final state
            parameters.gneb.set_moving_endpoints(p_state, True, fix_left=True, fix_right=False)
            parameters.gneb.set_equilibrium_delta_Rx(p_state, delta_Rx, delta_Rx)
            parameters.gneb.set_convergence(p_state, 1e-6)

            delta_energy_forward = []

            converged = False
            iteration = 0
            while not converged:
                simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_LBFGS_OSO)
                energies = chain.get_energy(p_state)

                delta_E = energies[-1] - energies[0]
                delta_energy_forward.append(delta_E)

                print(delta_E)
                print(convergence_energy*delta_Rx)

                if not output_chain_forward is None:
                    io.image_append(p_state, output_chain_forward, idx_image=1)
                transition.dimer_shift(p_state, False)
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=1)

                iteration += 1
                if iteration >= min_iter:
                    converged = abs(energies[-1] - energies[0]) < convergence_energy*delta_Rx
                    if max_iter > 0 and iteration >= max_iter:
                        break
                np.savetxt("delta_energy_forward.txt", delta_energy_forward)

            if relax_ends:
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=1)
                simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=1)
                if not output_chain_forward is None:
                    io.image_append(p_state, output_chain_forward, idx_image=1)

        if backward:
            print("Backward chain")
            if os.path.exists(output_chain_backward):
                os.remove(output_chain_backward)

            # Read dimer back in
            read_dimer(p_state)
            # In the backward chain we include image 0 of the dimer
            io.image_append(p_state, output_chain_backward, idx_image=0)

            parameters.gneb.set_moving_endpoints(p_state, True, fix_left=False, fix_right=True)
            parameters.gneb.set_equilibrium_delta_Rx(p_state, delta_Rx, delta_Rx)

            converged = False
            iteration = 0

            delta_energy_backward = [0]

            while not converged:
                transition.dimer_shift(p_state, True)
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=0)

                simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_LBFGS_OSO)
                energies = chain.get_energy(p_state)

                delta_E = energies[-1] - energies[0]
                delta_energy_backward.append(delta_E)

                print(delta_E)
                print(convergence_energy*delta_Rx)

                if not output_chain_backward is None:
                    io.image_append(p_state, output_chain_backward, idx_image=0)

                iteration += 1
                if iteration >= min_iter:
                    converged = abs(delta_E) < convergence_energy*delta_Rx
                    if max_iter > 0 and iteration >= max_iter:
                        break
                np.savetxt("delta_energy_backward.txt", delta_energy_backward)

            if relax_ends:
                configuration.add_noise(p_state, NOISE_SCALE, idx_image=1)
                simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=0)
                if not output_chain_backward is None:
                    io.image_append(p_state, output_chain_backward, idx_image=0)

if __name__ == "__main__":
    from spirit_extras import import_spirit
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths",        help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-i",           help = "input path, relative to calculation folder" , required=False, type=str, default=None)
    parser.add_argument("-of",          help = "output path, relative to calculation folder", required=False, type=str, default="chain_file_forward.ovf")
    parser.add_argument("-ob",          help = "output path, relative to calculation folder", required=False, type=str, default="chain_file_backward.ovf")
    parser.add_argument("-Rx",          help = "output path, relative to calculation folder", required=False, type=float, default = 1)
    parser.add_argument("-convergence", help = "output path, relative to calculation folder", required=False, type=float, default = 1)
    parser.add_argument("-min_iter",    help = "output path, relative to calculation folder", required=False, type=int, default = 10)
    parser.add_argument("-max_iter",    help = "output path, relative to calculation folder", required=False, type=int, default = -1)
    parser.add_argument("-backward",    help = "output path, relative to calculation folder", action="store_true", required=False)
    parser.add_argument("-forward",     help = "output path, relative to calculation folder",  action="store_true", required=False)
    parser.add_argument("-relax_ends",  help = "output path, relative to calculation folder",  action="store_true", required=False)

    args = parser.parse_args()

    for f in args.paths:
        main(f, args.i, args.of, args.ob, delta_Rx=args.Rx, convergence_energy=args.convergence, min_iter=args.min_iter, max_iter=args.max_iter, forward=args.forward, backward=args.backward, relax_ends=args.relax_ends)