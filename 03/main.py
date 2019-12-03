#! /usr/bin/env python3


DIRS = {
    'R':  1 +  0j,
    'U':  0 +  1j,
    'L': -1 +  0j,
    'D':  0 + -1j
}


def main():
    with open('./input.txt') as f:
        wires = [l.split(',') for l in f.readlines()]

    points = []
    collisions = set()

    for wire in wires:
        wp = 0 + 0j
        wps = []

        for turn in wire:
            d = DIRS[turn[0]]
            n = int(turn[1:])

            for _ in range(n):
                wp += d
                wps.append(wp)

        collisions |= (set([p for l in points for p in l]) & set(wps))
        points.append(wps)

    collision_dists = [int(abs(p.real) + abs(p.imag)) for p in collisions]
    path_lens = [sum(ps.index(coll) + 1 for ps in points) for coll in collisions]

    print("p1: {}, p2: {}".format(min(collision_dists), min(path_lens)))


if __name__ == "__main__":
    main()
