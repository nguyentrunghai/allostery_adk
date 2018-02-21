"""
annotated scatter plots of centers
"""

import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

from _energy_matrix import USWindow

parser = argparse.ArgumentParser()
parser.add_argument('--colvar_files_dir',       type=str, default="./")
parser.add_argument('--nr_colvar_files',        type=int, default=138)

parser.add_argument('--x',                      type=str, default="nmp_core_angle")
parser.add_argument('--y',                      type=str, default="lid_core_angle")

parser.add_argument('--out',                    type=str, default="us_center_positions.pdf")
args = parser.parse_args()

COLVAR_OUT_PREFIX = "colvar_"


def _annotated_scatter_plot(xs, ys, point_labels, colors, out, xlabel=None, ylabel=None, nticks=10):
    """
    :param xs:
    :param ys:
    :param point_lables:
    :param xlabel:
    :param ylabel:
    :param nticks:
    :return:
    """
    figure_size = (6.4, 6.4)
    dpi = 300
    fontsize = 8
    font = {"fontname": "Arial"}

    fig = plt.figure(figsize=figure_size)
    ax = plt.axes()

    ax.scatter(xs, ys, c="k", marker=".")
    for x, y, point_label in zip(xs, ys, point_labels):
        ax.annotate(point_label, (x, y), fontsize=fontsize, color=colors[point_label])

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


centers = []
for i in range(args.nr_colvar_files):
    colvar_file = os.path.join(args.colvar_files_dir, COLVAR_OUT_PREFIX + "%d.in" %i)
    print "loading " + colvar_file

    uswindow = USWindow(colvar_file)
    centers.append( uswindow.get_centers() )

xs = [center[args.x] for center in centers]
ys = [center[args.y] for center in centers]
point_labels = range(args.nr_colvar_files)

colors = ["r" if i<54 else "k" for i in range(args.nr_colvar_files)]
_annotated_scatter_plot(xs, ys, point_labels, colors, args.out, xlabel=args.x, ylabel=args.y)
