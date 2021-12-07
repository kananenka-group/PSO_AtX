#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=Au_Cluster
#SBATCH --partition=akanane
#SBATCH --time=7-00:00:00
#SBATCH --mem=1Gb
#SBATCH --output=job.out
#SBATCH --error=job.err
#SBATCH --mail-user='akanane@udel.edu'
#SBATCH --mail-type=FAIL,END
#SBATCH --export=NONE

. /opt/shared/slurm/templates/libexec/openmpi.sh

python main_PSO.py 
