import os
import numpy as np
from spirit_python_utilities.spirit_utils import import_spirit, gneb_workflow, data, plotting
import initial_path_creator, compute_abc
import matplotlib.pyplot as plt

SCRIPT_DIR   = os.path.dirname( os.path.abspath(__file__) )
N_CELL_LIST  = [23, 23, 24, 25, 26, 27, 28, 29, 30]

# JIJ          = [1, -0.25, 0.0004, -0.0001] # B = 0
# JIJ          = [1, 0.2, -0.273, -0.174] # C = 6B
# JIJ          = [1, 0.3, 0.246, -0.793] # C = 0

N_CELL_LIST  = [30]
JIJ          = [61, -10, 0, -5]
PINNED       = False

def main():
    e_barriers = []
    for n_cell in N_CELL_LIST:
        INPUT_FILE    = SCRIPT_DIR + "/input.cfg"
        INITIAL_CHAIN = SCRIPT_DIR + "/initial_path_{}.ovf".format(n_cell)

        if PINNED:
            NAME = "output_gneb_pinned_sc_{}".format(n_cell)
        else:
            NAME = "output_gneb_unpinned_sc_{}".format(n_cell)

        OUTPUT_FOLDER = SCRIPT_DIR + "/" + NAME

        def __state_prepare_cb(p_state):
            from spirit import geometry, configuration, hamiltonian
            geometry.set_n_cells(p_state, [n_cell, n_cell, n_cell])
            configuration.domain(p_state, [0,0,1])
            if PINNED:
                configuration.set_pinned(p_state, True, border_spherical=float(n_cell/2), inverted=True)
            hamiltonian.set_exchange(p_state, len(JIJ), JIJ)

        initial_path_creator.main(output_file = INITIAL_CHAIN, input_file = INPUT_FILE, noi=10, background=[0,0,1], radius=3, hopfion_normal=[1,1,1], state_prepare_callback = __state_prepare_cb)


        INITIAL_CHAIN = "/home/moritz/hopfion_simulations/initial_paths/chain_30_unpinned_pre.ovf"
        gnw = gneb_workflow.GNEB_Node(name=NAME, input_file=INPUT_FILE, output_folder=OUTPUT_FOLDER, initial_chain_file=INITIAL_CHAIN)

        gnw.n_iterations_check   = 2000
        gnw.max_total_iterations = 1e6
        gnw.convergence          = 1e-6
        gnw.path_shortening_constant = 1e-7

        gnw.setup_plot_callbacks()

        [A, B, C] = compute_abc.ABC(JIJ, compute_abc.SC)
        def state_prepare_cb(gnw, p_state):
            gnw.log("Setting n_cells to {0}, {0}, {0}".format(n_cell))
            gnw.log("Setting exchange to {} {} {} {}".format(*JIJ))
            gnw.log("A = {:.4f}, B = {:.4f}, C = {:.4f}, 6B = {:.4f}".format(A,B,C,6*B))
            __state_prepare_cb(p_state)

        gnw.state_prepare_callback = state_prepare_cb

        def before_gneb_cb(gnw, p_state):
            from spirit import parameters
            parameters.gneb.set_image_type_automatically(p_state)
        gnw.before_gneb_callback = before_gneb_cb
        gnw.run()

        # gnw.clamp_and_refine(idx_max_list=None, max_total_iterations=1e6, convergence=5e-4, apply_ci=False, target_noi=3)
        # gnw.clamp_and_refine(idx_max_list=None, max_total_iterations=1e6, convergence=1e-5, apply_ci=True, target_noi=3)

        gnw.to_json()
        gnw.collect_chain(gnw.output_folder + "/collected_chain.ovf")

        # Compute the energy barrier from the collected chain
        from spirit import state, io
        with state.State(INPUT_FILE) as p_state:
            __state_prepare_cb(p_state)
            io.chain_read(p_state, gnw.output_folder + "/collected_chain.ovf")
            epath = data.energy_path_from_p_state(p_state)

            e_barriers.append( [n_cell, epath.barrier()] )
            gnw.log("total barrier = {} mev".format(epath.barrier()))

            plotting.plot_energy_path(epath, plt.gca())
            plt.savefig(gnw.output_folder + "/collected_path.png", dpi=300)

            io.image_write(p_state, gnw.output_folder + "/sp.ovf", idx_image = epath.idx_sp())

    np.savetxt("e_barriers.txt", e_barriers)

if __name__ == "__main__":
    os.environ["OMP_NUM_THREADS"] = "16"

    def choose_spirit(x):
        return "f5e4ae637879c".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    main()