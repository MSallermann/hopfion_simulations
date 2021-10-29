
import matplotlib.pyplot as plt
from spirit_python_utilities.spirit_utils import import_spirit, util, plotting, data, gneb_workflow

def main(output_folder, initial_chain, input_file):

    from spirit import state, configuration, simulation, io, geometry, chain, transition, hamiltonian
    from spirit.parameters import gneb

    # Create the root gneb node
    gnw = gneb_workflow.GNEB_Node(output_folder, initial_chain_file=initial_chain, input_file=input_file, output_folder=output_folder)

    gnw.n_iterations_check = 2000
    gnw.convergence = 1e-6

    def mark_climbing_image(p_state, gnw, ax):
        """Helper function that marks the climbing image in a plot."""
        import numpy as np
        image_types =  np.array([gneb.get_climbing_falling(p_state, i) for i in range(chain.get_noi(p_state))])
        idx_climbing_list = np.array(range(chain.get_noi(p_state)))[image_types == gneb.IMAGE_CLIMBING]
        if(len(idx_climbing_list) == 0):
            return
        idx_climbing = idx_climbing_list[0]
        E0 = gnw.current_energy_path.total_energy[-1]
        ax.plot( gnw.current_energy_path.reaction_coordinate[idx_climbing], gnw.current_energy_path.total_energy[idx_climbing] - E0, marker="^", color="red" )

    def state_prepare_cb(gnw, p_state):
        pass

    def before_gneb_cb(gnw, p_state):
        # gneb.set_image_type_automatically(p_state)
        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP, n_iterations=1)
        gnw.current_energy_path = data.energy_path_from_p_state(p_state)
        plotting.plot_energy_path(gnw.current_energy_path, plt.gca())
        mark_climbing_image(p_state, gnw, plt.gca())
        plt.savefig(gnw.output_folder + "/path_{}_initial.png".format(gnw.total_iterations))
        plt.close()

    def step_cb(gnw, p_state):
        import numpy as np
        gnw.update_energy_path(p_state)
        plotting.plot_energy_path(gnw.current_energy_path, plt.gca())
        mark_climbing_image(p_state, gnw, plt.gca())
        plt.savefig(gnw.output_folder + "/path_{}.png".format(gnw.total_iterations))
        plt.close()

    def exit_cb(gnw, p_state):
        plotting.plot_energy_path(gnw.current_energy_path, plt.gca())
        mark_climbing_image(p_state, gnw, plt.gca())
        plt.savefig(gnw.output_folder + "/path_{}_final.png".format(gnw.total_iterations))
        plt.close()

    gnw.state_prepare_callback = state_prepare_cb
    gnw.before_gneb_callback   = before_gneb_cb
    gnw.gneb_step_callback     = step_cb
    gnw.exit_callback          = exit_cb

    gnw.run()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',  dest="output_folder", type=str, nargs='?', default="output", help='The output folder')
    parser.add_argument('-f',  dest="input_file", type=str, nargs='?', default="input.cfg", help='The input file')
    parser.add_argument('-ic', dest="initial_chain", required=True, type=str, nargs='?', help='The initial chain')

    args = parser.parse_args()

    def choose_spirit(x):
        return "5840c4564ba5275dc79aa7ae4cd4e79d6cf63b87".startswith(x.revision) and x.openMP # check for solver info revision and openMP

    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]
    print(spirit_info)

    main(args.output_folder, args.initial_chain, args.input_file)