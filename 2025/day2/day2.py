import re
import bisect

def part1_regex(lines):
    """First iteration. Naive approach. Works, but runs >1s."""
    seen = set()
    for line in lines:
        nums = [int(num) for num in line.split('-')]
        for n in range(nums[0], nums[1]):
            if re.match(r'^(\d+)\1', str(n)):
                seen.add(n)
    return sum(seen)

def part1_half_comparison(lines):
    """Optimisation 1: use a half-comparison and see if both ends are the same. Way faster (430ms)."""
    seen = set()
    # strings with repeated numbers must be of even length; then, compare the first half to the second half (split with integer division)
    is_repeated = lambda s: (len(s) % 2 == 0) and (s[:len(s)//2] == s[len(s)//2:])
    for line in lines:
        start_str, end_str = line.split('-', 1)
        start = int(start_str)
        end = int(end_str)
        for num in range(start, end):
            s = str(num)
            if is_repeated(s):
                seen.add(num)
    return sum(seen)

def part1_generate(lines):
    """
    Optimisation 2: Find the maximum number we need to generate and only generate the numbers that repeat digits up to that max.
    Then, use bisect to inspect the respective subset. Much faster (~30ms including python startup).
    """
    ranges = []
    max_end = 0
    for line in lines:
        start_str, end_str = line.split('-', 1)
        start = int(start_str)
        end = int(end_str)
        ranges.append((start, end))
        if end > max_end:
            max_end = end

    repeated_nums = gen_repeated_up_to(max_end - 1)
    seen_sum = 0
    seen = set()
    for start, end in ranges:
        lo = bisect.bisect_left(repeated_nums, start)
        hi = bisect.bisect_left(repeated_nums, end)
        for val in repeated_nums[lo:hi]:
            if val not in seen:
                seen.add(val)
                seen_sum += val
    return seen_sum

def gen_repeated_up_to(max):
    results = []
    max_digits = len(str(max))
    # only even-length generated numbers: 2*k digits
    for k in range(1, (max_digits // 2) + 1):
        start = 10**(k-1)
        end = 10**k
        print(k)
        # generate the numbers: for each number of digits k we go from 1**(k-1) to 10**k - 1
        # then, we smush them together to get a repeated thing A going on.
        #
        # e.g. max_digits = 6
        #     => k = 3; start = 10^(3-1) = 10^2 = 100; end = 10^3 = 1000
        # we itereate through 1..3, generating numbers of 1 to 3 digits:
        #   a in [1,10), a in [10,100), a in [100,1000)
        #         1-9          10-99          100-999
        # finally, we smash them together.
        for a in range(start, end):
            print(a)
            rep = int(str(a) + str(a))
            if rep > max:
                # stop with the exceed the total max
                break
            results.append(rep)
    results.sort()
    return results

def part2(lines):
    """
    Basically part one but another half second slower thanks to the repeated backreference.
    I do not particulary care for optimising this, Copilot suggested KMP.
    """
    seen = set()
    for line in lines:
        nums = [int(num) for num in line.split('-')]
        for n in range(nums[0], nums[1]):
            if bool(re.match(r'^(\d+)\1+$', str(n))):
                seen.add(n)
    return sum(seen)

def main():
    with open("input.txt", "rt") as fin:
        lines = [part.strip() for raw in fin for part in raw.split(',')]
    lines_list = list(lines)
    result1 = part1_generate(lines_list)
    result2 = part2(lines_list)
    print(f'Result 1: {result1}\nResult 2: {result2}')

if __name__ == "__main__":
    main()
