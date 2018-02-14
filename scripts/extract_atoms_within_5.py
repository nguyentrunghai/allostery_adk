
from _extract_atoms import extract_atoms_with_resids

def _write_to_text(list_of_data, line_format, out_file):
    with open(out_file, "w") as handle:
        for data in list_of_data:
            handle.write(line_format % data)
    return None

def _write_to_text(list_of_data, line_format, out_file):
    with open(out_file, "w") as handle:
        for data in list_of_data:
            handle.write(line_format % data)
    return None


if __name__ == "__main__":
    # amp
    #pdb_file = "/home/tnguye46/allostery/setup/tleap/adk_amp/complex.pdb"

    # atp
    pdb_file = "/home/tnguye46/allostery/setup/tleap/adk_atp/complex.pdb"

    atom_names = ["N", "CA", "CB", "C"]

    # amp
    #resids = [30, 31, 32, 33, 35, 36, 52, 53, 56, 57, 58, 59, 60, 64, 85, 86, 87, 88, 92, 156, 158, 167]

    # atp
    resids = [8, 9, 10, 11, 12, 13, 14, 15, 16, 84, 119, 120, 122, 123, 124, 132, 133, 134, 137, 138, 156, 167, 198, 199, 200, 201, 202, 205]

    atom_indices, extracted_pdb_lines = extract_atoms_with_resids(pdb_file, resids, atom_names=atom_names)

    _write_to_text(atom_indices, "%6d", "within_5_of_atp.dat")
    _write_to_text(extracted_pdb_lines, "%s", "within_5_of_atp_bb.pdb")

