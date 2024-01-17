from util import run_cmd, measure_time, ENV
import os

def build(fasta_file, k, m=20):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    sshash_file = basename + ".sshash"
    return measure_time(f"./sshash/build/sshash build -i {fasta_file} -k {k} -m {m} -o {sshash_file} -d tmp")

def clean(fasta_file):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    sshash_file = basename + ".sshash"
    os.remove(sshash_file)
