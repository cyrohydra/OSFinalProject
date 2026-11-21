import json

from oslab.banker.banker import is_safe, request_resources

with open("data/banker/safe_request.json") as data_files: 
    TEXTBOOK_STATE = json.load(data_files)
    AVALABLE = TEXTBOOK_STATE["available"]
    ALLOCATION = TEXTBOOK_STATE["allocation"]
    MAXIMUM_DEMAND = TEXTBOOK_STATE["max"]

def test_initial_state_is_safe_with_textbook_sequence():
    safety_check = is_safe(AVAILABLE, ALLOCATION, MAXIMUM_DEMAND)
    assert safety_check["safe"]
    assert safety_check["sequence"] == [1, 3, 4, 0, 2]


def test_request_granted_and_state_stays_safe():
    decision = request_resources(1, [1, 0, 2], AVAILABLE, ALLOCATION, MAXIMUM_DEMAND)
    assert decision["granted"] and decision["reason"] == "safe"
    state_after_grant = is_safe(decision["new_available"], decision["new_allocation"], MAXIMUM_DEMAND)
    assert state_after_grant["safe"]


def test_request_denied_because_unsafe():
    decision = request_resources(4, [3, 3, 0], AVAILABLE, ALLOCATION, MAXIMUM_DEMAND)
    assert not decision["granted"] and decision["reason"] == "unsafe"
    assert "deadlock" in decision["explanation"]

def test_request_exceeding_need_is_rejected():
    decision = request_resources(1, [9, 0, 0], AVAILABLE, ALLOCATION, MAXIMUM_DEMAND)
    assert decision["reason"] == "exceeds_need"


def test_request_exceeding_available_must_wait():
    decision = request_resources(0, [0, 4, 0], AVAILABLE, ALLOCATION, MAXIMUM_DEMAND)
    assert decision["reason"] == "not_available"


def test_data_files_match_the_two_required_cases():
    for file_name, should_be_granted in (("safe_request.json", True), ("unsafe_request.json", False)):
        with open("data/banker/" + file_name) as data_file:
            case = json.load(data_file)
        request = case["request"]
        decision = request_resources(request["process"], request["amount"], case["available"],
                                     case["allocation"], case["max"])
        assert decision["granted"] is should_be_granted
