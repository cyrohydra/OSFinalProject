"""Disk scheduling: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK.

Every algorithm returns a dict (easy to print, plot, or dump to JSON):
    {"algorithm": str, "path": [head positions], "total": int, "average": float}

Used by oslab/disk/cli.py:
    python cli.py disk --requests 98 183 37 122 14 124 65 67 --head 53
"""
import argparse


def _result(name, path, n_requests, jumps=(), count_jump=True):
    """Total head movement. `jumps` = path indexes reached by a return jump
    (C-SCAN / C-LOOK); the jump distance is counted only if count_jump."""
    total = 0
    for i in range(1, len(path)):
        if i in jumps and not count_jump:
            continue
        total += abs(path[i] - path[i - 1])
    avg = total / n_requests if n_requests else 0.0
    return {"algorithm": name, "path": path, "total": total, "average": round(avg, 2)}


def fcfs(requests, head, **_):
    return _result("FCFS", [head] + list(requests), len(requests))


def sstf(requests, head, **_):
    pending, path, cur = list(requests), [head], head
    while pending:
        nxt = min(pending, key=lambda r: abs(r - cur))  # ties: first in queue
        pending.remove(nxt)
        path.append(nxt)
        cur = nxt
    return _result("SSTF", path, len(requests))


def _sweep_up(kind, requests, head, end_cyl):
    """Head moving toward higher cylinders. Returns (path, jump_indexes)."""
    ahead = sorted(r for r in requests if r >= head)
    behind = sorted(r for r in requests if r < head)
    path, jumps = [head] + ahead, set()

    if kind == "scan":      # go to the disk edge, reverse, serve the rest
        if path[-1] != end_cyl:
            path.append(end_cyl)
        path += sorted(behind, reverse=True)
    elif kind == "look":    # go only as far as the last request, reverse
        path += sorted(behind, reverse=True)
    elif kind == "cscan":   # go to the edge, jump to 0, sweep up again
        if path[-1] != end_cyl:
            path.append(end_cyl)
        if behind:
            jumps.add(len(path))
            path.append(0)
            path += [r for r in behind if r != 0]
    elif kind == "clook":   # go to last request, jump to lowest, sweep up
        if behind:
            jumps.add(len(path))
            path += behind
    return path, jumps


def _scan_family(kind, label, requests, head, cylinders, direction, count_jump):
    end = cylinders - 1
    if direction == "up":
        path, jumps = _sweep_up(kind, requests, head, end)
    else:  # mirror the disk, run the "up" version, mirror back
        mirrored = [end - r for r in requests]
        path, jumps = _sweep_up(kind, mirrored, end - head, end)
        path = [end - p for p in path]
    return _result(label, path, len(requests), jumps, count_jump)


def scan(requests, head, cylinders=200, direction="up", count_jump=True):
    return _scan_family("scan", "SCAN", requests, head, cylinders, direction, count_jump)


def cscan(requests, head, cylinders=200, direction="up", count_jump=True):
    return _scan_family("cscan", "C-SCAN", requests, head, cylinders, direction, count_jump)


def look(requests, head, cylinders=200, direction="up", count_jump=True):
    return _scan_family("look", "LOOK", requests, head, cylinders, direction, count_jump)


def clook(requests, head, cylinders=200, direction="up", count_jump=True):
    return _scan_family("clook", "C-LOOK", requests, head, cylinders, direction, count_jump)


ALGORITHMS = {"fcfs": fcfs, "sstf": sstf, "scan": scan,
              "cscan": cscan, "look": look, "clook": clook}


def compare(requests, head, cylinders=200, direction="up", count_jump=True):
    """Run the SAME input through every algorithm (fair comparison)."""
    return [fn(requests, head, cylinders=cylinders, direction=direction,
               count_jump=count_jump) for fn in ALGORITHMS.values()]
