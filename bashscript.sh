#!/bin/bash
#SBATCH -J routingtimes
#SBATCH --output="out/out-%A_%a.out"
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4G
#SBATCH --array=0-299
#SBATCH --exclude=openlab[30-33]
# Mail me when starting and stopping
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nido4478@colorado.edu
#SBATCH --account=scavenger
#SBATCH --qos=scavenger
#SBATCH --partition=scavenger


module load Python3


python3 main.py -id $SLURM_ARRAY_TASK_ID




#set -euo pipefail
#. /usr/share/Modules/init/bash
#. /etc/profile.d/ummodules.sh


#module load Python3

#declare -a commands


#for p in $(seq 0 .01 .02); do
#		for n in {5..10..5}; do
#				for i in {1..10}; do
#						commands += ("Python3 'main.py' '${n}' '${p}'")
#					done
#			done
#	done


#eval "${commands[${SLURM_ARRAY_TASK_ID}]}"