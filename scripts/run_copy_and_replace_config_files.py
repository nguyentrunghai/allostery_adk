"""
to copy and replace some keyworks in the file
"""
from __future__ import print_function

import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--in_dir',               type=str, default="/home/tnguye46/allostery/restraint/equilibrate/adk")
parser.add_argument('--window_range',         type=str, default="54 177")
parser.add_argument('--config_file',          type=str, default="configuration.namd")
parser.add_argument('--launch_file',          type=str, default="/home/tnguye46/allostery/launch_cpu.sh")

args = parser.parse_args()


def _replace(infile, outfile, keyworks):
    """
    :param infile: str
    :param outfile: str
    :param keyworks: dict str -> str
    :return:
    """
    out_lines = []
    with open(infile, "r") as handle:

        for inline in handle:
            outline = inline

            for word in keyworks:

                if word in outline:
                    outline = outline.replace(word, keyworks[word])

            out_lines.append(outline)

    with open(outfile, "w") as handle:
        for outline in out_lines:
            handle.write(outline)
    return None

KEYWORDS1 = {"adk":"adk_amp", "receptor.prmtop":"complex.prmtop", "receptor.pdb":"complex.pdb"}
KEYWORDS2 = {"colvar_files":"colvar_files_adk_amp"}

begin = int()
begin, end = [int(s) for s in args.window_range.split()]
print("window_range", begin, end)

for window in range(begin, end):
    out_dir = ("%d"%window)
    if os.path.exists(out_dir):
        raise Exception(out_dir + " exist!")

    os.mkdir(out_dir)
    out_dir = os.path.abspath(out_dir)

    infile = os.path.join(args.in_dir, "%d"%window, args.config_file)
    outfile_tmp = os.path.join(out_dir, "tmp")

    _replace(infile, outfile_tmp, KEYWORDS1)

    outfile = os.path.join(out_dir, args.config_file)
    _replace(outfile_tmp, outfile, KEYWORDS2)

    os.system("cp " + args.launch_file + " " + out_dir + "/.")
    os.remove(outfile_tmp)


