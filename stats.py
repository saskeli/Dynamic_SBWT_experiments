import os
import json
import run_bifrost
import run_cbl
import run_dynboss
import run_sbwt
import run_sshash
import util


DATA_FOLDER = "data"


def stats_filename(prefix, fasta_file, k):
    basename = os.path.basename(fasta_file)
    size = util.get_filesize(fasta_file)
    return f"{DATA_FOLDER}/{prefix}_{k}_{size}_{basename}.json"


def build_stats(fasta_file, k):
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
    data["bytes"] = util.get_filesize(fasta_file)
    data["count"] = run_cbl.count(fasta_file, k)
    output = stats_filename("build", fasta_file, k)
    with open(output, "w+") as f:
        json.dump(data, f)
