#!/bin/bash
set -euxo pipefail

#Bifrost
cd bifrost
mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=.
make -j
make install

#bufboss
cd bufboss
cd KMC
make -j
cd ..
cd sdsl-lite
sh install.sh
cd ..
cd stxxl
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_GNU_PARALLEL=ON -DCMAKE_INSTALL_PREFIX=./install
make -j
make install
cd ../..
make -j all

bash install_sbwt.sh

cd CBL
cargo build --release
cd ..
