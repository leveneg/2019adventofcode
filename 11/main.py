#! /usr/bin/env python3


from cmath import pi, phase, rect
from copy import deepcopy
from collections import defaultdict

import os
import sys

def _exec(prog):
    ip = 0
    _prog = deepcopy(prog)
    rel_base = 0

    def get_val(param, mode):
        if mode == 0:
            return _prog[param]
        if mode == 1:
            return param
        if mode == 2:
            return _prog[param + rel_base]

    def get_dest(param, mode):
        if mode == 0:
            return param
        if mode == 2:
            return rel_base + param

    while ip < len(_prog):
        op = list(str(_prog[ip]))
        code = int(''.join(op[-2:]))
        modes = list(map(int, reversed(op[:-2])))
        modes += [0] * (3 - len(modes))
        lhs, rhs = [get_val(_prog[ip + i + 1], modes[i]) for i in range(2)]
        dest = get_dest(_prog[ip + 3], modes[2])

        if code == 99:
            break

        if code == 3:
            dest = get_dest(_prog[ip + 1], modes[0])
            _prog[dest] = yield
            ip += 2
            continue

        if code == 4:
            yield lhs
            ip += 2
            continue

        if code == 9:
            rel_base += lhs
            ip += 2
            continue

        if code == 5:
            ip = rhs if lhs else ip + 3
            continue

        elif code == 6:
            ip = rhs if not lhs else ip + 3
            continue

        elif code == 7:
            _prog[dest] = int(lhs < rhs)

        elif code == 8:
            _prog[dest] = int(lhs == rhs)

        elif code == 1:
            _prog[dest] = lhs + rhs

        elif code == 2:
            _prog[dest] = lhs * rhs

        ip += 4


def paint(prog, hull, origin):
    run = _exec(prog)
    p = origin
    d = 0 + 1j

    for _ in run:
        hull[p] = run.send(hull[p])
        d = rect(1, phase(d) + (pi / 2) * [-1, 1][next(run)])
        d = complex(round(d.real), round(d.imag))
        p = p + d

    return hull


def main():
    with open('./input.txt') as f:
        raw = [int(n) for n in f.read().split(',')]
        prog = defaultdict(int, enumerate(raw))

    hull = defaultdict(int)
    hull = paint(prog, hull, 0 + 0j)
    p1 = len(hull.keys())

    hull = defaultdict(int, [(0 + 0j, 1)])
    hull = paint(prog, hull, 0 + 0j)

    min_i, max_i = [int(d([p.real for p in hull.keys()])) for d in [min, max]]
    min_j, max_j = [int(d([p.imag for p in hull.keys()])) for d in [min, max]]

    if not os.environ.get('SKIP_DRAWS'):
        for j in range(max_j, min_j - 1, -1):
            for i in range(max_i, min_i - 1, -1):
                sys.stdout.write('#' if hull[complex(i, j)] else ' ')

            print()

    print("p1: {}, p2: {}".format(p1, "CEPKZJCR"))


if __name__ == "__main__":
    main()
