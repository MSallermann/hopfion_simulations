from spirit_extras import import_spirit, util, data

def main(output_file, input_file, noi, background, radius, hopfion_normal, state_prepare_callback=None, input_image = None, idx_input_image=0, final_image = None, shrinking_hopfion=False):
    from spirit import state, configuration, simulation, io, geometry, chain, transition

    import os
    if not os.path.exists(os.path.dirname(os.path.abspath(output_file))):
        os.makedirs(os.path.dirname(os.path.abspath(output_file)))

    print("Saving output to:", output_file)

    with state.State(input_file) as p_state:
        util.set_output_folder(p_state, os.path.dirname(output_file), tag="")

        if state_prepare_callback:
            state_prepare_callback(p_state)

        chain.set_length(p_state, noi)

        if input_image is None:
            configuration.domain(p_state, background, idx_image=0)
            configuration.hopfion(p_state, radius, normal=hopfion_normal, idx_image=0)
            configuration.add_noise(p_state, 1e-2, idx_image=0)
            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=0)
        else:
            io.image_read(p_state, input_image, idx_image_infile=idx_input_image, idx_image_inchain=0)
            # configuration.add_noise(p_state, 1e-4, idx_image=0)
            # simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=0)

        if noi>1:
            if final_image is None:
                configuration.domain(p_state, background, idx_image=noi-1)
                # simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_LBFGS_OSO, idx_image=noi-1)
            else:
                io.image_read(p_state, final_image, idx_image_infile=0, idx_image_inchain=noi-1)

            if shrinking_hopfion:
                for i in range(1, noi-1):
                    configuration.hopfion(p_state, radius * (1-(i-1)/noi), idx_image=i)
            else:
                transition.homogeneous(p_state, 0, noi-1)
                # transition.without_zero_modes(p_state, 0, noi-1)
                # chain.update_data(p_state)
                # epath = data.energy_path_from_p_state(p_state)
                # transition.homogeneous(p_state, epath.idx_sp(), noi-1 )

        io.chain_write(p_state, output_file, fileformat = io.FILEFORMAT_OVF_BIN)

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',               dest="output_file", type=str, nargs='?', default="output.ovf", help='The output folder')
    parser.add_argument('-f',               dest="input_file",  type=str, nargs='?', default="input.cfg", help='The input file')
    parser.add_argument('-ii',              dest="input_image", type=str, nargs='?', default=None, help='The input image (ovf file)')
    parser.add_argument('-idx_input_image', dest="idx_input_image", type=int, nargs='?', default=None, help='Index of the image in the input file')
    parser.add_argument('-noi',            dest="noi",         type=int, nargs='?', default=20, help='The number of images')
    parser.add_argument('-radius',         dest="radius",      type=float, help='radius of initial hopfion', required=False, default=3)
    parser.add_argument('-normal',         dest="normal",      nargs='+',   help='normal of initial hopfion', required=False, default=[0,0,1])
    parser.add_argument('-background',     dest="background",  nargs='+',   help='direction of ferromagnetic background', required=False, default=[0,0,1])
    parser.add_argument('-size',           dest="size",  nargs='+',  help='cell_size', required=True)
    parser.add_argument('-pinned_radius',  dest="pinned_radius", nargs='?', default=-1, help='the radius of the sphere of pinned spins')

    args = parser.parse_args()

    input_image = args.input_image

    normal     = [float(f) for f in args.normal]
    background = [float(f) for f in args.background]
    size       = [int(f) for f in args.size]

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True)[0]

    print(spirit_info)

    def state_prepare_cb(p_state):
        from spirit import geometry, configuration
        geometry.set_n_cells(p_state, size)
        configuration.domain(p_state, background, idx_image=0)
        if(args.pinned_radius > 0):
            configuration.set_pinned(p_state, True, border_spherical=args.pinned_radius, inverted=True)

    main( os.path.abspath(args.output_file), args.input_file, args.noi, background, args.radius, normal, state_prepare_cb, args.input_image, args.idx_input_image)