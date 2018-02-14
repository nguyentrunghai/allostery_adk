
import numpy as np

# right exclusive
RESID_POS       = [22, 26]
RESNAME_POS     = [17, 20]

ATOM_NAME_POS   = [11, 17]  
ATOM_INDEX_POS  = [6, 11]

X_POS           = [27, 38]
Y_POS           = [38, 46]
Z_POS           = [46, 54]


def extract_atoms_with_resids(pdb_file, residue_pdb_indices, atom_names=None):
    """
    pdb_file    :   str, file name
    atom_names  :   list of str, atom names to be extracted
    residue_pdb_indices   : list of int, residue indices in the pdb, starting from 1 

    return: 
            a list of int which are pdb atom indices, starting from 1
            a list of strings which are lines in pdb
    """
    extracted_pdb_lines = []
    atom_indices = []

    with open(pdb_file, "r") as handle:
        for line in handle:

            if line.startswith("ATOM") or line.startswith("HETATM"):
                resid = int( line[RESID_POS[0] : RESID_POS[1]] )
                atom_name = line[ATOM_NAME_POS[0] : ATOM_NAME_POS[1]].strip()
                atom_index = int( line[ATOM_INDEX_POS[0] : ATOM_INDEX_POS[1]] )

                if resid in residue_pdb_indices:

                    if atom_names is None:
                        extracted_pdb_lines.append(line)
                        atom_indices.append(atom_index)

                    elif atom_name in atom_names:
                        extracted_pdb_lines.append(line)
                        atom_indices.append(atom_index)

    return atom_indices, extracted_pdb_lines


def extract_atoms_with_resnames(pdb_file, residue_names, atom_names=None):
    """
    pdb_file    :   str, file name
    atom_names  :   list of str, atom names to be extracted
    residue_names   : list of str, residue names in the pdb

    return: 
            a list of int which are pdb atom indices, starting from 1
            a list of strings which are lines in pdb
    """
    extracted_pdb_lines = []
    atom_indices = []

    with open(pdb_file, "r") as handle:
        for line in handle:

            if line.startswith("ATOM") or line.startswith("HETATM"):
                resname = line[ RESNAME_POS[0] : RESNAME_POS[1] ]
                atom_name = line[ATOM_NAME_POS[0] : ATOM_NAME_POS[1]].strip()
                atom_index = int( line[ATOM_INDEX_POS[0] : ATOM_INDEX_POS[1]] )

                if resname in residue_names:

                    if atom_names is None:
                        extracted_pdb_lines.append(line)
                        atom_indices.append(atom_index)

                    elif atom_name in atom_names:
                        extracted_pdb_lines.append(line)
                        atom_indices.append(atom_index)

    return atom_indices, extracted_pdb_lines



def extract_atoms_withiout_resnames(pdb_file, residue_names, atom_names=None):
    """
    pdb_file    :   str, file name
    atom_names  :   list of str, atom names to be extracted
    residue_names   : list of str, residue names in the pdb

    return: 
            a list of int which are pdb atom indices, starting from 1
            a list of strings which are lines in pdb
    """
    extracted_pdb_lines = []
    atom_indices = []

    with open(pdb_file, "r") as handle:
        for line in handle:

            if line.startswith("ATOM") or line.startswith("HETATM"):
                resname = line[ RESNAME_POS[0] : RESNAME_POS[1] ]
                atom_name = line[ATOM_NAME_POS[0] : ATOM_NAME_POS[1]].strip()
                atom_index = int( line[ATOM_INDEX_POS[0] : ATOM_INDEX_POS[1]] )

                if resname not in residue_names:

                    if atom_names is None:
                        extracted_pdb_lines.append(line)
                        atom_indices.append(atom_index)

                    elif atom_name in atom_names:
                        extracted_pdb_lines.append(line)
                        atom_indices.append(atom_index)

    return atom_indices, extracted_pdb_lines


def _distance(atom_entry_1, atom_entry_2):
    """
    atom_entry_1, atom_entry_2  :   str, ATOM entries in a pdb file
    """
    pos = [X_POS, Y_POS, Z_POS]
    
    xyz_1 = np.array( [ float( atom_entry_1[b : e] ) for b, e in pos] )
    xyz_2 = np.array( [ float( atom_entry_2[b : e] ) for b, e in pos] )

    d = (xyz_1 - xyz_2)**2
    d = np.sqrt( d.sum() )
    return d


