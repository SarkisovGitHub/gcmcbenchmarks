#!/bin/bash

#$ -N cas_3_{pressure}
#$ -cwd
#$ -V
#$ -l h_rt=24:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.{pressure}

echo "Timing Cassandra setup 3 at pressure {pressure}" > timing.$JOB_ID
date >> timing.$JOB_ID
./cassandra.exe CO2_IRMOF.inp
date >> timing.$JOB_ID
