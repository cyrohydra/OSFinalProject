# OS Algorithms Lab Suite

Simulation suite for CPU scheduling, memory allocation, page replacement, disk scheduling,
synchronization, and Banker's algorithm. Course: Operating Systems (WCSU).

## Setup
```
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```
python cli.py --help
python cli.py disk --requests 98 183 37 122 14 124 65 67 --head 53 --plot disk.png
streamlit run oslab/ui/app.py
python -m pytest
```

## Layout
```
cli.py                 single entry point; each module registers its own subcommand
oslab/
  common/              shared data classes and result format
  scheduling/ memory/ paging/ disk/ sync/ banker/
                       one package per area; cli.py = register(sub) hook, rest = algorithms (no printing in algorithms)
  ui/app.py            Streamlit visualizations
data/                  sample workloads (one folder per module)
tests/                 pytest, one file per module
experiments/           scripts that regenerate every report figure
report/                write-up
```

## Adding a module's CLI
Edit `oslab/<module>/cli.py`: add arguments in `register(sub)` and implement `run(args)`.
See `oslab/disk/cli.py` for a finished example.
