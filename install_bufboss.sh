#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive
cd bufboss
cd KMC
make
cd ..
cd sdsl-lite
sh install.sh
cd ..
cd stxxl
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_GNU_PARALLEL=ON -DCMAKE_INSTALL_PREFIX=./install
make
make install
cd ../..
make all
