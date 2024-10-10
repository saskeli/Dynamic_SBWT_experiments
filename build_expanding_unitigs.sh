#!/bin/bash

FOF="../fof_build.txt"

for i in 2 4 8 16 32 64 128 256 512 1024; do
  head -n ${i} ${FOF} > tmp.txt
  ../../bcalm/build/bcalm -in tmp.txt -kmer-size 31 -abundance-min 1 -out ../out/${i}.fa 
  rm tmp.txt
done
