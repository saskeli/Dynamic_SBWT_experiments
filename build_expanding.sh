#!/bin/bash
set -euxo pipefail

FOF="../fof_build.txt"

for i in 2 4 8 16 32 64 128 256 512 1024; do
  head -n ${i} ${FOF} > tmp.txt
  ../../bcalm/build/bcalm -in tmp.txt -kmer-size 31 -abundance-min 1 -out ../out/${i}.fa 
  rm tmp.txt
done

for i in 2 4 8 16 32 64 128 256 512 1000; do
  echo out/${i}.unitigs.fa > inp.txt
  /usr/bin/time SBWT/build/bin/sbwt -t 1 -m 16 inp.txt out/${i}.sbwt 
  /usr/bin/time CBL/target/release/examples/cbl build out/${i}.unitigs.fa -o out/${i}.cbl
  /usr/bin/time bufboss/bin/bufboss_build -a out/${i}.unitigs.fa -o out/${i}.bufboss -k 31 -t tmp
  /usr/bin/time bifrost/build/bin/Bifrost build -r out/${i}.unitigs.fa -o out/${i}.bifrost -k 31 -t 1
done

