#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive
cd sshash
mkdir build
cd build
cmake ..
make -j
