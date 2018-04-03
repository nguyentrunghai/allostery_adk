"""
to collect reduced potential energies
"""

from __future__ import print_function

import argparse
import os

import netCDF4 as nc
import pymbar

from _energy_matrix import potential_energy_matrix
from _IO import save_to_nc

parser = argparse.ArgumentParser()

parser.add_argument('--namd_dir',               type=str, default="adk")
parser.add_argument('--colvar_setup_dir',       type=str, default="colvar_files")
parser.add_argument('--nwindows',               type=int, default=54)
parser.add_argument('--out',                    type=str, default="u_kln.nc")

args = parser.parse_args()

COLVAR_SETUP_FILE_MATCH = "colvar_*.in"
COLVAR_TRAJ_FILE = "equilibrate.colvars.traj"
NAMD_LOGFILE = "logfile"

COLVAR_SETUP_PREFIX, COLVAR_SETUP_SUFFIX = COLVAR_SETUP_FILE_MATCH.split("*")

colvar_setup_files = [os.path.join(args.colvar_setup_dir, COLVAR_SETUP_PREFIX + "%d"%i + COLVAR_SETUP_SUFFIX)
                      for i in range(args.nwindows)]

colvar_traj_files = [os.path.join(args.namd_dir, "%d"%i, COLVAR_TRAJ_FILE) for i in range(args.nwindows)]

namd_logfiles= [os.path.join(args.namd_dir, "%d"%i, NAMD_LOGFILE) for i in range(args.nwindows)]

u_kln, N_k = potential_energy_matrix(colvar_setup_files, colvar_traj_files, namd_logfiles)

nc_handle = nc.Dataset(args.out, mode="w", format="NETCDF4")

save_to_nc({"u_kln":u_kln, "N_k":N_k}, nc_handle)

nc_handle.close()
