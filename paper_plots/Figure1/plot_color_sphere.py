from spirit_extras import pyvista_plotting, plotting

import sys, os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../.."))

pyvista_plotting.plot_color_sphere(os.path.join(SCRIPT_DIR, "renderings", "color_sphere"), plotting.get_rgba_colors )