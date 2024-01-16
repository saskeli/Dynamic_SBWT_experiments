#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive
cd sshash
mkdir -p build
cd build
cmake ..
make -j
