#! /usr/bin/env python3


from collections import defaultdict


def  main():
    with open('./input.txt') as f:
        raw = f.read().splitlines()

    reactions = {}
    stock = defaultdict(int)
    for line in raw:
        sides = line.split(' => ')
        lhs, rhs = [[tuple(_s.split(' ')) for _s in s.split(', ')] for s in sides]
        reqs = [(int(r[0]), r[1]) for r in lhs]
        rn, rname = rhs[0]
        reactions[rname] = (int(rn), reqs)

    def walk(ends):
        if not ends:
            return 0

        (n_req, name), *rest = ends

        if name in stock:
            chg = min(n_req, stock[name])
            n_req -= chg
            stock[name] -= chg

        if name == 'ORE':
            return n_req

        n_out, reqs = reactions[name]
        n_made = -(-n_req // n_out) * n_out
        stock[name] += n_made - n_req
        reqs = [(int(n_made / n_out * n), name) for n, name in reqs]

        return walk(reqs) + walk(rest)

    p1 = walk([(1, 'FUEL')])

    max_req = 1e12
    p2 = 0
    l = p1
    r = max_req

    while l <= r:
        m = (l + r) // 2
        stock = defaultdict(int)
        req = walk([(m, 'FUEL')])

        if req < max_req:
            p2 = int(max(p2, m))
            l = m + 1
            continue

        if req > max_req:
            r = m - 1
            continue

        break

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
