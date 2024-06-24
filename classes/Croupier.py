from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
class Croupier(object):
    cards = []
    player1 = None
    player2 = None
<<<<<<< Updated upstream
=======
    player = None
    players = []
    weights = []
    amount = 0

>>>>>>> Stashed changes
    def __init__(self):
        self.deck = Deck()
<<<<<<< Updated upstream
        self.cards = [Card("4", "Ka"),
                      Card("2", "Pi"),
                      Card("K", "Tr"),
                      Card("K", "Ka"),
                      Card("K", "Ki")]
<<<<<<< Updated upstream
        self.player1 = Player('Nick', self.deck, False)
        self.player2 = Player('Tom', self.deck, False)
=======
        self.cards = [Card("10", "Ka"),
                      Card("2", "Pi"),
                      Card("Q", "Tr"),
                      Card("7", "Pi"),
                      Card("J", "Ka")]
        self.player1 = Player('Nick', self.deck, True)
        #self.player2 = Player('Tom', self.deck, True)
>>>>>>> Stashed changes
=======
        self.player1 = Player('Nick', self.deck, True)
        self.player2 = Player('Tom', self.deck, True)
>>>>>>> Stashed changes


    ###############################################ZROBIC KOMENTARZE DO HIGH_CARD I ONE_PAIR I THREE_OF_A_KIND
    def print(self):
        self.player1.give_cards(0, self.cards)
        #self.player2.give_cards(1)
        #print("Deck: ", len(self.deck.cards))
        #self.deck.print()
        self.player1.print()
        self.player2.print()

        #self.player1.cards_permutations()
<<<<<<< Updated upstream
        self.player1.print_arrangement()
=======
        #self.player1.print_arrangement()
>>>>>>> Stashed changes

<<<<<<< Updated upstream
        #print()
        #self.player1.print()
        #self.player2.check_arrangement()
        #self.player2.print_arrangement()
=======
        for self.player in self.players:
            self.player.print_arrangement()
            self.player.check_arrengement()
            self.weights.append(self.player.get_weight())
            print()

            while exchange := str(input("Wymiana kart [T/N]: ")).lower():
                if exchange == 't':
                    self.cards_exchange()
                if exchange == 'n':
                    break

            self.player.set_cards(self.player.get_cards())

        print()
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")

        for self.player in self.players:
            self.player.print_arrangement()
            self.player.check_arrengement()

        self.compare_players_weights()

    def deal_cards(self):
        for idx in range(self.amount):
            self.player.take_cards(self.deck)

    def cards_exchange(self, loop = True):
        while (loop):
            self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))
            print()

            if self.amount == -1:
                continue

            self.amount = self.player.return_to_croupier(self.amount)
            print(self.amount)

            if self.amount == -1:
                continue

            self.deal_cards()
            self.player.print_arrangement()
            self.player.check_arrengement()

            break

        print("------------------------------------------------------------")
        print()

    def compare_players_weights(self):
        for idx in self.weights:
            print(idx)

    def comp(self):
        pass
>>>>>>> Stashed changes
