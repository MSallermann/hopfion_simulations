import os
import numpy as np
from spirit_python_utilities.spirit_extras import import_spirit, gneb_workflow, data, plotting
import initial_path_creator, compute_abc
import matplotlib.pyplot as plt

SCRIPT_DIR   = os.path.dirname( os.path.abspath(__file__) )
N_CELL_LIST  = [23, 23, 24, 25, 26, 27, 28, 29, 30]

N_CELL_LIST  = [48]

JIJ_iso      = [1, 0.2, -0.273, -0.174] # C = 6B
JIJ_B0       = [1, -0.25, 0.0004, -0.0001] # B = 0
JIJ_C0       = [1, 0.3, 0.246, -0.793] # C = 0

JIJ_list = [JIJ_iso, JIJ_C0]
names = ["iso", "c0"]

N_CELL_LIST = [30]
JIJ_Bogo = [61, -10, 0, -5 ]
JIJ_list = [JIJ_Bogo]
names = ["bogo"]

# JIJ_list = [JIJ_list[1]]
# names    = [names[1]]

CREATE_INITIAL_PATHS   = False
PINNED                 = False
CLIMBING_IMAGE         = True
CLIMBING_AUTOMATICALLY = True
CLIMBING_IDX = 4
SHRINKING_HOPFION = True

def main():
    e_barriers = []

    for n_cell in N_CELL_LIST:
        for jij, name in zip(JIJ_list, names):

            if PINNED:
                NAME = "output_{}_{}_pinned_sc".format(name, n_cell)
            else:
                NAME = "output_{}_{}_unpinned_sc".format(name, n_cell)

            if CLIMBING_IMAGE:
                NAME += "_ci"

            if SHRINKING_HOPFION:
                NAME += "_shrinking"

            INPUT_FILE    = SCRIPT_DIR + "/input.cfg"
            OUTPUT_FOLDER = SCRIPT_DIR + "/" + NAME

            INITIAL_CHAIN = OUTPUT_FOLDER + "/initial_path_{}.ovf".format(n_cell)
            INITIAL_CHAIN = SCRIPT_DIR +  "/calculations48_preconverged_shrinking/" + NAME + "/chain.ovf"
            INITIAL_CHAIN = SCRIPT_DIR + "/output_bogo_30_unpinned_sc_shrinking/chain.ovf"
            INITIAL_CHAIN = None


            def __state_prepare_cb(p_state):
                from spirit import geometry, configuration, hamiltonian
                geometry.set_n_cells(p_state, [n_cell, n_cell, n_cell])
                configuration.domain(p_state, [0,0,1])
                if PINNED:
                    configuration.set_pinned(p_state, True, border_spherical=float(n_cell/2), inverted=True)
                hamiltonian.set_exchange(p_state, len(jij), jij)

            if CREATE_INITIAL_PATHS:
                INITIAL_CHAIN = SCRIPT_DIR + "/temp.ovf"
                # if os.path.exists(INITIAL_CHAIN):
                #     raise Exception(f"{INITIAL_CHAIN} already exists, make sure not to overwrite something you need!!!")
                initial_path_creator.main(output_file = INITIAL_CHAIN, input_file = INPUT_FILE, noi=10, background=[0,0,1], radius=3, hopfion_normal=[0,0,1], state_prepare_callback = __state_prepare_cb, shrinking_hopfion = SHRINKING_HOPFION)

            gnw = gneb_workflow.GNEB_Node(name=NAME, input_file=INPUT_FILE, output_folder=OUTPUT_FOLDER, initial_chain_file=INITIAL_CHAIN)

            gnw.n_iterations_check   = 2000
            gnw.target_noi   = 11
            gnw.max_total_iterations = 1e3
            gnw.convergence          = 1e-8
            gnw.path_shortening_constant = 1e-12
            gnw.allow_split = False

            gnw.setup_plot_callbacks()

            def before_gneb_cb(gnw, p_state):
                from spirit import parameters
                if CLIMBING_AUTOMATICALLY:
                    gnw.log("Setting image parameters automatically")
                    parameters.gneb.set_image_type_automatically(p_state)
                else:
                    gnw.log("Setting image {} to climbing".format(CLIMBING_IDX))
                    parameters.gneb.set_climbing_falling(p_state, parameters.gneb.IMAGE_CLIMBING, idx_image=CLIMBING_IDX)

            if CLIMBING_IMAGE:
                gnw.before_gneb_callback = before_gneb_cb

            [A, B, C] = compute_abc.ABC(jij, compute_abc.SC)[0]

            def state_prepare_cb(gnw, p_state):
                gnw.log("Setting n_cells to {0}, {0}, {0}".format(n_cell))
                gnw.log("Setting exchange to {} {} {} {}".format(*jij))
                gnw.log("A = {:.4f}, B = {:.4f}, C = {:.4f}, 6B = {:.4f}".format(A,B,C,6*B))
                __state_prepare_cb(p_state)

            gnw.state_prepare_callback = state_prepare_cb

            gnw.run()

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
                plt.close()

                io.image_write(p_state, gnw.output_folder + "/sp.ovf", idx_image = epath.idx_sp())

        np.savetxt("e_barriers.txt", e_barriers)

if __name__ == "__main__":
    os.environ["OMP_NUM_THREADS"] = "16"

    def choose_spirit(x):
        return "afeb6181bd4f1".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    main()