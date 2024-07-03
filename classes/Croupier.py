from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.DataFrameML import DataFrameML
from operator import itemgetter
from random import choice

class Croupier(object):
    cards = []
    players = []
    weights = []

    player = None
    data_frame_ml = DataFrameML()
    deck = Deck()

    weight = 0
    amount = 0
    idx_players = 0

    exchange = ''

    def __init__(self):
        pass

    def play(self):
        print()

        self.set_players_nicknames()

        print()

        #########################################################

        # # # Dla testowania wybranych uklaldow
        # self.set_cards()
        # player1 = Player(self.deck, cards = self.cards)
        # player1.get_arrangements().set_cards(self.cards)
        # player1.print()
        # player1.get_arrangements().check_arrangement()


        # player1.cards_permutations()
        #
        # for idx in range(0, len(player1.all_combs)):
        #     for idx1 in range(0, len(player1.all_combs[idx])):
        #         player1.all_combs[idx][idx1].print()
        #     print()
        #
        # player1.get_arrangements().check_arrangement()
        # player1.get_arrangements().print()

        #########################################################

        # # Dla testowania wybranych uklaldow
        # self.set_cards()
        # player1 = Player(cards=self.cards, if_deck=False)
        # player1.print()
        # player1.get_arrangements().check_arrangement()
        # player1.get_arrangements().set_weights()
        # print(player1.get_arrangements().get_weight())

        #########################################################
        #self.player.get_arrangements().init_data_frame_ml_before_ex()
        self.cards_check_exchange_add_weights()

        print()
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print()

        for self.player in self.players:
            self.player.print()
            self.player.get_arrangements().check_arrangement()
            self.player.get_arrangements().set_weights()
            self.player.get_arrangements().init_data_frame_ml_after_ex()

        print("Wagi ukladow graczy: ", self.weights)
        self.compare_players_weights()

    def set_cards(self):
        self.cards = [Card("2", "Ka"),
                      Card("3", "Tr"),
                      Card("4", "Ki"),
                      Card("5", "Pi"),
                      Card("7", "Tr")]

    def set_players_nicknames(self):
        #self.idx_players = int(input("Ilu graczy: "))
        self.idx_players = 2

        for idx in range(int(self.idx_players)):
            #nick = str(input("Pseudonim gracza: "))
            if idx == 0:
                nick = 'Nick'
            if idx == 1:
                nick = 'Adam'

            self.players.append(Player(deck = self.deck, nick = nick, index = idx, if_deck = True))

        self.deck.print()


    def cards_check_exchange_add_weights(self):
        for self.player in self.players:
            self.player.print()
            self.player.get_arrangements().check_arrangement()
            self.player.get_arrangements().set_weights()
            self.player.get_arrangements().set_data_frame_ml(DataFrameML(self.player.get_arrangements().get_id(), self.player.get_arrangements().get_weight()))
            print()

            self.weights.append(self.player.get_arrangements().get_weight())
            print(self.player.get_arrangements().get_weight())

            #self.exchange = str(input("Wymiana kart [T/N]: ")).lower()
            #self.exchange = choice(['t', 'n'])
            self.exchange = 't'
            print("Wymiana kart: ", self.exchange)
            if self.exchange == 't':
                self.cards_exchange()
            if self.exchange == 'n':
                pass

            print()
            print("------------------------------------------------------------")
            print()

    def deal_cards(self):
        for idx in range(self.amount):
            self.player.take_cards(self.deck)

    def cards_exchange(self):
        #self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))
        self.amount = choice(list(range(0, 6)))
        print("Ile kart do wymiany: ", self.amount)
        print()

        if self.amount == -1:
            return

        self.amount = self.player.return_to_croupier(self.amount)

        self.deal_cards()

        self.player.get_arrangements().set_cards(self.player.get_cards())

        print()
        print("------------------------------------------------------------")
        print()

        self.player.print()
        self.player.get_arrangements().check_arrangement()

        self.player.get_arrangements().set_weights()
        self.player.get_arrangements().get_data_frame_ml().set_exchange(self.exchange)
        self.player.get_arrangements().init_data_frame_ml_after_ex()

    def compare_players_weights(self):
        max_weight = list(max(enumerate(self.weights), key = itemgetter(1)))
        print("Wieksza waga: ", max_weight)

        print()
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print()

        for self.player in self.players:

            if self.player.index == max_weight[0]:
                print("WYGRANA")
                self.player.get_arrangements().set_cards(self.player.get_cards())
                self.player.win_or_not = True
                self.player.print()
                self.player.get_arrangements().check_arrangement()
            else:
                self.player.win_or_not = False

            self.player.get_arrangements().get_data_frame_ml().set_win_or_not(self.player.win_or_not)

        for self.player in self.players:
            self.player.get_arrangements().get_data_frame_ml().print()







