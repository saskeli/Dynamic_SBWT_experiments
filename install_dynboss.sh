#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
cd dynboss
cd dsk-1.6906
make dsk canon=0
# make dsk k=64 canon=0
cd ..
cd src
sudo apt install -y libboost-all-dev
sudo apt install -y libtclap-dev
sudo apt install -y libsdsl-dev
make revcomps=0
