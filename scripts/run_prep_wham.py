"""
to prepare input file for wham
"""

import os
import argparse
from collections import defaultdict

import numpy as np

from _energy_matrix import USWindow
from _wham import write_time_series_file, get_time_series_file_names, get_mins_maxs

parser = argparse.ArgumentParser()
parser.add_argument('--namd_dir',               type=str, default="adk")
parser.add_argument('--colvar_setup_dir',       type=str, default="colvar_files")
parser.add_argument('--nwindows',               type=int, default=10)

args = parser.parse_args()

meta_data_lines = defaultdict(list)
all_mins = defaultdict(list)
all_maxs = defaultdict(list)
for window in range(args.nwindows):

    colvar_file = os.path.join(args.colvar_setup_dir, "colvar_%d.in"%window )
    uswindow = USWindow(colvar_file)

    colvar_names = uswindow.get_colvar_names()
    print(window, colvar_names)
    centers = uswindow.get_centers()
    force_constant = uswindow.get_force_constant()

    colvar_traj_file = os.path.join( args.namd_dir, "%d"%window, "equilibrate.colvars.traj" )
    write_time_series_file(colvar_traj_file, colvar_names, window, exlude_first_frame=True)

    time_series_file_names = get_time_series_file_names(colvar_names, window)

    mins, maxs = get_mins_maxs(colvar_traj_file, colvar_names, exlude_first_frame=True)

    for name in colvar_names:
        line = time_series_file_names[name] + " %20.10f "%centers[name] + " %20.10f "%force_constant + "\n"
        meta_data_lines[name].append(line)

        all_mins[name].append(mins[name])
        all_maxs[name].append(maxs[name])

    join_name = "_".join(colvar_names)
    line = time_series_file_names[join_name] + " ".join([" %20.10f "%centers[n] for n in colvar_names]) + "".join(
        " %20.10f " % force_constant for _ in colvar_names) + "\n"

    meta_data_lines[join_name].append(line)

all_mins = {name : np.min(all_mins[name]) for name in colvar_names}
all_maxs = {name : np.max(all_maxs[name]) for name in colvar_names}

for name in colvar_names:
    with open("meta_" + name + ".dat", "w") as handle:
        handle.write("# min = %20.10f,  max = %20.10f\n" %(all_mins[name], all_maxs[name] ) )
        for line in meta_data_lines[name]:
            handle.write(line)

name = "_".join(colvar_names)
format_str = "".join([" %20.10f, " for _ in colvar_names])
with open("meta_" + name + ".dat", "w") as handle:
    handle.write("# mins" + format_str % tuple( [all_mins[n] for n in colvar_names]) + "\n" )
    handle.write("# maxs" + format_str % tuple( [all_maxs[n] for n in colvar_names]) + "\n" )

    for line in meta_data_lines[name]:
        handle.write(line)