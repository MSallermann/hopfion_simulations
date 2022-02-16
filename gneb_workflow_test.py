
import matplotlib.pyplot as plt
from spirit_python_utilities.spirit_extras import import_spirit, gneb_workflow

def main(output_folder, initial_chain, input_file):

    from spirit import state, configuration, simulation, io, geometry, chain, transition, hamiltonian
    from spirit.parameters import gneb

    gnw = gneb_workflow.GNEB_Node(output_folder, initial_chain_file=initial_chain, input_file=input_file, output_folder=output_folder)

    gnw.n_iterations_check = 2000
    gnw.max_total_iterations = 50000
    gnw.convergence = 1e-3

    gnw.setup_plot_callbacks()
    gnw.run()
    gnw.clamp_and_refine(mode = "max", max_total_iterations=10000, convergence=1e-4)
    gnw.clamp_and_refine(mode = 2,     max_total_iterations=10000, convergence=1e-5)
    gnw.clamp_and_refine(mode = 2,     max_total_iterations=12e3,  convergence=1e-8, apply_ci=True, target_noi=3)
    gnw.to_json()
    gnw.collect_chain(gnw.output_folder + "/collected_chain.ovf")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',  dest="output_folder", type=str, nargs='?', default="output", help='The output folder')
    parser.add_argument('-f',  dest="input_file", type=str, nargs='?', default="input.cfg", help='The input file')
    parser.add_argument('-ic', dest="initial_chain", required=True, type=str, nargs='?', help='The initial chain')

    args = parser.parse_args()

    def choose_spirit(x):
        return "5840c4564ba5275dc79aa7ae4cd4e79d6cf63b87".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning

    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]
    print(spirit_info)

    main(args.output_folder, args.initial_chain, args.input_file)