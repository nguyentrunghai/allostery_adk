
from __future__ import print_function

import os
import numpy as np

from _energy_matrix import USWindow

HOWTO = "replicate"   # "new", or "replicate"
COLVAR_DIR_TO_REPLICATE = "/home/tnguye46/allostery/restraint/colvar_files"

COLVAR_PART_FILE = "definition_of_pair_of_angles_adk_atp_dist.in"
COLVAR_OUT_PREFIX = "colvar_"

FORCE_CONSTANT = 0.5

COLVAR1_NAME = "nmp_core_angle"
COLVAR2_NAME = "lid_core_angle"

START = 54

#OLD_NMP_CORE_ANGLES = range(45, 71, 5)
#OLD_LID_CORE_ANGLES = range(105, 146, 5)

#NMP_CORE_ANGLES = list( np.arange(42.5, 76, 5) )
#NMP_CORE_ANGLES = sorted(NMP_CORE_ANGLES)

#LID_CORE_ANGLES = list( np.arange(102.5, 155, 5) )
#LID_CORE_ANGLES = sorted(LID_CORE_ANGLES)

#NMP_CORE_ANGLES = list( np.arange(42.5, 76, 5) )
#LID_CORE_ANGLES = [92.5, 97.5]

#NMP_CORE_ANGLES = [45, 50, 55, 60, 65, 70]
#LID_CORE_ANGLES = [95, 100]

#NMP_CORE_ANGLES = [45, 50, 55, 60, 65, 70]
#LID_CORE_ANGLES = [90]

NMP_CORE_ANGLES = list( np.arange(42.5, 76, 5) )
LID_CORE_ANGLES = [87.5]

def progress_windows_NOT_USED():
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

def progress_windows_NOT_USED():
    lid_core = LID_CORE_ANGLES
    nmp_core = NMP_CORE_ANGLES

    pairs = []
    for y in lid_core:
        for x in nmp_core:
            pairs.append((x, y))

    for x in OLD_NMP_CORE_ANGLES:
        pairs.append((x, 150))
    return pairs


def progress_windows():
    lid_core = LID_CORE_ANGLES
    nmp_core = NMP_CORE_ANGLES

    pairs = []
    for y in lid_core:
        for x in nmp_core:
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
    assert HOWTO in ["new", "replicate"]

    if HOWTO == "new":

        centers = progress_windows()
    
        colvar_part = open(COLVAR_PART_FILE, "r").read()

        for i, (center_colvar1, center_colvar2) in enumerate(centers):

            count = START + i
            out_file_name = COLVAR_OUT_PREFIX + "%d.in" %count
            print(out_file_name, center_colvar1, center_colvar2)

            if os.path.exists(out_file_name):
                raise Exception(out_file_name + " exist")

            harmonic_part = gen_harmonic_part(center_colvar1, center_colvar2)

            open(out_file_name, "w").write(colvar_part + harmonic_part)

    elif HOWTO == "replicate":

        colvar_part = open(COLVAR_PART_FILE, "r").read()

        keep_doing = True
        count = START

        while(keep_doing):
            colvar_file_to_replicate = os.path.join(COLVAR_DIR_TO_REPLICATE, COLVAR_OUT_PREFIX + "%d.in"%count)

            if os.path.exists(colvar_file_to_replicate):
                uswindow = USWindow(colvar_file_to_replicate)
                centers = uswindow.get_centers()

                out_file_name = COLVAR_OUT_PREFIX + "%d.in" % count
                center_colvar1 = centers[COLVAR1_NAME]
                center_colvar2 = centers[COLVAR2_NAME]
                print(out_file_name, center_colvar1, center_colvar2)

                if os.path.exists(out_file_name):
                    raise Exception(out_file_name + " exist")

                harmonic_part = gen_harmonic_part(center_colvar1, center_colvar2)
                open(out_file_name, "w").write(colvar_part + harmonic_part)

                count += 1

            else:
                keep_doing = False