
from _extract_atoms import extract_atoms_with_resids

def _write_to_text(list_of_data, line_format, out_file):
    with open(out_file, "w") as handle:
        for data in list_of_data:
            handle.write(line_format % data)
    return None

if __name__ == "__main__":
    pdb_file = "/home/tnguye46/allostery/setup/tleap/adk/receptor.pdb"
    atom_names = ["N", "CA", "CB", "C"]

    res_id = [(115, 125), (90, 100), (35, 55), (179, 185), (125, 153)]

    for start_ind, end_ind in res_id:
        out_prefix = "%d_%d"%(start_ind, end_ind)
        print out_prefix

        residue_pdb_indices = range(start_ind, end_ind+1)

        atom_indices, extracted_pdb_lines = extract_atoms_use_resids(pdb_file, residue_pdb_indices, atom_names=atom_names)

        _write_to_text(atom_indices, "%6d", out_prefix+".dat")
        _write_to_text(extracted_pdb_lines, "%s", out_prefix+".pdb")

