#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
sudo apt install -y zlib1g
cd sshash
mkdir build
cd build
cmake ..
make -j
