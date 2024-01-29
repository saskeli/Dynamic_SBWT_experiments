#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive
cd SBWT
cd build
cmake .. -DCMAKE_CXX_COMPILER=g++ -DMAX_KMER_LENGTH=32
make -j
