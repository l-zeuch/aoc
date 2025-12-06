import sys
import os
# HACK: I don't want to copy my benchmarking tools into every solution directory,
#       so let's just modify the path at runtime and import from there.
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
import bench
import argparse
from concurrent.futures import ThreadPoolExecutor

from typing import Iterable

def solve_part1(worksheet: Iterable) -> int:
    problems = list(_parse_input_part1(worksheet))
    return sum(map(_process_problem_part1, problems))


def solve_part1_mt(worksheet: Iterable, max_workers: int | None = None):
    """
    Multi-threaded version of part 1 solution.
    Note that in this specific circumstance (AoC) the input is so small that we have proportionally
    more overhead and, as a result, actually run slower than the single-threaded version.
    Not to mention that if you're not using a free-threaded build of Python >= 3.13, you've got to deal
    with the GIL as well.
    """
    problems = list(_parse_input_part1(worksheet))
    if max_workers is None:
        max_workers = min(len(problems), max(1, (os.cpu_count() or 1) * 2 ))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return sum(ex.map(_process_problem_part1, problems))


def _process_problem_part1(problem):
    operator = problem[-1]
    result = problem[0]
    for part in problem[1:-1]:
        result = _op(operator, result, part)
    return result


def _parse_input_part1(sheet): 
    t = [line.strip().split() for line in sheet]
    return [[int(s) if isinstance(x, str) and (s := x.strip()).isdigit() else x for x in list(col)] for col in zip(*t)]


def _op(operator, current, add):
    if operator == '*':
        current *= add
    elif operator == '+':
        current += add
    else:
        current += 0
    return current


def main():
    parser = argparse.ArgumentParser(
        description="AoC Day 5: Cafeteria"
    )
    parser.add_argument(
        "--test",
        help="Use sample input instead of the real one.",
        action="store_true",
    )
    parser.add_argument(
        "--bench",
        help="Benchmark the stuﬀ",
        action="store_true",
    )
    args = parser.parse_args()

    path = 'input.txt'
    if args.test:
        path = 'test.txt'
    with open(path, 'rt') as file:
        input = [line for line in file]

    if args.bench:
        print("Benchmarking...")
        p1 = bench.bench_func(solve_part1, input, repeat=20)
        bench.print_stats(p1)
        print()
        p1_mt = bench.bench_func(solve_part1_mt, input, repeat=20)
        bench.print_stats(p1_mt)
        print()
        bench.print_comparison(p1, p1_mt)


    sol1 = solve_part1(input)
    print(f'solution 1: {sol1}')


if __name__ == "__main__":
    main()
