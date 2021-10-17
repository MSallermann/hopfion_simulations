import argparse

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-o',  dest="output_folder", type=str, nargs='?', default="output", help='The output folder')
parser.add_argument('-f',  dest="input_file", type=str, nargs='?', default="input.cfg", help='The input file')
parser.add_argument('-ic', dest="initial_chain",   required=False, type=str, nargs='?', help='The initial chain')

from spirit_python_utilities.spirit_utils import import_spirit, util, plotting, data, gneb_workflow

def main():

    import os
    args = parser.parse_args()

    def choose_spirit(x):
        return "15eae12a1ae1a11a08b8ba0e8ef7befc4884452b".startswith(x.revision) and x.openMP
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    from spirit import state, configuration, simulation, io, geometry, chain, transition, hamiltonian
    from spirit.parameters import gneb
    import os

    gnw = gneb_workflow.GNEB_Node(args.output_folder, initial_chain_file=args.initial_chain, input_file=args.input_file, output_folder=args.output_folder)

    gnw.n_iterations_check = 2000
    gnw.convergence = 5e-5

    def state_prepare_cb(gnw, p_state):
        hamiltonian.set_anisotropy(p_state, 1e-3, [0,0,1])

    def before_gneb_cb(gnw, p_state):
        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP, n_iterations=1)
        gnw.current_energy_path = data.energy_path_from_p_state(p_state)
        plotting.plot_energy_path(gnw.current_energy_path, plt.gca())
        plt.savefig(gnw.output_folder + "/path_{}_initial.png".format(gnw.total_iterations))
        plt.close()

    def step_cb(gnw, p_state):
        plotting.plot_energy_path(gnw.current_energy_path, plt.gca())
        plt.savefig(gnw.output_folder + "/path_{}.png".format(gnw.total_iterations))
        plt.close()

    def exit_cb(gnw, p_state):
        plotting.plot_energy_path(gnw.current_energy_path, plt.gca())
        plt.savefig(gnw.output_folder + "/path_{}_final.png".format(gnw.total_iterations))
        plt.close()

    gnw.state_prepare_callback = state_prepare_cb
    gnw.before_gneb_callback   = before_gneb_cb
    gnw.gneb_step_callback     = step_cb
    gnw.exit_callback          = exit_cb

    gnw.run()

if __name__ == "__main__":
    main()