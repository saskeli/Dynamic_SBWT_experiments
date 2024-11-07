#!/bin/bash

USAGE="$0 <file_list> <data_folder> <output_folder> <limit> 

Add files from <file_list>, that can be found in <data_folder> to indexes found in <output_folder>.

The index files should have been created with build_expanding to make sure that the correct stuff gets added.

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
MAX_MEM=$(free -g | awk '/^Mem:/{print int($2 * 0.9)}')

i=1
while [ $i -lt $FILE_LIMIT ]; do
  i=$(($i * 2))

  FN=${OUT_FOLDER}/tmp.${FEXT}
  GFN=${OUT_FOLDER}/tmp.${EXT}
  if [ ! -f $FN ]; then
    head -n $(($i + 2)) ${FOF} | tail -n 2 | while read line ; do echo "${DATA_FOLDER}/${line}"; done | xargs cat > $GFN
    if [ "$EXT" != "$FEXT" ]; then
      gunzip $GFN
    fi
  fi

  echo $FN > ${OUT_FOLDER}/tmp.txt
  
  /usr/bin/time CBL/target/release/examples/cbl insert ${OUT_FOLDER}/${i}.cbl ${FN} -o ${OUT_FOLDER}/tmp.cbl  
  /usr/bin/time bifrost/build/bin/Bifrost update -g ${OUT_FOLDER}/${i}.bifrost.gfa.gz -r ${FN} -o ${OUT_FOLDER}/tmp.bifrost -t 1
  /usr/bin/time BBB/build/bin/buffer -r -t 1 ${OUT_FOLDER}/${i}.sbwt ${OUT_FOLDER}/tmp.txt ${OUT_FOLDER}/tmp.sbwt 
  echo "threads = ${MAX_THREADS}"
  /usr/bin/time bifrost/build/bin/Bifrost update -g ${OUT_FOLDER}/${i}.bifrost.gfa.gz -r ${FN} -o ${OUT_FOLDER}/tmp.bifrost -t $MAX_THREADS
  /usr/bin/time BBB/build/bin/buffer -r -t $((MAX_THREADS > 4 ? 4 : MAX_THREADS)) ${OUT_FOLDER}/${i}.sbwt ${OUT_FOLDER}/tmp.txt ${OUT_FOLDER}/tmp.sbwt 
  MEM=$((MAX_MEM > 4 ? 4 : MAX_MEM))
  /usr/bin/time BBB/build/bin/buffer -r -m $MEM -t $((MAX_THREADS > 16 ? 16 : MAX_THREADS)) ${OUT_FOLDER}/${i}.sbwt ${OUT_FOLDER}/tmp.txt ${OUT_FOLDER}/tmp.sbwt 
  MEM=$((MAX_MEM > 30 ? 30 : MAX_MEM))
  /usr/bin/time BBB/build/bin/buffer -r -m $MEM -t $MAX_THREADS ${OUT_FOLDER}/${i}.sbwt ${OUT_FOLDER}/tmp.txt ${OUT_FOLDER}/tmp.sbwt 

  rm -f ${OUT_FOLDER}/tmp.txt ${OUT_FOLDER}/tmp.${FEXT} ${OUT_FOLDER}/tmp.${EXT} ${OUT_FOLDER}/tmp.cbl 
  rm -f ${OUT_FOLDER}/tmp.bifrost.gfa.gz ${OUT_FOLDER}/tmp.bifrost.bfi ${OUT_FOLDER}/tmp.sbwt
done

i=1
while [ $i -lt $FILE_LIMIT ]; do
  i=$(($i * 2))
  FN=${OUT_FOLDER}/tmp.${FEXT}
  GFN=${OUT_FOLDER}/tmp.${EXT}
  if [ ! -f $FN ]; then
    head -n $(($i + 2)) ${FOF} | tail -n 2 | while read line ; do echo "${DATA_FOLDER}/${line}"; done | xargs cat > $GFN
    if [ "$EXT" != "$FEXT" ]; then
      gunzip $GFN
    fi
  fi

  /usr/bin/time bufboss/bin/bufboss_update -i ${OUT_FOLDER}/${i}.bufboss -a ${FN} -o ${OUT_FOLDER}/tmp.bufboss
  
  rm -f ${OUT_FOLDER}/tmp.${FEXT} ${OUT_FOLDER}/tmp.${EXT}
  rm -rf ${OUT_FOLDER}/tmp.bufboss
done