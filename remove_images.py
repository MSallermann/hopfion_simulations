import calculation_folder
import numpy as np
import matplotlib.pyplot as plt

def main(input_chain, output_chain, remove, invert):
    from spirit import state, simulation, chain, io

    OUTPUT_DIR = os.path.dirname(output_chain)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with state.State("input.cfg") as p_state:
        io.chain_read(p_state, input_chain)
        noi = chain.get_noi(p_state)

        idx_list    = list(range(noi))
        remove_list = idx_list[remove]
        if invert:
            remove_list = [x for x in idx_list if x not in remove_list]

        remove_list = np.array(remove_list)
        print(remove_list)

        for i in range(len(remove_list)):
            chain.delete_image(p_state, remove_list[i])
            remove_list -= 1

        io.chain_write(p_state, output_chain)

if __name__ == "__main__":
    from spirit_extras import import_spirit, chain_io, data, plotting
    spirit_info = import_spirit.find_and_insert("~/Coding/spirit_hopfion", stop_on_first_viable=True )[0]

    def string_to_slice(string):
        temp = [s for s in string.split(":")]
        temp2 = []
        for i,s in enumerate(temp):
            res = 0
            if len(s) > 0:
                res = int(s)
            else:
                if i==0:
                    res = 0
                elif i==1:
                    res = -1
                elif i==2:
                    res = 1
            temp2.append(res)
        return slice(*temp2)

    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",      help = "input path", type=str, required=True, default=None)
    parser.add_argument("-o",      help = "output path", required=True, type=str)
    parser.add_argument("-remove", help = "slice to remove, using start:stop:step syntax", required=True, type=str)
    parser.add_argument("-invert", help = "removes everything *except* the slice", required=False, action = "store_true")

    args = parser.parse_args()
    remove = string_to_slice(args.remove)
    main(args.i, args.o, remove, args.invert)