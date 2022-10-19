import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

import plot_spin_configuration
import calculation_folder

# Render the isosurfaces
def run(annotate_idx, calculation_path):
    calculation = calculation_folder.calculation_folder(calculation_path)
    gamma = calculation.descriptor["gamma"]
    l0 = calculation.descriptor["l0"]

    for i,(idx,anno) in enumerate(annotate_idx):
        plot_path = os.path.join(SCRIPT_DIR, "renderings", f"{idx}_{gamma:.3f}_{l0:.3f}")
        if not os.path.exists( plot_path + ".png"):
            plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=os.path.join(SCRIPT_DIR, "renderings", f"{idx}"), idx_image_infile=idx, distance=60, annotate=-1, mode="isosurface", view="hopfion_normal", output_dir=os.path.join(SCRIPT_DIR, "renderings"), output_suffix="_{gamma}_{l0}")
        else:
            print("Skipping", plot_path + ".png")


def render_globule(idx, calculation_path):
    calculation = calculation_folder.calculation_folder(calculation_path)
    gamma = calculation.descriptor["gamma"]
    l0 = calculation.descriptor["l0"]

    plot_path = os.path.join(SCRIPT_DIR, "renderings", f"globule_{idx}_{gamma:.3f}_{l0:.3f}")
    if not os.path.exists( plot_path + ".png"):
        plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=os.path.join(SCRIPT_DIR, "renderings", f"globule_iso_{idx}"), idx_image_infile=idx, distance=60, annotate=-1, mode="iso_with_arrows", view="hopfion_diagonal", output_dir=os.path.join(SCRIPT_DIR, "renderings"), output_suffix="_{gamma}_{l0}")
        plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=os.path.join(SCRIPT_DIR, "renderings", f"globule_ip_{idx}"), idx_image_infile=idx, distance=60, annotate=-1, mode="cross_section_ip", view="hopfion_inplane", output_dir=os.path.join(SCRIPT_DIR, "renderings"), output_suffix="_{gamma}_{l0}")
        plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=os.path.join(SCRIPT_DIR, "renderings", f"globule_oop_{idx}"), idx_image_infile=idx, distance=60, annotate=-1, mode="cross_section_oop", view="hopfion_normal", output_dir=os.path.join(SCRIPT_DIR, "renderings"), output_suffix="_{gamma}_{l0}")
        plot_spin_configuration.main(calculation_folder_path=calculation_path, relative_input_path="./chain_file_total.ovf", relative_output_path=os.path.join(SCRIPT_DIR, "renderings", f"globule_schematic_{idx}"), idx_image_infile=idx, distance=60, annotate=-1, mode="schematic", view="hopfion_diagonal", output_dir=os.path.join(SCRIPT_DIR, "renderings"), output_suffix="_{gamma}_{l0}")

    else:
        print("Skipping", plot_path + ".png")
