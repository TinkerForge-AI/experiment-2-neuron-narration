
"""
Neuron class: Narrative-driven, event-driven, explainable, self-reflective.
"""
import datetime
import uuid
from config import (
    DEFAULT_THRESHOLD, DEFAULT_REFRACTORY_OFFSET, DEFAULT_REFRACTORY_EVENTS, DEFAULT_DECAY_FACTOR,
    DEFAULT_PASSIVE_DECAY_LOG_THRESHOLD, DEFAULT_WEIGHTS, DEFAULT_TRUST_SCORE,
    TRUST_INCREMENT, TRUST_DECREMENT, TRUST_DEBATE_DECREMENT, TRUST_CHALLENGE_THRESHOLD,
    TRUST_ADOPT_THRESHOLD, ADOPTION_THRESHOLD, MENTORING_TRUST_BOOST
)




class Neuron:
    def receive_boundary_notification(self, param, value, safe_min, safe_max, watcher=None):
        self.log_event(f"I received a boundary notification from PatternWatcher. {param}={value} is outside safe range ({safe_min}-{safe_max}).")
        # Adaptive response: bring parameter back to safe range
        old_value = value
        if param == "threshold":
            self.threshold = min(max(self.threshold, safe_min), safe_max)
            self.log_event(f"I am reducing my threshold from {old_value} to {self.threshold} to return to safe operating range.")
        elif param == "refractory_offset":
            self.refractory_offset = min(max(self.refractory_offset, safe_min), safe_max)
            self.log_event(f"I am adjusting my refractory offset from {old_value} to {self.refractory_offset} for safety.")
        elif param == "decay_factor":
            self.decay_factor = min(max(self.decay_factor, safe_min), safe_max)
            self.log_event(f"I am adjusting my decay factor from {old_value} to {self.decay_factor} for safety.")
        elif param == "membrane_potential":
            self.potential = min(max(self.potential, safe_min), safe_max)
            self.log_event(f"I am resetting my membrane potential from {old_value} to {self.potential} for safety.")
        # Recovery narration and lessons learned
        self.log_event(f"Recovery complete. Lesson learned: returning to baseline {param} of {getattr(self, param)} maintains stability after stress.")
        if watcher:
            watcher.log_learning(f"Logged successful intervention for Neuron {self.id} on {param}. Updated recognition patterns for future events.")
    def adapt_parameters(self, refractory_offset_increase=False, decay_factor_decrease=False, network_dampening=False, watcher=None):
        from config import DEFAULT_REFRACTORY_OFFSET, DEFAULT_DECAY_FACTOR
        if refractory_offset_increase:
            old_offset = self.refractory_offset
            self.refractory_offset = min(1.0, self.refractory_offset + 0.2)
            self.log_event(f"Neuron {self.id}: Updated refractory offset from {old_offset} to {self.refractory_offset} as advised by PatternWatcher.")
            if watcher:
                watcher.log_event(f"PatternWatcher: Neuron {self.id} updated refractory offset to {self.refractory_offset}.")
        if decay_factor_decrease:
            old_decay = self.decay_factor
            self.decay_factor = max(0.5, self.decay_factor - 0.1)
            self.log_event(f"Neuron {self.id}: Updated decay factor from {old_decay} to {self.decay_factor} as advised by PatternWatcher.")
            if watcher:
                watcher.log_event(f"PatternWatcher: Neuron {self.id} updated decay factor to {self.decay_factor}.")
        if network_dampening:
            old_threshold = self.threshold
            self.threshold = min(self.threshold + 0.2, 2.0)
            self.log_event(f"Neuron {self.id}: Network-wide dampening applied. Increased threshold from {old_threshold} to {self.threshold}.")
    def __init__(self, neuron_id=None, threshold=DEFAULT_THRESHOLD, weights=None, history_length=5, refractory_offset=DEFAULT_REFRACTORY_OFFSET, refractory_events=DEFAULT_REFRACTORY_EVENTS, decay_factor=DEFAULT_DECAY_FACTOR, passive_decay_log_threshold=DEFAULT_PASSIVE_DECAY_LOG_THRESHOLD, interface=None, task_context="Generic Task"):
        self.id = neuron_id or str(uuid.uuid4())
        self.baseline_threshold = threshold
        self.threshold = threshold
        self.refractory_offset = refractory_offset
        self.refractory_events = refractory_events
        self.refractory_counter = 0
        self.in_refractory = False
        self.weights = weights or DEFAULT_WEIGHTS
        self.potential = 0.0
        self.baseline_potential = 0.0
        self.decay_factor = decay_factor
        self.history = []  # List of (timestamp, input, fired, input_event)
        self.asleep = False
        self.log = []
        self.history_length = history_length
        self.passive_decay_log_threshold = passive_decay_log_threshold
        self.last_input_received = False
        self.interface = interface
        self.patterns_monitored = set()
        self.patterns_adopted = set()
        self.trust_score = DEFAULT_TRUST_SCORE
        self.task_context = task_context
        self.log_event(f"I am born as Neuron {self.id} for task: '{self.task_context}' with baseline threshold {self.baseline_threshold}, refractory offset {self.refractory_offset}, decay factor {self.decay_factor}, and weights {self.weights}.", event_type="birth", extra={"task_context": self.task_context})

    def receive_pattern_notification(self, pattern, interface):
        self.log_event(f"Neuron {self.id}: Received pattern notification '{pattern}' from interface. Monitoring for now.")
        self.patterns_monitored.add(pattern)
        if interface:
            interface.update_adoption(self, pattern, "monitoring")
        self.log_event(f"Neuron {self.id}: I remain open to future PatternWatcher input, even after graduation.")

    def receive_pattern_recommendation(self, pattern, watcher):
        if pattern in self.patterns_adopted:
            self.log_event(f"Neuron {self.id}: Already recognize pattern '{pattern}' independently. No longer rely on PatternWatcher, but remain open to input.")
            return
        if self.trust_score > TRUST_ADOPT_THRESHOLD:
            self.patterns_adopted.add(pattern)
            self.log_event(f"Neuron {self.id}: PatternWatcher's suggestions have proven useful. I have adopted pattern '{pattern}' and updated my recognition.")
            watcher.update_trust(self, TRUST_INCREMENT, context="PatternWatcher’s recommendation led to successful adoption.")
            if self.interface:
                self.interface.update_adoption(self, pattern, "adopted")
        elif self.trust_score < TRUST_CHALLENGE_THRESHOLD:
            self.log_event(f"Neuron {self.id}: I am challenging PatternWatcher's directive regarding '{pattern}' and will log my experience.")
            watcher.update_trust(self, -TRUST_DECREMENT, context="Neuron challenged PatternWatcher directive.")
            if self.interface:
                self.interface.update_adoption(self, pattern, "challenging")
        else:
            self.log_event(f"Neuron {self.id}: Despite repeated suggestions, I remain unconvinced about '{pattern}'.")
            watcher.update_trust(self, -TRUST_DEBATE_DECREMENT, context="Neuron debated PatternWatcher recommendation.")
            if self.interface:
                self.interface.update_adoption(self, pattern, "debating")

    def encounter_pattern(self, pattern, negative=False):
        if pattern in self.patterns_monitored:
            if negative:
                self.log_event(f"Neuron {self.id}: Following a misfire with {pattern}, I am revising my recognition criteria and trust in my own judgment.")
                self.trust_score -= 0.1
                if self.interface:
                    self.interface.update_adoption(self, pattern, "revised")
            else:
                self.log_event(f"Neuron {self.id}: After repeated encounters, I now recognize '{pattern}' independently and have graduated from the interface, but remain open to input.")
                self.patterns_adopted.add(pattern)
                if self.interface:
                    self.interface.update_adoption(self, pattern, "independent")
                self.trust_score += 0.1
    def share_pattern(self, other_neuron, pattern):
        if pattern in self.patterns_adopted:
            self.log_event(f"Neuron {self.id}: Sharing my experience with {pattern} to help Neuron {other_neuron.id}.")
            other_neuron.receive_pattern_notification(pattern, self.interface)
            other_neuron.log_event(f"Neuron {other_neuron.id}: Received mentoring from Neuron {self.id} regarding {pattern}.")

    def log_event(self, message, event_type=None, watcher=None, extra=None):
        from log_config import LOG_MODE
        import datetime
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        if LOG_MODE == 'diagnostic':
            entry = f"- [{timestamp}] "
            if event_type:
                entry += f"**{event_type}**: "
            entry += message
            self.log.append(entry)
            print(entry)
        else:
            # Concise mode: group major events, collapse repeated recoveries
            if event_type == 'birth':
                self.log.append(f"- [{timestamp}] {message}")
            elif event_type == 'boundary_notification' and extra:
                if not hasattr(self, '_boundary_events'):
                    self._boundary_events = []
                self._boundary_events.append([
                    timestamp,
                    extra.get('param', ''),
                    extra.get('value', ''),
                    f"{extra.get('safe_min', '')}–{extra.get('safe_max', '')}",
                    extra.get('action', '')
                ])
            elif event_type == 'recovery':
                if not hasattr(self, '_recovery_events'):
                    self._recovery_events = set()
                key = (extra.get('param', ''), extra.get('value', ''))
                if key not in self._recovery_events:
                    self._recovery_events.add(key)
                    self.log.append(f"- [{timestamp}] {message}")
            elif event_type == 'lesson_learned':
                if not hasattr(self, '_lessons_learned'):
                    self._lessons_learned = []
                self._lessons_learned.append(f"- {message}")
            else:
                self.log.append(f"- [{timestamp}] {message}")
            print(f"- [{timestamp}] {message}")

    def export_concise_log(self):
        log_md = []
        if hasattr(self, '_boundary_events') and self._boundary_events:
            log_md.append("## Boundary Notifications\n")
            log_md.append("| Time | Parameter | Value | Safe Range | Action |\n|------|-----------|-------|-----------|--------|")
            for row in self._boundary_events:
                log_md.append("| " + " | ".join(str(x) for x in row) + " |")
        if hasattr(self, '_recovery_events') and self._recovery_events:
            log_md.append("\n## Recovery Events\n")
            for event in self._recovery_events:
                log_md.append(f"- {event}")
        if hasattr(self, '_lessons_learned'):
            log_md.append("\n## Lessons Learned\n" + '\n'.join(self._lessons_learned))
        if self.log:
            log_md.append("\n## Other Events\n" + '\n'.join(self.log))
        return '\n'.join(log_md)

    def markdown_log(self):
        content = "\n".join(self.log)
        return f"<details><summary>Neuron {self.id}</summary>\n{content}\n</details>"



    def receive_input(self, input_value, source=None, input_type="generic", metadata=None, task_context=None):
        self.last_input_received = True
        if self.asleep:
            self.log_event(f"I am currently asleep and will ignore incoming events until activated. (Task: {task_context or self.task_context})", event_type="state", extra={"task_context": task_context or self.task_context})
            return
        # Build input event abstraction
        input_event = {
            "value": input_value,
            "source": source,
            "input_type": input_type,
            "metadata": metadata or {},
            "task_context": task_context or self.task_context
        }
        self.log_event(f"Received input {input_value} of type '{input_type}' from {source} for task '{input_event['task_context']}'.", event_type="input", extra=input_event)
        # Decay membrane potential before adding new input
        old_potential = self.potential
        self.potential = self.potential * self.decay_factor + input_value * self.weights[0]
        self.log_event(f"My membrane potential has decayed from {old_potential} to {self.potential} after receiving input.", event_type="potential", extra=input_event)
        self.log_event(f"My threshold is currently {self.threshold}.", event_type="threshold", extra=input_event)
        # Update history with input event
        self.history.append((datetime.datetime.now().isoformat(), input_value, False, input_event))
        self.decide_to_fire(input_value, input_event)
    def passive_decay(self):
        """
        Apply passive decay if no input is received this cycle.
        Log only if the change is above passive_decay_log_threshold.
        """
        if self.asleep:
            return
        if not self.last_input_received:
            old_potential = self.potential
            self.potential = self.potential * self.decay_factor
            if abs(self.potential - old_potential) > self.passive_decay_log_threshold:
                self.log_event(f"No input received this cycle; my membrane potential has decayed from {old_potential} to {self.potential}.")
        self.last_input_received = False



    def decide_to_fire(self, input_value, input_event=None):
        if self.potential >= self.threshold:
            self.log_event(f"I decided to fire because my membrane potential ({self.potential}) exceeded my threshold ({self.threshold}) for task '{input_event['task_context'] if input_event else self.task_context}'.", event_type="fire", extra=input_event)
            self.history.append((datetime.datetime.now().isoformat(), input_value, True))
            self.enter_refractory()
            old_potential = self.potential
            self.potential = self.baseline_potential
            self.log_event(f"Resetting membrane potential from {old_potential} to baseline ({self.baseline_potential}) after firing.")
            self.adapt(fired=True)
            self.refractory_counter = 0  # Reset refractory counter on firing
        else:
            self.log_event(f"I did not fire because my membrane potential ({self.potential}) did not meet my threshold ({self.threshold}).")
            self.history.append((datetime.datetime.now().isoformat(), input_value, False))
            self.adapt(fired=False)
        self.summarize_history()
        self.update_refractory()


    def adapt(self, fired):
        if fired:
            # Adaptation logic can be extended here
            pass
        else:
            # If not firing for a while, lower threshold (unless in refractory)
            if not self.in_refractory and len(self.history) >= self.history_length and all(not h[2] for h in self.history[-self.history_length:]):
                old_threshold = self.threshold
                self.threshold = max(self.baseline_threshold, self.threshold - TRUST_DEBATE_DECREMENT)
                self.log_event(f"I am frustrated by not firing recently. Lowering threshold from {old_threshold} to {self.threshold}.")


    def summarize_history(self):
        recent = self.history[-self.history_length:]
        firings = [t for t, _, fired in recent if fired]
        self.log_event(f"Here is my recent firing history: {firings if firings else 'No recent firings.'}")


    def sleep(self):
        self.asleep = True
        self.log_event("I am going to sleep and will ignore events until woken.")


    def wake(self):
        self.asleep = False
        self.log_event("I am now awake and ready to receive events.")


    def notify_pattern(self, pattern):
        self.log_event(f"PatternWatcher has notified me about a recurring pattern: {pattern}. I will monitor this closely.")


    def get_log(self):
        return self.log

    def enter_refractory(self):
        self.in_refractory = True
        self.refractory_counter = 0
        old_threshold = self.threshold
        self.threshold = self.baseline_threshold + self.refractory_offset
        self.log_event(f"Entering refractory period; raising threshold to {self.threshold} after firing.")


    def update_refractory(self):
        if self.in_refractory:
            self.refractory_counter += 1
            if self.refractory_counter >= self.refractory_events:
                old_threshold = self.threshold
                self.threshold = self.baseline_threshold
                self.in_refractory = False
                self.log_event(f"My refractory period has ended, returning threshold from {old_threshold} to baseline {self.baseline_threshold}.")

# --- Sample Usage & Log Output ---
if __name__ == "__main__":
    neuron = Neuron(threshold=1.0)
    neuron.receive_input(0.3, source="stimulusA")
    neuron.receive_input(0.8, source="stimulusB")
    neuron.receive_input(0.5, source="stimulusC")
    neuron.sleep()
    neuron.receive_input(1.2, source="stimulusD")
    neuron.wake()
    neuron.receive_input(1.2, source="stimulusE")
    neuron.notify_pattern("Frequent firing after stimulusE")
    # Print organized Markdown log
    print(neuron.markdown_log())
