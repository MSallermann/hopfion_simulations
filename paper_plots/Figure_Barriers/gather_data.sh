BASE_PATH=/home/moritz/hopfion_simulations/all_sp

# Criterion data, writes criterion_data.txt
python3 ../../plot_energy_barrier.py $BASE_PATH/* -data ./barrier_data.txt
