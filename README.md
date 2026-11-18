# OSFinalProject# OS Algorithms Lab Suite

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
