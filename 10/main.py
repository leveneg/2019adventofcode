#! /usr/bin/env python3


from cmath import phase, pi
from collections import defaultdict, deque
from itertools import zip_longest


def main():
    with open('./input.txt') as f:
        lines = f.read().splitlines()

    roids = []
    best = (0, 0, {})

    for j, row in enumerate(lines):
        for i, cell in enumerate(row):
            if cell == "#":
                roids.append(i + 1j * j)

    for prim in roids:
        angles = defaultdict(list)

        for sec in roids:
            if prim == sec:
                continue

            angle = phase(sec - prim)
            angles[angle].append(sec)

        n_seen = len(angles)
        best_p, best_n, _ = best

        if n_seen > best_n:
            best = (prim, n_seen, angles)

    best_p, p1, angles = best
    angles = {k:sorted(v,key=lambda p:abs(best_p-p)) for k,v in sorted(angles.items())}
    ps = deque(angles.values())
    ps.rotate(-1 * list(angles.keys()).index(-pi / 2))
    grouped = zip_longest(*ps)
    order = list(filter(bool, [p for g in grouped for p in g]))
    p2 = int(order[199].real * 100 + order[199].imag)

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
