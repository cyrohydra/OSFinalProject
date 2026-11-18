"""CLI hook for the paging module (called from the top-level cli.py)."""


def register(sub):
    p = sub.add_parser("paging", help="Page replacement: FIFO, LRU, OPT")
    # TODO: add this module's arguments here, e.g. p.add_argument("--algo", ...)
    p.set_defaults(func=run)


def run(args):
    raise SystemExit("paging: not implemented yet")
