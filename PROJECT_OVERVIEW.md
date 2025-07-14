# Experiment 2: Narrated, Sparse, Hierarchical Neuron Simulation

## Project Essence

We aim to build a novel, biologically-inspired neural architecture for AI that is:
- **Sparse & Event-Driven:** Neurons only compute when relevant events occur, saving compute and mimicking real brains.
- **Narrative & Explainable:** Every action, state change, and adaptation is logged in human-readable format, enabling full stack-trace style explanations.
- **Hierarchical & Emergent:** Clusters and higher-order controllers form naturally when groups of neurons repeatedly co-fire, not by manual definition.
- **Lightweight & Scalable:** Neurons maintain minimal state and memory, enabling us to run many more than traditional ML approaches.
- **Pattern-Driven:** A persistent PatternWatcher observes for recurring activity and suggests macros, adaptations, or new clusters.
- **Locally Adaptive:** Each neuron can autonomously adjust its own rules and thresholds based on feedback and performance.
- **Parallel by Design:** The system leverages async and multiprocessing to model brain-like parallelism.

## Key Design Principles

- **Event-Driven Processing:** Only activate neurons on relevant input spikes or signals.
- **Local State & Memory:** Neurons log recent events and firing history, enabling local learning and self-adaptation.
- **Full Narrative Logging:** Every decision, event, and state change is described in human-readable sentences, forming a complete stack-trace.
- **Cluster Emergence:** Clusters are formed based on observed co-firing, not forced by design.
- **PatternWatcher:** Persistent observer for emergent patterns, logging and suggesting system-level adaptations.
- **Minimized Global Communication:** Clusters/modules communicate only for higher-order decisions; most processing is local.
- **Human-Auditable & Organized Logs:** Logging system is organized and may use “folds” to group related events for digestibility.

## Why This Matters

This architecture addresses the limitations of traditional "fat" neural networks:
- Offers deeper insight into neuron-level computation.
- Scales efficiently, with potentially millions of lightweight, narrative-driven neurons.
- Enables unparalleled transparency and auditability in AI systems.

## Next Steps

1. Define project directory structure.
2. Draft experiment documentation template.
3. Prototype Neuron, EventDispatcher, and PatternWatcher classes.
