from util import *
import os


def index_path(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    return prefix + ".sshash"


def build(fasta_file, **params):
    k = params["k"]
    m = params["m"]
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    sshash_file = prefix + ".sshash"
    return measure_time(
        f"./sshash/build/sshash build -i {fasta_file} -o {sshash_file} -k {k} -m {m} -d tmp",
        **params
    )


def query(indexed_file, query_file, **params):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    sshash_file = prefix + ".sshash"
    return measure_time(
        f"./sshash/build/sshash query -i {sshash_file} -q {query_file}",
        **params
    )
