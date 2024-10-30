#!/bin/bash

USAGE="$0 <file_list> <data_folder> <output_folder> <limit> -- build unitigs and time index creation

where:
    file_list    is a text file containing the names of fasta files to use.
    data_folder  is the folder containing the fasta files.
    output_foder is the directory to write unitigs and indexes to.
    limit        maximum number of genomes to build index of. Default: 1024.
    
All arguments, besides limit are required

Example $0 fof_build.txt data out"

if [ $# -lt 3 ]; then
    echo "$USAGE"
    exit 1
fi

BLA=$(head -n 1 $1)
EXT=${BLA##*.}
FEXT=$EXT
if [ "$EXT" = "gz" ]; then
    FN=${BLA%.*}
    FEXT=${FN##*.}
    EXT=${FEXT}.${EXT}
fi

echo "file extenstion: $EXT"

set -euxo pipefail

FOF=$1
DATA_FOLDER=$2
OUT_FOLDER=$3
FILE_LIMIT=$(($# > 3 ? $4 : 1024))

mkdir -p ${OUT_FOLDER}

i=1
while [ $i -lt $FILE_LIMIT ]; do
  i=$(($i * 2))
  FN=${OUT_FOLDER}/${i}.concat.${FEXT}
  GFN=${OUT_FOLDER}/${i}.concat.${EXT}
  if [ ! -f $FN ]; then
    head -n ${i} ${FOF} | while read line ; do echo "${DATA_FOLDER}/${line}"; done | xargs cat > $GFN
    if [ "$EXT" != "$FEXT" ]; then
      gunzip $GFN
    fi
  fi
done

rm -f ${OUT_FOLDER}/*glue*

MAX_THREADS=$(nproc)
MAX_THREADS=$((MAX_THREADS > 32 ? 32 : MAX_THREADS))

i=1
while [ $i -lt $FILE_LIMIT ]; do
  i=$(($i * 2))
  
  FN=${OUT_FOLDER}/${i}.concat.${FEXT}
  echo $FN > tmp.txt
  
  /usr/bin/time CBL/target/release/examples/cbl build ${FN} -o ${OUT_FOLDER}/${i}_concat.cbl
  /usr/bin/time bufboss/bin/bufboss_build -a ${FN} -o ${OUT_FOLDER}/${i}_concat.bufboss -k 31 -t tmp
  /usr/bin/time bifrost/build/bin/Bifrost build -r ${FN} -o ${OUT_FOLDER}/${i}_concat.bifrost -k 31 -t 1
  /usr/bin/time BBB/build/bin/buffer -r -t 1 tmp.txt ${OUT_FOLDER}/${i}_concat.sbwt 
  echo "threads = ${MAX_THREADS}"
  /usr/bin/time bifrost/build/bin/Bifrost build -r ${FN} -o ${OUT_FOLDER}/${i}_concat.bifrost -k 31 -t $MAX_THREADS
  /usr/bin/time BBB/build/bin/buffer -r -t $MAX_THREADS tmp.txt ${OUT_FOLDER}/${i}_concat_a.sbwt 
  /usr/bin/time BBB/build/bin/buffer -r -m 4 -t $MAX_THREADS tmp.txt ${OUT_FOLDER}/${i}_concat_b.sbwt 
  /usr/bin/time BBB/build/bin/buffer -r -m 10 -t $MAX_THREADS tmp.txt ${OUT_FOLDER}/${i}_concat_c.sbwt 

  rm tmp.txt
done