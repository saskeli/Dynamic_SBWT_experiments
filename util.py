# Adapted from https://github.com/jnalanko/SBWT_experiments/blob/master/setup.py

import subprocess
import struct
import sys
import os


ENV = os.environ.copy()
GNU_TIME = "/usr/bin/time"


def run_cmd(command):
    sys.stderr.write(command + "\n")
    return (
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, env=ENV)
        .stdout.decode("utf-8")
        .strip()
    )


def measure_time(command):
    """
    Measure time (in s) and memory usage (in KB) of a command
    """
    sys.stderr.write(command + "\n")
    result = (
        subprocess.run(
            f"{GNU_TIME} -f '%e %M' {command}",
            shell=True,
            stderr=subprocess.PIPE,
            env=ENV,
        )
        .stderr.decode("utf-8")
        .strip()
    )
    time_s, mem_kb = result.splitlines()[-1].split()
    return float(time_s), int(mem_kb)


def get_filesize(filename):
    if filename.endswith(".gz"):
        with open(filename, 'rb') as f:
            f.seek(-4, 2)
            return struct.unpack('I', f.read(4))[0]
    else:
        return os.path.getsize(filename)
