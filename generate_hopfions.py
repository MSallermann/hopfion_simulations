from spirit_extras import import_spirit, gneb_workflow, data, plotting
spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]
print(spirit_info)

import os
import numpy as np
import initial_path_creator, compute_abc
import matplotlib.pyplot as plt
from calculation_folder import calculation_folder

import compute_max_angle

import json

SCRIPT_DIR         = os.path.dirname( os.path.abspath(__file__) )
OUTPUT_BASE_FOLDER = os.path.join(SCRIPT_DIR, "gamma_l0_calculations")
INPUT_FILE         = SCRIPT_DIR + "/input.cfg"

def gamma_l0_to_name(gamma, l0):
    return "gamma_{:.3f}_l0_{:.3f}".format(gamma, l0)

def main():
    gamma_list = [i/7.0 for i in range(8)]
    l0_list    = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])[::-1]

    NOI = 32
    N_CELLS = [64, 64, 64]

    # N_CELLS = [32, 32, 32]

    # gamma_list = [i/7.0 for i in range(2)]
    # l0_list = np.array([1.0])
    gamma_l0_list = [[gamma, l0] for gamma in gamma_list for l0 in l0_list]

    # Viable 32^3 hopfions
    # gamma_l0_list = [
    #     *[ [0.0/7.0, l0] for l0 in [1.5] ],
    #     *[ [1.0/7.0, l0] for l0 in [1.5, 2.0, 2.5] ],
    #     *[ [2.0/7.0, l0] for l0 in [2.0, 2.5] ],
    #     *[ [3.0/7.0, l0] for l0 in [2.0, 2.5, 3.0] ],
    #     *[ [4.0/7.0, l0] for l0 in [2.0, 2.5, 3.0, 3.5] ],
    #     *[ [5.0/7.0, l0] for l0 in [2.0, 2.5, 3.0, 3.5, 4.0] ],
    #     *[ [6.0/7.0, l0] for l0 in [2.5, 3.0, 3.5, 4.0]],
    #     *[ [7.0/7.0, l0] for l0 in [3.5, 4.0] ],
    # ]

    # sort in descending l0 order
    gamma_l0_list.sort(reverse=True, key = lambda x: x[1])

    for i, (gamma, l0) in enumerate(gamma_l0_list):
        print(f"gamma {gamma}, l0 {l0}")

        name = gamma_l0_to_name(gamma, l0)
        folder = calculation_folder(output_folder = os.path.join(OUTPUT_BASE_FOLDER, name))

        if "initial_chain_file" in folder.descriptor.keys():
            if os.path.exists(os.path.join( folder.output_folder, folder.descriptor.get("initial_chain_file", "") ) ):
                continue

        input_image = None
        name_prev   = gamma_l0_to_name(gamma, l0 - 0.5 )
        if os.path.exists(os.path.join(OUTPUT_BASE_FOLDER, name_prev)):
            folder_prev = calculation_folder(output_folder = os.path.join(OUTPUT_BASE_FOLDER, name_prev))
            input_image = os.path.join( folder_prev.output_folder, folder_prev.descriptor["initial_chain_file"] )

        E0      = 0.025 # me
        J       = compute_abc.J_from_reduced(E0, l0, gamma).tolist()
        ABC     = compute_abc.ABC_from_reduced(E0, l0, gamma)

        folder.descriptor = dict(
            gamma   = gamma,
            l0      = l0,
            E0      = E0,
            J       = J,
            ABC     = ABC,
            n_cells = N_CELLS,
            initial_chain_file = "initial_chain.ovf"
        )
        def __state_prepare_cb(p_state):
            from spirit import geometry, configuration, hamiltonian
            geometry.set_n_cells(p_state, N_CELLS)
            configuration.domain(p_state, [0,0,1])
            hamiltonian.set_exchange(p_state, len(J), J)

        folder.to_json()
        initial_path_creator.main(output_file = folder.get_initial_chain_file_path(), input_file = INPUT_FILE, noi=NOI, background=[0,0,1], radius=5, hopfion_normal=[0,0,1], input_image=input_image, state_prepare_callback = __state_prepare_cb, shrinking_hopfion = False)
        compute_max_angle.main( folder.output_folder )

if __name__ == "__main__":
    main()