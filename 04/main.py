#! /usr/bin/env python3

INPUT = [128392, 643281]


def main():
    [low, high] = INPUT
    p1 = p2 = 0

    for n in range(low, high + 1):
        ns = str(n)

        if ''.join(sorted(ns)) != ns:
            continue

        duets = zip(ns, ns[1:])
        if any(a == b for a, b in duets):
            p1 += 1

        ns = " " + ns + " "
        quartets = zip(ns, ns[1:], ns[2:], ns[3:])
        if any(a != ba and a == b and b != ab for ba, a, b, ab in quartets):
            p2 += 1

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
