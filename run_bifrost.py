from util import run_cmd, measure_time, ENV
import os

BIFROST_LIB = os.path.abspath("bifrost/build/lib")
if "LD_LIBRARY_PATH" in ENV:
    ENV["LD_LIBRARY_PATH"] = BIFROST_LIB + ":" + ENV["LD_LIBRARY_PATH"]
else:
    ENV["LD_LIBRARY_PATH"] = BIFROST_LIB

def build(fasta_file, k):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    prefix = basename + ".bifrost"
    return measure_time(f"./bifrost/build/bin/Bifrost build -r {fasta_file} -o {prefix} -k {k} -t 1")

def clean(fasta_file):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    prefix = basename + ".bifrost"
    gfa_file = prefix + ".gfa.gz"
    bfi_file = prefix + ".bfi"
    os.remove(gfa_file)
    os.remove(bfi_file)
