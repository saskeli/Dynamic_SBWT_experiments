#!/bin/bash
set -euo pipefail

git submodule update --init --recursive
cd dynboss
cd dsk-1.6906
make dsk canon=0
# make dsk k=64 canon=0
cd ..
cd src
make revcomps=0
