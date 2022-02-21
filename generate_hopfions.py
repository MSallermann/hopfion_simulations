from spirit_extras import import_spirit, gneb_workflow, data, plotting
spirit_info = import_spirit.find_and_insert("~/Coding/spirit", stop_on_first_viable=True )[0]
print(spirit_info)

import os
import numpy as np
import initial_path_creator, compute_abc
import matplotlib.pyplot as plt
from calculation_folder import calculation_folder

import json

SCRIPT_DIR         = os.path.dirname( os.path.abspath(__file__) )
OUTPUT_BASE_FOLDER = os.path.join(SCRIPT_DIR, "gamma_l0_calculations")
INPUT_FILE         = SCRIPT_DIR + "/input.cfg"

def main():
    gamma_list = [i/7.0 for i in range(8)]
    gamma_list = [1.0]
    l0_list    = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    gamma_l0_list = [[gamma, l0] for gamma in gamma_list for l0 in l0_list]

    for gamma, l0 in gamma_l0_list:

        name = "gamma_{:.3f}_l0_{:.3f}".format(gamma, l0)

        folder = calculation_folder(output_folder = os.path.join(OUTPUT_BASE_FOLDER, name))

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

        def __state_prepare_cb(p_state):
            from spirit import geometry, configuration, hamiltonian
            geometry.set_n_cells(p_state, n_cells)
            configuration.domain(p_state, [0,0,1])
            hamiltonian.set_exchange(p_state, len(J), J)

        initial_path_creator.main(output_file = folder.get_initial_chain_file_path(), input_file = INPUT_FILE, noi=10, background=[0,0,1], radius=5, hopfion_normal=[0,0,1], state_prepare_callback = __state_prepare_cb, shrinking_hopfion = False)

if __name__ == "__main__":
    main()