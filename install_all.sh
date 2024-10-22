#!/bin/bash
set -euxo pipefail

#Bifrost
cd bifrost
mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=.
cd ../..

#bufboss
cd bufboss
cd stxxl
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_GNU_PARALLEL=ON -DCMAKE_INSTALL_PREFIX=./install
cd ../..

#BBB
cd BBB/build
cmake .. -DMAX_KMER_LENGTH=31