import functools
import math

import matplotlib.pyplot as plt
from tsp_core import get_segments, Location, Tour, SolutionStats
from tsp_solve import ReducedPartialPath


def add_axes(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        if 'ax' in kwargs and kwargs['ax'] is None:
            kwargs['ax'] = plt.gca()

        return func(*args, **kwargs)

    return new_func


def _scatter_locations(locations, ax):
    xx, yy = zip(*locations)
    ax.scatter(xx, yy)
    for i, loc in enumerate(locations):
        ax.annotate(str(i), loc, fontsize=16, fontweight='bold')


@add_axes
def plot_network(locations, edges, edge_alpha=0.5, edge_weight_limit=10, ax=None):
    _scatter_locations(locations, ax)

    if edge_alpha > 0:
        for s, loc_s in enumerate(locations):
            for t, loc_t in enumerate(locations):
                if s == t:
                    continue
                if math.isinf(edges[s][t]):
                    continue
                ax.plot(
                    (loc_s[0], loc_t[0]),
                    (loc_s[1], loc_t[1]),
                    alpha=edge_alpha,
                    c='k'
                )
                if len(edges) < edge_weight_limit:
                    mid_x = (loc_s[0] + loc_t[0]) / 2
                    mid_y = (loc_s[1] + loc_t[1]) / 2
                    ax.text(mid_x, mid_y, str(edges[s][t]), c='r')
    return ax


@add_axes
def plot_tour(locations: list[Location], tour: Tour, ax=None):
    segments = get_segments(tour)

    for s, t in segments:
        sx, sy = locations[s]
        tx, ty = locations[t]
        dx = tx - sx
        dy = ty - sy
        ax.arrow(
            sx, sy,
            dx, dy,
            width=0.01,
            alpha=0.8,
            color='g',
            length_includes_head=True
        )


@add_axes
def plot_solutions(solutions: dict[str, list[SolutionStats]], ax=None):
    for name, stats in solutions.items():
        x = [st.time for st in stats]
        y = [st.score for st in stats]
        ax.plot(x, y, marker='o')

    ax.legend(labels=solutions.keys())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Tour Score')


@add_axes
def plot_coverage(solutions: dict[str, list[SolutionStats]], ax=None):
    for name, stats in solutions.items():
        x = [st.time for st in stats]
        y = [st.fraction_leaves_covered for st in stats]
        ax.plot(x, y, marker='o')

    ax.legend(labels=solutions.keys())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Fraction of search space covered')


@add_axes
def plot_queue_size(solutions: dict[str, list[SolutionStats]], ax=None):
    for name, stats in solutions.items():
        x = [st.time for st in stats]
        y = [st.max_queue_size for st in stats]
        ax.plot(x, y, marker='o')

    ax.legend(labels=solutions.keys())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Max Queue Size')


def _get_edge_prob(score: float, edges: list[list[float]]):
    ave_weight_per_node = score / len(edges)
    ave_below = sum(
        sum(
            edge < ave_weight_per_node
            for edge in row
        ) / len(row)
        for row in edges
    ) / len(edges)
    return ave_below


@add_axes
def plot_edge_probability(
        solutions: dict[str, list[SolutionStats]],
        edges: list[list[float]], ax=None
):
    for name, stats in solutions.items():
        x = [st.time for st in stats]
        y = [_get_edge_prob(st.score, edges) for st in stats]
        ax.plot(x, y, marker='o')

    ax.legend(labels=solutions.keys())
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Average fraction of better edges')
    ax.set_ylim([0, ax.get_ylim()[-1]])


@add_axes
def plot_solution_progress(
        solutions: list[list[int]],
        edges: list[list[float]],
        ax=None
):
    for solution in solutions:
        xx = range(len(solution))
        pp = ReducedPartialPath.create_from_edges(edges, solution[0])
        yy = [pp.cost]

        for i in range(1, len(solution)):
            pp = pp._expand_child(solution[i - 1], solution[i])
            yy.append(pp.cost)

        ax.plot(xx, yy, marker='o')
        ax.set_xlabel('Node in solution')
        ax.set_ylabel('Lower bound on partial path')


@add_axes
def plot_solution_progress_compared(
        solutions: dict[str, list[int]],
        edges: list[list[float]],
        ax=None
):
    for name, solution in solutions.items():
        xx = range(len(solution))
        pp = ReducedPartialPath.create_from_edges(edges, solution[0])
        yy = [pp.cost]

        for i in range(1, len(solution)):
            pp = pp._expand_child(solution[i - 1], solution[i])
            yy.append(pp.cost)

        ax.plot(xx, yy, marker='o')
        ax.set_xlabel('Node in solution')
        ax.set_ylabel('Lower bound on partial path')

    ax.legend(labels=solutions.keys())


@add_axes
def plot_solution_evolution(
        solutions: list[list[int]],
        ax: plt.Axes = None
):
    ax.imshow(solutions)
