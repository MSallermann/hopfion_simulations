from spirit_extras import import_spirit, gneb_workflow
import matplotlib.pyplot as plt
import numpy as np
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(input_path, output_path=None):

    calculation = calculation_folder.calculation_folder(input_path)

    if not output_path:
        output_path = os.path.join(calculation.output_folder, "gneb_preconverge")

    initial_chain_file = calculation.to_abspath(calculation.descriptor["initial_chain_file"])
    initial_chain_file = calculation.to_abspath(os.path.join("gneb_preconverge", "chain.ovf"))

    # print(path)
    # print("gamma = {}, l0 = {}".format(calculation.descriptor["gamma"], calculation.descriptor["l0"]))

    # if os.path.exists( calculation.to_abspath("gneb_preconverge") ):
    #     print("Skip")
    #     return
    # print("---")

    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    gnw = gneb_workflow.GNEB_Node(name="gneb_preconverge", input_file = INPUT_FILE, output_folder = output_path, initial_chain_file = initial_chain_file)
    gnw.state_prepare_callback = state_prepare_cb
    gnw.target_noi = 16
    gnw.max_total_iterations = 100000
    gnw.setup_plot_callbacks()
    gnw.convergence = 1e-5
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
        OUTPUT_LOCAL   = "/local/th1/iff003/saller/mpi_test"

        from mpi_loop import mpi_loop
        import shutil
        from datetime import datetime
        now = datetime.now()

        def callable(i):
            input_path = args.paths[i]
            calculation = calculation_folder.calculation_folder(input_path)

            gamma = calculation.descriptor["gamma"]
            l0    = calculation.descriptor["l0"]

            identify = time = now.strftime("%m_%d_%Y_%H_%M_%S")

            calculation_name = f"gamma_{gamma:.3f}_l0_{l0:.3f}#{identify}"

            output_path = os.path.join(OUTPUT_SCRATCH, calculation_name, "gneb_preconverge2")
            main(input_path, output_path)

            print("Copy from SCRATCH to local")
            shutil.copytree(os.path.join(OUTPUT_SCRATCH, calculation_name), os.path.join(OUTPUT_LOCAL, calculation_name))

        mpi_loop(callable, len(args.paths))