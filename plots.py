from stats import DATA_FOLDER
from matplotlib import pyplot as plt
import os
import json


PLOT_FOLDER = "plot"
PLOT_FORMAT = ".png"
FONT_SIZE = 12
DATA_FILES = os.listdir(DATA_FOLDER)
SINGLE_TASKS = ["build", "query_self"]
QUERY_TASKS = ["query_other", "insert", "remove"]
TASKS = SINGLE_TASKS + QUERY_TASKS
DATA = {task: [] for task in TASKS}
TOOLS = {
    "build": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "DynamicBOSS"],
    "query_self": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS"],
    "query_other": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS"],
    "insert": ["CBL", "Bifrost", "BufBOSS"],
    "remove": ["CBL", "BufBOSS"],
}
MARKER = {
    "CBL": "o",
    "SSHash": "*",
    "SBWT": "s",
    "Bifrost": "P",
    "BufBOSS": "D",
    "DynamicBOSS": "X",
}
LABEL = {t: t for t in MARKER}
LABEL["DynamicBOSS"] = "DynBOSS"

for filename in DATA_FILES:
    if filename.endswith(".json"):
        with open(f"{DATA_FOLDER}/{filename}", "r") as f:
            if filename.startswith("build"):
                DATA["build"].append(json.load(f))
            elif filename.startswith("query_self"):
                DATA["query_self"].append(json.load(f))
            elif filename.startswith("query_other"):
                DATA["query_other"].append(json.load(f))
            elif filename.startswith("insert"):
                DATA["insert"].append(json.load(f))
            elif filename.startswith("remove"):
                DATA["remove"].append(json.load(f))


def plot_time_bytes(task):
    xkey = "bytes" if task in SINGLE_TASKS else "query_bytes"
    prefix = f"{PLOT_FOLDER}/plot_{task}_time_bytes"
    plt.rcParams.update({"font.size": FONT_SIZE})
    fig, ax = plt.subplots()
    for tool in TOOLS[task]:
        X = [d[xkey] for d in DATA[task]]
        Y = [d[tool]["time"] for d in DATA[task]]
        ax.scatter(X, Y, label=LABEL[tool], marker=MARKER[tool], alpha=0.5)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel("Construction time (in s)")
    ax.set_xlabel("Input size (in bytes)")
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.025),
        ncol=min(3, len(TOOLS[task])),
    )
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    plt.savefig(prefix + PLOT_FORMAT, bbox_inches="tight", dpi=300)


def plot_time_kmers(task):
    xkey = "kmers" if task in SINGLE_TASKS else "query_kmers"
    prefix = f"{PLOT_FOLDER}/plot_{task}_time_kmers"
    plt.rcParams.update({"font.size": FONT_SIZE})
    fig, ax = plt.subplots()
    for tool in TOOLS[task]:
        X = [d[xkey] for d in DATA[task]]
        Y = [d[tool]["time"] for d in DATA[task]]
        ax.scatter(X, Y, label=LABEL[tool], marker=MARKER[tool], alpha=0.5)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel("Construction time (in s)")
    ax.set_xlabel("# k-mers")
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.025),
        ncol=min(3, len(TOOLS[task])),
    )
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    plt.savefig(prefix + PLOT_FORMAT, bbox_inches="tight", dpi=300)


def plot_ram_kmers(task):
    xkey = "kmers" if task in SINGLE_TASKS else "query_kmers"
    prefix = f"{PLOT_FOLDER}/plot_{task}_ram_kmers"
    plt.rcParams.update({"font.size": FONT_SIZE})
    fig, ax = plt.subplots()
    for tool in TOOLS[task]:
        X = [d[xkey] for d in DATA[task]]
        Y = [d[tool]["mem"] / 1000 for d in DATA[task]]
        ax.scatter(X, Y, label=LABEL[tool], marker=MARKER[tool], alpha=0.5)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel("RAM usage during construction (in MB)")
    ax.set_xlabel("# k-mers")
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.025),
        ncol=min(3, len(TOOLS[task])),
    )
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    plt.savefig(prefix + PLOT_FORMAT, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    for task in TASKS:
        plot_time_bytes(task)
        plot_time_kmers(task)
        plot_ram_kmers(task)
