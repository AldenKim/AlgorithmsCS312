import math
import random
import heapq

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
            if total_cost == math.inf:
                continue
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
        path = stack.pop(-1)

        #expand
        set_path = set(path)
        for next_city in range(len(edges)):
            if next_city in set_path:
                continue

            new_path = path + [next_city]

            if len(new_path) == len(edges):
                #print(new_path)
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

    initial_solution = greedy_tour(edges, timer)
    if not initial_solution:
        return [SolutionStats(
            [], math.inf, timer.time(), 1, 0, 0, 0, 0
        )]

    best_score = initial_solution[-1].score
    best_solution = initial_solution[-1].tour
    stats.append(initial_solution[-1])

    initial_reduced, initial_lower = initialize_reduced_cost_matrix({}, edges)

    stack = [(initial_lower, [0], initial_reduced)]

    while stack:
        if timer.time_out():
            return stats

        low_bound, P, reduced_cost_matrix = stack.pop()

        if low_bound > best_score:
            n_nodes_pruned+=1
            continue

        if len(P) == len(edges):
            n_nodes_expanded += 1

            tour_cost = score_tour(P, edges)

            if tour_cost < best_score:
                best_score = tour_cost
                best_solution = P

                stats.append(SolutionStats(
                    tour=best_solution,
                    score=best_score,
                    time=timer.time(),
                    max_queue_size=len(stack),
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()))
            continue

        set_path = set(P)
        for next_city in range(len(edges)):
            if next_city not in set_path:
                new_path = P + [next_city]

                #check to see if this new path is infinity
                if edges[P[-1]][next_city] == math.inf:
                    n_nodes_pruned += 1
                    continue

                updated_matrix, new_bound = lower_bound(new_path, edges, reduced_cost_matrix, low_bound, P)

                if new_bound < best_score:
                    stack.append((new_bound, new_path, updated_matrix))
                else:
                    n_nodes_pruned += 1
                    cut_tree.cut(P + [next_city])
                    continue

        #print(pq)
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


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    initial_solution = greedy_tour(edges, timer)
    if not initial_solution:
        return [SolutionStats(
            [], math.inf, timer.time(), 1, 0, 0, 0, 0
        )]

    best_score = initial_solution[-1].score
    best_solution = initial_solution[-1].tour

    initial_reduced, initial_lower = initialize_reduced_cost_matrix({}, edges)

    pq = []
    heapq.heappush(pq, (-1, initial_lower, [0], initial_reduced))

    while pq:
        if timer.time_out():
            return stats

        _, low_bound, P, reduced_cost_matrix = heapq.heappop(pq)

        if low_bound > best_score:
            n_nodes_pruned += 1
            continue

        if len(P) == len(edges):
            n_nodes_expanded += 1

            tour_cost = score_tour(P, edges)

            if tour_cost < best_score:
                best_score = tour_cost
                best_solution = P

                stats.append(SolutionStats(
                    tour=best_solution,
                    score=best_score,
                    time=timer.time(),
                    max_queue_size=len(pq),
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()))
            continue

        set_path = set(P)
        for next_city in range(len(edges)):
            if next_city not in set_path:
                new_path = P + [next_city]

                # check to see if this new path is infinity
                if edges[P[-1]][next_city] == math.inf:
                    n_nodes_pruned += 1
                    continue

                updated_matrix, new_bound = lower_bound(new_path, edges, reduced_cost_matrix, low_bound, P)

                if new_bound < best_score:
                    heapq.heappush(pq, (-len(new_path), new_bound, new_path, updated_matrix))
                else:
                    n_nodes_pruned += 1
                    cut_tree.cut(P + [next_city])
                    continue

        # print(pq)
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

#REDUCES ROWS
def reduce_rows(reduced_cost_matrix: dict, len1: int, len2: int):
    curr_lower_bound = 0
    for i in range(len1):
        minimum_value = math.inf
        for j in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) < minimum_value:
                minimum_value = reduced_cost_matrix[(i, j)]

        if minimum_value == 0:
            continue
        for j in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) != math.inf:
                reduced_cost_matrix[(i, j)] -= minimum_value

        curr_lower_bound += minimum_value

    return reduced_cost_matrix, curr_lower_bound

#REDUCES COLUMNS
def reduce_col (reduced_cost_matrix: dict, len1: int, len2: int):
    curr_lower_bound = 0
    for j in range(len1):
        minimum_value = math.inf
        for i in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) < minimum_value:
                minimum_value = reduced_cost_matrix[(i, j)]

        if minimum_value == 0:
            continue
        for i in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) != math.inf:
                reduced_cost_matrix[(i, j)] -= minimum_value

        curr_lower_bound += minimum_value

    return reduced_cost_matrix, curr_lower_bound

#INTIALIZES THE FIRST REDUCES_COST_MATRIX
def initialize_reduced_cost_matrix(reduced_cost_matrix, edges):
    #adding items to the matrix
    for i in range(len(edges)):
        for j in range(len(edges[i])):
            if edges[i][j] < math.inf:
                reduced_cost_matrix[(i,j)] = edges[i][j]
            if i == j:
                reduced_cost_matrix[(i, j)] = math.inf

    #lowering the rows
    reduced_cost_matrix, curr_lower_bound = reduce_rows(reduced_cost_matrix, len(edges), len(edges[0]))

    #lower the cols
    reduced_cost_matrix, temp = reduce_col(reduced_cost_matrix, len(edges[0]), len(edges))

    return reduced_cost_matrix, curr_lower_bound + temp

#Finds lower bound
def lower_bound(p_i, edges, reduced_cost_matrix, prev_bound, path):
    n = len(edges)

    #partial_cost = sum(edges[p_i[i - 1]][p_i[i]] for i in range(1, len(p_i)))

    ##probably slowing down here
    x, y = p_i[-2], p_i[-1]
    remaining_path_cost = reduced_cost_matrix.get((x,y), math.inf)

    updated = reduced_cost_matrix.copy()

    for i in range(n):
        updated.pop((x, i), None)
        updated.pop((i, y), None)

    updated.pop((x,y), None)
    updated.pop((y, x), None)

    updated, curr_lower_bound = reduce_rows_lower(updated, n, n, set(path))
    updated, temp2 = reduce_col_low(updated, n, n,set(p_i[1:]))
    ##UPDATING MATRIX

    return updated, prev_bound + (curr_lower_bound + temp2) + remaining_path_cost

def reduce_rows_lower(reduced_cost_matrix: dict, len1: int, len2: int, p):
    curr_lower_bound = 0
    for i in range(len1):
        if i in p:
            continue
        minimum_value = math.inf
        for j in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) < minimum_value:
                minimum_value = reduced_cost_matrix[(i, j)]

        if minimum_value == 0:
            continue
        for j in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) != math.inf:
                reduced_cost_matrix[(i, j)] -= minimum_value

        curr_lower_bound += minimum_value

    return reduced_cost_matrix, curr_lower_bound

def reduce_col_low(reduced_cost_matrix: dict, len1: int, len2: int, p):
    curr_lower_bound = 0
    for j in range(len1):
        if j in p:
            continue
        minimum_value = math.inf
        for i in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) < minimum_value:
                minimum_value = reduced_cost_matrix[(i, j)]

        if minimum_value == 0:
            continue
        for i in range(len2):
            if reduced_cost_matrix.get((i, j), math.inf) != math.inf:
                reduced_cost_matrix[(i, j)] -= minimum_value

        curr_lower_bound += minimum_value

    return reduced_cost_matrix, curr_lower_bound

