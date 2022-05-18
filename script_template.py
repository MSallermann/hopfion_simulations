from spirit_extras import import_spirit
import os
import calculation_folder

SCRIPT_DIR = os.path.dirname( os.path.abspath(__file__) )
INPUT_FILE = SCRIPT_DIR + "/input.cfg"

def main(calculation_folder_path, relative_input_path, relative_output_path):
    # Read calculation folder from input path, and get the absolute input and output paths
    calculation          = calculation_folder.calculation_folder(calculation_folder_path)
    absolute_input_path  = calculation.to_abspath(relative_input_path)
    absolute_output_path = calculation.to_abspath(relative_output_path)

    print(f"Input:   {absolute_input_path}")
    print(f"Output:  {absolute_output_path}")

    # Write state prepare callback
    def state_prepare_cb(gnw, p_state):
        from spirit import geometry, configuration, hamiltonian
        geometry.set_n_cells(p_state, calculation.descriptor["n_cells"])
        configuration.domain(p_state, [0,0,1])
        hamiltonian.set_exchange(p_state, len(calculation.descriptor["J"]), calculation.descriptor["J"])

    # DO STUFF HERE

    calculation.to_json()

if __name__ == "__main__":
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    parser.add_argument("-i",   help = "Input path, relative to calculation folder" , required=True, type=str)
    parser.add_argument("-o",   help = "Output path, relative to calculation folder", required=True, type=str)
    parser.add_argument('-MPI', action='store_true')

    args = parser.parse_args()

    if not args.MPI:
        for f in args.paths:
            main(f, args.i, args.o)
    else:
        from mpi_loop import mpi_loop

        def callable(i):
            input_path = args.paths[i]
            main(input_path, args.i, args.o)

        mpi_loop(callable, len(args.paths))