from spirit_python_utilities.spirit_utils import import_spirit, util, plotting, data

def main(output_file, input_file, noi, background, radius, hopfion_normal, mode):
    from spirit import state, configuration, simulation, io, geometry, chain, transition

    import os
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    print("Saving output to:", output_file)

    with state.State(input_file) as p_state:
        util.set_output_folder(p_state, os.path.dirname(output_file), tag="")
        chain.set_length(p_state, noi)

        configuration.domain(p_state, background, idx_image=0)
        configuration.hopfion(p_state, radius, normal=hopfion_normal, idx_image=0)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, n_iterations = 1, idx_image=0)

        configuration.domain(p_state, background, idx_image=noi-1)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, n_iterations = 1, idx_image=noi-1)

        transition.homogeneous(p_state, 0, noi-1)

        io.chain_write(p_state, output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',           dest="output_file", type=str, nargs='?', default="output", help='The output folder')
    parser.add_argument('-f',           dest="input_file",  type=str, nargs='?', default="input.cfg", help='The input file')
    parser.add_argument('--noi',        dest="noi",         type=int, nargs='?', default=10, help='The number of images')
    parser.add_argument('--mode',       dest="mode",        type=str, nargs='?', default=10, help='The number of images')
    parser.add_argument('--radius',     dest="radius",      type=float, help='radius of initial hopfion', required=True)
    parser.add_argument('--normal',     dest="normal",     nargs='+',   help='normal of initial hopfion', required=True)
    parser.add_argument('--background', dest="background", nargs='+',   help='direction of ferromagnetic background', required=True)

    args = parser.parse_args()

    normal = [float(f) for f in args.normal]
    background = [float(f) for f in args.background]

    def choose_spirit(x):
        return "5840c4564ba5275dc79aa7ae4cd4e79d6cf63b87".startswith(x.revision) and x.openMP
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    print(spirit_info)
    main(args.output_file, args.input_file, args.noi, background, args.radius, normal, args.mode)