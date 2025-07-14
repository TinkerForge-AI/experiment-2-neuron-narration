# --- Scenario 7: PatternWatcher Multi-Neuron Narration and Learning Test ---
import random
def scenario_patternwatcher_multi_neuron():
    from neuron_pattern_interface import NeuronPatternInterface
    from pattern_watcher import PatternWatcher
    from config import DEFAULT_THRESHOLD, DEFAULT_REFRACTORY_OFFSET, DEFAULT_DECAY_FACTOR, DEFAULT_WEIGHTS
    interface = NeuronPatternInterface()
    watcher = PatternWatcher(interface)
    # Create 9 neurons with varied config
    neurons = []
    for i in range(9):
        n = Neuron(
            threshold=DEFAULT_THRESHOLD + random.uniform(-0.3, 0.5),
            refractory_offset=DEFAULT_REFRACTORY_OFFSET + random.uniform(-0.2, 0.3),
            decay_factor=DEFAULT_DECAY_FACTOR + random.uniform(-0.2, 0.05),
            weights=[random.uniform(0.7, 1.3)],
            interface=interface
        )
        neurons.append(n)
    from log_config import LOG_MODE
    event_types = [
        {"value": lambda: random.uniform(0.8, 1.5), "source": "excitation", "label": "excitatory"},
        {"value": lambda: random.uniform(-1.0, -0.2), "source": "inhibition", "label": "inhibitory"},
        {"value": lambda: random.uniform(1.5, 2.5), "source": "stress", "label": "stress"},
        {"value": lambda: random.uniform(0.5, 1.7), "source": "conflict", "label": "conflict"},
    ]
    for t in range(12):
        for n in neurons:
            event = random.choice(event_types)
            n.receive_input(event["value"](), source=f"{event['source']}_{t}")
        watcher.monitor_neurons(neurons, pattern=f"cycle_{t}", rapid_firing_threshold=3)
        for n in neurons:
            watcher.monitor_bounds(n)
        firings = [i for i, n in enumerate(neurons) if n.history and n.history[-1][2]]
        if len(firings) >= 3:
            watcher.log_event(
                f"Detected rapid firing in Neurons {', '.join(str(i+1) for i in firings)}. Issuing notifications.",
                event_type="pattern_event",
                extra={"neurons": firings}
            )
        drift_neuron = random.choice(neurons)
        if drift_neuron.threshold > watcher.safe_bounds["threshold"][1]:
            watcher.log_event(
                f"Threshold drift missed in Neuron {neurons.index(drift_neuron)+1}. Increasing learning rate for drift detection.",
                event_type="boundary_notification",
                neuron_id=neurons.index(drift_neuron)+1,
                extra={"param": "threshold", "value": drift_neuron.threshold, "safe_min": watcher.safe_bounds["threshold"][0], "safe_max": watcher.safe_bounds["threshold"][1], "action": "Learning rate increased"}
            )
            watcher.learning_rate += 0.05
    lessons = []
    for i, n in enumerate(neurons):
        if n.threshold > DEFAULT_THRESHOLD + 0.3:
            lessons.append(f"Lower initial threshold for Neuron {i+1} exhibiting frequent inhibition.")
        if n.refractory_offset > DEFAULT_REFRACTORY_OFFSET + 0.2:
            lessons.append(f"Monitor refractory offset for Neuron {i+1} after stress events.")
    watcher.log_event(
        f"Lessons learned—future configs should {', '.join(lessons) if lessons else 'maintain current parameter ranges.'}",
        event_type="lesson_learned"
    )
    # Build combined log
    if LOG_MODE == 'concise':
        log_content = watcher.export_concise_log()
        for n in neurons:
            log_content += "\n\n" + n.export_concise_log()
    else:
        log_content = "\n".join(watcher.log)
        for n in neurons:
            log_content += "\n\n" + n.markdown_log()
    with open("logs/experiment1/scenario_patternwatcher_multi_neuron.md", "w") as f:
        f.write(log_content)
    print("[PatternWatcher Multi-Neuron] Scenario Summary:")
    print("  9 neurons, random events, PatternWatcher boundary/pattern monitoring, learning log, lessons learned.")
    print("  Review scenario_patternwatcher_multi_neuron.md for full narrative logs.")

