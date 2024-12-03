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

FOF=$1
DATA_FOLDER=$2
OUT_FOLDER=$3
FILE_LIMIT=1024
if [ $# -gt 3 ]; then 
    FILE_LIMIT=$4
fi

set -euxo pipefail

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
MAX_MEM=$(free -g | awk '/^Mem:/{print int($2 * 0.9)}')

i=1
while [ $i -lt $FILE_LIMIT ]; do
  i=$(($i * 2))
  
  FN=${OUT_FOLDER}/${i}.concat.${FEXT}
  
  /usr/bin/time CBL/target/release/examples/cbl build -c ${FN} -o ${OUT_FOLDER}/${i}.cbl
  /usr/bin/time bufboss/bin/bufboss_build -a ${FN} -o ${OUT_FOLDER}/${i}.bufboss -k 31 -t tmp
  /usr/bin/time bifrost/build/bin/Bifrost build -r ${FN} -o ${OUT_FOLDER}/${i}.bifrost -k 31 -t 1
  /usr/bin/time Buffered_SBWT/build -r -t 1 -f ${FN} ${OUT_FOLDER}/${i}.sbwt 
  THREADS=$((MAX_THREADS > 4 ? 4 : MAX_THREADS))
  echo "threads = ${THREADS}"
  /usr/bin/time Buffered_SBWT/build -r -t $THREADS -f ${FN} ${OUT_FOLDER}/${i}a_.sbwt 
  THREADS=$((MAX_THREADS > 16 ? 16 : MAX_THREADS))
  echo "threads = ${THREADS}"
  /usr/bin/time Buffered_SBWT/build -r -m $((MAX_MEM > 4 ? 4 : MAX_MEM)) -t $THREADS -f ${FN} ${OUT_FOLDER}/${i}_b.sbwt 
  echo "threads = ${MAX_THREADS}"
  /usr/bin/time bifrost/build/bin/Bifrost build -r ${FN} -o ${OUT_FOLDER}/${i}.bifrost -k 31 -t $MAX_THREADS
  /usr/bin/time Buffered_SBWT/build -r -m $((MAX_MEM > 30 ? 30 : MAX_MEM)) -t $MAX_THREADS -f ${FN} ${OUT_FOLDER}/${i}_c.sbwt 

done