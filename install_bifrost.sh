#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
sudo apt install -y build-essential cmake zlib1g-dev
cd bifrost
mkdir build
cd build
cmake ..
make
make install
