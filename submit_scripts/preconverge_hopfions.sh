#!/bin/sh
#SBATCH -p th1-2020-64
source compiler-select intel
source python-select py3k
python -m pip install mpi4py --user
python -m pip install --upgrade spirit-extras --user
srun python preconverge_paths.py /local/th1/iff003/saller/gamma_l0_calculations/* -MPI