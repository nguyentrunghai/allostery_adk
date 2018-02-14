
COLVAR_PART_FILE = "definition_of_pair_of_angles_adk_amp_dist.in"
COLVAR_OUT_PREFIX = "colvar_"

FORCE_CONSTANT = 0.5

COLVAR1_NAME = "nmp_core_angle"
COLVAR2_NAME = "lid_core_angle"

NMP_CORE_ANGLES = range(45, 71, 5)
LID_CORE_ANGLES = range(105, 146, 5)

def progress_windows():
    lid_core = LID_CORE_ANGLES
    nmp_core_forward = NMP_CORE_ANGLES
    nmp_core_backward = NMP_CORE_ANGLES[::-1]

    pairs = []
    for j, y in enumerate(lid_core):
        if (j+1)%2 == 1:
            nmp_core = nmp_core_forward
        else:
            nmp_core = nmp_core_backward

        for i, x in enumerate(nmp_core):
            pairs.append((x, y))
    return pairs

def gen_harmonic_part(center_colvar1, center_colvar2):
    """
    """
    out_text = "harmonic {\n"
    out_text += "name harmonic_restr\n" 
    out_text += "colvars " + COLVAR1_NAME + " " + COLVAR2_NAME + "\n"
    out_text += "centers %0.3f %0.3f\n" %(center_colvar1, center_colvar2)
    out_text += "forceConstant %0.3f\n" % FORCE_CONSTANT
    out_text += "}\n"
    return out_text


if __name__ == "__main__":
    centers = progress_windows()
    
    colvar_part = open(COLVAR_PART_FILE, "r").read()

    for i, (center_colvar1, center_colvar2) in enumerate(centers):
        out_file_name = COLVAR_OUT_PREFIX + "%d.in" %i
        print out_file_name, center_colvar1, center_colvar2

        harmonic_part = gen_harmonic_part(center_colvar1, center_colvar2)

        open(out_file_name, "w").write(colvar_part + harmonic_part)

