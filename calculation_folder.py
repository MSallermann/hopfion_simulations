import json, os

class calculation_folder:
    """Represents one folder of a calculation. AKA one set of parameters for the Hopfion"""

    def __init__(self, output_folder):
        self.output_folder            = output_folder
        self._descriptor_file_name    = "params.json"
        self._initial_chain_file_name = "initial_chain.ovf"
        self.descriptor = {}

        self._lock_file = os.path.join(self.output_folder, "~lock")

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.from_json()

    def get_descriptor_file_path(self):
        return os.path.join(self.output_folder, self._descriptor_file_name)

    def get_initial_chain_file_path(self):
        return os.path.join(self.output_folder, self._initial_chain_file_name)

    def from_json(self):
        if os.path.exists(self.get_descriptor_file_path()):
            with open(self.get_descriptor_file_path(), "r") as f:
                self.descriptor = json.load(f)

    def lock(self):
        """Checks for lockfile in folder. If no lock file is present the lock file is created and True is returned. Can be used to signal to other processes"""
        if not os.path.exists(self._lock_file):
            with open(self._lock_file) as f:
                pass
            return True
        else:
            return False

    def unlock(self):
        """Unlocks"""
        if os.path.exists(self._lock_file):
            os.remove(self._lock_file)
            return True
        else:
            return False

    def to_json(self):
        with open(self.get_descriptor_file_path(), "w") as f:
            f.write(json.dumps(self.descriptor, indent=4))
