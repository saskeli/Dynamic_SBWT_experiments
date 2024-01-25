from util import *
import os


def index_path(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    return prefix + ".hash"


def build(fasta_file, k):
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    hash_file = prefix + ".hash"
    run_cmd(f"cd hashset && K={k} cargo +nightly build --release")
    return measure_time(
        f"./hashset/target/release/hashset build {fasta_file} -o {hash_file}"
    )


def query(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    hash_file = prefix + ".hash"
    return measure_time(
        f"./hashset/target/release/hashset query {hash_file} {query_file}"
    )


def insert(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    hash_file = prefix + ".hash"
    updated_file = f"{prefix}_add_{get_basename(query_file)}.hash"
    return measure_time(
        f"./hashset/target/release/hashset insert {hash_file} {query_file} -o {updated_file}"
    )


def remove(indexed_file, query_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    hash_file = prefix + ".hash"
    updated_file = f"{prefix}_rem_{get_basename(query_file)}.hash"
    return measure_time(
        f"./hashset/target/release/hashset remove {hash_file} {query_file} -o {updated_file}"
    )


def merge(indexed_file, other_indexed_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    hash_file = prefix + ".hash"
    other_prefix = f"{OUT_FOLDER}/{get_basename(other_indexed_file)}"
    other_hash_file = other_prefix + ".hash"
    updated_file = f"{prefix}_uni_{get_basename(other_indexed_file)}.hash"
    return measure_time(
        f"./hashset/target/release/hashset merge {hash_file} {other_hash_file} -o {updated_file}"
    )


def intersect(indexed_file, other_indexed_file):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    hash_file = prefix + ".hash"
    other_prefix = f"{OUT_FOLDER}/{get_basename(other_indexed_file)}"
    other_hash_file = other_prefix + ".hash"
    updated_file = f"{prefix}_int_{get_basename(other_indexed_file)}.hash"
    return measure_time(
        f"./hashset/target/release/hashset intersect {hash_file} {other_hash_file} -o {updated_file}"
    )


def clean(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    hash_file = prefix + ".hash"
    os.remove(hash_file)
