"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
from cmath import inf
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from solution import Solution
from file_wrappers import StdinFileWrapper, StdoutFileWrapper
from point import Point

def solve_naive(instance: Instance) -> Solution:
    sols = [sol_bottom_left_x(instance), sol_bottom_left_y(instance), sol_top_right_x(instance), sol_top_right_y(instance)]

    solution_one = Solution(
        instance=instance,
        towers=sols[0],
    )
    solution_two = Solution(
        instance=instance,
        towers=sols[1],
    )
    solution_three = Solution(
        instance=instance,
        towers=sols[2],
    )

    solution_four = Solution(
        instance=instance,
        towers=sols[3],
    )
    
    return min(solution_one, solution_two, solution_three, solution_four , key = lambda k: k.penalty())

def sol_bottom_left_x(instance):
    sols = []
    cities = instance.cities
    sorted_cities = sorted(cities , key=lambda k: k.x)
    for c in range(len(sorted_cities)):
        if not is_covered(sols, sorted_cities[c]):
            for i in range(c + 1, len(sorted_cities)):
                if not is_covered(sols, sorted_cities[i]) and Point.distance_sq(sorted_cities[c], sorted_cities[i]) <= 36:
                    mid_tower = addTowerMid(sorted_cities[c], sorted_cities[i])
                    sols.append(mid_tower)
                    break
            if not is_covered(sols, sorted_cities[c]):
                sols.append(sorted_cities[c])
    return sols

def sol_bottom_left_y(instance):
    sols = []
    cities = instance.cities
    sorted_cities = sorted(cities , key=lambda k: k.y)
    for c in range(len(sorted_cities)):
        if not is_covered(sols, sorted_cities[c]):
            for i in range(c + 1, len(sorted_cities)):
                if not is_covered(sols, sorted_cities[i]) and Point.distance_sq(sorted_cities[c], sorted_cities[i]) <= 36:
                    mid_tower = addTowerMid(sorted_cities[c], sorted_cities[i])
                    sols.append(mid_tower)
                    break
            if not is_covered(sols, sorted_cities[c]):
                sols.append(sorted_cities[c])
    return sols

def sol_top_right_x(instance):
    sols = []
    cities = instance.cities
    sorted_cities = sorted(cities , key=lambda k: k.x)
    sorted_cities.reverse()
    for c in range(len(sorted_cities)):
        if not is_covered(sols, sorted_cities[c]):
            for i in range(c + 1, len(sorted_cities)):
                if not is_covered(sols, sorted_cities[i]) and Point.distance_sq(sorted_cities[c], sorted_cities[i]) <= 36:
                    mid_tower = addTowerMid(sorted_cities[c], sorted_cities[i])
                    sols.append(mid_tower)
                    break
            if not is_covered(sols, sorted_cities[c]):
                sols.append(sorted_cities[c])
    return sols

def sol_top_right_y(instance):
    sols = []
    cities = instance.cities
    sorted_cities = sorted(cities , key=lambda k: k.y)
    sorted_cities.reverse()
    for c in range(len(sorted_cities)):
        if not is_covered(sols, sorted_cities[c]):
            for i in range(c + 1, len(sorted_cities)):
                if not is_covered(sols, sorted_cities[i]) and Point.distance_sq(sorted_cities[c], sorted_cities[i]) <= 36:
                    mid_tower = addTowerMid(sorted_cities[c], sorted_cities[i])
                    sols.append(mid_tower)
                    break
            if not is_covered(sols, sorted_cities[c]):
                sols.append(sorted_cities[c])
    return sols

def is_covered(towers, city):
    for tower in towers:
        if Point.distance_sq(tower, city) <= 9:
            return True
    return False

def addTowerMid(one, two):
    return Point((one.x + two.x) // 2 , (one.y + two.y) // 2)

SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive
}

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
