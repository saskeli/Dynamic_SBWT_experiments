from util import *
import os


def index_path(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    return prefix + ".cbl"


def build(fasta_file, k, prefix_bits=24):
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    run_cmd(
        f"cd CBL && K={k} PREFIX_BITS={prefix_bits} cargo +nightly build --release --examples"
    )
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


def count_query(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    out, _ = run_cmd(
        f"./CBL/target/release/examples/query_index {cbl_file} {query_file} 2>&1 | tail -n 2 | head -n 1 | cut -d ' ' -f 3"
    )
    return int(out)


def query(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    return measure_time(
        f"./CBL/target/release/examples/query_index {cbl_file} {query_file}"
    )


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


def merge(indexed_file, other_indexed_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    other_prefix = f"{OUT_FOLDER}/{get_basename(other_indexed_file)}"
    other_cbl_file = other_prefix + ".cbl"
    updated_file = f"{prefix}_uni_{get_basename(other_indexed_file)}.cbl"
    return measure_time(
        f"./CBL/target/release/examples/merge_index {cbl_file} {other_cbl_file} -o {updated_file}"
    )


def intersect(indexed_file, other_indexed_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    cbl_file = prefix + ".cbl"
    other_prefix = f"{OUT_FOLDER}/{get_basename(other_indexed_file)}"
    other_cbl_file = other_prefix + ".cbl"
    updated_file = f"{prefix}_int_{get_basename(other_indexed_file)}.cbl"
    return measure_time(
        f"./CBL/target/release/examples/intersect_index {cbl_file} {other_cbl_file} -o {updated_file}"
    )


def clean(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    os.remove(cbl_file)
