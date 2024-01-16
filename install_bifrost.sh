#!/bin/bash
set -euxo pipefail

cd bifrost
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=.
make
make install
