#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
cd SBWT
cd build
cmake .. -DCMAKE_CXX_COMPILER=g++-8 -DMAX_KMER_LENGTH=32
make -j8
