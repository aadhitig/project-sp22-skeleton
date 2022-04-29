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
    dict_cities = {}
    for city in instance.cities:
        if city.x in dict_cities:
            dict_cities[city.x].append(city.y)
        else:
            dict_cities[city.x] = [city.y]
    
    for x in range(0, instance.grid_side_length):
        if x in dict_cities.keys():
            y_coor = dict_cities[x]
            for y in y_coor:
                if not is_covered(sols, Point(x,y)):
                    sols.append(Point(x, y))
                
    return Solution(
        instance=instance,
        towers=sols,
    )

def is_covered(towers, city):
    for tower in towers:
        if Point.distance_sq(tower, city) <= 9:
            return True
    return False


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
