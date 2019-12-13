#! /usr/bin/env python3


import os
import sys

from collections import defaultdict
from copy import deepcopy


CHARS = {
    0: " ",
    1: "█",
    2: "░",
    3: "_",
    4: "®"
}


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
            yield None
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


def _print(screen):
    if os.environ.get('SKIP_DRAWS'):
        return

    ps = screen.keys()
    min_i, max_i = [int(d(p.real for p in ps)) for d in [min, max]]
    min_j, max_j = [int(d(p.imag for p in ps)) for d in [min, max]]

    os.system('clear')
    for j  in range(min_j, max_j + 1):
        for i in range(min_i, max_i + 1):
            sys.stdout.write(CHARS[screen[i + j * 1j]])

        print()


def main():
    with open('./input.txt') as f:
        raw = [int(n) for n in f.read().split(',')]
        prog = defaultdict(int, enumerate(raw))

    screen = defaultdict(int)
    run = _exec(prog)
    for x in run:
        y, _id = next(run), next(run)
        screen[x + y * 1j] = _id

    p1 = sum(1 for v in screen.values() if v == 2)

    screen = defaultdict(int)
    prog[0] = 2
    run = _exec(prog)
    p2 = 0
    finished_init = False

    for x in run:
        if x is None:
            next(run)
            paddle_x = list(screen.keys())[list(screen.values()).index(3)].real
            ball_x = list(screen.keys())[list(screen.values()).index(4)].real
            d = -1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0
            x = run.send(d)

        y, _id = next(run), next(run)

        if (x, y) == (-1, 0):
            p2 = _id
            finished_init = True
            continue

        screen[x + y * 1j] = _id

        if finished_init:
            _print(screen)

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
