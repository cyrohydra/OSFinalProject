"""CLI hook for the banker module (called from the top-level cli.py)."""


def register(sub):
    p = sub.add_parser("banker", help="Banker's algorithm: safe-state check")
    # TODO: add this module's arguments here, e.g. p.add_argument("--algo", ...)
    p.set_defaults(func=run)


def run(args):
    raise SystemExit("banker: not implemented yet")
