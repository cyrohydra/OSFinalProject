# Textbook example (Silberschatz): queue 98 183 37 122 14 124 65 67, head 53, 200 cylinders
from oslab.disk.algorithms import fcfs, sstf, scan, cscan, look, clook

Q, H = [98, 183, 37, 122, 14, 124, 65, 67], 53

def test_fcfs():  assert fcfs(Q, H)["total"] == 640
def test_sstf():  assert sstf(Q, H)["total"] == 236
def test_scan_down():  assert scan(Q, H, 200, "down")["total"] == 236
def test_look_down():  assert look(Q, H, 200, "down")["total"] == 208
def test_cscan_up():   assert cscan(Q, H, 200, "up")["total"] == 382
def test_clook_up():   assert clook(Q, H, 200, "up")["total"] == 322
def test_cscan_no_jump_cost():
    assert cscan(Q, H, 200, "up", count_jump=False)["total"] == 183
def test_average():    assert fcfs(Q, H)["average"] == 80.0
def test_empty_queue(): assert fcfs([], H)["total"] == 0
