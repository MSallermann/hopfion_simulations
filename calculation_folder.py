import json, os

class calculation_folder:
    """Represents one folder of a calculation. AKA one set of parameters for the Hopfion"""

    def __init__(self, output_folder):
        self.output_folder            = output_folder
        self._descriptor_file_name    = "params.json"
        self._initial_chain_file_name = "initial_chain.ovf"
        self.descriptor = {}

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

    def __del__(self):
        with open(self.get_descriptor_file_path(), "w") as f:
            f.write(json.dumps(self.descriptor, indent=4))
