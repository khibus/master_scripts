#!/bin/bash

eval "$(/progs/miniconda3/bin/conda shell.bash hook)"
conda activate bagel
export PATH=/progs2/bagel/build/bin:$PATH
export LD_LIBRARY_PATH=/progs/miniconda3/envs/bagel/lib:/progs2/bagel/build/lib
mkdir -p /scratch/$USER.$JOB_ID 
chmod 777 /scratch/$USER.$JOB_ID
cp $SGE_O_WORKDIR/$1.json /scratch/$USER.$JOB_ID/
if grep -Fxq "load_ref" $1.json; then
 cp $SGE_O_WORKDIR/*.archive /scratch/$USER.$JOB_ID/
fi

cd /scratch/$USER.$JOB_ID/

mpirun -np $2 BAGEL $1.json > $SGE_O_WORKDIR/$1.out 

cp *.molden $SGE_O_WORKDIR
cp *.archive $SGE_O_WORKDIR
rm -r /scratch/$USER.$JOB_ID


