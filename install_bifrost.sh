#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
cd bifrost
mkdir build
cd build
cmake ..
make
make install
