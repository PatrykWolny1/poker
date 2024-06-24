from arrangements.StraightRoyalFlush import StraightRoyalFlush
from arrangements.Carriage import Carriage
from arrangements.Full import Full
from arrangements.Color import Color
from arrangements.Straight import Straight
from arrangements.ThreeOfAKind import ThreeOfAKind
from arrangements.TwoPairs import TwoPairs
from arrangements.OnePair import OnePair
from arrangements.HighCard import HighCard

import itertools
class Arrangements(object):
    cards = []
    weights = []
    def __init__(self, cards = []):
        self.cards = cards
        self.straight_royal_flush = StraightRoyalFlush()
        self.carriage = Carriage()
        self.full = Full()
        self.color = Color()
        self.straight = Straight()
        self.three_of_a_kind = ThreeOfAKind()
        self.two_pairs = TwoPairs()
        self.one_pair = OnePair()
        self.high_card = HighCard()

    def set_cards(self, cards):
        self.cards = cards
        self.straight_royal_flush.set_cards(self.cards)
        self.carriage.set_cards(self.cards)
        self.full.set_cards(self.cards)
        self.color.set_cards(self.cards)
        self.straight.set_cards(self.cards)
        self.three_of_a_kind.set_cards(self.cards)
        self.two_pairs.set_cards(self.cards)
        self.one_pair.set_cards(self.cards)
        self.high_card.set_cards(self.cards)

<<<<<<< HEAD
    def get_weight(self):
        self.weights = []
=======
<<<<<<< Updated upstream
=======
    def get_weight(self):
        self.weights = []
        self.weights.append(self.straight_royal_flush.get_weight())
        self.weights.append(self.carriage.get_weight())
        self.weights.append(self.full.get_weight())
        self.weights.append(self.color.get_weight())
        self.weights.append(self.straight.get_weight())
        self.weights.append(self.three_of_a_kind.get_weight())
        self.weights.append(self.two_pairs.get_weight())
>>>>>>> hotfix
        self.weights.append(self.high_card.get_weight())
        self.weights.append(self.one_pair.get_weight())

        for idx in self.weights:
            if idx is not None:
                return idx

<<<<<<< HEAD
=======
>>>>>>> Stashed changes
>>>>>>> hotfix
    def check_arrangement(self):
        self.straight_royal_flush.straight_royal_flush()
        self.carriage.carriage()
        self.full.full()
        self.color.color()
        self.straight.straight()
        self.three_of_a_kind.three_of_a_kind()
        self.two_pairs.two_pairs()
        self.one_pair.one_pair()
        self.high_card.high_card()

    def print(self):
        for idx in self.cards:
            idx.print()
        print()