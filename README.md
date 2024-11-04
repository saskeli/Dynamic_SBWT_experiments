# CBL experiments fork

Forked from the experiment repo for the [CBL](https://github.com/imartayan/CBL) paper

For running tests you should clone with 
```sh
git clone --recurse-submodules --depth=1 --shallow-submodules https://github.com/saskeli/CBL_experiments.git
```

## Usage

The intention is to use a Singularity-CE container for running all experiments and builds to eliminate as many requirements as possible for the host system.

The only thing you need to have installed on the host system is [singularity-ce](https://github.com/sylabs/singularity).

Download data needed for experiments from [NCBI](https://www.ncbi.nlm.nih.gov/). Files are specified in `fof_build.txt` and `fof_query.txt`. There is probably a very good and convenient way to batch download them. But I'm lazy and wrote a script that can be used like this:
```bash
mkdir -p data
cd data
python3 ../downloader.py ../fof.txt
```

Build the singularity container with
```bash
singularity build --fakeroot ubuntu.sif build_ubuntu.txt 
```

Run all cmakes and download dependencies with
```bash
singularity run --userns ./ubuntu.sif ./install_all.sh
```

Build all binaries with
```bash
singularity run --userns ./ubuntu.sif ./build_all.sh
```

Build indexes can be done with he following. (here piping the output to exp.txt).
```bash
singularity run --userns ./ubuntu.sif ./build_expanding.sh fof_build.txt data out &> exp.txt
```

Results are parsed and plots drawn with the `expanding.ipynb` jupyter notebook.
