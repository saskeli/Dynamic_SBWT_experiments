from util import *
import os


def build(fasta_file, k):
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    run_cmd(f"K={k} cd CBL && cargo +nightly build --release --examples")
    return measure_time(
        f"./CBL/target/release/examples/build_index {fasta_file} -o {cbl_file}"
    )


def count(fasta_file, k):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    run_cmd(f"K={k} cd CBL && cargo +nightly build --release --examples")
    out, _ = run_cmd(
        f"./CBL/target/release/examples/index_count {cbl_file} 2>&1 | tail -n 1 | cut -d ' ' -f 3"
    )
    return int(out)


def clean(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    cbl_file = prefix + ".cbl"
    os.remove(cbl_file)
