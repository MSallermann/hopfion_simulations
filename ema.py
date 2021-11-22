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

    N_MODES = 10
    N_CELL = [30, 30, 30]
    Jij_base = [61, -10, 0, -5]


    for lam in [-0.2,-0.1,-0.05, 1]:
        with state.State(cfgfile, quiet) as p_state:
            geometry.set_n_cells(p_state, N_CELL)

            Jij = compute_abc.get_degenerate_jij(Jij_base, compute_abc.SC, 1, lam)

            hamiltonian.set_exchange(p_state, len(Jij), Jij)

            configuration.plus_z(p_state)
            configuration.hopfion(p_state, radius=3, normal=[1,1,1])

            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO)

            parameters.ema.set_n_modes(p_state, N_MODES)
            parameters.ema.set_sparse(p_state, True)

            simulation.start(p_state, simulation.METHOD_EMA, n_iterations=1)
            io.eigenmodes_write(p_state, "eigenmodes_{}.ovf".format(lam))

if __name__ == "__main__":
    from spirit_python_utilities.spirit_utils import import_spirit, gneb_workflow, data, plotting

    os.environ["OMP_NUM_THREADS"] = "16"

    def choose_spirit(x):
        return "f5e4ae637879c".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    main()