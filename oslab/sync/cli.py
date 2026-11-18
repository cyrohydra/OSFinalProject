"""CLI hook for the sync module (called from the top-level cli.py)."""


def register(sub):
    p = sub.add_parser("sync", help="Synchronization: Dining Philosophers / Producer-Consumer")
    # TODO: add this module's arguments here, e.g. p.add_argument("--algo", ...)
    p.set_defaults(func=run)


def run(args):
    raise SystemExit("sync: not implemented yet")
