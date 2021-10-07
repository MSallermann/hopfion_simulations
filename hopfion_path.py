import argparse

from matplotlib.pyplot import plot

parser = argparse.ArgumentParser()
parser.add_argument('-o',  dest="output_folder", type=str, nargs='?', default="output", help='The output folder')
parser.add_argument('-p',  dest="plot_folder", type=str, nargs='?', default="plots", help='The plot folder, relative to output folder')
parser.add_argument('-t',  dest="output_tag", type=str, nargs='?', default="<time>", help='The output file tag')
parser.add_argument('-f',  dest="input_file", type=str, nargs='?', default="input.cfg", help='The input file')
parser.add_argument('-ii', dest="initial_image", required=False, type=str, nargs='?', help='The initial image')
parser.add_argument('-if', dest="final_image",   required=False, type=str, nargs='?', help='The final image')
parser.add_argument('-ic', dest="initial_chain",   required=False, type=str, nargs='?', help='The initial chain')
parser.add_argument('--dry', dest="dry_run", action="store_true")

from spirit_python_utilities.spirit_utils import import_spirit, util, plotting, Spin_System

def main():

    import os
    args = parser.parse_args()

    if args.dry_run:
        print("performing dry run!")

    output_folder = args.output_folder
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    plot_folder = os.path.join(output_folder, args.plot_folder)
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    print("Saving output to:", args.output_folder)
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = lambda x: (not x.cuda) and (x.openMP) )[0]
    print(spirit_info)
    from spirit import state, configuration, simulation, io, geometry, chain, transition
    from spirit.parameters import gneb
    import os

    with state.State(args.input_file) as p_state:
        util.set_output_folder(p_state, args.output_folder, tag=args.output_tag)
        import matplotlib.pyplot as plt

        noi = -1
        if args.initial_image and args.final_image:
            noi = 10
            chain.set_length(p_state, noi)
            io.image_read(p_state, args.initial_image, idx_image_inchain=0)
            io.image_read(p_state, args.final_image, idx_image_inchain=noi-1)
            transition.homogeneous(p_state, 0, noi-1)
        elif args.initial_chain:
            io.chain_read(p_state, args.initial_chain)
            noi = chain.get_noi(p_state)
        else:
            raise Exception("No initial chain or initial and final image supplied")

        energy_path = plotting.energy_path_from_p_state(p_state)
        print(energy_path.total_energy)

        plotting.plot_energy_path(energy_path, ax=plt.gca())
        plt.tight_layout()
        plt.savefig( plot_folder + "/path_energy_before_gneb.png", dpi=300 )
        plt.close()

        if args.dry_run:
            return

        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP_OSO, n_iterations = 99000)

        energy_path = plotting.energy_path_from_p_state(p_state)
        plotting.plot_energy_path(energy_path, ax=plt.gca())
        plt.tight_layout()
        plt.savefig( plot_folder + "/path_energy_before_climbing.png", dpi=300 )
        plt.close()
        io.chain_write(p_state, os.path.join(args.output_folder, "chain_before_climbing.ovf"))

        gneb.set_image_type_automatically(p_state)
        simulation.start(p_state, simulation.METHOD_GNEB, simulation.SOLVER_VP_OSO, n_iterations = 10000)

        io.chain_write(p_state, os.path.join(args.output_folder, "final_chain.ovf"))

        energy_path = plotting.energy_path_from_p_state(p_state)
        plotting.plot_energy_path(energy_path, ax=plt.gca())
        plt.tight_layout()
        plt.savefig( plot_folder + "/path_energy_after_climbing.png", dpi=300 )
        plt.close()

if __name__ == "__main__":
    main()