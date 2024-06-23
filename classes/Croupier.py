from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
class Croupier(object):
    cards = []
    player1 = None
    player2 = None
    def __init__(self):
        self.deck = Deck()
        self.cards = [Card("4", "Ka"),
                      Card("2", "Pi"),
                      Card("K", "Tr"),
                      Card("K", "Ka"),
                      Card("K", "Ki")]

        self.player1 = Player('Nick', self.deck, False)
        self.player2 = Player('Tom', self.deck, False)

    ###############################################ZROBIC KOMENTARZE DO HIGH_CARD I ONE_PAIR I THREE_OF_A_KIND
    def print(self):
        self.player1.give_cards(0, self.cards)
        #self.player2.give_cards(1)
        #print("Deck: ", len(self.deck.cards))
        #self.deck.print()
        self.player1.print()
        self.player2.print()

        #self.player1.cards_permutations()
        self.player1.print_arrangement()

        #self.player1.print_arrangement()

        #print()
        #self.player1.print()
        #self.player2.check_arrangement()
        #self.player2.print_arrangement()