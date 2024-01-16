#!/bin/bash
set -euo pipefail

cd bifrost
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=.
make
make install
