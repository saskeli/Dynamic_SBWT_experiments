#!/bin/bash


for i in 2 4 8 16 32 64 128 256 512 1000; do
  SBWT/build/bin/sbwt build -i out/${i}.unitigs.fa -o out/${i}.sbwt -k 31 -t 4
done
