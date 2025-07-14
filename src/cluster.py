"""
Cluster: Emergent formation and higher-order controller logic.
"""
import multiprocessing
import uuid
from utils import narrative_log

class Cluster:
    def __init__(self, neurons):
        self.id = str(uuid.uuid4())
        self.neurons = neurons
        self.log = []
        narrative_log(self.log, f"Cluster {self.id} formed with neurons {[n.id for n in neurons]}.")

    def run(self, event):
        for neuron in self.neurons:
            neuron.state += event['value']
            narrative_log(self.log, f"Cluster {self.id} dispatched event to Neuron {neuron.id}.")

    def get_log(self):
        return self.log
