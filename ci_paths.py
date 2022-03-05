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

    output_path_gneb = os.path.join(calculation_out.output_folder, "gneb_ci")

    if os.path.exists(output_path_gneb):
        print(f"Skipping because {output_path_gneb} already exists")
        return

    # Where in the input calculation folder is the initial chain file saved?
    # initial_chain_file = calculation.to_abspath(calculation.descriptor["initial_chain_file"])
    initial_chain_file = calculation.to_abspath(os.path.join("gneb_preconverge", "chain.ovf"))

    # Write state prepare callback
    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    # Settings for GNEB workflow
    gnw = gneb_workflow.GNEB_Node(name="gneb_ci", input_file = INPUT_FILE, output_folder = output_path_gneb, initial_chain_file = initial_chain_file)
    gnw.state_prepare_callback = state_prepare_cb
    gnw.target_noi             = 16
    gnw.max_total_iterations   = 20000
    gnw.setup_plot_callbacks()
    gnw.convergence            = 1e-5

    # Update the energy path
    from spirit.parameters import gneb
    gnw.update_energy_path()
    gnw.image_types = [[int(gnw.current_energy_path.idx_sp()), gneb.IMAGE_CLIMBING]]
    gnw.to_json()
    gnw.run()


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
            identify = time = now.strftime("gneb_ci#%m_%d_%Y_%H_%M_%S")

            output_path = os.path.join(OUTPUT_SCRATCH, identify, calculation_name)

            main(input_path, output_path)

            print("Copy from SCRATCH to local")
            shutil.copytree(os.path.join(OUTPUT_SCRATCH, identify, calculation_name), os.path.join(OUTPUT_LOCAL, identify, calculation_name))

        mpi_loop(callable, len(args.paths))