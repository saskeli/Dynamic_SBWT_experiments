from util import run_cmd, measure_time
import os

def build(fasta_file, k):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    count_file = basename + ".solid_kmers_binary"
    packed_file = count_file + ".packed"
    time1, mem1 = measure_time(f"./dynboss/dsk-1.6906/dsk {fasta_file} {k}")
    time2, mem2 = measure_time(f"./dynboss/bin/cosmo-pack {count_file}")
    time3, mem3 = measure_time(f"./dynboss/bin/dynamicBOSS build -p {packed_file}")
    return time1 + time2 + time3, mem1 + mem2 + mem3

def clean(fasta_file):
    basename = fasta_file
    if fasta_file.endswith(".gz"):
        basename = fasta_file[:-3]
    count_file = basename + ".solid_kmers_binary"
    packed_file = count_file + ".packed"
    graph_file = packed_file + ".dbg"
    os.remove(count_file)
    os.remove(packed_file)
    os.remove(graph_file)
