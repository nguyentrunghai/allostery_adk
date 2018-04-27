"""
to select window and snapshot index for algdock calculations
"""

import os
import argparse
import pickle

import numpy as np
import mdtraj as md

from _wham import load_2d_pmf_prob, bin_centers_2_bin_edges
from _energy_matrix import load_colvar_values_matrices

parser = argparse.ArgumentParser()

parser.add_argument('--namd_dir',      type=str, default="/home/tnguye46/allostery/restraint/production/adk")
parser.add_argument('--amber_prmtop',      type=str, default="/home/tnguye46/allostery/setup/tleap/adk/receptor.prmtop")

parser.add_argument('--nwindows',      type=int, default=177)

parser.add_argument('--wham_2d_pmf_file',      type=str, default="/home/tnguye46/allostery/restraint/wham/adk/2d_nmp_core_angle_lid_core_angle/pmf.dat")
parser.add_argument('--nxbins',                 type=int, default=25)
parser.add_argument('--nybins',                 type=int, default=40)

parser.add_argument('--out',      type=str, default="selected_snapshots.pkl")

args = parser.parse_args()

KB = 0.0019872041   # kcal/mol/K
TEMPERATURE = 300.
BETA = 1./ KB / TEMPERATURE

COVAR_TRAJ_FILE = "equilibrate.colvars.traj"
NAMD_TRAJ_FILE  = "equilibrate.dcd"
X_NAME = "nmp_core_angle"
Y_NAME = "lid_core_angle"


def _save_pdb(dcd_file, top_file, frame, pdb_out):
    traj = md.load_dcd(dcd_file, top=top_file)
    assert 0 <= frame < len(traj), "frame out of range"
    traj[frame].save_pdb(pdb_out)
    return None


x, y, pmf, prob = load_2d_pmf_prob(args.wham_2d_pmf_file, args.nxbins, args.nybins)
xedges = bin_centers_2_bin_edges(x)
yedges = bin_centers_2_bin_edges(y)

colvar_traj_files = [ os.path.join(args.namd_dir, "%d"%window, COVAR_TRAJ_FILE) for window in range(args.nwindows) ]
colvar_values = load_colvar_values_matrices(colvar_traj_files)

dcd_traj_files = [ os.path.join(args.namd_dir, "%d"%window, NAMD_TRAJ_FILE) for window in range(args.nwindows) ]

colvar_x = colvar_values[X_NAME][:,1:] # exclude first frame
colvar_y = colvar_values[Y_NAME][:,1:] # exclude first frame
nsamples = colvar_x.shape[-1]

sel_snapshots = []
done_count = 1
for i, (y_below, y_above) in enumerate( zip(yedges[:-1], yedges[1:]) ):
    y_center = (y_below + y_above)/2.
    y_dist2 = (colvar_y - y_center)**2

    for j, (x_left, x_right) in enumerate( zip(xedges[:-1], xedges[1:]) ):
        x_center = (x_left + x_right)/2.

        x_dist2 = (colvar_x - x_center) **2
        dist = np.sqrt(x_dist2 + y_dist2)

        min_index =  dist.argmin()
        row_min = min_index // nsamples
        col_min = min_index % nsamples

        min_value_x =  colvar_x[row_min, col_min]
        min_value_y = colvar_y[row_min, col_min]

        weight = np.exp( - BETA * pmf[i,j] )

        window = row_min
        snapshot = col_min

        pdb_out = "%d_"%window + "%d.pdb"%snapshot

        if (x_left < min_value_x < x_right) and (y_below < min_value_y < y_above):
            out_data = {"window":window,
                        "snapshot":snapshot,
                        "x":min_value_x,
                        "y":min_value_y,
                        "xedges" :(x_left, x_right),
                        "yedges" : (y_below, y_above),
                        "wham_unnormalized_weight" : weight,
                        "wham_pmf":pmf[i,j],
                        "pdb":pdb_out}


            _save_pdb(dcd_traj_files[window], args.amber_prmtop, snapshot, pdb_out)

            sel_snapshots.append(out_data)

        done_count += 1
        print("Done for ", done_count)
        if snapshot == 0:
            print "first snapshot selected", window, snapshot


pickle.dump(sel_snapshots, open(args.out, "w"))

