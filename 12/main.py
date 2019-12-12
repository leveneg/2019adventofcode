#! /usr/bin/env python3


from collections import namedtuple
from itertools import combinations
from math import gcd


def step_dim(dims):
    for prim, sec in combinations(dims, 2):
        if prim[0] == sec[0]:
            continue

        d = [-1, 1][prim[0] < sec[0]]
        prim[1], sec[1] = prim[1] + d, sec[1] - d

    for dim in dims:
        dim[0] += dim[1]

    return dims


def step(moons):
    dims = [step_dim([[p[ax], v[ax]] for p, v in moons]) for ax in range(3)]

    return [list(zip(*v)) for v in zip(*dims)]


def main():
    moons = [
        [[-10, -13, 7 ], [0, 0, 0]],
        [[ 1,   2,  1 ], [0, 0, 0]],
        [[-15, -3,  13], [0, 0, 0]],
        [[ 3,   7, -4 ], [0, 0, 0]],
    ]

    for _ in range(1000):
        moons = step(moons)

    pots, kins = [[sum(map(abs, m[i])) for m in moons] for i in range(2)]
    p1 = sum(p * k for p, k in zip(pots, kins))

    p2 = 1
    for ax in range(3):
        i = 1
        dims = [[p[ax], v[ax]] for p, v in moons]
        _d = [d[:] for d in dims]

        while step_dim(_d) != dims:
            i += 1

        p2 = abs(p2 * i) // gcd(p2, i)

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
