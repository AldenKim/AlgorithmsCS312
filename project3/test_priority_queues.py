from priorityqueues import ArrayPQ, HeapPQ
from math import inf as INF

def test_pqs():
    items = list(range(10))

    array_pq = ArrayPQ(items)
    for i in range(10):
        array_pq.update_priority(i, INF)

    heap_pq = HeapPQ(items)
    for i in range(10):
        heap_pq.update_priority(i, INF)

    array_pq.update_priority(7, 7)
    heap_pq.update_priority(7, 7)

    assert array_pq.pop_min() == 7
    assert heap_pq.pop_min() == 7

    array_pq.update_priority(3, 3)
    array_pq.update_priority(5, 1)
    heap_pq.update_priority(3, 3)
    heap_pq.update_priority(5, 1)

    assert array_pq.pop_min() == 5
    assert array_pq.pop_min() == 3

    print(heap_pq.heap_tree)
    assert heap_pq.pop_min() == 5
    print(heap_pq.heap_tree)
    assert heap_pq.pop_min() == 3
