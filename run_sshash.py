from util import measure_time
import os


def build(fasta_file, k, m=20):
    basename = os.path.basename(fasta_file)
    sshash_file = basename + ".sshash"
    return measure_time(
        f"./sshash/build/sshash build -i {fasta_file} -k {k} -m {m} -o {sshash_file} -d tmp"
    )


def clean(fasta_file):
    basename = os.path.basename(fasta_file)
    sshash_file = basename + ".sshash"
    os.remove(sshash_file)
