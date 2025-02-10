#!/bin/bash

USAGE="$0 <file_list> <data_folder> <output_folder> <limit> 

Search with files from <file_list>, that can be found in <data_folder> from indexes found in <output_folder>.

The index file names should match those created with build_expanding.

where:
    file_list    is a text file containing the names of fasta files to use.
    data_folder  is the folder containing the fasta files.
    output_foder is the directory where indexes are.
    limit        maximum number of genomes the indexes are built of. Default: 1024.
    
All arguments, besides the limit are required

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

MAX_THREADS=$(nproc)
MAX_THREADS=$((MAX_THREADS > 32 ? 32 : MAX_THREADS))

FN=${OUT_FOLDER}/tmp.${FEXT}
GFN=${OUT_FOLDER}/tmp.${EXT}
if [ ! -f $FN ]; then
  tail -n 500 ${FOF} | while read line ; do echo "${DATA_FOLDER}/${line}"; done | xargs cat > $GFN
  if [ "$EXT" != "$FEXT" ]; then
    gunzip $GFN
  fi
fi

i=1
while [ $i -lt $FILE_LIMIT ]; do
  i=$(($i * 2))
  
  /usr/bin/time CBL/target/release/examples/cbl query ${OUT_FOLDER}/${i}.cbl ${FN}
  # We need reverse complements for bufboss?
  /usr/bin/time bufboss/bin/bufboss_query -i ${OUT_FOLDER}/${i}.bufboss -q ${FN} -o /dev/null
  /usr/bin/time bifrost/build/bin/Bifrost query -g ${OUT_FOLDER}/${i}.bifrost.gfa.gz -I ${OUT_FOLDER}/${i}.bifrost.bfi -q ${FN} -o ${OUT_FOLDER}/tmp -p -t 1
  /usr/bin/time Buffered_SBWT/search -i ${OUT_FOLDER}/${i}.sbwt ${FN}
  echo "threads = ${MAX_THREADS}"
  /usr/bin/time bifrost/build/bin/Bifrost query -g ${OUT_FOLDER}/${i}.bifrost.gfa.gz -I ${OUT_FOLDER}/${i}.bifrost.bfi -q ${FN} -o ${OUT_FOLDER}/tmp -p -t $MAX_THREADS

  rm -f ${OUT_FOLDER}/tmp.tsv 
done

rm -f ${OUT_FOLDER}/tmp.${EXT} ${OUT_FOLDER}/tmp.${FEXT}
