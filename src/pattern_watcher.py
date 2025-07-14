"""
PatternWatcher: Persistent, cumulative pattern detection and logging.
"""
import json
import os
from utils import narrative_log

class PatternWatcher:
    def __init__(self, db_path):
        self.db_path = db_path
        self.patterns = self.load_patterns()
        self.log = []
        narrative_log(self.log, f"PatternWatcher initialized. Loaded {len(self.patterns)} patterns.")

    def load_patterns(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}

    def save_patterns(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.patterns, f, indent=2)
        narrative_log(self.log, f"PatternWatcher saved {len(self.patterns)} patterns.")

    def observe(self, neuron_logs):
        # Simple pattern: count co-firing events
        for log in neuron_logs:
            for entry in log:
                if "fired" in entry:
                    self.patterns.setdefault(entry, 0)
                    self.patterns[entry] += 1
        narrative_log(self.log, f"PatternWatcher observed logs and updated patterns.")
        self.save_patterns()

    def get_log(self):
        return self.log
