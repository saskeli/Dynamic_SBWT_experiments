#!/bin/bash

cd CBL
K=31 cargo +nightly build --release --examples
cd ..

for i in 2 4 8 16 32 64 128 256 512 1000; do
  CBL/target/release/examples/cbl build out/${i}.unitigs.fa -o out/${i}.cbl
done
