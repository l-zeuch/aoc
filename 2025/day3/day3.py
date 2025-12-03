def part1(lines):
    total_jolts = 0
    for line in lines:
        # we try to find the largest element that is not the last element;
        # we still need some room to spare!
        largest = -1
        index_of_largest = 0
        for idx, c in enumerate(line[:-1]):
            i = int(c)
            if i > largest:
                largest = i
                index_of_largest = idx
        # starting from this largest element, find the other largest element
        # in this newly created subset.
        second = 0
        for c in line[(index_of_largest+1):]:
            i = int(c)
            if i > second:
                second = i
        jolts = largest*10 + second
        total_jolts += jolts
    return total_jolts

def part2(lines):
    total_jolts = 0

    for bank in lines:
        batteries = [int(x) for x in bank]

        results = []
        search_bank = list(batteries)

        for i in range(12):
            if len(search_bank) == 0:
                results.append(0)
                continue

            largest = -1
            index_of_largest = 0

            need = 12-i
            can_take = len(search_bank) - need

            for idx, v in enumerate(search_bank[:can_take+1]):
                if v > largest:
                    largest = v
                    index_of_largest = idx


            results.append(largest)
            search_bank = search_bank[(index_of_largest + 1):]

        tmp = 0
        for d in results:
            tmp = tmp * 10 + d
        total_jolts += tmp

    return total_jolts

def main():
    with open("input.txt", "rt") as fin:
        lines = [line.strip() for line in fin]
    lines_lst = list(lines) # create an immutable reference
    #sol1 = part1(lines_lst)
    sol2 = part2(lines_lst)
    print(f"part 1: placeholder; part 2: {sol2}")

if __name__ == "__main__":
    main()
