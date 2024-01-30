from util import *
import os


def index_path(fasta_file):
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    return prefix + ".packed.dbg"


def build(fasta_file, **params):
    k = params["k"]
    os.makedirs(OUT_FOLDER, exist_ok=True)
    prefix = f"{OUT_FOLDER}/{get_basename(fasta_file)}"
    count_file = prefix + ".solid_kmers_binary"
    packed_file = prefix + ".packed"
    time1, mem1 = measure_time(f"./dynboss/dsk-1.6906/dsk {fasta_file} {k} -o {prefix}", **params)
    time2, mem2 = measure_time(f"./dynboss/bin/cosmo-pack {count_file} -o {prefix}", **params)
    time3, mem3 = measure_time(f"./dynboss/bin/dynamicBOSS build -p {packed_file}", **params)
    return time1 + time2 + time3, max(mem1, mem2, mem3)


def query(indexed_file, query_file, **params):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    dbg_file = prefix + ".packed.dbg"
    if query_file.endswith(".gz"):
        unzipped_file = f"{OUT_FOLDER}/{get_basename(query_file)}"
        run_cmd(f"gzip -cd {query_file} > {unzipped_file}")
        query_file = unzipped_file
    return measure_time(f"./dynboss/bin/dynamicBOSS query -g {dbg_file} -s {query_file}", **params)


def insert(indexed_file, query_file, **params):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    dbg_file = prefix + ".packed.dbg"
    if query_file.endswith(".gz"):
        unzipped_file = f"{OUT_FOLDER}/{get_basename(query_file)}"
        run_cmd(f"gzip -cd {query_file} > {unzipped_file}")
        query_file = unzipped_file
    return measure_time(f"./dynboss/bin/dynamicBOSS add -g {dbg_file} -s {query_file}", **params)


def remove(indexed_file, query_file, **params):
    prefix = f"{OUT_FOLDER}/{get_basename(indexed_file)}"
    dbg_file = prefix + ".packed.dbg"
    if query_file.endswith(".gz"):
        unzipped_file = f"{OUT_FOLDER}/{get_basename(query_file)}"
        run_cmd(f"gzip -cd {query_file} > {unzipped_file}")
        query_file = unzipped_file
    return measure_time(f"./dynboss/bin/dynamicBOSS delete -g {dbg_file} -s {query_file}", **params)
