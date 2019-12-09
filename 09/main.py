#! /usr/bin/env python3


from collections import defaultdict
from copy import deepcopy


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

    run = _exec(prog)
    next(run)
    p1 = run.send(1)
    for p1 in run:
        pass

    run = _exec(prog)
    next(run)
    p2 = run.send(2)
    for p2 in run:
        pass

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
