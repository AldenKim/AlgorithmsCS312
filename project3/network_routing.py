from priorityqueues import LinearPQ, HeapPQ
from math import inf as INF

def find_shortest_path_with_heap(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    dist = []
    prev = []
    for i in range(len(graph)):
        dist.append(INF)
        prev.append(None)
    dist[source] = 0

    H = HeapPQ(dist)

    return iterate_through(H, dist, prev, graph, target)

def find_shortest_path_with_array(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    dist = []
    prev = []
    for i in range(len(graph)):
        dist.append(INF)
        prev.append(None)
    dist[source] = 0

    H = LinearPQ(dist)

    return iterate_through(H, dist, prev, graph, target)

def iterate_through(H, dist, prev, graph, target):
    while not H.is_empty():
        u = H.pop_min()

        if u == target:
            break
        for edge in graph[u]:
            if dist[edge] > (dist[u] + graph[u][edge]):
                dist[edge] = dist[u] + graph[u][edge]
                prev[edge] = u
                H.update_priority(edge, dist[edge])

    ans = []
    helper = target
    while helper is not None:
        ans.append(helper)
        helper = prev[helper]

    return ans[::-1], dist[target]
