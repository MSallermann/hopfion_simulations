from spirit_extras import import_spirit, gneb_workflow
import matplotlib.pyplot as plt
import numpy as np
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(path):

    calculation = calculation_folder.calculation_folder(path)

    print(path)
    print("gamma = {}, l0 = {}".format(calculation.descriptor["gamma"], calculation.descriptor["l0"]))

    if os.path.exists( calculation.to_abspath("gneb_preconverge") ):
        print("Skip")
        return

    print("---")

    calculation.lock()

    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    gnw = gneb_workflow.GNEB_Node(name="gneb_preconverge", input_file=INPUT_FILE, output_folder= os.path.join(calculation.output_folder, "gneb_preconverge"), initial_chain_file=calculation.to_abspath(calculation.descriptor["initial_chain_file"]))
    gnw.state_prepare_callback = state_prepare_cb
    gnw.target_noi = 16
    gnw.max_total_iterations = 20000
    gnw.setup_plot_callbacks()
    gnw.convergence = 5e-4
    gnw.to_json()
    gnw.run()
    calculation.unlock()

if __name__ == "__main__":

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    for f in args.paths:
        main(f)