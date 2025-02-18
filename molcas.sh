#!/bin/bash

export MOLCAS_ROOT=/progs/OpenMolcas/build
workdir=/scratch/$USER.$JOB_ID
export MOLCAS_WORKDIR=/scratch/$USER.$JOB_ID
export PATH=/progs/openmpi-4.1.1/bin:$PATH
export LD_LIBRARY_PATH=/progs/openmpi-4.1.1/lib:$LD_LIBRARY_PATH
echo $MOLCAS_ROOT > /home/$USER/.Molcas/molcas

export MOLCAS_NPROCS=$3

if [ $4 ]; then
 export MOLCAS_MEM=$4
fi
mkdir -p $workdir
chmod 777 $workdir
cp $1.input $workdir
# cp *.RasOrb $workdir
# cp *.molden $workdir
# cp $1.JobIph $workdir
#cp *.guessorb* $workdir
# cp *.ScfOrb $workdir
#cp *.JobMix $workdir
cd $workdir

python3 $MOLCAS_ROOT/pymolcas $1.input > $SGE_O_WORKDIR/$1.out

 cp $workdir/*grid              $SGE_O_WORKDIR
 cp $workdir/*M2Msi             $SGE_O_WORKDIR
 cp $workdir/*guessorb*         $SGE_O_WORKDIR
 cp $workdir/*rasscf*           $SGE_O_WORKDIR
 cp $workdir/*scf*              $SGE_O_WORKDIR
 cp $workdir/*h5                $SGE_O_WORKDIR
 cp $workdir/*.RasOrb*          $SGE_O_WORKDIR
 cp $workdir/$1*/*.RasOrb*      $SGE_O_WORKDIR
 cp $workdir/*.molden           $SGE_O_WORKDIR
 cp $workdir/$1*/*.molden       $SGE_O_WORKDIR
 cp $workdir/*.JobIph           $SGE_O_WORKDIR
 cp $workdir/$1*/*.JobIph       $SGE_O_WORKDIR
 cp $workdir/*.ScfOrb*          $SGE_O_WORKDIR
 cp $workdir/$1*/*.ScfOrb*      $SGE_O_WORKDIR
 cp $workdir/*.JobMix           $SGE_O_WORKDIR
 cp $workdir/$1*/*.JobMix       $SGE_O_WORKDIR
 cp $workdir/$1*/*.grid         $SGE_O_WORKDIR
 cp $workdir/*rassi*            $SGE_O_WORKDIR
 cp $workdir/$1*/*rassi*        $SGE_O_WORKDIR
 cp $workdir/RUNFILE            $SGE_O_WORKDIR
 cp $workdir/$1*/RUNFILE        $SGE_O_WORKDIR
rm -r $workdir