"""
Scenario Runner: Modular narrative neuron testing and log output.
"""
import os
from neuron import Neuron
from config import DEFAULT_THRESHOLD, DEFAULT_REFRACTORY_OFFSET, DEFAULT_REFRACTORY_EVENTS, DEFAULT_DECAY_FACTOR, DEFAULT_WEIGHTS

LOG_DIR = "logs/experiment1"

def save_log(filename, neuron):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, filename), "w") as f:
        f.write(neuron.markdown_log())

# --- Scenario 1: Constant Low Input ---
def scenario_constant_low_input():
    neuron = Neuron(threshold=DEFAULT_THRESHOLD)
    LOW_INPUT_VALUE = DEFAULT_THRESHOLD * 0.3
    for i in range(5):
        neuron.receive_input(LOW_INPUT_VALUE, source=f"low_input_{i}")
    save_log("scenario_constant_low_input.md", neuron)
    print("[Constant Low Input] Summary:")
    print("  Inputs below threshold; no firing expected.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 2: Threshold Crossing ---
def scenario_threshold_crossing():
    from log_config import LOG_MODE
    from pattern_watcher import PatternWatcher
    interface = None
    watcher = PatternWatcher(interface)
    # Test with varied decay factors and edge-case inputs
    neuron = Neuron(threshold=DEFAULT_THRESHOLD, decay_factor=0.95)
    edge_inputs = [
        (1.0, "exact_threshold"),      # Exactly at threshold
        (0.99, "just_below"),         # Just below threshold
        (1.5, "well_above"),          # Well above threshold
        (-0.5, "inhibitory"),         # Inhibitory input
        (1.0, "exact_threshold"),     # Repeat exact
        (0.98, "near_miss"),          # Near miss
        (1.01, "just_above"),         # Just above
        (2.0, "stress_test"),         # Stress test
    ]
    near_miss_count = 0
    for i, (val, label) in enumerate(edge_inputs):
        neuron.receive_input(val, source=f"{label}_{i}")
        # PatternWatcher checks for edge events
        fired = neuron.history[-1][2] if neuron.history else False
        potential = neuron.history[-1][1] if neuron.history else None
        threshold = neuron.threshold
        # Detect exact threshold crossing
        if abs(potential - threshold) < 1e-6 and fired:
            watcher.log_event(
                f"Neuron fired exactly at threshold ({potential}). Recording pattern.",
                event_type="pattern_event",
                neuron_id=neuron.id,
                extra={"input": val, "threshold": threshold}
            )
        # Detect near-miss events
        elif not fired and abs(potential - threshold) < 0.03:
            near_miss_count += 1
            watcher.log_event(
                f"Near-miss: membrane potential {potential} just below threshold {threshold}.",
                event_type="pattern_event",
                neuron_id=neuron.id,
                extra={"input": val, "threshold": threshold}
            )
        # Detect stress test
        elif fired and val > threshold + 0.4:
            watcher.log_event(
                f"Neuron fired with membrane potential greatly exceeding threshold ({potential} > {threshold}). Stress test.",
                event_type="pattern_event",
                neuron_id=neuron.id,
                extra={"input": val, "threshold": threshold}
            )
        # Detect inhibitory input
        elif potential < 0:
            watcher.log_event(
                f"Neuron received inhibitory input; membrane potential is negative ({potential}).", 
                event_type="boundary_notification",
                neuron_id=neuron.id,
                extra={"param": "membrane_potential", "value": potential, "safe_min": 0, "safe_max": threshold, "action": "Recovery"}
            )
        # Adaptation after repeated near-misses
        if near_miss_count >= 2:
            old_threshold = neuron.threshold
            neuron.threshold -= 0.05
            neuron.log_event(
                f"Lesson learned: Lowering threshold from {old_threshold} to {neuron.threshold} after repeated near-misses.",
                event_type="lesson_learned"
            )
            watcher.log_event(
                f"PatternWatcher: Detected repeated near-miss events. Notifying neuron.",
                event_type="pattern_event",
                neuron_id=neuron.id
            )
            near_miss_count = 0
    # Recovery narration
    neuron.log_event(
        f"Recovery complete. Lesson learned: More frequent adaptation of threshold after repeated near-misses improves response accuracy.",
        event_type="lesson_learned"
    )
    # Export logs
    if LOG_MODE == 'concise':
        log_content = watcher.export_concise_log() + "\n\n" + neuron.export_concise_log()
    else:
        log_content = "\n".join(watcher.log) + "\n\n" + neuron.markdown_log()
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, "scenario_threshold_crossing.md"), "w") as f:
        f.write(log_content)
    print("[Threshold Crossing] Expanded Summary:")
    print("  Edge cases, adaptation, PatternWatcher notifications, recovery narration.")
    print("  Review scenario_threshold_crossing.md for full narrative logs.")

