experiment-2-neuron-narration/
│
├── src/
│   ├── neuron.py            # Neuron class (event-driven, lightweight, narrative logging)
│   ├── dispatcher.py        # Event loop / callback system
│   ├── cluster.py           # Cluster and higher-order controller logic
│   ├── pattern_watcher.py   # Persistent PatternWatcher class
│   ├── utils.py             # Logging, serialization, helpers
│   └── main.py              # Experiment runner, entrypoint
│
├── logs/
│   ├── experiment1/         # Log files (organized by experiment/run)
│   ├── experiment2/
│   └── ...
│
├── patterns/
│   └── pattern_db.json      # Persistent pattern database (across experiments)
│
├── docs/
│   ├── PROJECT_OVERVIEW.md  # Essence & principles (see above)
│   ├── EXPERIMENT_TEMPLATE.md # Experiment log template (see below)
│   └── README.md            # Quickstart, setup, architecture summary
│
└── requirements.txt         # Dependencies