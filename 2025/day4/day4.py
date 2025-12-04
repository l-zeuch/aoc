import sys
import os
# HACK: I don't want to copy my benchmarking tools into every solution directory,
#       so let's just modify the path at runtime and import from there.
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from bench import *

import argparse
import copy
from typing import List, Tuple

# top, top right, right, bottom right, bottom, bottom left, left, top left
DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1,1), (1, 0), (1,-1), (0, -1), (-1,-1)]

def part1_copy(grid):
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

def part2_copy(grid):
    can_take = 0
    current_grid = [row.copy() for row in grid]
    while True:
        added, current_grid = part1_copy(current_grid)
        if added == 0:
            break
        can_take += added
    return can_take

#    print("=== AFTER ===")
#    for row in new_grid:
#        print("".join(row))
    return can_take, new_grid

def part1_inplace(grid):
#    print("=== BEFORE ===")
#    for row in grid:
#        print("".join(row))

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            if row[c] == 'x':
                row[c] = '.'

    # keep track of what we can remove, but don't change whilst we're counting
    can_take: List[Tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue
            neighbors = 0
            for dx, dy in DIRECTIONS:
                nr, nc = r + dx, c + dy
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                    neighbors += 1
            if neighbors < 4:
                can_take.append((r, c))
    for (r, c) in can_take:
        grid[r][c] = 'x'

    return len(can_take), grid

def part2_inplace(grid):
    can_take = 0
    while True:
        added, _ = part1_inplace(grid)
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
    parser.add_argument(
        "--part",
        help="Select the part to run",
        type=int,
        choices=[1, 2],
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
        print(f'Benchmarking solutions {args.part if args.part else "1 and 2"} (copy vs in-place)...\n')
        # avoid the benchmarking runs mutate grid in-place: provide a fresh copy each run.
        if args.part == 1:
            p1_copy = bench_func(part1_copy, grid, repeat=20)
            p1_inplace = bench_func(lambda _: part1_inplace([row.copy() for row in grid]), None, repeat=20)
            print_stats(p1_copy)
            print()
            print_stats(p1_inplace)
            print()
            print_comparison(p1_copy, p1_inplace)
        elif args.part == 2:
            p2_copy = bench_func(part2_copy, grid, repeat=20)
            p2_inplace = bench_func(lambda _: part2_inplace([row.copy() for row in grid]), None, repeat=20) 
            print_stats(p2_copy)
            print()
            print_stats(p2_inplace)
            print()
            print_comparison(p2_copy, p2_inplace)
        else: # run everything
            p1_copy = bench_func(part1_copy, grid, repeat=20)
            p1_inplace = bench_func(lambda _: part1_inplace([row.copy() for row in grid]), None, repeat=20)
            p2_copy = bench_func(part2_copy, grid, repeat=20)
            p2_inplace = bench_func(lambda _: part2_inplace([row.copy() for row in grid]), None, repeat=20) 

            print_stats(p1_copy)
            print()
            print_stats(p1_inplace)
            print()
            print_comparison(p1_copy, p1_inplace)
            print()
            print_stats(p2_copy)
            print()
            print_stats(p2_inplace)
            print()
            print_comparison(p2_copy, p2_inplace)
        return

    if args.part == 1:
        sol, _ = part1_inplace(grid)
        print(f'solution 1: {sol}')
        return
    elif args.part == 2:
        sol2 = part2_inplace(grid)
        print(f'solution 2: {sol2}')
        return
    else: # everything
        sol, _ = part1_inplace(grid)
        print(f'solution 1: {sol}')
        # part1 mutates in-place; start with a fresh copy for part2.
        grid2 = [[c for c in line] for line in lines]
        sol2 = part2_inplace(grid2)
        print(f'solution 2: {sol2}')

if __name__ == "__main__":
    main()
