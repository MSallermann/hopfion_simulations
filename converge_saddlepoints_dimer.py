from spirit_extras import import_spirit, gneb_workflow
import matplotlib.pyplot as plt
import numpy as np
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(input_calculation_folder_path, output_calculation_folder_path=None):
    # Read calculation folder from input path
    calculation = calculation_folder.calculation_folder(input_calculation_folder_path)

    # If no output calculation folder is give we assume it is the same as the input
    if output_calculation_folder_path is None:
        output_calculation_folder_path = input_calculation_folder_path

    if input_calculation_folder_path != output_calculation_folder_path:
        # Create new calculation folder at output path
        calculation_out = calculation_folder.calculation_folder(output_calculation_folder_path)
        calculation_out.descriptor = calculation.descriptor.copy()
        calculation_out.to_json()
    else:
        calculation_out = calculation

    initial_chain_file = calculation.to_abspath(calculation.descriptor["preconverged_chain_file"])
    output_path_gneb   = os.path.join(calculation_out.output_folder, "gneb_sp_dimer2")

    if os.path.exists(output_path_gneb):
        print(f"Skipping because {output_path_gneb} already exists")
        return

    # Write state prepare callback
    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    gnw = gneb_workflow.GNEB_Node(name="gneb_sp", input_file=INPUT_FILE, output_folder = output_path_gneb, initial_chain_file=initial_chain_file)
    gnw.state_prepare_callback = state_prepare_cb
    gnw.setup_plot_callbacks()

    gnw.update_energy_path()
    epath = gnw.current_energy_path

    # Figure out idx_mid
    n_interpolated       = epath.n_interpolated()
    idx_max_interpolated = np.argmax(epath.interpolated_total_energy)
    Rx_max_interpolated  = epath.interpolated_reaction_coordinate[idx_max_interpolated]
    gnw.log(f"Rx_max_interpolated = {Rx_max_interpolated}")

    idx_mid_candidates = np.sort( np.argsort( np.abs(np.array(np.array(epath.reaction_coordinate) - Rx_max_interpolated )) )[:2] )
    gnw.log(f"idx_mid_candidates = {idx_mid_candidates}")

    # Set up the gneb dimer
    gnw.prepare_dimer(idx_mid_candidates[0])

    gnw.allow_split          = False

    # Pre-converge with vp
    gnw.delta_Rx_left        = 1.0
    gnw.delta_Rx_right       = 1.0
    gnw.convergence          = 1e-5
    gnw.max_total_iterations = 40000
    gnw.run()

    from spirit import simulation
    # Final convergence with lbfgs
    gnw.backup_chain( os.path.join(gnw.output_folder, "chain_before_lbfgs.ovf") )
    gnw.solver_gneb = simulation.SOLVER_LBFGS_OSO
    gnw.delta_Rx_left        = 0.5
    gnw.delta_Rx_right       = 0.5
    gnw.max_total_iterations += 20000
    gnw.convergence          = 1e-12
    gnw.run()

    # Final step, insert one image between the endpoints to get the true saddle point
    from spirit import parameters
    gnw.target_noi  = 3
    gnw.image_types = [[1, parameters.gneb.IMAGE_CLIMBING]]
    gnw.delta_Rx_left  = 0.25
    gnw.delta_Rx_right = 0.25
    gnw.max_total_iterations += 20000
    gnw.run()

    gnw.history_to_file( os.path.join(gnw.output_folder, "history.txt") )

    calculation.descriptor["saddlepoint_chain_file"] = calculation.to_relpath(output_path_gneb)
    calculation.to_json()

if __name__ == "__main__":

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    parser.add_argument('-MPI', action='store_true')

    args = parser.parse_args()

    if not args.MPI:
        for f in args.paths:
            main(f)
    else:
        from mpi_loop import mpi_loop
        import shutil, os
        from datetime import datetime
        now = datetime.now()

        def callable(i):
            input_path = args.paths[i]
            calculation_name = os.path.basename(os.path.normpath(input_path))
            # Identifier
            main(input_path, input_path)

        mpi_loop(callable, len(args.paths))