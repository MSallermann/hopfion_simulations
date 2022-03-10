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

    output_path_gneb = os.path.join(calculation_out.output_folder, "gneb_sp")

    if os.path.exists(output_path_gneb):
        print(f"Skipping because {output_path_gneb} already exists")
        return

    initial_chain_file = calculation.to_abspath(os.path.join("gneb_preconverge", "chain.ovf"))

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
    # first compute the maximum of the *interpolated* energy
    # then find the two images wich lie left and right to the interpolated maximum
    # look at the interpolated curvature of the two images and choose the one with lower curvature

    n_interpolated       = epath.n_interpolated()
    idx_max_interpolated = np.argmax(epath.interpolated_total_energy)
    Rx_max_interpolated  = epath.interpolated_reaction_coordinate[idx_max_interpolated]
    gnw.log(f"Rx_max_interpolated = {Rx_max_interpolated}")

    idx_mid_candidates = np.argsort( np.abs(np.array(np.array(epath.reaction_coordinate) - Rx_max_interpolated )) )[:2]
    gnw.log(f"idx_mid_candidates = {idx_mid_candidates}")

    interpolated_curvature_0 = np.array(epath.interpolated_curvature())[ idx_mid_candidates[0] * (n_interpolated + 1 ) ]
    interpolated_curvature_1 = np.array(epath.interpolated_curvature())[ idx_mid_candidates[1] * (n_interpolated + 1 ) ]

    if interpolated_curvature_0 < interpolated_curvature_1:
        idx_mid = idx_mid_candidates[0]
    else:
        idx_mid = idx_mid_candidates[1]

    gnw.log(f"curvatures = [{interpolated_curvature_0}, {interpolated_curvature_1}]")
    gnw.log(f"idx_mid = {idx_mid}")

    gnw.prepare_moving_endpoints(idx_mid)
    gnw.allow_split = False

    def half_and_run(convergence, solver, factor = 2.0):
        gnw.update_energy_path()
        rx = gnw.current_energy_path.reaction_coordinate
        gnw.delta_Rx_left        = (rx[1] - rx[0]) / factor
        gnw.delta_Rx_right       = (rx[2] - rx[1]) / factor
        gnw.n_iterations_check   =  5000
        gnw.max_total_iterations += 20000
        gnw.convergence          = convergence
        gnw.solver_gneb          = solver
        gnw.log(f"Rx_left  = {gnw.delta_Rx_left}")
        gnw.log(f"Rx_right = {gnw.delta_Rx_right}")
        gnw.run()
        return (gnw.delta_Rx_left + gnw.delta_Rx_right) / 2.0

    from spirit import simulation

    convergence  = 1e-3
    factor       = 2.0
    delta_Rx    = half_and_run(convergence, simulation.SOLVER_VP_OSO, factor=factor)

    # Relax with VP solver until delta_Rx is small
    while delta_Rx > 0.2:
        convergence = convergence/factor
        delta_Rx    = half_and_run(convergence, simulation.SOLVER_VP_OSO, factor=factor)

    # Before we relax with gneb, we back up the chain
    gnw.backup_chain( os.path.join(gnw.output_folder, "chain_before_lbfgs.ovf") )

    # Relax the rest with LBFGS
    half_and_run(1e-7, simulation.SOLVER_LBFGS_OSO, factor=factor)

    gnw.history_to_file( os.path.join(gnw.output_folder, "history.txt") )

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
        OUTPUT_SCRATCH = "/SCRATCH/saller"
        OUTPUT_LOCAL   = "/local/th1/iff003/saller/"

        ## for debugging:
        # OUTPUT_SCRATCH = "./SCRATCH"
        # OUTPUT_LOCAL   = "./LOCAL"

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