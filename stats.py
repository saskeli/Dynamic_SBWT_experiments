from util import *
import os
import json
import run_bifrost
import run_cbl
import run_dynboss
import run_sbwt
import run_sshash


DATA_FOLDER = "data"


def build_filename(prefix, fasta_file):
    basename = get_basename(fasta_file)
    size = get_filesize(fasta_file)
    return f"{DATA_FOLDER}/{prefix}_{size}_{basename}.json"


def build_stats(fasta_file, k):
    output = build_filename("build", fasta_file)
    data = {"file": fasta_file}
    time, mem = run_cbl.build(fasta_file, k)
    data["CBL"] = {"time": time, "mem": mem}
    time, mem = run_sshash.build(fasta_file, k)
    data["SSHash"] = {"time": time, "mem": mem}
    time, mem = run_sbwt.build(fasta_file, k)
    data["SBWT"] = {"time": time, "mem": mem}
    time, mem = run_bifrost.build(fasta_file, k)
    data["Bifrost"] = {"time": time, "mem": mem}
    time, mem = run_dynboss.build(fasta_file, k)
    data["DynamicBOSS"] = {"time": time, "mem": mem}
    data["k"] = k
    data["kmers"] = run_cbl.count(fasta_file)
    data["bytes"] = get_filesize(fasta_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def query_filename(prefix, indexed_file, query_file):
    index_basename = get_basename(indexed_file)
    query_basename = get_basename(query_file)
    size = get_filesize(indexed_file)
    return f"{DATA_FOLDER}/{prefix}_{size}_{index_basename}_{query_basename}.json"


def query_self_stats(fasta_file):
    output = query_filename("query_self", fasta_file, fasta_file)
    data = {"file": fasta_file}
    time, mem = run_cbl.query(fasta_file, fasta_file)
    data["CBL"] = {"time": time, "mem": mem}
    time, mem = run_sshash.query(fasta_file, fasta_file)
    data["SSHash"] = {"time": time, "mem": mem}
    time, mem = run_sbwt.query(fasta_file, fasta_file)
    data["SBWT"] = {"time": time, "mem": mem}
    time, mem = run_bifrost.query(fasta_file, fasta_file)
    data["Bifrost"] = {"time": time, "mem": mem}
    time, mem = run_dynboss.query(fasta_file, fasta_file)
    data["DynamicBOSS"] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(fasta_file)
    data["bytes"] = get_filesize(fasta_file)
    with open(output, "w+") as f:
        json.dump(data, f)
