import plot_util

def main(data, outfile="parameter_table.txt"):

    col_header = [r"$r_0$", r"$\gamma$", r"$E_0$", r"$\mathcal{A}$", r"$\mathcal{B}$", r"$\mathcal{C}$", r"$\mathrm{a}$", r"$J_1$", r"$J_2$", r"$J_3$", r"$J_4$"]

    col_unit   = [ r"$[\textup{\AA}]$", "" , r"$[\mathrm{meV}]$", r"$[\mathrm{meV}\textup{\AA}]$", r"$[\mathrm{meV}/\textup{\AA}]$", r"$[\mathrm{meV}/\textup{\AA}]$", r"[\textup{\AA}]", r"$[\mathrm{meV}]$", r"$[\mathrm{meV}]$", r"$[\mathrm{meV}]$", r"$[\mathrm{meV}]$"   ]

    with open( outfile, "w" ) as f:

        # We begin by writing the header
        header_string = r"\begin{tabular}{"

        for h in col_header:
            header_string += " c "
        header_string += "}\n"
        header_string += 4*" "

        header_string += r"\toprule"  + "\n"
        header_string += r"\toprule"  + "\n"

        for h in col_header[:-1]:
            header_string += h + " & "
        header_string += col_header[-1] + r"\\" + "\n"

        for h in col_unit[:-1]:
            header_string += h + " & "
        header_string += col_unit[-1] + r"\\" + "\n"

        header_string += 4*" " + r"\midrule" + "\n"


        f.write(header_string)

        def data_compare(d):
            return d["l0"]*1e99 + d["gamma"]

        data.sort(key=data_compare)

        # sort data into bins of same l0
        data_binned = dict()
        for d in data:
            if d['l0'] not in data_binned.keys():
                data_binned[ d['l0'] ] = []
            data_binned[ d['l0'] ].append( d )

        # sort bins of l0 by increasing gamma
        for k,i in data_binned.items():
            data_binned[k].sort( key = lambda x: x["gamma"] )

        print(data_binned.keys())
        # return
        # package data into bins of same r0


        f.write( r"\addlinespace" + "\n" )

        for idx_l0,l0 in enumerate(data_binned.keys()):
            print(l0)

            for idx_d,d in enumerate(data_binned[l0]):
                line = ""
                # f.write(  )

                if idx_d == 0:
                    line += r"\multirow{" + f"{len(data_binned[l0])}" + r"}{*}" + "{" + f"{d['l0']:^10.1f}"  + "}  &  "
                else:
                    line += " & "

                line += f"{plot_util.gamma_to_frac(d['gamma']):^10} & {d['E0']:^10} & " 
                
                for i in range(3):
                    line += f"{d['ABC'][i]:^10.4f} & "

                line += f"{1:^10} &"

                for i in range(4):
                    if i==0:
                        line += f"{d['J'][i]:^10.0f}"
                    else:
                        line += f"{d['J'][i]:^10.4f}"

                    if i != 3:
                        line += " & "

                line += "\\\\ \n"
                #  & {d['ABC'][1]:^10.5f} & {d['ABC'][2]:^10.5f}   \n"
                # print(d["l0"], d["gamma"])
                f.write(line)

            if idx_l0 < len(data_binned.keys())-1:

                f.write( r"\addlinespace" + "\n" )
                f.write( r"\midrule" + "\n" )
                f.write( r"\addlinespace" + "\n" )
                # f.write(r"\midrule" + "\n")

        f.write( r"\bottomrule" + "\n" )
        f.write( r"\bottomrule" + "\n" )

        f.write(  r"\end{tabular}" )

if __name__ == "__main__":
    import calculation_folder
    import glob
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")
    parser.add_argument("-data", type=str, default=None)

    args = parser.parse_args()

    data  = [] # angle > 0
    for f in args.paths:
        print(f)
        calculation = calculation_folder.calculation_folder(f)

        if calculation.descriptor["max_angle_between_neighbours"] < 1e-3:
            continue

        data.append( calculation.descriptor.copy() )

    main(data)