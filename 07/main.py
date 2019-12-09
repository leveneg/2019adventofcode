#! /usr/bin/env python3


from itertools import permutations


def _exec(prog):
    ip = 0
    _prog = prog[:]

    while ip < len(_prog):
        op = list(str(_prog[ip]))
        code = int(''.join(op[-2:]))

        if code == 99:
            break

        if code == 3:
            _prog[_prog[ip + 1]] = yield
            ip += 2
            continue

        if code == 4:
            yield _prog[_prog[ip + 1]]

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
        prog = [int(n) for n in f.read().split(',')]

    n_amps = 5
    best = 0
    p1 = p2 = 0

    for phase_set in permutations(range(5), n_amps):
        out = 0

        for amp_idx in range(n_amps):
            run = _exec(prog)
            next(run)

            run.send(phase_set[amp_idx])
            out = run.send(out)

        best = out if out > best else best

    p1 = best
    best = 0

    for phases in permutations(range(5, 10), n_amps):
        amps = [_exec(prog) for _ in range(n_amps)]
        out = 0
        done = False

        for idx, amp in enumerate(amps):
            next(amp)
            amp.send(phases[idx])

        while not done:
            for amp in amps:
                try:
                    out = amp.send(out)
                    next(amp)

                except StopIteration:
                    done = True

        best = out if out > best else best

    p2 = best

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
