#!/bin/bash
set -euxo pipefail

cd sshash
mkdir -p build
cd build
cmake ..
make -j
