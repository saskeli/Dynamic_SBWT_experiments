#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive
cd bifrost
mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=.
make
make install
