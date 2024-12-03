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

#Buffered_SBWT
cd Buffered_SBWT/sdsl-lite
cmake CMakelists.txt
cd -

#CBL apparently with 2 builds since there is no way to just download dependences.
cd CBL
K=31 cargo build --release --examples
cd ..

#bcalm for unitigs
mkdir -p bcalm/build
cd bcalm/build
cmake ..
cd -