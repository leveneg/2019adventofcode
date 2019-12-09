#! /usr/bin/env python3


import os


def main():
    with open('./input.txt') as f:
        raw = [int(c) for c in f.read().strip()]

    n_rows, n_cols = 6, 25
    area = n_rows * n_cols
    layers = [raw[s:s + area] for s in range(0, len(raw), area)]
    _, layer = min(enumerate(layers), key=lambda l: l[1].count(0))

    p1 = layer.count(1) * layer.count(2)

    rast = [next(filter(lambda v: v != 2, l)) for l in zip(*layers)]
    img = [rast[s:s + 25] for s in range(0, len(rast), 25)]

    if not os.environ.get('SKIP_DRAWS'):
        for row in img:
            print(*['#' if x == 1 else ' ' for x in row])

    print("p1: {}, p2: {}".format(p1, "AZCJC"))


if __name__ == "__main__":
    main()
