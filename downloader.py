import subprocess
import sys

def make_url(s):
    base_url = "https://ftp.ncbi.nlm.nih.gov/genomes/all/"
    ss = s.split('_')
    parts = [ss[0], ss[1][:3], ss[1][3:6], ss[1][6:9], "_".join(ss[:-1]), s]
    return base_url + "/".join(parts)

def download(f_path):
    with open(f_path) as inf:
        for i, l in enumerate(inf):
            url = make_url(l.strip())
            print(i, l, url)
            subprocess.run(["wget", url])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download(sys.argv[1])
