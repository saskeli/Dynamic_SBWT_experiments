from util import *
import os


def build(fasta_file, k):
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    bufboss_folder = prefix + "_bufboss"
    if fasta_file.endswith(".gz"):
        unzipped_file = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
        run_cmd(f"gzip -cd {fasta_file} > {unzipped_file}")
        fasta_file = unzipped_file
    return measure_time(
        f"./bufboss/bin/bufboss_build -a {fasta_file} -o {bufboss_folder} -k {k} -t tmp"
    )


def query(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    bufboss_folder = prefix + "_bufboss"
    if query_file.endswith(".gz"):
        unzipped_file = f"{OUT_FOLDER}/{get_basename(query_file)}"
        run_cmd(f"gzip -cd {query_file} > {unzipped_file}")
        query_file = unzipped_file
    return measure_time(f"./bufboss/bin/bufboss_query -i {bufboss_folder} -q {query_file}")


def clean(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    bufboss_folder = prefix + "_bufboss"
    os.remove(bufboss_folder)
