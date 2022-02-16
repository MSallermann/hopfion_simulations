import os
import numpy as np
from spirit_extras.spirit_extras import import_spirit, gneb_workflow, data, plotting
import initial_path_creator, compute_abc
import matplotlib.pyplot as plt

import json

SCRIPT_DIR         = os.path.dirname( os.path.abspath(__file__) )
OUTPUT_BASE_FOLDER = os.path.join(SCRIPT_DIR, "gamma_l0_calculations")
INPUT_FILE    = SCRIPT_DIR + "/input.cfg"

class calculation_folder:
    def __init__(self):
        self.name                    = ""
        self.output_folder           = ""
        self.descriptor_file_name    = "params.json"
        self.initial_chain_file_name = "initial_chain.ovf"
        self.descriptor = {}

    def get_descriptor_file_path(self):
        return os.path.join(self.output_folder, self.descriptor_file_name)

    def get_initial_chain_file_path(self):
        return os.path.join(self.output_folder, self.initial_chain_file_name)

    def create(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        with open(self.get_descriptor_file_path(), "w") as f:
            f.write(json.dumps(self.descriptor, indent=4))

def main():

    for i in range(8):
        gamma = float(i)/7.0
        gamma = 6.0/7.0
        l0    = 2.5 + float(i)/8.0 # A

        folder                = calculation_folder()
        folder.name           = "gamma_{:.3f}_l0_{:.3f}".format(gamma, l0)
        folder.output_folder  = os.path.join(OUTPUT_BASE_FOLDER, folder.name)

        E0      = 1.0 # me
        J       = compute_abc.J_from_reduced(E0, l0, gamma, lam=1.0).tolist()
        ABC     = compute_abc.ABC_from_reduced(E0, l0, gamma)

        n_cells = [64, 64, 64]

        folder.descriptor = dict(
            gamma   = gamma,
            l0      = l0,
            E0      = E0,
            J       = J,
            ABC     = ABC,
            n_cells = n_cells,
            initial_chain_file = "initial_chain.ovf"
        )

        folder.create()

        def __state_prepare_cb(p_state):
            from spirit import geometry, configuration, hamiltonian
            geometry.set_n_cells(p_state, n_cells)
            configuration.domain(p_state, [0,0,1])
            hamiltonian.set_exchange(p_state, len(J), J)

        initial_path_creator.main(output_file = folder.get_initial_chain_file_path(), input_file = INPUT_FILE, noi=10, background=[0,0,1], radius=3, hopfion_normal=[0,0,1], state_prepare_callback = __state_prepare_cb, shrinking_hopfion = False)

if __name__ == "__main__":

    def choose_spirit(x):
        return True
        # return "afeb6181bd4f1".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True, choose = choose_spirit )[0]

    main()