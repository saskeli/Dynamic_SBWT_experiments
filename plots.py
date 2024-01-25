from stats import DATA_FOLDER
from matplotlib import pyplot as plt
from matplotlib import ticker
import os
import json
import shutil


PLOT_FOLDER = "plot"
PLOT_FORMAT = ".png"
FONT_SIZE = 12
SINGLE_TASKS = ["build", "query_self"]
QUERY_TASKS = ["query_other", "insert", "remove"]
TASKS = SINGLE_TASKS + QUERY_TASKS
TOOLS = {
    "build": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "DynamicBOSS", "HashSet"],
    "size": ["CBL", "SSHash", "SBWT", "Bifrost", "DynamicBOSS", "HashSet"],
    "query_self": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "HashSet"],
    "query_other": ["CBL", "SSHash", "SBWT", "Bifrost", "BufBOSS", "HashSet"],
    "insert": ["CBL", "Bifrost", "BufBOSS", "HashSet"],
    "remove": ["CBL", "BufBOSS", "HashSet"],
    "pareto": ["CBL", "Bifrost", "BufBOSS", "HashSet"],
}
MARKER = {
    "CBL": "o",
    "SSHash": "*",
    "SBWT": "s",
    "Bifrost": "P",
    "BufBOSS": "D",
    "DynamicBOSS": "X",
    "HashSet": "^",
}
LABEL = {t: t for t in MARKER}
LABEL["DynamicBOSS"] = "DynBOSS"
LABEL["build"] = {
    "time": "Construction time (in s)",
    "mem": "RAM usage during construction (in MB)",
    "size": "Index size on disk (in bytes)",
    "bytes": "Input size (in bytes)",
    "kmers": "# $k$-mers",
}
LABEL["query_self"] = {
    "time": "Time for positive queries (in s)",
    "mem": "RAM usage for positive queries (in MB)",
    "bytes": "Query size (in bytes)",
    "kmers": "# queried $k$-mers",
}
LABEL["query_other"] = {
    "time": "Time for random queries (in s)",
    "mem": "RAM usage for random queries (in MB)",
    "query_bytes": "Query size (in bytes)",
    "query_kmers": "# queried $k$-mers",
}
LABEL["insert"] = {
    "time": "Time for insertions (in s)",
    "mem": "RAM usage during insertions (in MB)",
    "query_bytes": "Query size (in bytes)",
    "query_kmers": "# inserted $k$-mers",
}
LABEL["remove"] = {
    "time": "Time for deletions (in s)",
    "mem": "RAM usage during deletions (in MB)",
    "query_bytes": "Query size (in bytes)",
    "query_kmers": "# deleted $k$-mers",
}
DATA_FILES = os.listdir(DATA_FOLDER)
DATA = {task: [] for task in TASKS}


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


def plot_task(task, ykey, xkey, name=None):
    if name is not None:
        prefix = f"{PLOT_FOLDER}/{name}"
    elif ykey == "size":
        prefix = f"{PLOT_FOLDER}/plot_size_{xkey.split('_')[-1]}"
    elif ykey == "mem":
        prefix = f"{PLOT_FOLDER}/plot_{task}_ram_{xkey.split('_')[-1]}"
    else:
        prefix = f"{PLOT_FOLDER}/plot_{task}_{ykey}_{xkey.split('_')[-1]}"
    plt.rcParams.update({"font.size": FONT_SIZE})
    fig, ax = plt.subplots()
    for tool in TOOLS[task]:
        X, Y = [], []
        for d in DATA[task]:
            if tool in d and ykey in d[tool]:
                X.append(d[xkey])
                if ykey == "mem":
                    Y.append(d[tool][ykey] / 1000)
                else:
                    Y.append(d[tool][ykey])
        ax.scatter(X, Y, label=LABEL[tool], marker=MARKER[tool], alpha=0.5)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel(LABEL[task][ykey])
    ax.set_xlabel(LABEL[task][xkey])
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.025),
        ncol=ncol(len(TOOLS[task])),
    )
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    plt.savefig(prefix + PLOT_FORMAT, bbox_inches="tight", dpi=300)
    plt.close()


def plot_pareto(task, threshold=0, name=None):
    if name is not None:
        prefix = f"{PLOT_FOLDER}/{name}"
    else:
        prefix = f"{PLOT_FOLDER}/plot_pareto_{task}"
    plt.rcParams.update({"font.size": FONT_SIZE})
    fig, ax = plt.subplots()
    for tool in TOOLS[task]:
        if tool in TOOLS["pareto"]:
            X, Y = [], []
            for d in DATA[task]:
                n = d["kmers" if task in SINGLE_TASKS else "query_kmers"]
                if n > threshold and tool in d and d[tool]["time"] != float("inf"):
                    X.append(d[tool]["mem"] * 8000 / n)
                    Y.append(d[tool]["time"] * 1e9 / n)
            if X and Y:
                X = [sum(X) / len(X)]
                Y = [sum(Y) / len(Y)]
                ax.scatter(X, Y, label=LABEL[tool], marker=MARKER[tool], alpha=0.5)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylabel(LABEL[task]["time"].split("(")[0] + "(in ns/$k$-mer)")
    ax.set_xlabel("RAM usage (in bits/$k$-mer)")
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.025),
        ncol=ncol(len(TOOLS[task])),
    )
    ax.xaxis.set_major_formatter(ticker.LogFormatterSciNotation(labelOnlyBase=True))
    ax.xaxis.set_minor_formatter(ticker.LogFormatterSciNotation(labelOnlyBase=True))
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    plt.savefig(prefix + PLOT_FORMAT, bbox_inches="tight", dpi=300)
    plt.close()


def ncol(n):
    if n <= 4:
        return n
    return (n + 1) // 2


if __name__ == "__main__":
    for task in SINGLE_TASKS:
        plot_task(task, "time", "bytes")
        plot_task(task, "time", "kmers")
        plot_task(task, "mem", "kmers")
    for task in QUERY_TASKS:
        plot_task(task, "time", "query_bytes")
        plot_task(task, "time", "query_kmers")
        plot_task(task, "mem", "query_kmers")
    for task in TASKS:
        plot_pareto(task, threshold=2e7)
    plot_task("build", "size", "kmers")
    shutil.make_archive(PLOT_FOLDER, "zip", PLOT_FOLDER)
