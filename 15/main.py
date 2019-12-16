#! /usr/bin/env python3


from collections import defaultdict
from copy import deepcopy

import os
import sys
import math


CHARS = ['█', ' ', 'O', '°', '?']


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


def main():
    with open('./input.txt') as f:
        raw = [int(n) for n in f.read().split(',')]
        prog = defaultdict(int, enumerate(raw))

    seen = set()
    p = 0 + 0j
    path = []
    run = _exec(prog)
    next(run)
    p1 = 0
    _map = defaultdict(lambda: 4)
    oxy_p = None

    while True:
        neighbors = [ p + 1j, p - 1j, p - 1, p + 1 ]

        if not [n for n in neighbors if n not in seen]:
            if not path:
                break

            last = path.pop()
            d = neighbors.index(last) + 1
            run.send(d)
            next(run)
            p = last

            continue

        for d, n in enumerate(neighbors):
            if n in seen:
                continue

            state = run.send(d + 1)
            next(run)
            seen.add(n)
            _map[n] = state

            if state == 0:
                continue

            path.append(p)
            p = n

            if state == 2:
                p1 = len(path)
                oxy_p = p

            break

    dists = defaultdict(lambda: math.inf)
    queue = [(0, oxy_p)]

    while queue:
        dist, p = queue.pop(0)

        if p in dists:
            continue

        dists[p] = min(dists[p], dist)

        for n in [p + 1j, p - 1j, p - 1, p + 1]:
            if _map[n] == 1:
                queue.append((dist + 1, n))

    furthest, p2 = max(dists.items(), key=lambda p: p[1])

    if not os.environ.get('SKIP_DRAWS'):
        p = furthest
        while p != oxy_p:
            _map[p] = 3
            p = min([p + 1j, p - 1j, p - 1, p + 1], key=lambda _p: dists[_p])

        min_i, max_i = [int(f(p.real for p in _map.keys())) for f in [min, max]]
        min_j, max_j = [int(f(p.imag for p in _map.keys())) for f in [min, max]]

        for j in range(max_j, min_j - 1, -1):
            for i in range(min_i, max_i + 1):
                sys.stdout.write(CHARS[_map[i + j * 1j]])

            print()

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
