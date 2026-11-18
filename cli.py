"""OS Algorithms Lab Suite: single entry point.

    python cli.py --help
    python cli.py disk --requests 98 183 37 122 14 124 65 67 --head 53

Each module in oslab/ owns a cli.py with register(sub) that adds its own subcommand.
"""

import argparse

from oslab.scheduling import cli as sched
from oslab.memory import cli as mem
from oslab.paging import cli as page
from oslab.disk import cli as disk
from oslab.sync import cli as sync
from oslab.banker import cli as banker

MODULES = [sched, mem, page, disk, sync, banker]


def main():
    parser = argparse.ArgumentParser(prog="oslab", description="OS Algorithms Lab Suite")
    sub = parser.add_subparsers(dest="command", required=True)
    for m in MODULES:
        m.register(sub)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
