from spirit_extras import plotting, pyvista_plotting, import_spirit, data
import matplotlib.pyplot as plt
import numpy as np
import calculation_folder
import json

def main(path):
    from spirit import state, geometry, chain, simulation, io

    calculation = calculation_folder.calculation_folder(path)
    params = calculation.descriptor

    if "max_angle_between_neighbours" in params.keys():
        return

    with state.State("input.cfg", quiet=True) as p_state:
        geometry.set_n_cells(p_state, params["n_cells"])

        io.image_read(p_state, os.path.join(path, params["initial_chain_file"]), 0, 0)
        spin_system = data.spin_system_from_p_state(p_state)

        spin_system.shape()
        max_ang = 0

        for c in range(spin_system.n_cells[2]-1):
            for b in range(spin_system.n_cells[1]-1):
                for a in range(spin_system.n_cells[0]-1):
                    s = spin_system.spins[0, a, b, c]
                    spins = [   spin_system.spins[0, a+1, b, c],
                                spin_system.spins[0, a, b+1, c],
                                spin_system.spins[0, a, b, c+1] ]
                    for s2 in spins:
                        angle = np.arccos(np.dot(s, s2))
                        max_ang = max(max_ang, angle)

        print(calculation.descriptor["l0"], calculation.descriptor["gamma"])
        print(max_ang)
        params["max_angle_between_neighbours"] = max_ang
        calculation.to_json()
    return max_ang

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="input_folder", type=str, nargs='?', help='The input folder')

    args = parser.parse_args()

    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    import glob

    files = glob.glob( args.input_folder)

    for f in files:
        main(f)