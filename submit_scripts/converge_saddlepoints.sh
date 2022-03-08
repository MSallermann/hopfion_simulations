#!/bin/sh
#SBATCH -p th1-2020-64
source compiler-select intel
source python-select py3k
python -m pip install mpi4py --user
python -m pip install --upgrade spirit-extras --user
srun python converge_saddlepoints.py /local/th1/iff003/saller/gneb_preconverge#03_07_2022_00_26_25/* -MPI