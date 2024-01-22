from util import measure_time, run_cmd
import os


def build(fasta_file, k):
    basename = os.path.basename(fasta_file)
    cbl_file = basename + ".cbl"
    run_cmd(f"K={k} cd CBL && cargo +nightly build --release --examples")
    return measure_time(
        f"./CBL/target/release/examples/build_index {fasta_file} -o {cbl_file}"
    )


def count(fasta_file, k):
    basename = os.path.basename(fasta_file)
    cbl_file = basename + ".cbl"
    run_cmd(f"K={k} cd CBL && cargo +nightly build --release --examples")
    out, _ = run_cmd(
            f"./CBL/target/release/examples/index_count {cbl_file} 2>&1 | tail -n 1 | cut -d ' ' -f 3"
        )
    return int(out)


def clean(fasta_file):
    basename = os.path.basename(fasta_file)
    cbl_file = basename + ".cbl"
    os.remove(cbl_file)
