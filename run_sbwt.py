from util import run_cmd, measure_time, ENV
import os

def build(fasta_file, k, m=20):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    sbwt_file = basename + ".sbwt"
    return measure_time(f"./SBWT/build/bin/sbwt build -i {fasta_file} -k {k} -o {sbwt_file} -t 1")

def clean(fasta_file):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    sbwt_file = basename + ".sbwt"
    os.remove(sbwt_file)
