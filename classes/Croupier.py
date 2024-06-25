from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
from operator import itemgetter

class Croupier(object):
    cards = []
    players = []
    weights = []

    player = None

    weight = 0
    amount = 0
    idx_players = 0

    def __init__(self):
        self.deck = Deck()

    ###############################################ZROBIC KOMENTARZE DO HIGH_CARD I ONE_PAIR I THREE_OF_A_KIND

    def play(self):
        # print()
        #
        # self.set_players_nicknames()
        #
        # print()

        self.set_cards()
        player1 = Player(self.deck, self.cards)
        player1.get_arrangements().set_cards(self.cards)
        player1.print()
        player1.get_arrangements().check_arrangement()


        # self.cards_check_exchange_add_weights()
        #
        # print()
        # print("------------------------------------------------------------")
        # print("------------------------------------------------------------")
        #
        # for self.player in self.players:
        #     self.player.get_arrangements().set_cards(self.player.get_cards())
        #     self.player.print()
        #     self.player.get_arrangements().check_arrangement()
        #
        # print(self.weights)
        #
        # self.compare_players_weights()

    def set_cards(self):
        self.cards = [Card("K", "Ka"),
                      Card("K", "Pi"),
                      Card("A", "Tr"),
                      Card("A", "Ka"),
                      Card("Q", "Ki")]

    def set_players_nicknames(self):
        self.idx_players = int(input("Ilu graczy: "))

        for idx in range(self.idx_players):
            nick = str(input("Pseudonim gracza: "))
            self.players.append(Player(self.deck, nick, idx, True))

    def cards_check_exchange_add_weights(self):
        for self.player in self.players:
            self.player.print()
            self.player.get_arrangements().check_arrangement()
            print()

            exchange = str(input("Wymiana kart [T/N]: ")).lower()
            if exchange == 't':
                self.cards_exchange()
            if exchange == 'n':
                pass

            self.weights.append(self.player.get_weight())
            print(self.player.get_weight())

            print()
            print("------------------------------------------------------------")
            print()

    def deal_cards(self):
        for idx in range(self.amount):
            self.player.take_cards(self.deck)
        self.player.get_arrangements().set_cards(self.player.get_cards())

    def cards_exchange(self):
        self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))

        print()

        if self.amount == -1:
            return

        self.amount = self.player.return_to_croupier(self.amount)

        self.deal_cards()

        print()
        print("------------------------------------------------------------")
        print()

        #self.player.get_arrangements().set_cards(self.player.get_cards())
        self.player.print()
        self.player.get_arrangements().check_arrangement()


    def compare_players_weights(self):
        max_weight = list(max(enumerate(self.weights), key = itemgetter(1)))
        print(max_weight)

        print("------------------------------------------------------------")
        print("------------------------------------------------------------")

        for self.player in self.players:
            if self.player.index == max_weight[0]:
                print("WYGRANA")
                self.player.get_arrangements().set_cards(self.player.get_cards())
                self.player.print()
                self.player.get_arrangements().check_arrangement()



