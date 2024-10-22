#!/bin/bash
set -euxo pipefail

#bifrost
cd bifrost/build
make -j
make install
cd ../..

#bufboss
cd bufboss/KMC
make -j
cd ..
cd stxxl/build
make -j
make install
cd -
cd sdsl-lite/build
make -j
cd -
make -j all
cd ..

#BBB
cd BBB/build
make -j buffer
cd ../..

#CBL
cd CBL
K=31 cargo build --release --examples
cd ..