from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
class Croupier(object):
    cards = []
    player1 = None
    player2 = None
    amount = 0

    def __init__(self):
        self.deck = Deck()
        self.cards = [Card("4", "Ka"),
                      Card("2", "Pi"),
                      Card("K", "Tr"),
                      Card("K", "Ka"),
                      Card("K", "Ki")]

        self.player1 = Player('Nick', self.deck, True)
        self.player2 = Player('Tom', self.deck, True)

    ###############################################ZROBIC KOMENTARZE DO HIGH_CARD I ONE_PAIR I THREE_OF_A_KIND

    def play(self):
        loop = True
                
        while (True):
            #self.player1.give_cards(0, self.cards)
            #print("Deck: ", len(self.deck.cards))
            #self.deck.print()
            exchange = str(input("Wymiana kart [T/N]: "))

            if exchange.lower() == 't':
                loop = True
            if exchange.lower() == 'n':
                break

            print()
            while (loop):
                self.player1.print_arrangement()
                print()

                self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))
                print()

                if self.amount == -1:
                    break

                self.amount = self.player1.return_to_croupier(self.amount)
                print(self.amount)

                if self.amount == -1:
                    continue

                self.deal_cards()
                self.player1.print_arrangement()

                #print()
                #self.deck.print()

                # self.player2.print()
                # self.player2.give_cards(1)

                #self.player1.cards_permutations()

                #self.player2.check_arrangement()
                #self.player2.print_arrangement()

    def deal_cards(self):
        for idx in range(self.amount):
            self.player1.take_cards(self.deck)
