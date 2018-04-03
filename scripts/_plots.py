

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
sns.set_style("white")

# see http://matplotlib.org/api/markers_api.html
MARKERS = ["v", "^", "<", ">", "o", ".", ",", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_" ] 


def plot_lines(xs, ys, xerrs=None, yerrs=None,
                        xlabel=None, ylabel=None,
                        out="out.pdf",
                        legends=None, legend_pos="best", legend_fontsize=8,
                        x_logscale=False,
                        y_logscale=False,
                        figure_size=(3.2, 2.4),
                        dpi=300,
                        tick_fontsize=8,
                        label_fontsize=8,
                        font = {"fontname": "Arial"},
                        lw=1.0,
                        line_styles=None,
                        markers=None,
                        markersize=4,
                        colors=None,
                        limits=None,
                        n_xtics=8,
                        n_ytics=8):
    """
    """
    assert isinstance(xs, list), "xs must be a list of 1D array"
    assert isinstance(ys, list), "ys must be a list of 1D array"
    assert len(xs) == len(ys), "xs and ys must have the same len"

    if xerrs is not None:
        assert isinstance(xerrs, list) and len(xerrs) == len(xs), "xerrs must be a list of same len as xs"

    if yerrs is not None:
        assert isinstance(yerrs, list) and len(yerrs) == len(ys), "yerrs must be a list of same len as ys"

    if legends is not None:
        assert len(legends) == len(xs), "legends has wrong len"

    fig = plt.figure(figsize=figure_size)
    ax = plt.axes()

    if colors is None:
        colors = [ None for _ in range(len(xs)) ]

    if markers is None:
        markers = [ None for _ in range(len(xs)) ]
        markersize  = None

    if line_styles is None:
        line_styles = [ "-" for _ in range(len(xs)) ]

    if xerrs is None:
        xerrs = [ None for _ in range(len(xs)) ]

    if yerrs is None:
        yerrs = [ None for _ in range(len(xs)) ]

    for i in range(len(xs)):
        ax.errorbar(xs[i], ys[i], xerr=xerrs[i], yerr=yerrs[i], linestyle=line_styles[i], color=colors[i], marker=markers[i], ms=markersize, lw=lw)

    ax.locator_params(axis='x', nbins=n_xtics)
    ax.locator_params(axis='y', nbins=n_ytics)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(tick_fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(tick_fontsize)

    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=label_fontsize, **font)

    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=label_fontsize, **font)

    if limits is not None:
        ax.set_xlim(limits[0:2])
        ax.set_ylim(limits[2:4])

    if x_logscale:
        ax.set_xscale("log")
    if y_logscale:
        ax.set_yscale("log")

    if legends is not None:
        plt.legend(legends, loc=legend_pos, fancybox=False, fontsize=legend_fontsize)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


def plot_heatmap_imshow(density_grid, left, right, bottom, top,
                        xlabel, ylabel, zlabel, out,
                        nticks=8,
                        figure_size = (3.2, 2.4) ):
    """
    :param density_grid: 2d array
    :param left: float
    :param right: float
    :param bottom: float
    :param top: foat
    :param xlabel: str
    :param ylabel: str
    :param zlabel: str
    :param out: str
    :param nticks: in
    :return:
    """
    dpi = 300
    fontsize = 8
    font = { "fontname": "Arial"}

    plt.figure(figsize=figure_size)

    # for more colormaps see http://matplotlib.org/examples/color/colormaps_reference.html
    my_cmap = plt.get_cmap('hot')

    plt.imshow(density_grid, cmap=my_cmap, interpolation='nearest', origin="upper",
                extent=(left, right, bottom, top))

    ax = plt.axes()
    cbar = plt.colorbar(fraction=0.046, pad=0.04)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    ax.locator_params(axis='x', nbins=nticks)
    ax.locator_params(axis='y', nbins=nticks)

    cbar.locator = ticker.MaxNLocator(nbins=nticks)
    cbar.update_ticks()
    cbar.ax.tick_params(labelsize=fontsize)
    cbar.set_label(zlabel, fontsize=fontsize, **font)

    plt.xlabel(xlabel, fontsize=fontsize, **font)
    plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None

