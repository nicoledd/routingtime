#!/bin/bash
#SBATCH -J routingtimes
#SBATCH --output="out0/out-%A_%a.out"
#SBATCH --time=03:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4G
#SBATCH --array=0-399
#SBATCH --exclude=openlab[30-33]
# Mail me when starting and stopping
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nido4478@colorado.edu
#SBATCH --account=scavenger
#SBATCH --qos=scavenger
#SBATCH --partition=scavenger


module load Python3

python3 -m pip install --user networkx


python3 main.py -id $SLURM_ARRAY_TASK_ID || echo "TERRIBLE_ERROR_HAPPENED"
