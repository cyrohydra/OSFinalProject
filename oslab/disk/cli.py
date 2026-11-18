"""CLI hook for the disk module (called from the top-level cli.py)."""

from .algorithms import ALGORITHMS, compare


def register(sub):
    p = sub.add_parser("disk", help="Disk scheduling: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK")
    p.add_argument("--requests", type=int, nargs="+", required=True)
    p.add_argument("--head", type=int, required=True)
    p.add_argument("--cylinders", type=int, default=200)
    p.add_argument("--direction", choices=["up", "down"], default="up")
    p.add_argument("--algo", choices=list(ALGORITHMS) + ["all"], default="all")
    p.add_argument("--no-jump-cost", action="store_true",
                   help="don't count the C-SCAN/C-LOOK return jump")
    p.add_argument("--plot", metavar="FILE.png", help="save a head-movement plot")
    p.set_defaults(func=run)


def run(args):
    cj = not args.no_jump_cost
    if args.algo == "all":
        results = compare(args.requests, args.head, args.cylinders, args.direction, cj)
    else:
        results = [ALGORITHMS[args.algo](args.requests, args.head, cylinders=args.cylinders,
                                         direction=args.direction, count_jump=cj)]
    print(f'{"Algorithm":<8} {"Total":>6} {"Avg":>7}   Path')
    for r in results:
        print(f'{r["algorithm"]:<8} {r["total"]:>6} {r["average"]:>7}   '
              + " -> ".join(map(str, r["path"])))
    if args.plot:
        from .plot import plot_head_movement
        print("saved", plot_head_movement(results, args.plot))
