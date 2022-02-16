import os
import sys
from typing import no_type_check
import compute_abc

def main():
    ### Import Spirit modules
    from spirit import state
    from spirit import configuration
    from spirit import simulation
    from spirit import io
    from spirit import parameters
    from spirit import geometry
    from spirit import hamiltonian
    import time
    import numpy as np

    cfgfile = "input.cfg"
    quiet = False

    CHAIN_FILE = "/home/moritz/hopfion_simulations/output_bogo_30_unpinned_sc_ci_shrinking/chain.ovf"

    N_MODES = 20

    for K in [0]:
        with state.State(cfgfile, quiet) as p_state:
            io.chain_read(p_state, CHAIN_FILE)

            for idx in [8]:
                # hamiltonian.set_anisotropy(p_state, K, [0,0,1], idx_image=0)
                # simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=0)

                parameters.ema.set_n_modes(p_state, N_MODES, idx_image=idx)
                parameters.ema.set_sparse(p_state, True, idx_image=idx)
                simulation.start(p_state, simulation.METHOD_EMA, n_iterations=1, idx_image = idx)

                io.eigenmodes_write(p_state, "eigenmodes_sp_{}.ovf".format(K), idx_image=idx)

if __name__ == "__main__":
    from spirit_python_utilities.spirit_extras import import_spirit, gneb_workflow, data, plotting

    os.environ["OMP_NUM_THREADS"] = "16"

    def choose_spirit(x):
        return "afeb6181bd4f1".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    main()