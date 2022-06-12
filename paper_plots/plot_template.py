import matplotlib.pyplot as plt
from   matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib as mpl
import numpy as np
import os

class Paper_Plot:
    # Settings
    cm = 1/2.54

    # Annotations
    annotate_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    offset_u = 1.5*np.array([0,10])
    offset_r = 1.5*np.array([10,0])
    offset_l = -1.5*offset_r
    offset_d = -1.5*offset_u
    offset_ur = (offset_r + offset_u) / np.sqrt(2)
    offset_ul = (offset_l + offset_u) / np.sqrt(2)
    offset_dr = (offset_r + offset_d) / np.sqrt(2)
    offset_dl = (offset_l + offset_d) / np.sqrt(2)

    offset_dict = {
        "u" : offset_u,
        "r" : offset_r,
        "l" : offset_l,
        "d" : offset_d,
        "ur" : offset_ur,
        "ul" : offset_ul,
        "dr" : offset_dr,
        "dl" : offset_dl
    }

    def __init__(self, width) -> None:
        mpl.rcParams["font.size"]        = 8 #'dejavusans' (default),
        mpl.rcParams["font.family"]      = "serif" #'dejavusans' (default),
        mpl.rcParams["mathtext.fontset"] = "dejavuserif" #'dejavusans' (default),
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('axes',  labelsize=8)

        self.annotate_offset_scale = 1

        self.width  = width
        self.height = width

        self.ncols              = 1
        self.nrows              = 1
        self.horizontal_margins = [0.1, 0.1]
        self.vertical_margins   = [0.1, 0.1]
        self.wspace             = 0
        self.hspace             = 0

        self.width_ratios  = None
        self.height_ratios = None

        self._fig = None
        self._gs  = None

        # self.annotate_increment = 0
        self.annotation_dict = {}

    def height_from_aspect_ratio(self, aspect_ratio):
        rel_margin_w = sum(self.horizontal_margins)
        rel_space_w  = self.wspace * (1-rel_margin_w)/self.ncols

        rel_margin_h = sum(self.vertical_margins)
        rel_space_h  = self.hspace * (1-rel_margin_h)/self.nrows

        self.height = self.width/aspect_ratio * (1 - rel_margin_w - rel_space_w) / (1 - rel_margin_h - rel_space_h)

    def fig(self):
        self._fig = plt.figure(figsize = (self.width, self.height))
        return self._fig

    def gs(self):
        self._gs = GridSpec(figure=self._fig, nrows=self.nrows, ncols=self.ncols, left=self.horizontal_margins[0], bottom=self.vertical_margins[0], right=1-self.horizontal_margins[1], top=1-self.vertical_margins[1], hspace=self.hspace, wspace=self.wspace, width_ratios=self.width_ratios, height_ratios=self.height_ratios) 
        return self._gs

    def annotate(self, ax, text, pos = [0,0.98], fontsize=8):
        ax.text(*pos, text, fontsize=fontsize, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

    def image_to_ax(self, ax, path):
        image = plt.imread(path)
        ax.imshow(image)
        ax.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)
        ax.set_facecolor([0,0,0,0])
        for k,s in ax.spines.items():
            s.set_visible(False)

    def spine_axis(self, subplotspec):
        a = self._fig.add_axes( subplotspec.get_position(self._fig) )
        a.set_facecolor([0,0,0,0])
        a.tick_params(axis='both', which='both', bottom=0, left=0, labelbottom=0, labelleft=0)
        return a

    def row(self, row_idx, sl=slice(None, None, None)):
        col_indices = range(self.ncols)[sl]
        return [ self._fig.add_subplot( self._gs[row_idx, col_idx] ) for col_idx in col_indices ]

    def col(self, col_idx, sl=slice(None, None, None)):
        row_indices = list(range(self.nrows)[sl])
        print(row_indices)
        return [ self._fig.add_subplot(self._gs[row_idx, col_idx] ) for row_idx in row_indices ]

    def annotate_graph(self, ax, xy, xy_text, text=None, key="key1", offset_scale=1):

        if not key is None:
            if not key in self.annotation_dict:
                self.annotation_dict[key] = {"annotate_increment" : 0, "annotation_list" : []}

        arrowprops = dict(arrowstyle="-")

        if text is None:
            text = self.annotate_letter[self.annotation_dict[key]["annotate_increment"]]
            self.annotation_dict[key]["annotate_increment"]  += 1

        if type(xy_text) is str:
            xy_text = Paper_Plot.offset_dict[xy_text.lower()]

        if not key is None:
            self.annotation_dict[key]["annotation_list"].append( [xy, text] )

        ax.annotate(text, xy, xy_text * offset_scale, arrowprops = arrowprops, verticalalignment="center", horizontalalignment="center", textcoords="offset points")

if __name__ == "__main__":

    def render_from_annotations(annotation_list, xlist, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for xy, text in annotation_list:
            idx = np.argmin( np.abs(xlist - xy[0]) )
            if os.path.exists(os.path.join(output_directory, f"idx_{idx}.png")):
                print("Skipping idx {idx}")
                continue
            print(f"Rendering idx {idx}")
            ## Implement rendering here

    pplot = Paper_Plot(11 * Paper_Plot.cm)
    pplot.nrows = 4
    pplot.ncols = 5
    pplot.horizontal_margins[0] = 0.15
    pplot.vertical_margins[0]   = 0.125

    pplot.height_from_aspect_ratio(5/4)

    fig = pplot.fig()
    gs  = pplot.gs()

    # Main plot
    ax_plot = fig.add_subplot(gs[1:,:-1])
    ax_plot.spines["top"].set_color("lightgrey")
    ax_plot.spines["right"].set_color("lightgrey")
    ax_plot.set_ylabel("y_label")
    ax_plot.set_xlabel("x_label")

    x = np.linspace(0,5)
    y = np.sin(x)
    ax_plot.plot(x, y)

    for i in range(0, 40, 5):
        pplot.annotate_graph(ax_plot, (x[i], y[i]), "d")

    annotation_list = pplot.annotation_dict["key1"]["annotation_list"]

    render_from_annotations(annotation_list, x, "template_renderings")

    counter = 0
    for a in pplot.row(0):
        pplot.image_to_ax(a, "sample.png")
        a.spines["left"].set_visible(True)
        a.spines["left"].set_color("lightgrey")
        pplot.annotate(a, annotation_list[counter][1] )
        counter += 1

    for a in pplot.col(-1, slice(1,None,1)):
        pplot.image_to_ax(a, "sample.png")
        a.spines["top"].set_visible(True)
        a.spines["top"].set_color("lightgrey")
        pplot.annotate(a, annotation_list[counter][1] )
        counter += 1

    pplot.spine_axis(gs[:,:])

    fig.savefig("myfig.png", dpi=300)