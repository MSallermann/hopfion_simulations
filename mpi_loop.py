from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

def mpi_loop(callable, n_items):
    print(f"rank = {rank}")
    print(f"size = {size}")
    print(f"name = {name}")
    for i in range(rank, n_items, size):
        callable(i)