from config import ADOPTION_THRESHOLD, MENTORING_TRUST_BOOST
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
        # Aggregate feedback: if enough neurons revise, notify PatternWatcher
        revised_count = sum(1 for n in self.neuron_adoption if self.neuron_adoption[n].get(pattern) == "revised")
        if revised_count >= ADOPTION_THRESHOLD:
            from pattern_watcher import PatternWatcher
            # This assumes a singleton PatternWatcher for notification
            print(f"NeuronPatternInterface: Multiple neurons ({revised_count}) have revised {pattern}. Notifying PatternWatcher.")
    def mentor_neuron(self, mentor, mentee, pattern):
        # Mentor shares pattern and boosts trust
        if pattern in mentor.patterns_adopted:
            mentee.patterns_monitored.add(pattern)
            mentee.trust_score += MENTORING_TRUST_BOOST
            print(f"NeuronPatternInterface: Neuron {mentor.id} mentored Neuron {mentee.id} on {pattern}. Trust boosted.")
