#! /usr/bin/env python3


from collections import defaultdict


def main():
    with open('./input.txt') as f:
        lines = f.read().splitlines()
        orbits = [tuple(l.split(')')) for l in lines]

    p1 = p2 = 0
    to_primary = {}
    to_secondaries = defaultdict(list)
    objs = set()

    for orbit in orbits:
        primary, secondary = orbit
        to_primary[secondary] = primary
        to_secondaries[primary].append(secondary)
        objs |= set([primary, secondary])

    def walk(obj, dist=0):
        return dist if obj == "COM" else walk(to_primary[obj], dist + 1)

    p1 = sum(map(walk, objs))

    seen = set()
    queue = [("YOU", 0)]

    while len(queue) > 0:
        obj, dist = queue.pop(0)

        if obj == "SAN":
            p2 = dist - 2
            break

        seen.add(obj)
        neighbors = [to_primary.get(obj)] + to_secondaries[obj]

        for neighbor in neighbors:
            if neighbor and neighbor not in seen:
                queue.append((neighbor, dist + 1))

    print("p1: {}, p2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
