from spirit_extras import plotting, pyvista_plotting, import_spirit, data
import matplotlib.pyplot as plt
import numpy as np
import calculation_folder
import json
import os

def main(path):
    from spirit import state, geometry, chain, simulation, io

    calculation = calculation_folder.calculation_folder(path)
    params = calculation.descriptor

    gamma = params["gamma"]
    r0    = params["l0"]

    params["criterion_fulfilledness"] = max(gamma, 6*(1-gamma)) - 6.5*(1/r0)**2
    calculation.to_json()

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+")

    args = parser.parse_args()

    for f in args.paths:
        main(f)