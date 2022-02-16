from spirit_python_utilities.spirit_extras import import_spirit, util

def main(output_file, input_file, noi, background, radius, hopfion_normal, state_prepare_callback=None, shrinking_hopfion=False):
    from spirit import state, configuration, simulation, io, geometry, chain, transition

    import os
    if not os.path.exists(os.path.dirname(os.path.abspath(output_file))):
        os.makedirs(os.path.dirname(os.path.abspath(output_file)))

    print("Saving output to:", output_file)

    with state.State(input_file) as p_state:
        state_prepare_callback(p_state)

        configuration.domain(p_state, background, idx_image=0)

        if state_prepare_callback:
            state_prepare_callback(p_state)

        util.set_output_folder(p_state, os.path.dirname(output_file), tag="")
        chain.set_length(p_state, noi)

        configuration.hopfion(p_state, radius, normal=hopfion_normal, idx_image=0)
        configuration.add_noise(p_state, 1e-2, idx_image=0)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=0)

        configuration.domain(p_state, background, idx_image=noi-1)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=noi-1)

        if shrinking_hopfion:
            for i in range(1, noi-1):
                configuration.hopfion(p_state, radius * (1-(i-1)/noi), idx_image=i)
        else:
            transition.homogeneous(p_state, 0, noi-1)

        io.chain_write(p_state, output_file)

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',           dest="output_file", type=str, nargs='?', default="output.ovf", help='The output folder')
    parser.add_argument('-f',           dest="input_file",  type=str, nargs='?', default="input.cfg", help='The input file')
    parser.add_argument('--noi',        dest="noi",         type=int, nargs='?', default=10, help='The number of images')
    parser.add_argument('--mode',       dest="mode",        type=str, nargs='?', default=10, help='mode')
    parser.add_argument('--radius',     dest="radius",      type=float, help='radius of initial hopfion', required=True)
    parser.add_argument('--normal',     dest="normal",      nargs='+',   help='normal of initial hopfion', required=True)
    parser.add_argument('--background', dest="background",  nargs='+',   help='direction of ferromagnetic background', required=True)
    parser.add_argument('--size', dest="size",  nargs='+',  help='cell_size', required=True)
    parser.add_argument('--pinned_radius', dest="pinned_radius", nargs='?', default=-1, help='the radius of the sphere of pinned spins')

    args = parser.parse_args()

    normal     = [float(f) for f in args.normal]
    background = [float(f) for f in args.background]
    size = [int(f) for f in args.size]

    def choose_spirit(x):
        return "5840c4564ba5275dc79aa7ae4cd4e79d6cf63b87".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning

    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit)[0]

    print(spirit_info)

    def state_prepare_cb(p_state):
        from spirit import geometry, configuration
        geometry.set_n_cells(p_state, size)
        configuration.domain(p_state, background, idx_image=0)
        if(args.pinned_radius > 0):
            configuration.set_pinned(p_state, True, border_spherical=args.pinned_radius, inverted=True)

    main( os.path.abspath(args.output_file), args.input_file, args.noi, background, args.radius, normal, state_prepare_cb)