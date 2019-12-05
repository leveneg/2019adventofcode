#! /usr/bin/env python3

def exec(prog, inputs):
    ip = 0
    _prog = prog[:]
    last_out = None

    while ip < len(_prog):
        op = list(str(_prog[ip]))
        code = int(''.join(op[-2:]))

        if code == 99:
            break

        if code == 3:
            _prog[_prog[ip + 1]] = next(inputs)
            ip += 2
            continue

        if code == 4:
            last_out = _prog[_prog[ip + 1]]
            ip += 2
            continue

        modes = list(map(int, reversed(op[:-2])))
        modes += [0] * (3 - len(modes))
        lhs = _prog[ip + 1] if modes[0] else _prog[_prog[ip + 1]]
        rhs = _prog[ip + 2] if modes[1] else _prog[_prog[ip + 2]]
        dest = _prog[ip + 3]

        if code == 5:
            ip = rhs if lhs else ip + 3
            continue

        if code == 6:
            ip = rhs if not lhs else ip + 3
            continue

        if code == 7:
            _prog[dest] = int(lhs < rhs)

        if code == 8:
            _prog[dest] = int(lhs == rhs)

        if code == 1:
            _prog[dest] = lhs + rhs

        if code == 2:
            _prog[dest] = lhs * rhs

        ip += 4

    return last_out


def main():
    with open('./input.txt') as f:
        prog = [int(n) for n in f.readline().split(',')]

    p1 = exec(prog, iter([1]))
    p2 = exec(prog, iter([5]))

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
