#! /usr/bin/env python3

from itertools import product

def exec(prog, noun, verb):
    ip = 0
    _prog = prog[:]
    _prog[1] = noun
    _prog[2] = verb

    while ip < len(_prog):
        op = _prog[ip]

        if op == 99:
            break

        lhs = _prog[_prog[ip + 1]]
        rhs = _prog[_prog[ip + 2]]

        if op == 1:
            _prog[_prog[ip + 3]] = lhs + rhs

        if op == 2:
            _prog[_prog[ip + 3]] = lhs * rhs

        ip += 4

    return _prog[0]

def main():
    p1 = p2 = 0

    with open('./input.txt') as f:
        prog = [int(i) for i in f.readlines()[0].split(',')]

    for noun, verb in product(range(100), range(100)):
        result = exec(prog, noun, verb)

        if noun == 12 and verb == 2:
            p1 = result

        if result == 19690720:
            p2 = 100 * noun + verb

        if p1 and p2:
            break

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()

