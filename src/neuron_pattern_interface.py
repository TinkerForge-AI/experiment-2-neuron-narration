"""
NeuronPatternInterface: Manages pattern registry, neuron adoption, and narrative notifications.
"""
class NeuronPatternInterface:
    def __init__(self):
        self.pattern_registry = {}  # pattern -> [PatternWatcher]
        self.neuron_adoption = {}  # neuron_id -> {pattern: status}

    def register_pattern(self, pattern, watcher):
        self.pattern_registry.setdefault(pattern, []).append(watcher)
        print(f"NeuronPatternInterface: Registered pattern '{pattern}' from PatternWatcher.")

    def notify_neuron(self, neuron, pattern):
        print(f"NeuronPatternInterface: Notifying Neuron {neuron.id} about pattern '{pattern}'.")
        neuron.receive_pattern_notification(pattern, self)

    def update_adoption(self, neuron, pattern, status):
        self.neuron_adoption.setdefault(neuron.id, {})[pattern] = status
        print(f"NeuronPatternInterface: Neuron {neuron.id} adoption status for '{pattern}' is now '{status}'.")
        if status == "revised":
            print(f"NeuronPatternInterface: Neuron {neuron.id} has revised their recognition of {pattern}.")
