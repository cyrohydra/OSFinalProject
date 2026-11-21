"""CLI hook for the banker module (called from the top-level cli.py)."""

import json
 
from .banker import is_safe, need_matrix, request_resources

def register(subparsers):
    parser = subparsers.add_parser(
        "banker", help="Banker's algorithm: safe-state check and request granting")
    parser.add_argument("--data", required=True,
                        help="JSON with available, allocation, max (and optionally a request)")
    parser.add_argument("--process", type=int,
                        help="index of the process making a request (overrides the file)")
    parser.add_argument("--request", type=int, nargs="+",
                        help="resource request vector (overrides the file)")
    parser.set_defaults(func=run)
def _print_table(title, matrix, resource_labels):
    print(title)
    print("     " + " ".join(f"{label:>3}" for label in resource_labels))
    for process_index, row in enumerate(matrix):
        print(f"P{process_index:<3} " + " ".join(f"{units:>3}" for units in row))


def run(args):
    with open(args.data) as data_file:
        system_state = json.load(data_file)
    available_resources = system_state["available"]
    allocation = system_state["allocation"]
    maximum_demand = system_state["max"]
    resource_labels = [chr(ord("A") + index) for index in range(len(available_resources))]

    _print_table("Allocation", allocation, resource_labels)
    print()
    _print_table("Max", maximum_demand, resource_labels)
    print()
    _print_table("Need (max - allocation)", need_matrix(maximum_demand, allocation), resource_labels)
    print("\nAvailable:", dict(zip(resource_labels, available_resources)))

    safety_check = is_safe(available_resources, allocation, maximum_demand)
    print("\nCurrent state is", "SAFE" if safety_check["safe"] else "UNSAFE")
    for line in safety_check["trace"]:
        print("  " + line)
    if safety_check["safe"]:
        print("  Safe sequence:", " -> ".join(f"P{index}" for index in safety_check["sequence"]))

    # The request comes from the data file unless --process/--request override it.
    request_in_file = system_state.get("request")
    process_id, requested = ((request_in_file["process"], request_in_file["amount"])
                             if request_in_file else (None, None))
    if args.process is not None and args.request:
        process_id, requested = args.process, args.request
    if process_id is not None:
        print(f"\nRequest: P{process_id} asks for {requested}")
        decision = request_resources(process_id, requested, available_resources,
                                     allocation, maximum_demand)
        print(decision["explanation"])
