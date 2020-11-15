#!/bin/bash

#$ -N rsp_c3_{pressure}
#$ -cwd
#$ -V
#$ -l h_rt=168:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

module load intel/2016

export LD_LIBRARY_PATH=/exports/applications/apps/SL7/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/mpi/intel64/bin:/exports/applications/apps/SL7/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/mkl/lib/intel64:/exports/applications/apps/SL7/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/../../inspector_xe/lib64:/exports/applications/apps/SL7/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/ipp/lib/intel64:/exports/applications/apps/SL7/intel/parallel_studio_xe_2016/compilers_and_libraries/linux/lib/intel64:/usr/local/blcr/0.8.6_b4/lib64:/usr/local/blcr/0.8.6_b4/lib:/exports/applications//gridengine/2011.11p1_155/lib/linux-x64

cat /proc/cpuinfo > cpuinfo.{pressure}

# Ensure that RASPA is linked in parent directory!
export RASPA_DIR=/exports/csce/eddie/eng/groups/eddie_see_imp_bio/richard/INT_RASPA
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RASPA_DIR/lib

echo "Timing Raspa setup 3 at pressure {pressure}" > timing.$JOB_ID
date >> timing.$JOB_ID
$RASPA_DIR/bin/simulate simulation.input
date >> timing.$JOB_ID
