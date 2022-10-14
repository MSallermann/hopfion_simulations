from spirit_extras import import_spirit

import os
from spirit_extras.calculation_folder import Calculation_Folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(calculation_folder_path, relative_gneb_path):

    # Read calculation folder from input path, and get the absolute input and output paths
    calculation          = Calculation_Folder(calculation_folder_path, descriptor_file="params.json")

    absolute_gneb_path   = calculation.to_abspath(relative_gneb_path)

    # Write state prepare callback
    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation["J"]), calculation["J"])

    # DO STUFF HERE
    from spirit_extras import gneb_workflow
    import numpy as np

    if os.path.exists(absolute_gneb_path):
        print(f"Skipping because {absolute_gneb_path} already exists")
        return

    gnw = gneb_workflow.GNEB_Node(name = "gneb_sp", input_file = INPUT_FILE, output_folder = absolute_gneb_path, initial_chain_file = calculation.to_abspath(calculation["initial_guess_sp"]))
    # gnw = gneb_workflow.GNEB_Node(name = "gneb_sp", input_file = INPUT_FILE, output_folder = absolute_gneb_path)

    gnw.state_prepare_callback = state_prepare_cb
    gnw.setup_plot_callbacks()

    gnw.update_energy_path()
    epath = gnw.current_energy_path

    # Figure out idx_mid
    if not idx_dimer is None:
        gnw.log("idx dimer specified by user")
        gnw.prepare_dimer(idx_dimer[0], idx_dimer[1])
    else:
        if epath.noi() == 3: # cheeky shortcut
            gnw.log("Using index 0 and 2 for dimer, since we have three images")
            gnw.prepare_dimer(0,2)
        else:
            n_interpolated       = epath.n_interpolated()
            idx_max_interpolated = np.argmax(epath.interpolated_total_energy)
            Rx_max_interpolated  = epath.interpolated_reaction_coordinate[idx_max_interpolated]
            gnw.log(f"Rx_max_interpolated = {Rx_max_interpolated}")

            idx_mid_candidates = np.sort( np.argsort( np.abs(np.array(np.array(epath.reaction_coordinate) - Rx_max_interpolated )) )[:2] )
            gnw.log(f"idx_mid_candidates = {idx_mid_candidates}")

            # Set up the gneb dimer
            gnw.prepare_dimer(idx_mid_candidates[0])


    base_Rx = epath.reaction_coordinate[1] - epath.reaction_coordinate[0]

    gnw.allow_split          = False

    # Pre-converge with vp
    gnw.delta_Rx_left        = base_Rx
    gnw.delta_Rx_right       = base_Rx
    gnw.convergence          = 1e-5
    gnw.max_total_iterations = 40000
    gnw.run()

    from spirit import simulation
    # Final convergence with lbfgs
    gnw.backup_chain( os.path.join(gnw.output_folder, "chain_before_lbfgs.ovf") )
    gnw.solver_gneb = simulation.SOLVER_LBFGS_OSO
    gnw.delta_Rx_left        = base_Rx
    gnw.delta_Rx_right       = base_Rx
    gnw.max_total_iterations += 20000
    gnw.convergence          = 0.25*1e-7
    gnw.run()

    gnw.history_to_file( os.path.join(gnw.output_folder, "history.txt") )
    calculation.descriptor["saddlepoint_chain_file"] = calculation.to_relpath(absolute_gneb_path)
    #END DO STUFF

    calculation.to_json()

if __name__ == "__main__":
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", help = "calculation folders, which need to exist at the specified location", type=str, nargs="+")
    parser.add_argument("-i",    help = "input path, relative to calculation folder" , required=True, type=str)
    parser.add_argument("-idx_dimer", nargs=2, help = "indices of the dimer, if not specified they will be chosen automatically", required=False, default=None)
    parser.add_argument('-MPI',  help = "speed up loop over folders with MPI (useful when wildcards are used to specify multiple calculation folders)", action='store_true')

    args = parser.parse_args()

    if not args.idx_dimer is None:
        idx_dimer = [int(f) for f in args.idx_dimer]
    else:
        idx_dimer = None

    if not args.MPI:
        for f in args.paths:
            main(f, args.i)
    else:
        from mpi_loop import mpi_loop

        def callable(i):
            input_path = args.paths[i]
            main(input_path, args.i)

        mpi_loop(callable, len(args.paths))