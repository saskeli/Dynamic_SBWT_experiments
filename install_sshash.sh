#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
cd sshash
mkdir build
cd build
cmake ..
make -j
