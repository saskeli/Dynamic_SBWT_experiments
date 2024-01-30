from util import get_basename, get_filesize
import os
import json
import run_bifrost
import run_bufboss
import run_cbl
import run_dynboss
import run_hashset
import run_sbwt
import run_sshash


DATA_FOLDER = "data"
CLI = {
    "Bifrost": run_bifrost,
    "BufBOSS": run_bufboss,
    "CBL": run_cbl,
    "DynamicBOSS": run_dynboss,
    "HashSet": run_hashset,
    "SBWT": run_sbwt,
    "SSHash": run_sshash,
}
TOOLS = {
    "build": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "DynamicBOSS", "HashSet"],
    "size": ["CBL", "SSHash", "SBWT", "Bifrost", "DynamicBOSS", "HashSet"],
    "query_self": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "HashSet"],
    "query_other": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "HashSet"],
    "insert": ["CBL", "Bifrost", "BufBOSS", "HashSet"],
    "remove": ["CBL", "BufBOSS", "HashSet"],
    "merge": ["CBL", "HashSet"],
    "intersect": ["CBL", "HashSet"],
}


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


def build_filename(prefix, fasta_file, **params):
    k = params["k"]
    prefix_bits = params["prefix_bits"]
    basename = get_basename(fasta_file)
    size = get_filesize(fasta_file)
    _k = "" if k == 31 and prefix_bits == 24 else f"_{k}"
    _p = "" if prefix_bits == 24 else f"_{prefix_bits}"
    return f"{DATA_FOLDER}/{prefix}{_k}{_p}_{size}_{basename}.json"


def query_filename(prefix, indexed_file, query_file, **params):
    k = params["k"]
    prefix_bits = params["prefix_bits"]
    index_basename = get_basename(indexed_file)
    query_basename = get_basename(query_file)
    size = get_filesize(indexed_file)
    _k = "" if k == 31 and prefix_bits == 24 else f"_{k}"
    _p = "" if prefix_bits == 24 else f"_{prefix_bits}"
    return f"{DATA_FOLDER}/{prefix}{_k}{_p}_{size}_{index_basename}_{query_basename}.json"


def build_stats(fasta_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = build_filename("build", fasta_file, **params)
    data = {"file": fasta_file}
    for tool in TOOLS["build"]:
        time, mem = CLI[tool].build(fasta_file, **params)
        data[tool] = {"time": time, "mem": mem}
        if tool in TOOLS["size"]:
            index_file = CLI[tool].index_path(fasta_file)
            if os.path.exists(index_file):
                data[tool]["size"] = get_filesize(index_file)
    data["k"] = params["k"]
    data["prefix_bits"] = params["prefix_bits"]
    data["kmers"] = run_cbl.count(fasta_file, **params)
    data["bytes"] = get_filesize(fasta_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def query_self_stats(indexed_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("query_self", indexed_file, indexed_file, **params)
    data = {"file": indexed_file}
    for tool in TOOLS["query_self"]:
        if not os.path.exists(CLI[tool].index_path(indexed_file)):
            CLI[tool].build(indexed_file, **params)
        if os.path.exists(CLI[tool].index_path(indexed_file)):
            time, mem = CLI[tool].query(indexed_file, indexed_file, **params)
            data[tool] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file, **params)
    data["bytes"] = get_filesize(indexed_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def query_other_stats(indexed_file, query_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("query_other", indexed_file, query_file, **params)
    data = {"file": indexed_file, "query_file": query_file}
    for tool in TOOLS["query_other"]:
        if not os.path.exists(CLI[tool].index_path(indexed_file)):
            CLI[tool].build(indexed_file, **params)
        if os.path.exists(CLI[tool].index_path(indexed_file)):
            time, mem = CLI[tool].query(indexed_file, query_file, **params)
            data[tool] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file, **params)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, query_file, **params)
    data["query_bytes"] = get_filesize(query_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def insert_stats(indexed_file, query_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("insert", indexed_file, query_file, **params)
    data = {"file": indexed_file, "query_file": query_file}
    for tool in TOOLS["insert"]:
        if not os.path.exists(CLI[tool].index_path(indexed_file)):
            CLI[tool].build(indexed_file, **params)
        if os.path.exists(CLI[tool].index_path(indexed_file)):
            time, mem = CLI[tool].insert(indexed_file, query_file, **params)
            data[tool] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file, **params)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, query_file, **params)
    data["query_bytes"] = get_filesize(query_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def remove_stats(indexed_file, query_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("remove", indexed_file, query_file, **params)
    data = {"file": indexed_file, "query_file": query_file}
    for tool in TOOLS["remove"]:
        if not os.path.exists(CLI[tool].index_path(indexed_file)):
            CLI[tool].build(indexed_file, **params)
        if os.path.exists(CLI[tool].index_path(indexed_file)):
            time, mem = CLI[tool].remove(indexed_file, query_file, **params)
            data[tool] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file, **params)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, query_file, **params)
    data["query_bytes"] = get_filesize(query_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def merge_stats(indexed_file, other_indexed_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("merge", indexed_file, other_indexed_file, **params)
    data = {"file": indexed_file, "other_file": other_indexed_file}
    for tool in TOOLS["merge"]:
        if not os.path.exists(CLI[tool].index_path(indexed_file)):
            CLI[tool].build(indexed_file, **params)
        if not os.path.exists(CLI[tool].index_path(other_indexed_file)):
            CLI[tool].build(other_indexed_file, **params)
        if os.path.exists(CLI[tool].index_path(indexed_file)) and os.path.exists(CLI[tool].index_path(other_indexed_file)):
            time, mem = CLI[tool].merge(indexed_file, other_indexed_file, **params)
            data[tool] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file, **params)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, other_indexed_file, **params)
    data["query_bytes"] = get_filesize(other_indexed_file)
    with open(output, "w+") as f:
        json.dump(data, f)


def intersect_stats(indexed_file, other_indexed_file, **params):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    output = query_filename("intersect", indexed_file, other_indexed_file, **params)
    data = {"file": indexed_file, "other_file": other_indexed_file}
    for tool in TOOLS["intersect"]:
        if not os.path.exists(CLI[tool].index_path(indexed_file)):
            CLI[tool].build(indexed_file, **params)
        if not os.path.exists(CLI[tool].index_path(other_indexed_file)):
            CLI[tool].build(other_indexed_file, **params)
        if os.path.exists(CLI[tool].index_path(indexed_file)) and os.path.exists(CLI[tool].index_path(other_indexed_file)):
            time, mem = CLI[tool].intersect(indexed_file, other_indexed_file, **params)
            data[tool] = {"time": time, "mem": mem}
    data["kmers"] = run_cbl.count(indexed_file, **params)
    data["bytes"] = get_filesize(indexed_file)
    data["query_kmers"] = run_cbl.count_query(indexed_file, other_indexed_file, **params)
    data["query_bytes"] = get_filesize(other_indexed_file)
    with open(output, "w+") as f:
        json.dump(data, f)
