from __future__ import print_function

import os
import argparse

import numpy as np
import netCDF4 as nc

from _energy_matrix import load_colvar_values_matrices
from _plots import plot_lines, plot_heatmap_imshow

def _edges_2_centers(edges):
    centers = np.zeros(len(edges)-1, dtype=float)
    for i in range(len(edges)-1):
        centers[i] = (edges[i] + edges[i+1])/2.
    return centers


def make_1d_hist(x, weights, bins, range=None):
    """
    """
    assert x.ndim == 1, "x must be 1d"
    assert x.shape == weights.shape, "x and weights must have the same shape"
    assert bins > 1, "bins must be larger than 1"

    hist, xedges = np.histogram(x, bins=bins, range=range, normed=True, weights=weights)
    xcenters = _edges_2_centers(xedges)
    
    return hist, xcenters


def make_2d_hist(y, x, weights, bins, range=None):
    assert x.ndim == y.ndim == 1, "x and y must be 1d"
    assert x.shape == y.shape == weights.shape, "x, y and weights must have the same shape"

    hist, yedges, xedges = np.histogram2d(y, x, bins=bins, range=range, normed=True, weights=weights)
    ycenters = _edges_2_centers(yedges)
    xcenters = _edges_2_centers(xedges)
    return hist, ycenters, xcenters


parser = argparse.ArgumentParser()

parser.add_argument('--namd_dir',           type=str, default="/home/tnguye46/allostery/restraint/production/adk")
parser.add_argument('--nwindows',           type=int, default=177)
parser.add_argument('--exclude_windows',        type=str, default=" ")
parser.add_argument('--weight_file',        type=str, default="/home/tnguye46/allostery/restraint/mbar_weights/adk/mbar_weights.nc")

parser.add_argument('--x',        type=str, default="nmp_core_angle")
parser.add_argument('--y',        type=str, default="lid_core_angle")

parser.add_argument('--bins_1d_x',  type=int, default=25)
parser.add_argument('--bins_1d_y',  type=int, default=50)

parser.add_argument('--bins_2d_x',  type=int, default=10)
parser.add_argument('--bins_2d_y',  type=int, default=20)

parser.add_argument('--xrange',        type=str, default="40.0  77.0")
parser.add_argument('--yrange',        type=str, default="83.0  157.0")

args = parser.parse_args()

COLVAR_TRAJ_FILE = "equilibrate.colvars.traj"
KB = 0.0019872041   # kcal/mol/K
TEMPERATURE = 300.

exclude_windows = [int(s) for s in args.exclude_windows.split()]
print("exclude_windows", exclude_windows)
use_windows = [i for i in range(args.nwindows) if i not in exclude_windows]

colvar_traj_files = [os.path.join(args.namd_dir, "%d"%i, COLVAR_TRAJ_FILE) for i in use_windows]

colvar_values = load_colvar_values_matrices(colvar_traj_files)

x = colvar_values[args.x].ravel()
y = colvar_values[args.y].ravel()

weights = nc.Dataset(args.weight_file, "r").variables["weights"][:]
weights = weights.ravel()

#----------------------------------------------------------------------
# 1d nmp_core_angle
print("1d nmp_core_angle")
x_range = [float(s) for s in args.xrange.split()]
print("x_range", x_range)

xhist, xcenters = make_1d_hist(x, weights, args.bins_1d_x, range=x_range)

xpmf = -KB * TEMPERATURE * np.log(xhist)

out = "prob_1d_x.pdf"
xlabel = "nmp core angle (deg)"
ylabel = "Probability"
plot_lines([xcenters], [xhist], xlabel=xlabel, ylabel=ylabel, out=out)

out = "pmf_1d_x.pdf"
ylabel = "PMF (kcal/mol)"
plot_lines([xcenters], [xpmf], xlabel=xlabel, ylabel=ylabel, out=out)


#----------------------------------------------------------------------
# 1d lid_core_angle
print("1d lid_core_angle")
y_range = [float(s) for s in args.yrange.split()]
print("y_range", y_range)

yhist, ycenters = make_1d_hist(y, weights, args.bins_1d_y, range=y_range)

ypmf = -KB * TEMPERATURE * np.log(yhist)

out = "prob_1d_y.pdf"
xlabel = "lid core angle (deg)"
ylabel = "Probability"
plot_lines([ycenters], [yhist], xlabel=xlabel, ylabel=ylabel, out=out)

out = "pmf_1d_y.pdf"
ylabel = "PMF (kcal/mol)"
plot_lines([ycenters], [ypmf], xlabel=xlabel, ylabel=ylabel, out=out)


#--------------------------------------------------------------------
# 2d (x,y) = (nmp_core_angle, lid_core_angle)
print("2d (nmp_core_angle, lid_core_angle)")
yx_range = [y_range, x_range]
print("xy_range", yx_range)

yxhist, ycenters, xcenters = make_2d_hist(y, x, weights, [args.bins_2d_y, args.bins_2d_x], range=yx_range)

yxpmf = -KB * TEMPERATURE * np.log(yxhist)

left = xcenters[0]
right = xcenters[-1]
bottom = ycenters[0]
top = ycenters[-1] 


out = "prob_2d.pdf"
xlabel = "nmp core angle (deg)"
ylabel = "lid core angle (deg)"
zlabel = "Probability"
plot_heatmap_imshow(yxhist[::-1,:], left, right, bottom, top,
                    xlabel, ylabel, zlabel, out,
                    nticks=8, 
                    figure_size=(6.4, 4.8) )


out = "pmf_2d.pdf"
zlabel = "PMF (kcal/mol)"
plot_heatmap_imshow(yxpmf[::-1,:], left, right, bottom, top,
        xlabel, ylabel, zlabel, out,
        nticks=8,
        figure_size=(6.4, 4.8) )

