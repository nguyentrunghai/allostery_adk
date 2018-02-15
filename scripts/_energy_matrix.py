

from __future__ import print_function

from collections import defaultdict

import numpy as np
import pandas as pd

KB = 0.0019872041   # kcal/mol/K
TEMPERATURE = 298.15
BETA = 1./ KB / TEMPERATURE

class USWindow(object):
    def __init__(self, colvar_file):
        """
        :param colvar_file: str, name of namd colvar file
        """
        self._centers, self._force_constant = self._read_colvar_file(colvar_file)
        self._colvar_names = sorted( self._centers.keys() )

    def _read_colvar_file(self, file_name):
        """
        :param file_name:  str, name of namd colvar file
        :return: (centers, force_constant)
                    centers is a dict mapping from colvar names to float
                    force_constant is a float
        """
        lines = []
        with open(file_name, "r") as handle:
            whether_read_line = False
            for line in handle:
                if line.strip().startswith("harmonic"):
                    whether_read_line = True
                if whether_read_line:
                    lines.append(line)

        names = None
        centers = None
        force_constant = None

        for line in lines:
            if line.strip().startswith("colvars"):
                names = line.strip().split()[1:]

            if line.strip().startswith("centers"):
                centers = line.strip().split()[1:]

            if line.strip().startswith("forceConstant"):
                force_constant = line.strip().split()[-1]

        assert names is not None, "names is None"
        assert centers is not None, "centers is None"
        assert force_constant is not None, "force_constant is None"

        centers = {name: float(center) for name, center in zip(names, centers)}
        force_constant = float(force_constant)
        return centers, force_constant

    def get_colvar_names(self):
        return self._colvar_names

    def cal_biasing_potentials(self, colvar_values):
        """
        :param colvar_values: pandas DataFrame, having colums in self._colvar_names
        :return: pandas Series
        """
        nsamples = len(colvar_values)
        potentials = pd.Series(np.zeros(nsamples))

        for colvar in self._colvar_names:
            potentials += 0.5 * self._force_constant * (colvar_values[colvar] - self._centers[colvar])**2

        if np.any(potentials.isnull()):
            raise Exception("There are null values in potentials")

        return potentials

    def cal_biasing_forces(self, colvar_values):
        """
        :param colvar_values:  pandas DataFrame, having colums in self._colvar_names
        :return: pandas DataFrame
        """
        nsamples = len(colvar_values)
        centers = pd.DataFrame([self._centers]*nsamples)
        data = colvar_values[self._colvar_names]
        forces = - self._force_constant * (data - centers)

        if np.any(forces.isnull()):
            raise Exception("There are null values in forces")
        return forces


def load_colvar_values_and_forces(file_name):
    """
    :param file_name: str
    :return: a pandas DataFrame
    """
    header = open(file_name, "r").readline()
    assert header.startswith("#"), file_name + ": first line does not start with #"
    columns = header.split()[2:]
    data = np.loadtxt(file_name)[:, 1:]
    return pd.DataFrame(data, columns=columns)


def load_colvar_values(file_name):
    """
    :param file_name: str
    :return: a pandas DataFrame
    """
    data = load_colvar_values_and_forces(file_name)
    all_columns = list(data.columns)
    sel_columns = [col for col in all_columns if ( not col.startswith("fa_") ) and col.split("fa_")[-1] in all_columns]
    return data[sel_columns]


def load_namd_energy(file_name):
    """

    :param file_name: str
    :return: energies, pandas DataFrame
    """
    energy_lines = []
    header_line = None
    with open(file_name, "r") as handle:
        for line in handle:
            if line.startswith("ETITLE:"):
                header_line = line

            elif line.startswith("ENERGY:"):
                energy_lines.append(line)

    if header_line is None:
        raise Exception("Cannot find header line")
    if len(energy_lines) == 0:
        raise Exception("There is no energy line")

    columns = header_line.split()[1:]
    ncols = len(columns)
    nlines = len(energy_lines)

    data = np.zeros([nlines, ncols])

    for i, line in enumerate(energy_lines):
        data[i,:] = np.array( [ float(entry) for entry in line.split()[1:] ] )

    return pd.DataFrame(data, columns=columns)


def unbiased_potentials(namd_logfile):
    """
    :param namd_logfile: str
    :return: u0, pandas Series
    """
    data = load_namd_energy(namd_logfile)
    u0 = data["POTENTIAL"] - data["MISC"]

    if np.any(u0.isnull()):
        raise Exception("There are null value in unbiased_potentials extracted from " + namd_logfile)
    return u0


def potential_energy_matrix(colvar_setup_files, colvar_traj_files, namd_logfiles):
    """
    :param colvar_setup_files: list of str
    :param colvar_traj_files: list of str
    :param namd_logfiles: list of str
    :return: u_kln, 3D ndarray
    """
    assert len(colvar_setup_files) == len(colvar_traj_files) == len(namd_logfiles), "all list of files must have the same len"

    u0_kl = []
    for namd_logfile in namd_logfiles:
        u0 = unbiased_potentials(namd_logfile)
        u0_kl.append(u0)
    u0_kl = np.array(u0_kl)

    K, N = u0_kl.shape
    L = K + 1
    print("(K, N) = ", K, N)
    u_kln = np.zeros([K, L, N])
    u_kln[:, -1, :] = u0_kl

    us_windows = [USWindow(colvar_setup_file) for colvar_setup_file in colvar_setup_files]
    colvar_values = [load_colvar_values(colvar_traj_file) for colvar_traj_file in colvar_traj_files]

    for k in range(K):
        sample_k = colvar_values[k]

        for l in range(K):
            window_l = us_windows[l]

            pot = window_l.cal_biasing_potentials(sample_k)

            u_kln[k, l, :] = pot.values

    u_kln *= BETA

    N_k = np.ones([L], dtype=int)*N
    N_k[-1] = 0

    return u_kln, N_k


def load_colvar_values_matrices(colvar_traj_files):
    """
    :param colvar_traj_files: list of str
    :return: dict mapping colvar name to ndarray of shape (K, N)
    """
    colvar_values = defaultdict(list)

    for traj_file in colvar_traj_files:
        values = load_colvar_values(traj_file)

        for colvar in values.columns:
            colvar_values[colvar].append(values[colvar].values)

    colvar_values = {colvar:np.array(colvar_values[colvar]) for colvar in colvar_values}

    shapes = [colvar_values[colvar].shape for colvar in colvar_values]
    assert len(set(shapes)) == 1, "colvar_values has arrays of different shape"

    return colvar_values

