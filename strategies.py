import random
import math


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


class Player():
    def decision0(self, card):
        raise NotImplementedError()

    def decision1c(self, card):
        raise NotImplementedError()

    def decision1b(self, card):
        raise NotImplementedError()

    def decision2(self, card):
        raise NotImplementedError()

    def result_ww(self, pos, cards):
        pass

    def result_wbf(self, pos, card):
        pass

    def result_wbc(self, pos, cards):
        pass

    def result_bf(self, pos, card):
        pass

    def result_bc(self, pos, cards):
        pass

    def name(self):
        return type(self).__name__


class AlwaysOne(Player):
    def decision0(self, card):
        return 1

    def decision1c(self, card):
        return 1

    def decision1b(self, card):
        return 1

    def decision2(self, card):
        return 1


class AlwaysZero(Player):
    def decision0(self, card):
        return 0

    def decision1c(self, card):
        return 0

    def decision1b(self, card):
        return 0

    def decision2(self, card):
        return 0


class IfThree(Player):
    def decision0(self, card):
        return int(card == 3)

    def decision1c(self, card):
        return int(card == 3)

    def decision1b(self, card):
        return int(card == 3)

    def decision2(self, card):
        return int(card == 3)


class IfNotOne(Player):
    def decision0(self, card):
        return int(card != 1)

    def decision1c(self, card):
        return int(card != 1)

    def decision1b(self, card):
        return int(card != 1)

    def decision2(self, card):
        return int(card != 1)


class RandomDecision(Player):
    def decision0(self, card):
        return random.choice([0, 1])

    def decision1c(self, card):
        return random.choice([0, 1])

    def decision1b(self, card):
        return random.choice([0, 1])

    def decision2(self, card):
        return random.choice([0, 1])


class SimpleHeur(Player):
    def decision0(self, card):
        return int(card == 3)

    def decision1c(self, card):
        return int(card == 3)

    def decision1b(self, card):
        return int(card >= 2)

    def decision2(self, card):
        return int(card >= 2)


class AdaptiveNaive(Player):
    def __init__(self):
        self.c0 = [0.0, 0.0, 0.0]
        self.c1c = [0.0, 0.0, 0.0]
        self.c1b = [0.0, 0.0, 0.0]
        self.c2 = [0.0, 0.0, 0.0]

    def decision0(self, card):
        return int(random.random() < sigmoid(self.c0[card-1]))

    def decision1c(self, card):
        return int(random.random() < sigmoid(self.c1c[card-1]))

    def decision1b(self, card):
        return int(random.random() < sigmoid(self.c1b[card-1]))

    def decision2(self, card):
        return int(random.random() < sigmoid(self.c2[card-1]))

    def result_ww(self, pos, cards):
        won = (cards[pos] > cards[1-pos])
        move = 1.0 if won else -1.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1] -= move
        elif pos == 1:
            self.c1c[card - 1] -= move

    def result_wbf(self, pos, card):
        move = 1.0 if pos == 1 else -1.0
        if pos == 0:
            self.c0[card - 1] -= move
            self.c2[card - 1] -= move
        if pos == 1:
            self.c1c[card - 1] += move

    def result_wbc(self, pos, cards):
        won = (cards[pos] > cards[1 - pos])
        move = 2.0 if won else -2.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1] -= move
            self.c2[card - 1] += move
        elif pos == 1:
            self.c1c[card - 1] += move

    def result_bf(self, pos, card):
        move = 1.0 if pos == 0 else -1.0
        if pos == 0:
            self.c0[card - 1] += move
        if pos == 1:
            self.c1b[card - 1] -= move

    def result_bc(self, pos, cards):
        won = (cards[pos] > cards[1 - pos])
        move = 2.0 if won else -2.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1] += move
        elif pos == 1:
            self.c1b[card - 1] += move


