
import os
import argparse

import netCDF4 as nc
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
sns.set_style("white")

from _energy_matrix import load_colvar_values_matrices


def _plot_1d_his(x, weights, bins, out, xlabel=None, ylabel=None, nticks=6):
    """
    """
    figure_size = (3.2, 2.4)
    dpi = 300
    fontsize = 8
    font = {"fontname": "Arial"}

    plt.figure(figsize=figure_size)

    n, bin_edges, _ = plt.hist(x, bins, weights=weights, normed=True, histtype='bar', color="k")

    ax = plt.axes()
    ax.locator_params(axis='x', nbins=nticks)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=fontsize, **font)

    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


def _plot_1d_kde(xs, out,
                 xlabel=None, ylabel=None,
                 color="r",
                 alpha=1.,
                 nticks=6):
    """
    """
    figure_size = (3.2, 2.4)
    dpi = 300
    fontsize = 8
    font = {"fontname": "Arial"}

    plt.figure(figsize=figure_size)
    ax = plt.axes()

    for x in xs:
        sns.kdeplot(x, shade=True, color=color, alpha=alpha)

    ax.locator_params(axis="x", nbins=nticks)
    ax.locator_params(axis="y", nbins=nticks)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=fontsize, **font)

    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None



def _plot_2d_his(x, y, weights, bins, out, xlabel=None, ylabel=None, zlabel=None, nticks=6):
    """
    """
    figure_size = (3.2, 2.4)
    dpi = 300
    fontsize = 8
    font = { "fontname": "Arial"}

    # for more colormaps see http://matplotlib.org/examples/color/colormaps_reference.html
    my_cmap = plt.get_cmap('hot')

    plt.figure(figsize=figure_size)

    n, xedges, yedges, im = plt.hist2d(x, y, bins, weights=weights, normed=True, cmap=my_cmap)

    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.locator = ticker.MaxNLocator(nbins=nticks)
    cbar.update_ticks()

    if zlabel is not None:
        cbar.set_label(zlabel, fontsize=fontsize, **font)
    cbar.ax.tick_params(labelsize=fontsize)

    ax = plt.axes()
    ax.locator_params(axis='x', nbins=nticks)
    ax.locator_params(axis='y', nbins=nticks)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=fontsize, **font)

    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


def _plot_2d_kde(x, y, out, xlabel=None, ylabel=None, zlabel=None, nticks=10):
    """
    """
    sns.set(font_scale=0.75)
    figure_size = (3.2, 2.4)
    dpi = 300
    fontsize = 8
    font = {"fontname": "Arial"}

    # for more colormaps see http://matplotlib.org/examples/color/colormaps_reference.html
    my_cmap = plt.get_cmap('hot')

    plt.figure(figsize=figure_size)
    ax = sns.kdeplot(x, y, shade=True, cbar=True, cmap=my_cmap, cbar_kws={"label": zlabel})

    ax.locator_params(axis="x", nbins=nticks)
    ax.locator_params(axis="y", nbins=nticks)

    # for tick in ax.xaxis.get_major_ticks():
    # tick.label.set_fontsize(fontsize)

    # for tick in ax.yaxis.get_major_ticks():
    # tick.label.set_fontsize(fontsize)

    if xlabel is not None:
        # plt.xlabel(xlabel, fontsize=fontsize, **font)
        plt.xlabel(xlabel)

    if ylabel is not None:
        # plt.ylabel(ylabel, fontsize=fontsize, **font)
        plt.ylabel(ylabel)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


parser = argparse.ArgumentParser()

parser.add_argument('--namd_dir',           type=str, default="/home/tnguye46/allostery/restraint/production/adk")
parser.add_argument('--nwindows',               type=int, default=54)
parser.add_argument('--weight_file',        type=str,
                    default="/home/tnguye46/allostery/restraint/mbar_weights/adk/mbar_weights.nc")

parser.add_argument('--x',        type=str, default="nmp_core_angle")
parser.add_argument('--y',        type=str, default="lid_core_angle")

parser.add_argument('--bins_1d',  type=int, default=20)
parser.add_argument('--bins_2d',  type=int, default=20)

args = parser.parse_args()

COLVAR_TRAJ_FILE = "equilibrate.colvars.traj"

colvar_traj_files = [os.path.join(args.namd_dir, "%d"%i, COLVAR_TRAJ_FILE) for i in range(args.nwindows)]

colvar_values = load_colvar_values_matrices(colvar_traj_files)

x = colvar_values[args.x].ravel()
y = colvar_values[args.y].ravel()

weights = nc.Dataset(args.weight_file, "r").variables["weights"][:]
weights = weights.ravel()

out = args.x + "_1d_unweighted.pdf"
_plot_1d_his(x, None, args.bins_1d, out, xlabel=args.x, ylabel="density")

out = args.x + "_1d_weighted.pdf"
_plot_1d_his(x, weights, args.bins_1d, out, xlabel=args.x, ylabel="density")

out = args.y + "_1d_unweighted.pdf"
_plot_1d_his(y, None, args.bins_1d, out, xlabel=args.y, ylabel="density")

out = args.y + "_1d_weighted.pdf"
_plot_1d_his(y, weights, args.bins_1d, out, xlabel=args.y, ylabel="density")


out = args.x + "_1d_kde_unweighted.pdf"
_plot_1d_kde(colvar_values[args.x], out, xlabel=args.x, ylabel="density", alpha=0.1)

out = args.y + "_1d_kde_unweighted.pdf"
_plot_1d_kde(colvar_values[args.y], out, xlabel=args.y, ylabel="density", alpha=0.1)

#
out = "2d_weighted.pdf"
_plot_2d_his(x, y, weights, args.bins_2d, out, xlabel=args.x, ylabel=args.y, zlabel="density")

out = "2d_unweighted.pdf"
_plot_2d_his(x, y, None, args.bins_2d, out, xlabel=args.x, ylabel=args.y, zlabel="density")


out = "2d_kde_unweighted.pdf"
_plot_2d_kde(x, y, out, xlabel=args.x, ylabel=args.y, zlabel="density")