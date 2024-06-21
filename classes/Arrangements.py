from classes.Card import Card
from arrangements.StraightRoyalFlush import StraightRoyalFlush
from arrangements.Carriage import Carriage
from arrangements.Full import Full
from arrangements.Color import Color
from arrangements.Straight import Straight
from arrangements.ThreeOfAKind import ThreeOfAKind
from arrangements.TwoPairs import TwoPairs

import itertools
class Arrangements(object):
    cards = []
    wgt = 0
    carriage = None

    def __init__(self, cards = []):
        self.cards = cards
        self.straight_royal_flush = StraightRoyalFlush()
        self.carriage = Carriage()
        self.full = Full()
        self.color = Color()
        self.straight = Straight()
        self.three_of_a_kind = ThreeOfAKind()
        self.two_pairs = TwoPairs()

    def set_cards(self, cards):
        self.cards = cards
        self.straight_royal_flush.set_cards(self.cards)
        self.carriage.set_cards(self.cards)
        self.full.set_cards(self.cards)
        self.color.set_cards(self.cards)
        self.straight.set_cards(self.cards)
        self.three_of_a_kind.set_cards(self.cards)
        self.two_pairs.set_cards(self.cards)

    def if_the_same(self):
        #self.carriage_generating()
        #self.full_generating()
        #self.straight_generating()

        #self.cards = []
        #self.cards.append(Card("A"))
        #self.cards.append(Card("J"))
        #self.cards.append(Card("J"))
        #self.cards.append(Card("J"))
        #self.cards.append(Card("J"))

        #self.get_indicies()
        pass
    def check_arrangement(self):
        self.straight_royal_flush.straight_royal_flush()
        self.carriage.carriage()
        self.full.full()
        self.color.color()
        self.straight.straight()
        self.three_of_a_kind.three_of_a_kind()
        self.two_pairs.two_pairs()

    def print(self):
        for idx in self.cards:
            idx.print()
        print()