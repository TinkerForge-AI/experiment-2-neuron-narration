"""
PatternWatcher: Persistent, cumulative pattern detection and logging.
"""
import json
import os
from utils import narrative_log
from config import DEFAULT_TRUST_SCORE, PATTERNWATCHER_CONFIDENCE_STEP


class PatternWatcher:
    def monitor_neurons(self, neurons, pattern, rapid_firing_threshold=3):
        # Check for rapid firing in all neurons
        rapid_firing_neurons = []
        for neuron in neurons:
            firings = [t for t, _, fired in neuron.history if fired]
            if len(firings) >= rapid_firing_threshold:
                rapid_firing_neurons.append(neuron)
        if rapid_firing_neurons:
            self.log_event(f"PatternWatcher: Persistent rapid firing detected in {len(rapid_firing_neurons)} neurons. Recommending increased refractory offset and decay factor.")
            for neuron in rapid_firing_neurons:
                neuron.adapt_parameters(refractory_offset_increase=True, decay_factor_decrease=True, watcher=self)
        if len(rapid_firing_neurons) > 1:
            self.log_event(f"PatternWatcher: Multiple neurons exhibiting rapid firing. Triggering network-wide dampening.")
            for neuron in rapid_firing_neurons:
                neuron.adapt_parameters(network_dampening=True, watcher=self)
    def __init__(self, interface, task_context="Generic Task"):
        from patternwatcher_config import (
            SAFE_THRESHOLD_MIN, SAFE_THRESHOLD_MAX,
            SAFE_REFRACTORY_OFFSET_MIN, SAFE_REFRACTORY_OFFSET_MAX,
            SAFE_DECAY_FACTOR_MIN, SAFE_DECAY_FACTOR_MAX,
            SAFE_MEMBRANE_POTENTIAL_MIN, SAFE_MEMBRANE_POTENTIAL_MAX,
            PATTERNWATCHER_SENSITIVITY, PATTERNWATCHER_LEARNING_RATE,
            PATTERNWATCHER_MEMORY_WINDOW, PATTERNWATCHER_NOTIFICATION_THRESHOLD,
            PATTERNWATCHER_LEARNING_HISTORY, PATTERNWATCHER_SUCCESSFUL_RECOGNITIONS, PATTERNWATCHER_FAILED_RECOGNITIONS
        )
        self.interface = interface
        self.task_context = task_context
        self.log = []
        self.trust_scores = {}  # neuron_id -> trust score
        self.pattern_confidence = {}  # pattern -> confidence
        # Safe/unsafe bounds
        self.safe_bounds = {
            "threshold": (SAFE_THRESHOLD_MIN, SAFE_THRESHOLD_MAX),
            "refractory_offset": (SAFE_REFRACTORY_OFFSET_MIN, SAFE_REFRACTORY_OFFSET_MAX),
            "decay_factor": (SAFE_DECAY_FACTOR_MIN, SAFE_DECAY_FACTOR_MAX),
            "membrane_potential": (SAFE_MEMBRANE_POTENTIAL_MIN, SAFE_MEMBRANE_POTENTIAL_MAX),
        }
        self.sensitivity = PATTERNWATCHER_SENSITIVITY
        self.learning_rate = PATTERNWATCHER_LEARNING_RATE
        self.memory_window = PATTERNWATCHER_MEMORY_WINDOW
        self.notification_threshold = PATTERNWATCHER_NOTIFICATION_THRESHOLD
        self.learning_history = PATTERNWATCHER_LEARNING_HISTORY
        self.successful_recognitions = PATTERNWATCHER_SUCCESSFUL_RECOGNITIONS
        self.failed_recognitions = PATTERNWATCHER_FAILED_RECOGNITIONS

    def monitor_bounds(self, neuron):
        # Check all neuron parameters for safe/unsafe bounds
        unsafe_events = []
        for param, (safe_min, safe_max) in self.safe_bounds.items():
            value = getattr(neuron, param, None)
            if value is not None:
                unsafe_fraction = 0
                if value < safe_min:
                    unsafe_fraction = abs((safe_min - value) / (safe_max - safe_min))
                elif value > safe_max:
                    unsafe_fraction = abs((value - safe_max) / (safe_max - safe_min))
                elif value > safe_max * self.notification_threshold or value < safe_min * (2 - self.notification_threshold):
                    unsafe_fraction = self.notification_threshold
                if unsafe_fraction >= self.notification_threshold:
                    unsafe_events.append((param, value, safe_min, safe_max))
        for param, value, safe_min, safe_max in unsafe_events:
            self.log_event(f"Threshold for Neuron {neuron.id} is approaching unsafe {('high' if value > safe_max else 'low')} limit ({param}: {value}, safe range: {safe_min}-{safe_max}). Notifying neuron.")
            neuron.receive_boundary_notification(param, value, safe_min, safe_max, watcher=self)
            self.learning_history.append({
                "event": "boundary_notification",
                "neuron_id": neuron.id,
                "param": param,
                "value": value,
                "safe_min": safe_min,
                "safe_max": safe_max
            })

    def log_learning(self, message):
        self.log_event(f"PatternWatcher Learning Log: {message}")
        self.learning_history.append({"event": "learning_log", "message": message})

    def discover_pattern(self, pattern):
        self.log_event(f"PatternWatcher has discovered recurring pattern '{pattern}'. Registering with NeuronPatternInterface.")
        self.interface.register_pattern(pattern, self)
        self.pattern_confidence[pattern] = self.pattern_confidence.get(pattern, 0.5)  # Initial confidence

    def recommend_pattern(self, neuron, pattern):
        self.log_event(f"PatternWatcher recommends pattern '{pattern}' to Neuron {neuron.id}.")
        neuron.receive_pattern_recommendation(pattern, self)
        # Adapt confidence based on neuron feedback
        if neuron.trust_score > 0.8:
            self.pattern_confidence[pattern] = min(1.0, self.pattern_confidence.get(pattern, 0.5) + PATTERNWATCHER_CONFIDENCE_STEP)
            self.log_event(f"PatternWatcher: Increased confidence in pattern '{pattern}' due to positive neuron feedback.")
        elif neuron.trust_score < 0.3:
            self.pattern_confidence[pattern] = max(0.0, self.pattern_confidence.get(pattern, 0.5) - PATTERNWATCHER_CONFIDENCE_STEP)
            self.log_event(f"PatternWatcher: Decreased confidence in pattern '{pattern}' due to skepticism from neuron.")

    def update_trust(self, neuron, delta, context=None):
        old_score = self.trust_scores.get(neuron.id, DEFAULT_TRUST_SCORE)
        new_score = min(1.0, max(0.0, old_score + delta))
        self.trust_scores[neuron.id] = new_score
        explanation = f"Neuron {neuron.id}: My trust score for PatternWatcher has changed from {old_score:.2f} to {new_score:.2f}."
        if context:
            explanation += f" Reason: {context}"
        self.log_event(explanation)
        # PatternWatcher reflects on neuron behavior
        if delta < 0:
            self.log_event(f"PatternWatcher: Noted skepticism from Neuron {neuron.id}. Will review my classification of relevant patterns.")
            # Lower confidence in all patterns associated with this neuron
            for pattern in self.pattern_confidence:
                self.pattern_confidence[pattern] = max(0.0, self.pattern_confidence[pattern] - PATTERNWATCHER_CONFIDENCE_STEP)
        elif delta > 0 and new_score > 0.8:
            self.log_event(f"PatternWatcher: Neuron {neuron.id} adapted independently. Considering updating global pattern criteria.")
            for pattern in self.pattern_confidence:
                self.pattern_confidence[pattern] = min(1.0, self.pattern_confidence[pattern] + PATTERNWATCHER_CONFIDENCE_STEP)
    def reflect_on_revision(self, pattern):
        self.log_event(f"PatternWatcher: Alert—multiple neurons have revised {pattern}. Global review triggered.")

    def log_event(self, message, event_type=None, neuron_id=None, extra=None):
        # Always include task context in narration
        if extra is None:
            extra = {}
        if 'task_context' not in extra:
            extra['task_context'] = getattr(self, 'task_context', 'Generic Task')
        # ...existing code...
        from log_config import LOG_MODE
        import datetime
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        # Diagnostic mode: full detail, markdown, grouped by event type
        if LOG_MODE == 'diagnostic':
            entry = f"- [{timestamp}] "
            if event_type:
                entry += f"**{event_type}**: "
            entry += message
            if neuron_id:
                entry += f" (Neuron {neuron_id})"
            if extra:
                entry += f" | {extra}"
            self.log.append(entry)
            print(entry)
        else:
            # Concise mode: group major events, markdown headings/tables
            if event_type == 'boundary_notification' and extra:
                if not hasattr(self, '_boundary_table'):
                    self._boundary_table = []
                self._boundary_table.append([
                    timestamp,
                    f"Neuron {neuron_id}",
                    extra.get('param', ''),
                    extra.get('value', ''),
                    f"{extra.get('safe_min', '')}–{extra.get('safe_max', '')}",
                    extra.get('action', '')
                ])
            elif event_type == 'pattern_event':
                if not hasattr(self, '_pattern_events'):
                    self._pattern_events = []
                self._pattern_events.append(f"- [{timestamp}] {message}")
            elif event_type == 'lesson_learned':
                if not hasattr(self, '_lessons_learned'):
                    self._lessons_learned = []
                self._lessons_learned.append(f"- {message}")
            else:
                self.log.append(f"- [{timestamp}] {message}")
            print(f"- [{timestamp}] {message}")

    def export_concise_log(self):
        # Export grouped markdown log for concise mode
        log_md = []
        if hasattr(self, '_pattern_events'):
            log_md.append("## PatternWatcher Events\n" + '\n'.join(self._pattern_events))
        if hasattr(self, '_boundary_table') and self._boundary_table:
            log_md.append("\n## Boundary Notifications\n")
            log_md.append("| Time | Neuron | Parameter | Value | Safe Range | Action |\n|------|--------|-----------|-------|-----------|--------|")
            for row in self._boundary_table:
                log_md.append("| " + " | ".join(str(x) for x in row) + " |")
        if hasattr(self, '_lessons_learned'):
            log_md.append("\n## Lessons Learned\n" + '\n'.join(self._lessons_learned))
        # Add any other logs
        if self.log:
            log_md.append("\n## Other Events\n" + '\n'.join(self.log))
        return '\n'.join(log_md)
