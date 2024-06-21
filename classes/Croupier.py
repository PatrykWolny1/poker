from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
class Croupier(object):
    cards = []
    player1 = None
    def __init__(self):
        self.deck = Deck()
        self.cards = [Card("K", "Ki"),
                      Card("K", "Pi"),
                      Card("K", "Ka"),
                      Card("10", "Tr"),
                      Card("9", "Pi")]
        self.player1 = Player('Nick', self.deck, False)
        self.player2 = Player('Tom', self.deck, False)

    def print(self):
        #self.player1.give_cards(0, self.cards)
        #self.player2.give_cards(1)
        #print("Deck: ", len(self.deck.cards))
        #self.deck.print()
        #self.player1.print()

        self.player1.cards_permutations()
        self.player1.print_arrangement()

        #print()
        #self.player1.print()
        #self.player2.check_arrangement()
        #self.player2.print_arrangement()