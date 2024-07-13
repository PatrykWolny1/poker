from classes.Card import Card
import random

class Deck(object):
    # markings = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    # colors = ('Ki', 'Tr', 'Ka', 'Pi')
    # weight = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    #cards = []
    # counter = 0

    def __init__(self):
        self.markings = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        self.colors = ('Ki', 'Tr', 'Ka', 'Pi')
        self.weight = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
        self.cards = []
        for color in self.colors:
            for marking in self.markings:
                self.cards.append(Card(marking, color))
        self.counter = 0
    def print(self):
        for i in range(len(self.cards)):
            print(i + 1, self.cards[i].print_str())
        print()

    def shuffling(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards[self.counter]
        self.cards.pop(self.counter)
        self.counter = self.counter + 1
        return card
