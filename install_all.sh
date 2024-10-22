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
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_GNU_PARALLEL=ON -DCMAKE_INSTALL_PREFIX=./install
cd ../..
mkdir -p sdsl-lite/build
cd sdsl-lite/build
cmake -DCMAKE_BUILD_TYPE="Release" ..
cd -
cd ..

#BBB
cd BBB/build
cmake .. -DMAX_KMER_LENGTH=31