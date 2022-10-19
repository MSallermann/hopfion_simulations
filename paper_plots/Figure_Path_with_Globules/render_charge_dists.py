import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

import top_charge
import calculation_folder

# Render the isosurfaces
def run(annotate_idx, calculation_path):
    calculation = calculation_folder.calculation_folder(calculation_path)
    gamma = calculation.descriptor["gamma"]
    l0 = calculation.descriptor["l0"]

    for i,(idx,anno) in enumerate(annotate_idx):
        plot_path = os.path.join(SCRIPT_DIR, "renderings", f"{idx}_{gamma:.3f}_{l0:.3f}_charge")
        if not os.path.exists( plot_path + ".png"):
            top_charge.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=os.path.join(SCRIPT_DIR, "renderings", f"{idx}"), idx_image_infile=idx, distance=16, annotate=-1, view="hopfion_inplane", output_dir=os.path.join(SCRIPT_DIR, "renderings"), output_suffix="_{gamma:.3f}_{l0:.3f}_charge")
        else:
            print("Skipping", plot_path + ".png")
