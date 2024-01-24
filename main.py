from util import TIMEOUT
import stats


K = 31
TIMEOUT = 300

BUILD = [
    "../files_1801-1900_31/SRR972708.unitigs.fa.gz",
    "../files_1801-1900_31/SRR975415.unitigs.fa.gz",
    "../files_1801-1900_31/SRR962597.unitigs.fa.gz",
    "../files_1801-1900_31/SRR976738.unitigs.fa.gz",
    "../files_1801-1900_31/SRR953494.unitigs.fa.gz",
    "../files_1801-1900_31/SRR950080.unitigs.fa.gz",
    "../files_1801-1900_31/SRR950083.unitigs.fa.gz",
    "../files_1801-1900_31/SRR953488.unitigs.fa.gz",
    "../files_1801-1900_31/SRR972717.unitigs.fa.gz",
    "../files_1801-1900_31/SRR972716.unitigs.fa.gz",
    "../files_1801-1900_31/SRR975416.unitigs.fa.gz",
    "../files_1801-1900_31/SRR975412.unitigs.fa.gz",
    "../files_1801-1900_31/SRR962604.unitigs.fa.gz",
    "../files_1801-1900_31/SRR976749.unitigs.fa.gz",
    "../files_1801-1900_31/SRR953495.unitigs.fa.gz",
    # "../files_1801-1900_31/SRR953496.unitigs.fa.gz",
]

QUERY = [
    (
        "../files_1801-1900_31/SRR972708.unitigs.fa.gz",
        "../files_1801-1900_31/SRR972716.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR975415.unitigs.fa.gz",
        "../files_1801-1900_31/SRR975414.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR962597.unitigs.fa.gz",
        "../files_1801-1900_31/SRR950879.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR976738.unitigs.fa.gz",
        "../files_1801-1900_31/SRR976743.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR953494.unitigs.fa.gz",
        "../files_1801-1900_31/SRR950882.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR950080.unitigs.fa.gz",
        "../files_1801-1900_31/SRR950881.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR950083.unitigs.fa.gz",
        "../files_1801-1900_31/SRR950079.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR953488.unitigs.fa.gz",
        "../files_1801-1900_31/SRR972713.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR972717.unitigs.fa.gz",
        "../files_1801-1900_31/SRR972715.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR972716.unitigs.fa.gz",
        "../files_1801-1900_31/SRR960732.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR975416.unitigs.fa.gz",
        "../files_1801-1900_31/SRR960733.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR975412.unitigs.fa.gz",
        "../files_1801-1900_31/SRR975411.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR962604.unitigs.fa.gz",
        "../files_1801-1900_31/SRR962602.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR976749.unitigs.fa.gz",
        "../files_1801-1900_31/SRR962600.unitigs.fa.gz",
    ),
    (
        "../files_1801-1900_31/SRR953495.unitigs.fa.gz",
        "../files_1801-1900_31/SRR950084.unitigs.fa.gz",
    ),
    # (
    #     "../files_1801-1900_31/SRR953496.unitigs.fa.gz",
    #     "../files_1801-1900_31/SRR953497.unitigs.fa.gz",
    # ),
]

if __name__ == "__main__":
    for fasta_file in BUILD:
        stats.build_stats(fasta_file, K)
        stats.query_self_stats(fasta_file)

    for indexed_file, query_file in QUERY:
        stats.query_other_stats(indexed_file, query_file)
        stats.insert_stats(indexed_file, query_file)
        stats.remove_stats(indexed_file, query_file)
