#!/usr/bin/env python3
import os

def part1(instructions):
    current_pos = 50
    zeros_seen = 0
    for instruction in instructions:
        current_pos += instruction
        if current_pos >= 0:
            current_pos %= 100
        else:
            current_pos = (99 + (current_pos + 1)) % 100
        if current_pos == 0:
            zeros_seen += 1

    return zeros_seen

def part2(instructions):
    current_pos = 50
    zeros_seen = 0
    for instruction in instructions:
        if instruction > 0:
            offset = current_pos
        elif current_pos == 0:
            offset = 0
        else:
            offset = 100 - current_pos
        zeros_seen += int((abs(instruction) + offset) / 100)
        current_pos += instruction
        if current_pos >= 0:
            current_pos %= 100
        else:
            current_pos = (99 + (current_pos +1)) % 100

    return zeros_seen

def main():
    with open("input.txt", "rt") as fin:
        lines = [line.strip() for line in fin]

    instructions = [int(line[1:]) * -1 if line[0] == "L" else int(line[1:]) for line in lines]

    password1 = part1(instructions)
    password2 = part2(instructions)

    print(f'password 1 is {password1}; password 2 is {password2}')

if __name__ == "__main__":
    main()
