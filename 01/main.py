#! /usr/bin/env python3

def calcMass(base, isPartTwo=False):
    calc = base // 3 - 2

    if not isPartTwo:
        return calc

    rt = 0

    while calc > 0:
        rt += calc
        calc = calc // 3 - 2

    return rt

def main():
    p1 = p2 = 0

    with open('./input.txt') as f:
        for line in f:
            base = int(line)

            p1 += calcMass(base)
            p2 += calcMass(base, True)

    print("p1: {}, p2: {}".format(p1, p2))

if __name__ == "__main__":
    main()
