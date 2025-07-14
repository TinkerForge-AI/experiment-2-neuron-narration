# Sparse, Hierarchical Neuron Simulation System

## Essence & Principles

This project models a brain-inspired, event-driven, narrative, and hierarchical neuron system in Python. Neurons are lightweight, only compute on events, and log all activity in human-readable Markdown. Clusters emerge naturally from correlated neuron activity, and a persistent PatternWatcher detects and logs recurring patterns. The system is modular, scalable, and designed for research and explainability.

- **Sparse & Event-Driven:** Neurons act only on relevant events.
- **Narrative & Explainable:** All actions are logged in readable sentences.
- **Hierarchical & Emergent:** Clusters form from co-firing neurons.
- **Lightweight & Scalable:** Minimal state per neuron.
- **Pattern-Driven:** Persistent pattern detection and logging.
- **Locally Adaptive:** Neurons adjust thresholds/rules autonomously.
- **Parallel by Design:** Uses asyncio and multiprocessing.
- **Minimized Global Communication:** Most communication is local.

## Architecture

- `src/neuron.py`: Neuron class
- `src/dispatcher.py`: Event loop
- `src/cluster.py`: Cluster logic
- `src/pattern_watcher.py`: PatternWatcher
- `src/utils.py`: Logging, helpers
- `src/main.py`: Experiment runner

## Usage

Run `main.py` to simulate neuron firing, cluster emergence, and pattern detection. Logs are saved in Markdown format for review.
