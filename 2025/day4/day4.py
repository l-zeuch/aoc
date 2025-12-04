import sys
import os
# HACK: I don't want to copy my benchmarking tools into every solution directory,
#       so let's just modify the path at runtime and import from there.
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from bench import *

import argparse
import copy

def part1(grid):
#    print("=== BEFORE ===")
#    for row in grid:
#        print("".join(row))

    rows = len(grid)
    cols = len(grid[0])
    new_grid = copy.deepcopy(grid)
    can_take = 0
    # top, top right, right, bottom right, bottom, bottom left, left, top left
    directions = [(-1, 0), (-1, 1), (0, 1), (1,1), (1, 0), (1,-1), (0, -1), (-1,-1)]
    for r, row in enumerate(grid):
        for c, roll in enumerate(row):
            cell = grid[r][c]
            if cell != '@':
                new_grid[r][c] = cell
                continue
            if cell == 'x':
                new_grid[r][c] = '.'

            neighbors = 0
            for x, y in directions:
                new_r, new_c = r + x, c + y
                if new_r in range(rows) and new_c in range(cols) and grid[new_r][new_c] == '@':
                    neighbors += 1
            if neighbors < 4:
                can_take += 1
                new_grid[r][c] = 'x'
            else:
                new_grid[r][c] = '@'

#    print("=== AFTER ===")
#    for row in new_grid:
#        print("".join(row))
    return can_take, new_grid

def part2(grid):
    can_take = 0
    current_grid = [row.copy() for row in grid]
    while True:
        added, current_grid = part1(current_grid)
        if added == 0:
            break
        can_take += added
    return can_take

def main():
    parser = argparse.ArgumentParser(
        description="AoC Day 4: Printing Department",
    )
    parser.add_argument(
        "--test",
        help="Use sample input instead of the real one.",
        action="store_true",
    )
    parser.add_argument(
        "--bench",
        help="Run benchmarks",
        action="store_true",
    )
    args = parser.parse_args()

    path = 'input.txt'
    if args.test:
        path = 'test.txt'

    with open(path, 'rt') as f:
        lines = [line.strip() for line in f.readlines()]
    # first we make a grid to easily traverse it with our direction tuples.
    grid = [[c for c in line] for line in lines]

    if args.bench:
        print("Benchmarking...")
        r1_1 = bench_func(part1, grid, repeat=20)
        r2_1 = bench_func(part2, grid, repeat=20)
        print_stats(r1_1)
        print()
        print_stats(r2_1)
        return

    sol1, _ = part1(grid)
    sol2 = part2(grid)
    print(f'solution 1: {sol1}, solution 2: {sol2}')

if __name__ == "__main__":
    main()
