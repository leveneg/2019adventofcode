#! /usr/bin/env python3


from itertools import chain, repeat
from pprint import pprint


BASE_PATTERN = [0, 1, 0, -1]


def process(signal):
    signal = signal[:]

    for _ in range(100):
        output = []

        for idx in range(len(signal)):
            pattern = [i for sl in zip(*repeat(BASE_PATTERN, idx + 1)) for i in sl]
            d = 0

            for i, n in enumerate(signal):
                d += (pattern[(i + 1) % len(pattern)] * n)

            output.append(abs(d) % 10)

        signal = output

    return signal


def main():
    with open('./input.txt') as f:
        raw = f.read().strip()
        signal = [int(n) for n in raw]

    p1 = ''.join(map(str, process(signal)[:8]))

    offset = int(''.join(map(str, signal[:7])))
    signal = list(chain(*repeat(signal, 10000)))[offset:]

    for _ in range(100):
        _sum = 0

        for i in range(len(signal) - 1, -1, -1):
            signal[i] = _sum = (_sum + signal[i]) % 10

    p2 = ''.join(map(str, signal[:8]))

    print('p1: {}, p2: {}'.format(p1, p2))


if __name__ == "__main__":
    main()
