# Adapted from https://github.com/jnalanko/SBWT_experiments/blob/master/setup.py

import subprocess
import struct
import sys
import os


ENV = os.environ.copy()
GNU_TIME = "/usr/bin/time"
TIMEOUT = 120
OUT_FOLDER = "out"


def run_cmd(command):
    sys.stderr.write("> " + command + "\n")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)
    out, err = proc.communicate()
    out = out.decode("utf-8").strip()
    err = err.decode("utf-8").strip()
    sys.stdout.write(out + "\n")
    sys.stderr.write(err + "\n")
    return out, err


def measure_time(command, timeout=TIMEOUT):
    """
    Measure time (in s) and memory usage (in KB) of a command
    """
    _, err = run_cmd(f"timeout {timeout} {GNU_TIME} -f '%e %M' {command}")
    try:
        time_s, mem_kb = err.splitlines()[-1].split()
        return float(time_s), int(mem_kb)
    except Exception:
        return None, None


def get_filesize(filename):
    if filename.endswith(".gz"):
        with open(filename, "rb") as f:
            f.seek(-4, 2)
            return struct.unpack("I", f.read(4))[0]
    else:
        return os.path.getsize(filename)
