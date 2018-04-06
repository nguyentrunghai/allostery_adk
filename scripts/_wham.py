"""
define functions to do wham analysis
"""

import os

import numpy as np

from _energy_matrix import load_colvar_values


def write_time_series_file(colvar_traj_file, colvar_names, window_index, exlude_first_frame=False):
    """
    :param colvar_traj_file: str
    :param colvar_names: list of str
    :param window_index: int
    :return: None
    """
    data = load_colvar_values(colvar_traj_file)
    if exlude_first_frame:
        data = data.iloc[1:]

    for name in colvar_names:
        out = name + "_%d.dat"%window_index
        with open(out, "w") as handle:
            for i, colvar_val in enumerate(data[name]):
                handle.write("%10d%20.10f\n"%(i, colvar_val))

    format_string = "%10d" + "".join(["%20.10f" for _ in colvar_names]) + "\n"
    out = "_".join(colvar_names) + "_%d.dat"%window_index
    with open(out, "w") as handle:
        for i, row in enumerate(data.index):
            handle.write(format_string % tuple( [i] + [data.iloc[i][name] for name in colvar_names] ) )

    return None


def get_time_series_file_names(colvar_names, window_index):
    """
    :param colvar_names:
    :param window_index:
    :return: dict str -> str
    """
    cwd = os.getcwd()
    file_names = {name : os.path.join(cwd, name + "_%d.dat"%window_index) for name in colvar_names}

    name = "_".join(colvar_names)
    file_names[name] = os.path.join(cwd, "_".join(colvar_names) + "_%d.dat"%window_index)
    return file_names


def get_mins_maxs(colvar_traj_file, colvar_names, exlude_first_frame=False):
    """
    :param colvar_traj_file: str
    :param colvar_names: str
    :return: mins, maxs, dict str -> float
    """
    data = load_colvar_values(colvar_traj_file)
    if exlude_first_frame:
        data = data.iloc[1:]

    mins = {name : np.min(data[name]) for name in colvar_names}
    maxs = {name : np.max(data[name]) for name in colvar_names}
    return mins, maxs


def load_1d_pmf_prob(file_name):
    data = np.loadtxt(file_name)
    x = data[:,0]
    pmf = data[:,1]
    pmf_err = data[:,2]
    prob = data[:,3]
    prob_err = data[:, 4]
    return x, pmf, pmf_err, prob, prob_err


def load_2d_pmf_prob(file_name, nxbins, nybins):
    with open(file_name, "r") as handle:
        lines = handle.readlines()

    lines = lines[1:]
    lines = [line for line in lines if not line.startswith("\n")]

    assert len(lines) == nxbins * nybins, "nr of line is wrong"

    x = np.zeros([nxbins], dtype=float)
    y = np.zeros([nybins], dtype=float)
    pmf = np.zeros([nybins, nxbins], dtype=float)
    prob = np.zeros([nybins, nxbins], dtype=float)

    l_count = -1
    for i in range(nxbins):
        for j in range(nybins):
            l_count += 1
            entries = lines[l_count].split()

            x[i] = float(entries[0])
            y[j] = float(entries[1])

            pmf[j, i] = float(entries[2])
            prob[j, i] = float(entries[3])
    return x, y, pmf, prob


def bin_centers_2_bin_edges(bin_centers):
    """
    :param bin_centers: array of shape (n,)
    :return: array of shape (n+1,)
    """
    assert bin_centers.ndim == 1, "bin_centers must be 1d"
    assert bin_centers.shape[0] > 1, "bin_centers must have at least two elements"
    bin_size = bin_centers[1] - bin_centers[0]

    n = bin_centers.shape[0]
    bin_edges = np.zeros([n+1], dtype=float)
    bin_edges[0] = bin_centers[0] - bin_size/2.

    for i in range(n):
        bin_edges[i+1] = bin_centers[i] + bin_size/2.
    return bin_edges