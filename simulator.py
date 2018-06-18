import random
from strategies import *


def match(pl0, pl1):
    cards = random.sample([1, 2, 3], 2)
    winner = int(cards[1] > cards[0])
    d0 = pl0.decision0(cards[0])
    if d0 == 0:
        # wait
        d1 = pl1.decision1c(cards[1])
        if d1 == 0:
            # wait
            pl0.result_ww(0, cards)
            pl1.result_ww(1, cards)
            return [1 if winner == i else -1 for i in range(2)]
        elif d1 == 1:
            # bet
            d2 = pl0.decision2(cards[0])
            if d2 == 0:
                # fold
                pl0.result_wbf(0, cards[0])
                pl1.result_wbf(1, cards[1])
                return [-1, 1]
            elif d2 == 1:
                # check
                pl0.result_wbc(0, cards)
                pl1.result_wbc(1, cards)
                return [2 if winner == i else -2 for i in range(2)]
    elif d0 == 1:
        # bet
        d1 = pl1.decision1b(cards[1])
        if d1 == 0:
            # fold
            pl0.result_bf(0, cards[0])
            pl1.result_bf(1, cards[1])
            return [1, -1]
        elif d1 == 1:
            # check
            pl0.result_bc(0, cards)
            pl1.result_bc(1, cards)
            return [2 if winner == i else -2 for i in range(2)]
    raise ValueError("wtf")


def simulate(Klas1, Klas2, rounds=100, verbose=False):
    def vprint(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    pls = [Klas1(), Klas2()]

    points = [0, 0]
    starting = random.choice([0, 1])
    vprint("First: Player {}, {}".format(starting, pls[starting].name()))
    vprint("Second: Player {}, {}".format(1-starting, pls[1-starting].name()))
    current = starting
    for i in range(rounds):
        mp = match(pls[current], pls[1-current])[::(1 if current == 0 else -1)]
        vprint("Match results:", mp[0], mp[1])
        points[0] += mp[0]
        points[1] += mp[1]
        vprint("Sum:", points[0], points[1])
        current = 1 - current
    if points[1] == points[0]:
        vprint('DRAW')
    else:
        winner = int(points[1] > points[0])
        vprint("Winner: {}, with {} points".format(pls[winner].name(), max(points)))
    return points


if __name__ == "__main__":
    strategies = [ExpectedNaiveDefaults, ExpectedNaive, AdaptiveNaive, IfNotOne, SimpleHeur, AlwaysOne, IfThree,
                  RandomDecision, AlwaysZero]
    points = [0 for s in strategies]
    ROUNDS = 100
    REPEATS = 100

    for i, s0 in enumerate(strategies):
        for j, s1 in list(enumerate(strategies)):
            results = [0, 0]
            for r in range(REPEATS):
                rpart = simulate(s0, s1, rounds=ROUNDS)
                results[0] += rpart[0]
                results[1] += rpart[1]
            print(s0.__name__, s1.__name__, results)
            points[i] += results[0]
            points[j] += results[1]
    print()
    print("Final:")
    for p, s in zip(points, strategies):
        print(s.__name__, p)
