#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
sudo apt install -y g++ gcc cmake git python3-dev libz-dev
sudo apt install -y g++-8
cd SBWT
cd build
cmake .. -DCMAKE_CXX_COMPILER=g++-8 -DMAX_KMER_LENGTH=32
make -j8
