
"""
Scenario Runner: Modular narrative neuron testing and log output.
"""
import os
from neuron import Neuron

LOG_DIR = "logs/experiment1"

def save_log(filename, neuron):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, filename), "w") as f:
        f.write(neuron.markdown_log())

# --- Scenario 1: Constant Low Input ---
def scenario_constant_low_input():
    neuron = Neuron(threshold=1.0)
    for i in range(5):
        neuron.receive_input(0.3, source=f"low_input_{i}")
    save_log("scenario_constant_low_input.md", neuron)
    print("[Constant Low Input] Summary:")
    print("  Inputs below threshold; no firing expected.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 2: Threshold Crossing ---
def scenario_threshold_crossing():
    neuron = Neuron(threshold=1.0)
    inputs = [0.6, 0.5, 1.1, 0.4, 0.7]
    for i, val in enumerate(inputs):
        neuron.receive_input(val, source=f"cross_input_{i}")
    save_log("scenario_threshold_crossing.md", neuron)
    print("[Threshold Crossing] Summary:")
    print("  Inputs alternate below/above threshold; observe firing and adaptation.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 3: Rapid Repeated Firing ---
def scenario_rapid_repeated_firing():
    neuron = Neuron(threshold=1.0)
    for i in range(5):
        neuron.receive_input(1.2, source=f"high_input_{i}")
    neuron.notify_pattern("Rapid repeated firing detected")
    save_log("scenario_rapid_repeated_firing.md", neuron)
    print("[Rapid Repeated Firing] Summary:")
    print("  High-value inputs induce repeated firing and adaptation.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 4: Sleep/Wake Stress Test ---
def scenario_sleep_wake_stress():
    neuron = Neuron(threshold=1.0)
    neuron.sleep()
    for i in range(3):
        neuron.receive_input(1.0, source=f"ignored_input_{i}")
    neuron.wake()
    for i in range(2):
        neuron.receive_input(1.1, source=f"active_input_{i}")
    save_log("scenario_sleep_wake_stress.md", neuron)
    print("[Sleep/Wake Stress Test] Summary:")
    print("  Inputs during sleep ignored; firing resumes after wake.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 5: Pattern Notification Mock ---
def scenario_pattern_notification():
    neuron = Neuron(threshold=1.0)
    neuron.receive_input(0.9, source="pre_pattern")
    neuron.notify_pattern("Recurring pattern: stimulusX")
    neuron.receive_input(1.2, source="post_pattern")
    save_log("scenario_pattern_notification.md", neuron)
    print("[Pattern Notification Mock] Summary:")
    print("  PatternWatcher notification and neuron response.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 6: Feedback Variation ---





def scenario_feedback_variation():
    """
    Enhanced feedback variation scenario: passive decay, refractory normalization, feedback source narration, introspective commentary.
    """
    neuron = Neuron(threshold=1.0, refractory_offset=0.5, refractory_events=2, decay_factor=0.9, weights=[1.0])
    inputs = [1.2, None, 1.1, None, 1.3, None, 1.4, None, 1.2]
    feedback_sequence = [
        ('positive', 'Supervisor'),
        ('negative', 'PatternWatcher'),
        ('positive', 'Supervisor'),
        ('negative', 'PatternWatcher')
    ]
    feedback_idx = 0
    firings = 0
    for i, val in enumerate(inputs):
        # A. Passive Decay Narration
        if val is not None:
            neuron.receive_input(val, source=f"feedback_input_{i}")
        else:
            prev_potential = neuron.potential
            neuron.passive_decay()
            if abs(neuron.potential - prev_potential) > neuron.passive_decay_log_threshold:
                neuron.log_event(f"No input received this cycle; my membrane potential decayed from {prev_potential} to {neuron.potential}.")
        # C. Firing Threshold Fluctuation (Narrate refractory duration)
        if neuron.in_refractory:
            neuron.log_event(f"Waiting for {neuron.refractory_events - neuron.refractory_counter} more cycles before returning to baseline threshold.")
        # Check for refractory normalization
        neuron.update_refractory()
        # B. Feedback Events Frequency
        feedback = None
        source = None
        if neuron.history and neuron.history[-1][2]:
            firings += 1
            current = neuron.threshold
            if feedback_idx < len(feedback_sequence):
                feedback, source = feedback_sequence[feedback_idx]
                feedback_idx += 1
            else:
                feedback, source = ('none', 'Supervisor')
            if feedback == 'positive':
                new = max(0.5, neuron.threshold - 0.1)
                neuron.log_event(f"I received positive feedback from {source}; lowering my threshold from {current} to {new} to become more sensitive.")
                neuron.threshold = new
            elif feedback == 'negative':
                new = neuron.threshold + 0.1
                neuron.log_event(f"I received negative feedback from {source}; raising my threshold from {current} to {new} to avoid spurious firing.")
                neuron.threshold = new
            else:
                neuron.log_event(f"I received neutral feedback from {source}; keeping my threshold at {current}.")
    save_log("scenario_feedback_variation.md", neuron)
    print("[Feedback Variation Enhanced] Scenario Summary:")
    print(f"  Final threshold: {neuron.threshold}")
    print(f"  Number of firings: {firings}")
    print(f"  Adaptation sequence: {feedback_sequence}")

def run_all_scenarios():
    print("Running Neuron Scenario Suite...")
    scenario_constant_low_input()
    scenario_threshold_crossing()
    scenario_rapid_repeated_firing()
    scenario_sleep_wake_stress()
    scenario_pattern_notification()
    scenario_feedback_variation()
    print("All scenarios complete. Review logs in logs/experiment1/.")


def run_all_scenarios():
    print("Running Neuron Scenario Suite...")
    scenario_constant_low_input()
    scenario_threshold_crossing()
    scenario_rapid_repeated_firing()
    scenario_sleep_wake_stress()
    scenario_pattern_notification()
    scenario_feedback_variation()
    print("All scenarios complete. Review logs in logs/experiment1/.")

if __name__ == "__main__":
    run_all_scenarios()
