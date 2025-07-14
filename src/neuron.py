
"""
Neuron class: Narrative-driven, event-driven, explainable, self-reflective.
"""
import datetime
import uuid



class Neuron:
    def __init__(self, neuron_id=None, threshold=1.0, weights=None, history_length=5, refractory_offset=0.5, refractory_events=3, decay_factor=0.9, passive_decay_log_threshold=0.01):
        self.id = neuron_id or str(uuid.uuid4())
        self.baseline_threshold = threshold
        self.threshold = threshold
        self.refractory_offset = refractory_offset
        self.refractory_events = refractory_events
        self.refractory_counter = 0
        self.in_refractory = False
        self.weights = weights or [1.0]
        self.potential = 0.0
        self.baseline_potential = 0.0
        self.decay_factor = decay_factor
        self.history = []  # List of (timestamp, input, fired)
        self.asleep = False
        self.log = []
        self.history_length = history_length
        self.passive_decay_log_threshold = passive_decay_log_threshold
        self.last_input_received = False
        self.log_event(f"I am born as Neuron {self.id} with baseline threshold {self.baseline_threshold}, refractory offset {self.refractory_offset}, decay factor {self.decay_factor}, and weights {self.weights}.")

    def log_event(self, message):
        timestamp = datetime.datetime.now().isoformat()
        self.log.append(f"- {timestamp}: {message}")

    def markdown_log(self):
        content = "\n".join(self.log)
        return f"<details><summary>Neuron {self.id}</summary>\n{content}\n</details>"



    def receive_input(self, input_value, source=None):
        self.last_input_received = True
        if self.asleep:
            self.log_event("I am currently asleep and will ignore incoming events until activated.")
            return
        self.log_event(f"I've received an input event with value {input_value} from {source}.")
        # Decay membrane potential before adding new input
        old_potential = self.potential
        self.potential = self.potential * self.decay_factor + input_value * self.weights[0]
        self.log_event(f"My membrane potential has decayed from {old_potential} to {self.potential} after receiving input.")
        self.log_event(f"My threshold is currently {self.threshold}.")
        self.decide_to_fire(input_value)
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



    def decide_to_fire(self, input_value):
        if self.potential >= self.threshold:
            self.log_event(f"I decided to fire because my membrane potential ({self.potential}) exceeded my threshold ({self.threshold}).")
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
                self.threshold = max(self.baseline_threshold, self.threshold - 0.05)
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
