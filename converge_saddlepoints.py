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

    if os.path.exists( calculation.to_abspath("gneb_sp") ):
        print("Skip")
        return

    print("---")

    calculation.lock()

    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    initial_chain_file = calculation.to_abspath(os.path.join("gneb_preconverge" , "chain.ovf"))

    gnw = gneb_workflow.GNEB_Node(name="gneb_sp", input_file=INPUT_FILE, output_folder = os.path.join(calculation.output_folder, "gneb_sp"), initial_chain_file=initial_chain_file)
    gnw.state_prepare_callback = state_prepare_cb
    gnw.setup_plot_callbacks()
    gnw.n_iterations_step
    gnw.n_iterations_check   = 1000
    gnw.max_total_iterations = 20000
    gnw.prepare_moving_endpoints()
    rx = gnw.current_energy_path.reaction_coordinate
    gnw.delta_Rx_left  = (rx[1] - rx[0]) / 2
    gnw.delta_Rx_right = (rx[2] - rx[1]) / 2
    gnw.convergence = 1e-7
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