"""CLI hook for the scheduling module (called from the top-level cli.py)."""


def register(sub):
    p = sub.add_parser("scheduling", help="CPU scheduling: FCFS, SJF, Priority, RR, MLFQ")
    # TODO: add this module's arguments here, e.g. p.add_argument("--algo", ...)
    p.set_defaults(func=run)


def run(args):
    raise SystemExit("scheduling: not implemented yet")
