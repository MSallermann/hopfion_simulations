import numpy as np

import argparse

from matplotlib.pyplot import plot

parser = argparse.ArgumentParser()
parser.add_argument('-o', dest="output_folder", type=str, nargs='?', default=".", help='The output folder')
parser.add_argument('-f', dest="input_file", type=str, nargs='?', default="input.cfg", help='The input file')
parser.add_argument('-radius', dest="radius", type=float, default=15)


from spirit_python_utilities.spirit_utils import import_spirit, util, plotting, data
from spirit_python_utilities.spirit_utils.data import Spin_System

def main():
    import os
    args = parser.parse_args()

    output_folder = args.output_folder
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    print("Saving output to:", args.output_folder)
    spirit_info = import_spirit.find_and_insert("~/Coding")[0]

    from spirit import state, configuration, simulation, io, geometry, chain, transition
    from spirit.parameters import gneb
    import os

    pinned_sites = []
    defect_sites = []
    with state.State(args.input_file) as p_state:
        util.set_output_folder(p_state, args.output_folder)
        n_cells = geometry.get_n_cells(p_state)

        system = data.spin_system_from_p_state(p_state)
        print(system.center())
        system.shape()
        for c in range(system.n_cells[2]):
            for b in range(system.n_cells[1]):
                for a in range(system.n_cells[0]):
                    if np.linalg.norm( system.positions[0,a,b,c] - system.center() ) >= args.radius:
                        pinned_sites.append( [0,a,b,c,0,0,1] )
                        defect_sites.append( [0,a,b,c,-1] )

    with open("pinned_sites.txt", "w") as f:
        f.write("n_pinned {}\n".format(len(pinned_sites)))
        for t in pinned_sites:
            f.write( "{} {} {} {} {} {} {}\n".format( *t ) )

    with open("defect_sites.txt", "w") as f:
        f.write("n_defects {}\n".format(len(defect_sites)))
        for t in pinned_sites:
            f.write( "{} {} {} {} {}\n".format( *t ) )

if __name__ == "__main__":
    main()