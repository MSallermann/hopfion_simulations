import os, sys
import calculation_folder
import sys

from spirit_extras import import_spirit, data
import matplotlib.pyplot as plt
import numpy as np
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

quiet = False

def main(path):
    from spirit import simulation
    calculation = calculation_folder.calculation_folder(path)
    output_name = "gneb_sp3"

    # print(path)
    # print("gamma = {}, l0 = {}".format(calculation.descriptor["gamma"], calculation.descriptor["l0"]))
    # if os.path.exists( calculation.to_abspath(output_name) ):
    #     print("Skip")
    #     return
    # print("---")

    calculation.lock()

    def state_prepare_cb(p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    initial_chain_file = calculation.to_abspath(os.path.join(output_name , "chain.ovf"))

    from spirit import state
    from spirit import configuration
    from spirit import simulation
    from spirit import io
    from spirit import parameters
    from spirit import geometry
    from spirit import hamiltonian
    import time
    import numpy as np

    N_MODES = 7
    with state.State(INPUT_FILE, quiet) as p_state:
        state_prepare_cb(p_state)
        io.chain_read(p_state, initial_chain_file)
        epath = data.energy_path_from_p_state(p_state)
        idx   = 1

        parameters.ema.set_n_modes(p_state, N_MODES, idx_image=idx)
        parameters.ema.set_sparse(p_state, True, idx_image=idx)
        print("start")
        simulation.start(p_state, simulation.METHOD_EMA, n_iterations=1, idx_image = idx)
        io.eigenmodes_write(p_state, calculation.to_abspath("eigenmodes_sp.ovf"), idx_image=idx)


if __name__ == "__main__":

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    args = parser.parse_args()

    for f in args.paths:
        main(f)