"""CLI hook for the memory module (called from the top-level cli.py)."""


def register(sub):
    p = sub.add_parser("memory", help="Memory allocation: First, Best, Worst, Next Fit")
    # TODO: add this module's arguments here, e.g. p.add_argument("--algo", ...)
    p.set_defaults(func=run)


def run(args):
    raise SystemExit("memory: not implemented yet")
