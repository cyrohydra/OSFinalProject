"""Banker's algorithm: safety check and request granting (deadlock avoidance).

Terms used below:
  available_resources   how many units of each resource type are free right now
  allocation            allocation[p][r] = units of resource r process p holds now
  maximum_demand        maximum_demand[p][r] = most units of r that process p will ever ask for
  remaining_need        maximum_demand - allocation (what a process may still request)
"""

def need_matrix(maximum_demand, allocation):
  """remaining_need[p][r] = maximum_demand[p][r] - allocation[p][r]"""
  return [
        [max_units - held_units for max_units, held_units in zip(max_row, allocation_row)]
        for max_row, allocation_row in zip(maximum_demand, allocation)
    ]

def is_safe(available_resources, allocation, maximum_demand):
    """Check whether every process can finish in some order.

        loop through all processes, checking if they can finish with the current work vector.
        If a process can finish, add its allocation to work and mark it as finished.
        If no process can finish, return 'stuck'.
        process_count is the number of processes, resource_count is the number of resource types.
        available_resources is a list of available resources.
        remaining_need is a matrix of what each process may still request.
        free_resources is a list of currently free resources, which grows as processes finish and release their allocations.
        has_finished is a list of booleans indicating whether each process has finished.
        safe_sequence is a list of process indexes in the order they can finish.
        trace is a list of the state of free_resources after each process finishes.
    """
    process_count = len(allocation)
    resource_count = len(available_resources)
    remaining_need = need_matrix(maximum_demand, allocation)

    free_resources = list(available_resources)   
    # grows as processes finish and release
    has_finished = [False] * process_count
    safe_sequence = []
    trace = []

    made_progress = True
    while made_progress:
        made_progress = False
        for process_index in range(process_count):
            if has_finished[process_index]:
                continue
            can_finish = all(
                remaining_need[process_index][resource_index] <= free_resources[resource_index]
                for resource_index in range(resource_count)
            )
            if can_finish:
                trace.append(
                    f"P{process_index}: need {remaining_need[process_index]} <= "
                    f"free {free_resources}, so it can finish; "
                    f"it then releases {allocation[process_index]}"
                )
                free_resources = [
                    free_resources[resource_index] + allocation[process_index][resource_index]
                    for resource_index in range(resource_count)
                ]
                has_finished[process_index] = True
                safe_sequence.append(process_index)
                made_progress = True

    stuck_processes = [index for index in range(process_count) if not has_finished[index]]
    return {"safe": not stuck_processes, "sequence": safe_sequence, "trace": trace,

            "stuck": stuck_processes, "work": free_resources}


# Banker's Algorithm: request granting 
def request_resources(process_id, requested, available_resources, allocation, maximum_demand):
    """Decide whether process `process_id` may be granted the `requested` units now."""
    resource_count = len(available_resources)
    remaining_need = need_matrix(maximum_demand, allocation)
    summary = {"process": process_id, "request": list(requested)}

    # Rule 1: a process may not ask for more than it declared it would ever need.
    if any(requested[r] > remaining_need[process_id][r] for r in range(resource_count)):
        return {**summary, "granted": False, "reason": "exceeds_need", "safety": None,
                "explanation": f"Denied: P{process_id} asks for {requested} but its remaining need is "
                               f"{remaining_need[process_id]}. It is exceeding its declared maximum."}

    # Rule 2: the units must actually be free right now; otherwise the process waits.
    if any(requested[r] > available_resources[r] for r in range(resource_count)):
        return {**summary, "granted": False, "reason": "not_available", "safety": None,
                "explanation": f"Denied for now: only {available_resources} is available, but "
                               f"P{process_id} asks for {requested}. It must wait."}

    # Rule 3: pretend to grant the request and check if the system is still safe.
    # If it is safe, grant the request; otherwise, deny it.
    available_after_grant = [available_resources[r] - requested[r] for r in range(resource_count)]
    allocation_after_grant = [list(row) for row in allocation]
    allocation_after_grant[process_id] = [
        allocation_after_grant[process_id][r] + requested[r] for r in range(resource_count)
    ]
    safety_check = is_safe(available_after_grant, allocation_after_grant, maximum_demand)

    if safety_check["safe"]:
        safe_order = " -> ".join(f"P{index}" for index in safety_check["sequence"])
        return {**summary, "granted": True, "reason": "safe", "safety": safety_check,
                "new_available": available_after_grant, "new_allocation": allocation_after_grant,
                "explanation": f"Granted: after giving P{process_id} {requested}, the system is still "
                               f"safe. Safe sequence: {safe_order}."}

    
    stuck_names = ", ".join(f"P{index}" for index in safety_check["stuck"])
    return {**summary, "granted": False, "reason": "unsafe", "safety": safety_check,
            "explanation": f"Denied: granting {requested} to P{process_id} would leave only "
                           f"{available_after_grant} available, and no safe order exists "
                           f"({stuck_names} could never finish). That state risks deadlock."}
