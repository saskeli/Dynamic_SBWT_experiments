from util import *
import os


def build(fasta_file, k):
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    run_cmd(f"cd CBL && K={k} cargo +nightly build --release --examples")
    return measure_time(
        f"./CBL/target/release/examples/build_index {fasta_file} -o {cbl_file}"
    )


def count(indexed_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    out, _ = run_cmd(
        f"./CBL/target/release/examples/index_count {cbl_file} 2>&1 | tail -n 1 | cut -d ' ' -f 3"
    )
    return int(out)


def insert(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    updated_file = f"{prefix}_add_{get_basename(query_file)}.cbl"
    return measure_time(
        f"./CBL/target/release/examples/insert_index {cbl_file} {query_file} -o {updated_file}"
    )


def remove(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    updated_file = f"{prefix}_rem_{get_basename(query_file)}.cbl"
    return measure_time(
        f"./CBL/target/release/examples/remove_index {cbl_file} {query_file} -o {updated_file}"
    )


def clean(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    os.remove(cbl_file)
