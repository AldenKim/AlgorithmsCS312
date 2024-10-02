import argparse
import numpy as np
from time import time

from generate import generate_random_points
from convex_hull import compute_hull
from plotting import plot_points, draw_hull, title, show_plot, draw_line


def main(n: int, distribution: str, seed: int | None):

    points = generate_random_points(distribution, n, seed)
    plot_points(points)

    """seconds = [(10.0, 0.0), (100.0, 0.0014), (1000.0, 0.01694), (10000.0, 0.13128), (100000.0, 1.2253399999999999)
               , (500000.0, 6.708499999999999), (1000000.0, 13.96312)]
    n_values = [point[0] for point in seconds]
    t_values = [point[1] for point in seconds]

    def helper(nVal, kVal):
        nVal = np.array(nVal)
        return kVal*(nVal * np.log(nVal))

    best_k = 0.00000101

    plt.figure()
    print("k val " + str(best_k))
    plt.plot(n_values, t_values, marker='o', linestyle='-')
    plt.plot(n_values, helper(n_values, best_k), marker = 'x', linestyle='--', label=f'Fitted O(n log n), k={best_k:.5f}')

    plt.xscale('log')

    plt.xlabel('n ')
    plt.ylabel('Time (seconds)')

    plt.title('Analysis')

    plt.show(block = True)"""

    """helper = 0
    for i in range(5):
        start = time()
        hull_points = compute_hull(points)
        end = time()
        print (str(i+1) + ". " + str(round(end - start, 4)) + " seconds")
        helper += round(end - start, 4)

    print("Average: " + str(helper / 5) + " seconds")"""

    start = time()
    hull_points = compute_hull(points)
    end = time()

    draw_hull(hull_points)
    title(f'{n} {distribution} points: {round(end - start, 4)} seconds')
    show_plot(block = True)


if __name__ == '__main__':

    # To debug or run in your IDE
    # you can uncomment the lines below and modify the arguments as needed
    import sys
    sys.argv = ['main.py', '-n', '1000000', '--seed', '312', '--debug']

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='The number of points to generate', default=10)
    parser.add_argument('-d', '--dist', '--distribution',
                        help='The distribution from which to generate points',
                        default='uniform'
                        )
    parser.add_argument('--seed', type=int, default=None, help="Random seed")
    parser.add_argument('--debug', action='store_true', help='Turn on debug plotting')
    args = parser.parse_args()

    if args.debug:
        # To debug your algorithm with incremental plotting:
        # - run this script with --debug (e.g. add '--debug' to the sys.argv above)
        # - set breakpoints
        # As you step through your code, you will see the plot update as you go
        import matplotlib.pyplot as plt
        plt.switch_backend('Qt5Agg')
        plt.ion()

    main(args.n, args.dist, args.seed)
