import util
import stats
import os


PARAMS = {"k": 31, "prefix_bits": 28, "m": 20, "timeout": 300}
FOF_BUILD = "fof_build.txt"
FOF_QUERY = "fof_query.txt"
BUILD = []
QUERY = []


if __name__ == "__main__":
    if os.path.exists(FOF_BUILD):
        with open(FOF_BUILD, "r") as f:
            for line in f:
                filename = line.strip()
                if filename:
                    assert os.path.exists(filename), f"Cannot find {filename}"
                    BUILD.append(filename)
    else:
        print(f"Please write the FASTA files to build in {FOF_BUILD}")

    if os.path.exists(FOF_QUERY):
        with open(FOF_QUERY, "r") as f:
            for line in f:
                filename = line.strip()
                if filename:
                    assert os.path.exists(filename), f"Cannot find {filename}"
                    QUERY.append(filename)
    else:
        print(f"Please write the FASTA files to query in {FOF_QUERY}")

    for fasta_file in set(BUILD):
        print(f"BUILD {fasta_file}")
        stats.build_stats(fasta_file, **PARAMS)
        stats.query_self_stats(fasta_file, **PARAMS)

    for indexed_file, query_file in set(zip(BUILD, QUERY)):
        print(f"QUERY {indexed_file} with {query_file}")
        stats.query_other_stats(indexed_file, query_file, **PARAMS)
        stats.insert_stats(indexed_file, query_file, **PARAMS)
        stats.remove_stats(indexed_file, query_file, **PARAMS)
        stats.merge_stats(indexed_file, query_file, **PARAMS)
        stats.intersect_stats(indexed_file, query_file, **PARAMS)
