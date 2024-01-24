from util import *
import os
import json
import run_bifrost
import run_bufboss
import run_cbl
import run_dynboss
import run_sbwt
import run_sshash


DATA_FOLDER = "data"


def update_data(json_file, key, value):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        data[key] = value
        with open(json_file, "w") as f:
            json.dump(data, f)
    else:
        data = {key: value}
        with open(json_file, "w+") as f:
            json.dump(data, f)


def build_filename(prefix, fasta_file):
    basename = get_basename(fasta_file)
    size = get_filesize(fasta_file)
    return f"{DATA_FOLDER}/{prefix}_{size}_{basename}.json"


def build_stats(fasta_file, k):
    os.makedirs(DATA_FOLDER, exist_ok=True)
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
    time, mem = run_bufboss.build(fasta_file, k)
    data["BufBOSS"] = {"time": time, "mem": mem}
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


def query_self_stats(indexed_file):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("query_self", indexed_file, indexed_file)
    data = {"file": indexed_file}
    time, mem = run_cbl.query(indexed_file, indexed_file)
    data["CBL"] = {"time": time, "mem": mem}
    time, mem = run_sshash.query(indexed_file, indexed_file)
    data["SSHash"] = {"time": time, "mem": mem}
    time, mem = run_sbwt.query(indexed_file, indexed_file)
    data["SBWT"] = {"time": time, "mem": mem}
    time, mem = run_bifrost.query(indexed_file, indexed_file)
    data["Bifrost"] = {"time": time, "mem": mem}
    time, mem = run_bufboss.query(indexed_file, indexed_file)
    data["BufBOSS"] = {"time": time, "mem": mem}
    # time, mem = run_dynboss.query(indexed_file, indexed_file)
    # data["DynamicBOSS"] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file)
    data["bytes"] = get_filesize(indexed_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def query_other_stats(indexed_file, query_file):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("query_other", indexed_file, query_file)
    data = {"file": indexed_file, "query_file": query_file}
    time, mem = run_cbl.query(indexed_file, query_file)
    data["CBL"] = {"time": time, "mem": mem}
    time, mem = run_sshash.query(indexed_file, query_file)
    data["SSHash"] = {"time": time, "mem": mem}
    time, mem = run_sbwt.query(indexed_file, query_file)
    data["SBWT"] = {"time": time, "mem": mem}
    time, mem = run_bifrost.query(indexed_file, query_file)
    data["Bifrost"] = {"time": time, "mem": mem}
    time, mem = run_bufboss.query(indexed_file, query_file)
    data["BufBOSS"] = {"time": time, "mem": mem}
    # time, mem = run_dynboss.query(indexed_file, query_file)
    # data["DynamicBOSS"] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, query_file)
    data["query_bytes"] = get_filesize(query_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def insert_stats(indexed_file, query_file):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("insert", indexed_file, query_file)
    data = {"file": indexed_file, "query_file": query_file}
    time, mem = run_cbl.insert(indexed_file, query_file)
    data["CBL"] = {"time": time, "mem": mem}
    time, mem = run_bifrost.insert(indexed_file, query_file)
    data["Bifrost"] = {"time": time, "mem": mem}
    time, mem = run_bufboss.insert(indexed_file, query_file)
    data["BufBOSS"] = {"time": time, "mem": mem}
    # time, mem = run_dynboss.insert(indexed_file, query_file)
    # data["DynamicBOSS"] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, query_file)
    data["query_bytes"] = get_filesize(query_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def remove_stats(indexed_file, query_file):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("remove", indexed_file, query_file)
    data = {"file": indexed_file, "query_file": query_file}
    time, mem = run_cbl.remove(indexed_file, query_file)
    data["CBL"] = {"time": time, "mem": mem}
    time, mem = run_bufboss.remove(indexed_file, query_file)
    data["BufBOSS"] = {"time": time, "mem": mem}
    # time, mem = run_dynboss.remove(indexed_file, query_file)
    # data["DynamicBOSS"] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, query_file)
    data["query_bytes"] = get_filesize(query_file)
    with open(output, "w+") as f:
        json.dump(data, f)
