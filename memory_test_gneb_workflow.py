import increase_n_cell
from spirit_python_utilities.spirit_extras import import_spirit, gneb_workflow, data, plotting, memory_monitor

if __name__ == "__main__":
    import os
    os.environ["OMP_NUM_THREADS"] = "16"

    def choose_spirit(x):
        return "afeb6181bd4f1".startswith(x.revision) and x.openMP and x.pinning # check for solver info revision and openMP and pinning
    spirit_info = import_spirit.find_and_insert("~/Coding", stop_on_first_viable=True, choose = choose_spirit )[0]

    with memory_monitor.MemoryMonitor() as monitor:
        increase_n_cell.main()
        monitor.plot("gneb_workflow_memory.png")