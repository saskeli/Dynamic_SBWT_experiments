from util import *
import os


def build(fasta_file, k, m=20):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    sshash_file = prefix + ".sshash"
    return measure_time(
        f"./sshash/build/sshash build -i {fasta_file} -o {sshash_file} -k {k} -m {m} -d tmp"
    )


def clean(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    sshash_file = prefix + ".sshash"
    os.remove(sshash_file)
