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

#Buffered_SBWT
cd Buffered_SBWT
make -j fast
cd ..

#CBL
cd CBL
cargo clean && K=31 cargo build --release --examples
cd ..

#BCALM

cd bcalm/build
make -j
cd -