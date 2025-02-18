#!/bin/bash

# Setting OPENMPI paths here:

export PATH=/progs/openmpi-4.1.1/bin:$PATH
export LD_LIBRARY_PATH=/progs/openmpi-4.1.1/lib:$LD_LIBRARY_PATH

# Here giving the path to the ORCA binaries and giving communication protocol

export orcadir=/progs/orca-5.0.4
export PATH=$orcadir:$PATH

# Creating local scratch folder for the user on the computing node. /scratch directory must exist.

mkdir -p /scratch/$USER.$JOB_ID 
chmod 777 /scratch/$USER.$JOB_ID
cp $SGE_O_WORKDIR/*.inp /scratch/$USER.$JOB_ID/
cp $SGE_O_WORKDIR/*.gbw /scratch/$USER.$JOB_ID/
cp $SGE_O_WORKDIR/*.xyz /scratch/$USER.$JOB_ID/
cp $SGE_O_WORKDIR/*.hess /scratch/$USER.$JOB_ID/
cp $SGE_O_WORKDIR/*.pc /scratch/$USER.$JOB_ID/
cd /scratch/$USER.$JOB_ID/

$orcadir/orca $1.inp >> $SGE_O_WORKDIR/$1.out 

cp *.gbw $SGE_O_WORKDIR
cp *.engrad $SGE_O_WORKDIR
cp *.xyz $SGE_O_WORKDIR
cp *.loc $SGE_O_WORKDIR
cp *.qro $SGE_O_WORKDIR
cp *.uno $SGE_O_WORKDIR
cp *.unso $SGE_O_WORKDIR
cp *.uco $SGE_O_WORKDIR
cp *.qro $SGE_O_WORKDIR
cp *.hess $SGE_O_WORKDIR
cp  *.cis $SGE_O_WORKDIR
cp *.dat $SGE_O_WORKDIR
cp *.mp2nat $SGE_O_WORKDIR
cp *.nat $SGE_O_WORKDIR
cp *.scfp_fod $SGE_O_WORKDIR
cp *.scfp $SGE_O_WORKDIR
cp *.scfr $SGE_O_WORKDIR
cp *.nbo $SGE_O_WORKDIR
cp *.nto $SGE_O_WORKDIR
cp FILE.47 $SGE_O_WORKDIR
cp *_property.txt $SGE_O_WORKDIR
cp *spin* $SGE_O_WORKDIR
rm -r /scratch/$USER.$JOB_ID


