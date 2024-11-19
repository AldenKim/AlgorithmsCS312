import math
import random

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    for i in range(len(edges)):
        if timer.time_out():
            return stats

        tour = [i]
        visited = set()
        visited.add(i)
        curr = i
        total_cost = 0

        while len(tour) < len(edges):
            next_city = None
            min_cost = math.inf

            for city, cost in enumerate(edges[curr]):
                if city not in visited and cost < min_cost:
                    next_city = city
                    min_cost = cost

            if next_city is None:
                n_nodes_pruned += 1
                cut_tree.cut(tour)
                break

            tour.append(next_city)
            visited.add(next_city)
            total_cost += min_cost
            n_nodes_expanded += 1
            curr = next_city

        if len(tour) == len(edges):
            total_cost += edges[curr][i]
            if not stats or total_cost < stats[-1].score:
                stats.append(SolutionStats(
                    tour = tour,
                    score = total_cost,
                    time = timer.time(),
                    max_queue_size=1,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))

    if stats:
        return stats
    return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]

def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    best_score = math.inf
    best_solution = None

    stack = [[0]]

    while stack:
        if timer.time_out():
            return stats

        #pop
        path = stack.pop()

        #expand
        for next_city in range(len(edges)):
            if next_city in path:
                continue

            new_path = path + [next_city]

            if len(new_path) == len(edges):
                n_nodes_expanded += 1

                tour_cost = score_tour(new_path, edges)

                if tour_cost < best_score:
                    best_score = tour_cost
                    best_solution = new_path
                    stats.append(SolutionStats(
                        tour = best_solution,
                        score = best_score,
                        time = timer.time(),
                        max_queue_size = len(stack),
                        n_nodes_expanded = n_nodes_expanded,
                        n_nodes_pruned = n_nodes_pruned,
                        n_leaves_covered = cut_tree.n_leaves_cut(),
                        fraction_leaves_covered = cut_tree.fraction_leaves_covered()))
                else:
                    stack.append(new_path)
            else:
                stack.append(new_path)

    if best_solution:
        return stats

    return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    best_score = math.inf
    best_solution = None

    stack = [[0]]

    while stack:
        P = stack.pop()



    if stats:
        return stats
    return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
