# optimal solution?
# better than greedy?
# greedy, DFS, B&B, smart
from byu_pytest_utils import with_import
from tsp_core import Timer
from math import inf


@with_import('tsp_solve')
def test_greedy(greedy_tour):
    graph = [
        [0, 9, inf, 8, inf],
        [inf, 0, 4, inf, 2],
        [inf, 3, 0, 4, inf],
        [inf, 6, 7, 0, 12],
        [1, inf, inf, 10, 0]
    ]
    timer = Timer(10)
    stats = greedy_tour(graph, timer)
    assert stats[0].tour == [1, 4, 0, 3, 2]
    assert stats[0].score == 21

    assert len(stats) == 1


@with_import('tsp_solve')
def test_dfs(dfs):
    graph = [
        [0, 9, inf, 8, inf],
        [inf, 0, 4, inf, 2],
        [inf, 3, 0, 4, inf],
        [inf, 6, 7, 0, 12],
        [1, inf, inf, 10, 0]
    ]
    timer = Timer(10)
    stats = dfs(graph, timer)
    scores = {
        tuple(stat.tour): stat.score
        for stat in stats
    }
    assert scores[0, 3, 2, 1, 4] == 21
    assert len(scores) == 1


@with_import('tsp_solve')
def test_branch_and_bound():
    ...
