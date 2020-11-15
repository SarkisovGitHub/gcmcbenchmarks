#!/bin/bash

#$ -N dlm_{pressure}
#$ -cwd
#$ -V
#$ -l h_rt=06:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.{pressure}

echo "Timing DLMonte setup 1 at pressure {pressure}" > timing.$JOB_ID
date >> timing.$JOB_ID
./DLMONTE-SRL.X
date >> timing.$JOB_ID
