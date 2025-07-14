# config.py
# Centralized configuration for neuron simulation system

DEFAULT_THRESHOLD = 1.0  # Default neuron firing threshold
DEFAULT_REFRACTORY_OFFSET = 0.5  # Default refractory period offset
DEFAULT_REFRACTORY_EVENTS = 3  # Default refractory event count
DEFAULT_DECAY_FACTOR = 0.9  # Default membrane potential decay factor
DEFAULT_PASSIVE_DECAY_LOG_THRESHOLD = 0.01  # Minimum change to log passive decay
DEFAULT_WEIGHTS = [1.0]  # Default input weights
DEFAULT_TRUST_SCORE = 0.5  # Initial trust score for PatternWatcher
TRUST_INCREMENT = 0.05  # Trust score increase step
TRUST_DECREMENT = 0.05  # Trust score decrease step
TRUST_DEBATE_DECREMENT = 0.01  # Trust score decrease for debate
TRUST_CHALLENGE_THRESHOLD = 0.3  # Trust threshold for challenge
TRUST_ADOPT_THRESHOLD = 0.8  # Trust threshold for adoption
ADOPTION_THRESHOLD = 3  # Number of encounters before independent recognition
MENTORING_TRUST_BOOST = 0.1  # Trust boost for mentoring
PATTERNWATCHER_CONFIDENCE_STEP = 0.2  # Confidence step for PatternWatcher adaptation
