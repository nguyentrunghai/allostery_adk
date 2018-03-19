
from __future__ import print_function

import argparse
import os

import numpy as np
import netCDF4 as nc
import pymbar

from _energy_matrix import potential_energy_matrix
from _IO import save_to_nc

parser = argparse.ArgumentParser()

parser.add_argument('--namd_dir',               type=str, default="adk")
parser.add_argument('--colvar_setup_dir',       type=str, default="colvar_files")
parser.add_argument('--nwindows',               type=int, default=54)
parser.add_argument('--out',                    type=str, default="mbar_weights.nc")

args = parser.parse_args()

COLVAR_SETUP_FILE_MATCH = "colvar_*.in"
COLVAR_TRAJ_FILE = "equilibrate.colvars.traj"
NAMD_LOGFILE = "logfile"

COLVAR_SETUP_PREFIX, COLVAR_SETUP_SUFFIX = COLVAR_SETUP_FILE_MATCH.split("*")


def _run_mbar(u_kln, N_k):
    K = len(N_k)
    f_k_BAR = np.zeros(K)
    for k in range(K-2):
        w_F = u_kln[ k, k+1, :N_k[k] ] - u_kln[ k, k, :N_k[k] ]
        w_R = u_kln[ k+1, k, :N_k[k+1] ] - u_kln[ k+1, k+1, :N_k[k+1] ]
        f_k_BAR[k+1] = pymbar.BAR(w_F, w_R, relative_tolerance=0.000001, verbose=False, compute_uncertainty=False)
    f_k_BAR = np.cumsum(f_k_BAR)
    mbar = pymbar.MBAR(u_kln, N_k, verbose = True, initial_f_k = f_k_BAR)
    return mbar


colvar_setup_files = [os.path.join(args.colvar_setup_dir, COLVAR_SETUP_PREFIX + "%d"%i + COLVAR_SETUP_SUFFIX)
                      for i in range(args.nwindows)]

colvar_traj_files = [os.path.join(args.namd_dir, "%d"%i, COLVAR_TRAJ_FILE) for i in range(args.nwindows)]

namd_logfiles= [os.path.join(args.namd_dir, "%d"%i, NAMD_LOGFILE) for i in range(args.nwindows)]

u_kln, N_k = potential_energy_matrix(colvar_setup_files, colvar_traj_files, namd_logfiles)

#mbar = pymbar.MBAR( u_kln, N_k, verbose=True )

mbar = _run_mbar(u_kln, N_k)

weights = mbar.getWeights()

weights = weights[:, -1]

K = u_kln.shape[0]

weights = weights.reshape((K, -1))

nc_handle = nc.Dataset(args.out, mode="w", format="NETCDF4")

save_to_nc({"weights":weights}, nc_handle)

nc_handle.close()

for i in range(weights.shape[0]):
    print(i, weights[i].sum())

print("max weight", weights.max())
