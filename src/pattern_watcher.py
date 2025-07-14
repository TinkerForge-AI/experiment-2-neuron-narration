"""
PatternWatcher: Persistent, cumulative pattern detection and logging.
"""
import json
import os
from utils import narrative_log


class PatternWatcher:
    def __init__(self, interface):
        self.interface = interface
        self.log = []
        self.trust_scores = {}  # neuron_id -> trust score

    def discover_pattern(self, pattern):
        self.log_event(f"PatternWatcher has discovered recurring pattern '{pattern}'. Registering with NeuronPatternInterface.")
        self.interface.register_pattern(pattern, self)

    def recommend_pattern(self, neuron, pattern):
        self.log_event(f"PatternWatcher recommends pattern '{pattern}' to Neuron {neuron.id}.")
        neuron.receive_pattern_recommendation(pattern, self)

    def update_trust(self, neuron, delta, context=None):
        old_score = self.trust_scores.get(neuron.id, 0.5)
        new_score = min(1.0, max(0.0, old_score + delta))
        self.trust_scores[neuron.id] = new_score
        explanation = f"Neuron {neuron.id}: My trust score for PatternWatcher has changed from {old_score:.2f} to {new_score:.2f}."
        if context:
            explanation += f" Reason: {context}"
        self.log_event(explanation)
        # PatternWatcher reflects on neuron behavior
        if delta < 0:
            self.log_event(f"PatternWatcher: Noted skepticism from Neuron {neuron.id}. Will review my classification of relevant patterns.")
        elif delta > 0 and new_score > 0.8:
            self.log_event(f"PatternWatcher: Neuron {neuron.id} adapted independently. Considering updating global pattern criteria.")
    def reflect_on_revision(self, pattern):
        self.log_event(f"PatternWatcher: Alert—multiple neurons have revised {pattern}. Global review triggered.")

    def log_event(self, message):
        print(message)
        self.log.append(message)
