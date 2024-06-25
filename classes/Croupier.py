from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
from operator import itemgetter

class Croupier(object):
    cards = []
    player1 = None
    player2 = None
    player = None
    players = []
    weights = []
    amount = 0
    idx_players = 0

    player = None
    players = []
    weight = 0
    amount = 0

    def __init__(self):
        self.deck = Deck()
        self.cards = [Card("4", "Ka"),
                      Card("2", "Pi"),
                      Card("K", "Tr"),
                      Card("K", "Ka"),
                      Card("K", "Ki")]

        #self.player1 = Player('Nick', self.deck, True)
        #self.player2 = Player('Tom', self.deck, True)

    ###############################################ZROBIC KOMENTARZE DO HIGH_CARD I ONE_PAIR I THREE_OF_A_KIND

    def play(self):
        print()

        self.idx_players = int(input("Ilu graczy: "))

        for idx in range(self.idx_players):
            nick = str(input("Pseudonim gracza: "))
            self.players.append(Player(nick, idx, self.deck, True))

        #self.player1.give_cards(0, self.cards)
        #print("Deck: ", len(self.deck.cards))
        #self.deck.print()

        print()

        for self.player in self.players:
            self.player.print_arrangement()
            self.player.check_arrangement()
            print()

            exchange = str(input("Wymiana kart [T/N]: ")).lower()
            if exchange == 't':
                self.cards_exchange()
            if exchange == 'n':
                break

            self.player.get_weights_arrangement()
            self.weights.append(self.player.get_weight())
            print(self.weight)

            print()
            print("------------------------------------------------------------")
            print()

        print()
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")

        for self.player in self.players:
            self.player.set_cards_arrangement(self.player.get_cards())
            self.player.print_arrangement()
            self.player.check_arrangement()

            print(self.player.weight)

        print(self.weights)

        self.compare_players_weights()

    def deal_cards(self):
        for idx in range(self.amount):
            self.player.take_cards(self.deck)

    def cards_exchange(self):
        self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))

        print()

        if self.amount == -1:
            return

        self.amount = self.player.return_to_croupier(self.amount)
        print(self.amount)

        self.deal_cards()

        self.player.set_cards_arrangement(self.player.get_cards())
        self.player.print_arrangement()
        self.player.check_arrangement()

    def compare_players_weights(self):
        max_weight = list(max(enumerate(self.weights), key = itemgetter(1)))
        print(max_weight)

        for self.player in self.players:
            if self.player.index == max_weight[0]:
                print("WYGRANA")
                self.player.set_cards_arrangement(self.player.get_cards())
                self.player.print_arrangement()
                self.player.check_arrangement()



