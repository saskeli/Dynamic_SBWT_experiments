#!/bin/bash
set -euo pipefail

cd bifrost
mkdir build
cd build
cmake ..
make
sudo make install
