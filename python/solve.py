"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from solution import Solution
from file_wrappers import StdinFileWrapper, StdoutFileWrapper
from point import Point


def solve_naive(instance: Instance) -> Solution:
    sols = []
    r = 1
    if instance.grid_side_length == 30:
        for x in range(0, 30, 6):
            for y in range(0, 30, 6):
                point = Point(x, y)
                sols.append(point)
        for x in range(3, 30, 6):
            for y in range(3, 30, 6):
                point = Point(x, y)
                sols.append(point)
        for y in range(0, 30, 3):
            point = Point(29, y)
            sols.append(point)
        for x in range(0, 30, 3):
            point = Point(x, 29)
            sols.append(point)
        sols.append(Point(29,29))
        return Solution(
            instance=instance,
            towers=sols,
        )
    elif instance.grid_side_length == 50:
        for x in range(0, 50, 6):
            for y in range(0, 50, 6):
                point = Point(x, y)
                sols.append(point)
        for x in range(3, 50, 6):
            for y in range(3, 50, 6):
                point = Point(x, y)
                sols.append(point)
        for y in range(0, 50, 6):
            point = Point(49, y)
            sols.append(point)
        for x in range(0, 50, 6):
            point = Point(x, 49)
            sols.append(point)
        sols.append(Point(49,49))
        return Solution(
            instance=instance,
            towers=sols,
        )
    else:
        for x in range(0, 100, 6):
            for y in range(0, 100, 6):
                point = Point(x, y)
                sols.append(point)
        for x in range(3, 100, 6):
            for y in range(3, 100, 6):
                point = Point(x, y)
                sols.append(point)
        return Solution(
            instance=instance,
            towers=sols,
        )


SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive
}


# You shouldn't need to modify anything below this line.
def infile(args):
    if args.input == "-":
        return StdinFileWrapper()

    return Path(args.input).open("r")


def outfile(args):
    if args.output == "-":
        return StdoutFileWrapper()

    return Path(args.output).open("w")


def main(args):
    with infile(args) as f:
        instance = Instance.parse(f.readlines())
        solver = SOLVERS[args.solver]
        solution = solver(instance)
        assert solution.valid()
        with outfile(args) as g:
            print("# Penalty: ", solution.penalty(), file=g)
            solution.serialize(g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a problem instance.")
    parser.add_argument("input", type=str, help="The input instance file to "
                        "read an instance from. Use - for stdin.")
    parser.add_argument("--solver", required=True, type=str,
                        help="The solver type.", choices=SOLVERS.keys())
    parser.add_argument("output", type=str,
                        help="The output file. Use - for stdout.",
                        default="-")
    main(parser.parse_args())