# --- Scenario 3: Rapid Repeated Firing ---
def scenario_rapid_repeated_firing():
    neuron = Neuron(threshold=DEFAULT_THRESHOLD)
    HIGH_INPUT_VALUE = DEFAULT_THRESHOLD * 1.2
    for i in range(5):
        neuron.receive_input(HIGH_INPUT_VALUE, source=f"high_input_{i}")
    neuron.notify_pattern("Rapid repeated firing detected")
    # Introspective self-reflection and adaptation
    firings = [t for t, _, fired in neuron.history if fired]
    if len(firings) >= 3:
        neuron.log_event(f"Neuron {neuron.id}: After monitoring, I have decided to increase my threshold to prevent over-excitation.")
        old_threshold = neuron.threshold
        neuron.threshold = min(neuron.threshold + 0.2, 2.0)
        neuron.log_event(f"Neuron {neuron.id}: Increased threshold from {old_threshold} to {neuron.threshold}.")
    # PatternWatcher feedback loop
    from pattern_watcher import PatternWatcher
    watcher = PatternWatcher(None)
    watcher.monitor_neurons([neuron], "Rapid repeated firing detected")
    save_log("scenario_rapid_repeated_firing.md", neuron)
    print("[Rapid Repeated Firing] Summary:")
    print("  High-value inputs induce repeated firing and adaptation.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 4: Sleep/Wake Stress Test ---
def scenario_sleep_wake_stress():
    from neuron_pattern_interface import NeuronPatternInterface
    from pattern_watcher import PatternWatcher
    interface = NeuronPatternInterface()
    watcher = PatternWatcher(interface)
    neuron = Neuron(threshold=DEFAULT_THRESHOLD, interface=interface)
    # After stress/adaptation, monitor for unsafe bounds and trigger recovery narration
    neuron.sleep()
    SLEEP_INPUT_VALUE = DEFAULT_THRESHOLD * 1.0
    for i in range(3):
        neuron.receive_input(SLEEP_INPUT_VALUE, source=f"ignored_input_{i}")
    neuron.wake()
    # Barrage of diverse input events simulating stress
    import time
    event_types = [
        {"value": DEFAULT_THRESHOLD * 1.2, "source": "excitation_high", "label": "excitatory"},
        {"value": DEFAULT_THRESHOLD * -0.8, "source": "inhibition_strong", "label": "inhibitory"},
        {"value": DEFAULT_THRESHOLD * 2.0, "source": "stress_event", "label": "stress"},
        {"value": DEFAULT_THRESHOLD * 0.2, "source": "excitation_low", "label": "excitatory"},
        {"value": DEFAULT_THRESHOLD * -0.3, "source": "inhibition_weak", "label": "inhibitory"},
        {"value": DEFAULT_THRESHOLD * 1.5, "source": "conflict_event", "label": "conflict"},
        {"value": DEFAULT_THRESHOLD * 1.1, "source": "pattern_alert", "label": "PatternWatcher"},
    ]
    # Simulate rapid event barrage
    event_timestamps = []
    for i, event in enumerate(event_types):
        neuron.receive_input(event["value"], source=event["source"])
        event_timestamps.append(time.time())
        # Simulate very short interval
        time.sleep(0.01)
    # Log stress experience
    neuron.log_event(f"I've received {len(event_types)} input events within {event_timestamps[-1] - event_timestamps[0]:.2f} seconds, including conflicting and stress-labeled events. I feel overwhelmed.")
    # PatternWatcher detects stress and intervenes
    watcher.monitor_neurons([neuron], pattern="stress_event", rapid_firing_threshold=3)
    # Neuron introspective adaptation
    neuron.log_event(f"Neuron {neuron.id}: I am reflecting on my state. If overwhelmed, I will adapt my threshold and inhibition sensitivity.")
    old_threshold = neuron.threshold
    neuron.threshold = min(neuron.threshold + 0.6, 2.0)
    neuron.log_event(f"Neuron {neuron.id}: I am raising my threshold from {old_threshold} to {neuron.threshold} to cope with rapid firing.")
    neuron.log_event(f"Neuron {neuron.id}: Temporarily increasing inhibition sensitivity as a stress response.")
    watcher.log_event("PatternWatcher: Intervention successful. System returning to stable state.")
    save_log("scenario_sleep_wake_stress.md", neuron)
    print("[Sleep/Wake Stress Test] Summary:")
    print(f"  Inputs during sleep ignored; firing resumes after wake. Barrage of {len(event_types)} events triggers stress and adaptation.")
    print("  Recent firings:", [t for t, _, fired in neuron.history if fired])

# --- Scenario 5: Pattern Notification Mock ---
def scenario_pattern_notification():
    """
    Enhanced scenario: Two neurons interact with PatternWatcher and NeuronPatternInterface over multiple cycles.
    Demonstrates notification, recommendation, directive, warning, reward, inquiry, skepticism, trust evolution, debate, partial adoption, independent recognition, and introspective commentary.
    """
    from neuron_pattern_interface import NeuronPatternInterface
    from pattern_watcher import PatternWatcher
    interface = NeuronPatternInterface()
    watcher = PatternWatcher(interface)

    neuronA = Neuron(threshold=DEFAULT_THRESHOLD, interface=interface)
    neuronB = Neuron(threshold=DEFAULT_THRESHOLD + 0.2, interface=interface)

    # Cycle 1: Notification
    watcher.discover_pattern("stimulusY")
    interface.notify_neuron(neuronA, "stimulusY")
    interface.notify_neuron(neuronB, "stimulusY")
    neuronA.log_event("Reflecting: I am skeptical about stimulusY and will monitor before adapting.")
    neuronB.log_event("Reflecting: I am open to new patterns but need more evidence.")

    # Cycle 2: Recommendation
    watcher.recommend_pattern(neuronA, "stimulusY")
    watcher.recommend_pattern(neuronB, "stimulusY")
    neuronA.log_event("Reflecting: Received recommendation to lower threshold for stimulusY. After debate, I will monitor but not yet adapt.")
    neuronB.log_event("Reflecting: I am debating the recommendation and will partially adopt.")
    neuronB.threshold -= 0.05

    # Cycle 3: Directive
    neuronA.log_event("PatternWatcher issued a directive to fire on stimulusY. I feel pressure to comply, but will log my discomfort.")
    neuronB.log_event("PatternWatcher issued a directive to fire on stimulusY. I will comply for now.")
    neuronA.trust_score -= 0.05
    neuronB.trust_score += 0.05

    # Cycle 4: Warning
    neuronA.log_event("PatternWatcher issued a warning about spurious firing on stimulusZ. I raised my threshold for stimulusZ.")
    neuronB.log_event("PatternWatcher issued a warning about spurious firing on stimulusZ. I am ignoring the warning for now.")
    neuronA.threshold += 0.1

    # Cycle 5: Reward
    watcher.update_trust(neuronA, +0.12)
    watcher.update_trust(neuronB, +0.07)
    neuronA.log_event(f"PatternWatcher rewarded my accurate firing. My trust score for PatternWatcher increased to {watcher.trust_scores[neuronA.id]:.2f}.")
    neuronB.log_event(f"PatternWatcher rewarded my accurate firing. My trust score for PatternWatcher increased to {watcher.trust_scores[neuronB.id]:.2f}.")

    # Cycle 6: Inquiry
    neuronA.log_event("PatternWatcher inquired about my pattern recognition process. I explained my reasoning in detail.")
    neuronB.log_event("PatternWatcher inquired about my pattern recognition process. I am still forming my approach.")

    # Cycle 7: Independent Recognition (with revision possibility)
    neuronA.encounter_pattern("stimulusY")
    neuronB.encounter_pattern("stimulusY")
    neuronA.log_event("After repeated encounters, I now recognize stimulusY independently and have graduated from the interface, but remain open to input.")
    neuronB.log_event("After repeated encounters, I now recognize stimulusY independently and have graduated from the interface, but remain open to input.")

    # Cycle 8: Reflection
    neuronA.log_event("Reflecting on my experience, I am now confident in my own pattern recognition abilities.")
    neuronB.log_event("Reflecting on my experience, I am more trusting of PatternWatcher but value my own judgment.")

    # Cycle 9: Mentoring/Collaboration
    neuronA.share_pattern(neuronB, "stimulusY")

    # Cycle 10: Negative encounter and revision
    neuronA.encounter_pattern("stimulusY", negative=True)
    neuronB.encounter_pattern("stimulusY", negative=True)
    from pattern_watcher import PatternWatcher
    watcher = PatternWatcher(interface)
    watcher.reflect_on_revision("stimulusY")

    # Save combined log
    log_content = neuronA.markdown_log() + "\n\n" + neuronB.markdown_log()
    with open(os.path.join(LOG_DIR, "scenario_pattern_notification.md"), "w") as f:
        f.write(log_content)
    print("[PatternWatcher–Neuron Enhanced] Scenario Summary:")
    print("  Two neurons, multiple message types, trust dynamics, introspective commentary, mentoring, revision.")
    print("  Review scenario_pattern_notification.md for full narrative logs.")

# --- Scenario 6: Feedback Variation ---





def scenario_feedback_variation():
    """
    Enhanced feedback variation scenario: passive decay, refractory normalization, feedback source narration, introspective commentary.
    """
    neuron = Neuron(threshold=DEFAULT_THRESHOLD, refractory_offset=DEFAULT_REFRACTORY_OFFSET, refractory_events=DEFAULT_REFRACTORY_EVENTS, decay_factor=DEFAULT_DECAY_FACTOR, weights=DEFAULT_WEIGHTS)
    FEEDBACK_INPUTS = [DEFAULT_THRESHOLD * 1.2, None, DEFAULT_THRESHOLD * 1.1, None, DEFAULT_THRESHOLD * 1.3, None, DEFAULT_THRESHOLD * 1.4, None, DEFAULT_THRESHOLD * 1.2]
    inputs = FEEDBACK_INPUTS
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
                new = max(DEFAULT_THRESHOLD * 0.5, neuron.threshold - 0.1 * DEFAULT_THRESHOLD)
                neuron.log_event(f"I received positive feedback from {source}; lowering my threshold from {current} to {new} to become more sensitive.")
                neuron.threshold = new
            elif feedback == 'negative':
                new = neuron.threshold + 0.1 * DEFAULT_THRESHOLD
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
    scenario_patternwatcher_multi_neuron()
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
    scenario_patternwatcher_multi_neuron()