class ExpectedNaive(Player):
    def __init__(self):
        self.c0 = [([], []), ([], []), ([], [])]
        self.c1c = [([], []), ([], []), ([], [])]
        self.c1b = [([], []), ([], []), ([], [])]
        self.c2 = [([], []), ([], []), ([], [])]

    def choose(self, elem):
        # elem is like ([], [])
        exp0 = (sum(elem[0]) + 0.0) / (len(elem[0]) + 2)
        exp1 = (sum(elem[1]) + 0.0) / (len(elem[1]) + 2)
        if random.random() < (1.0 / ((len(elem[1]) + 1)*(len(elem[0]) + 1))):
            return random.choice([0, 1])
        else:
            return int(exp1 > exp0)

    def decision0(self, card):
        return self.choose(self.c0[card-1])

    def decision1c(self, card):
        return self.choose(self.c1c[card-1])

    def decision1b(self, card):
        return self.choose(self.c1b[card-1])

    def decision2(self, card):
        return self.choose(self.c2[card-1])

    def result_ww(self, pos, cards):
        won = (cards[pos] > cards[1-pos])
        move = 1.0 if won else -1.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1][0].append(move)
        elif pos == 1:
            self.c1c[card - 1][0].append(move)

    def result_wbf(self, pos, card):
        move = 1.0 if pos == 1 else -1.0
        if pos == 0:
            self.c0[card - 1][0].append(move)
            self.c2[card - 1][0].append(move)
        if pos == 1:
            self.c1c[card - 1][1].append(move)

    def result_wbc(self, pos, cards):
        won = (cards[pos] > cards[1 - pos])
        move = 2.0 if won else -2.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1][0].append(move)
            self.c2[card - 1][1].append(move)
        elif pos == 1:
            self.c1c[card - 1][1].append(move)

    def result_bf(self, pos, card):
        move = 1.0 if pos == 0 else -1.0
        if pos == 0:
            self.c0[card - 1][1].append(move)
        if pos == 1:
            self.c1b[card - 1][0].append(move)

    def result_bc(self, pos, cards):
        won = (cards[pos] > cards[1 - pos])
        move = 2.0 if won else -2.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1][1].append(move)
        elif pos == 1:
            self.c1b[card - 1][1].append(move)


class ExpectedNaiveDefaults(Player):
    def __init__(self):
        self.c0 = [([-1.0], [-1.0]), ([0.0], [0.0]), ([1.3], [1.3])]
        self.c1c = [([-1.0], [-1.0]), ([0.0], [0.0]), ([1.0], [1.3])]
        self.c1b = [([-1.0], [-2.0]), ([-1.0], [0.0]), ([-1.0], [2.0])]
        self.c2 = [([-1.0], [-2.0]), ([-1.0], [0.0]), ([-1.0], [2.0])]

    def choose(self, elem):
        # elem is like ([], [])
        exp0 = (sum(elem[0])) / len(elem[0])
        exp1 = (sum(elem[1])) / len(elem[1])
        if exp0 == exp1 or random.random() < 0.01:
            return random.choice([0, 1])
        else:
            return int(exp1 > exp0)

    def decision0(self, card):
        return self.choose(self.c0[card-1])

    def decision1c(self, card):
        return self.choose(self.c1c[card-1])

    def decision1b(self, card):
        return self.choose(self.c1b[card-1])

    def decision2(self, card):
        return self.choose(self.c2[card-1])

    def result_ww(self, pos, cards):
        won = (cards[pos] > cards[1-pos])
        move = 1.0 if won else -1.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1][0].append(move)
        elif pos == 1:
            self.c1c[card - 1][0].append(move)

    def result_wbf(self, pos, card):
        move = 1.0 if pos == 1 else -1.0
        if pos == 0:
            self.c0[card - 1][0].append(move)
            self.c2[card - 1][0].append(move)
        if pos == 1:
            self.c1c[card - 1][1].append(move)

    def result_wbc(self, pos, cards):
        won = (cards[pos] > cards[1 - pos])
        move = 2.0 if won else -2.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1][0].append(move)
            self.c2[card - 1][1].append(move)
        elif pos == 1:
            self.c1c[card - 1][1].append(move)

    def result_bf(self, pos, card):
        move = 1.0 if pos == 0 else -1.0
        if pos == 0:
            self.c0[card - 1][1].append(move)
        if pos == 1:
            self.c1b[card - 1][0].append(move)

    def result_bc(self, pos, cards):
        won = (cards[pos] > cards[1 - pos])
        move = 2.0 if won else -2.0
        card = cards[pos]
        if pos == 0:
            self.c0[card - 1][1].append(move)
        elif pos == 1:
            self.c1b[card - 1][1].append(move)
