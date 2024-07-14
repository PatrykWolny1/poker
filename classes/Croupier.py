from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.DataFrameML import DataFrameML
from decision_tree_structure.Node import Node
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
from operator import itemgetter
from random import choice
import numpy as np

class Croupier(object):

    def __init__(self):
        self.data_frame_ml:DataFrameML = DataFrameML()
        self.deck:Deck = Deck()
        self.cards:list = []
        self.players:list = []
        self.weights:list = []
        
        self.weight:int = 0
        self.amount:int = 0
        self.idx_players:int = 0
        
        self.exchange:str = ''
    def play(self):        
        print()
        
        # self.set_cards()
        # self.set_players_nicknames()
            
        print()
        
        #########################################################

        # # Dla testowania wybranych uklaldow
        # self.set_cards()
        # player1 = Player(self.deck, cards = self.cards)
        # player1.arrangements.set_cards(self.cards)
        # player1.print()
        # player1.arrangements.check_arrangement()

        player1 = Player(deck=self.deck, perm_logic=True)
        player1.cards_permutations()

        # for idx in range(0, len(player1.all_combs)):
        #     for idx1 in range(0, len(player1.all_combs[idx])):
        #         player1.all_combs[idx][idx1].print()
        #     print()

        player1.arrangements.print()
        print()
        player1.arrangements.check_arrangement()

        #########################################################
        #########################################################
        # self.weights_cards = []
        # for idx in range(0, len(self.cards)):
        #     self.weights_cards.append(self.cards[idx].weight)
            
            
        # #self.one_pair_strategy = OnePairStructureStrategy(cards=self.weights)
        
        # self.root = OnePairStructureStrategy(cards=self.weights_cards)
        # self.root.show_tree()
        # print(str(self.root.root_object))

        # #self.root_visited = OnePairStructureStrategy(cards=self.weights).root_object
        
        # self.cards_check_exchange_add_weights()
        
        # print()
        # print("------------------------------------------------------------")
        # print("------------------------------------------------------------")
        # print()
        
        # for self.player in self.players:
        #     self.player.print(False)
        #     self.player.arrangements.check_arrangement()
        #     self.player.arrangements.set_weights()
        
        # print("Wagi ukladow graczy: ", self.weights)
        # self.compare_players_weights()
        
        # print(self.amount, self.exchange)
        # self.root.show_tree(True, self.amount, self.exchange)
        # print(str(self.root.root_object))

    def set_cards(self):
        self.cards = [Card("2", "Ka"),
                      Card("2", "Pi"),
                      Card("9", "Ka"),
                      Card("5", "Tr"),
                      Card("7", "Ki")]

    def set_players_nicknames(self):
        #self.idx_players = int(input("Ilu graczy: "))
        self.idx_players = 2

        for idx in range(int(self.idx_players)):
            #nick = str(input("Pseudonim gracza: "))
            if idx == 0:
                nick = 'Nick'
            if idx == 1:                                            #carriage lub full 
                nick = 'Adam'
                
            self.players.append(Player(deck=self.deck, nick=nick, index=idx, if_deck=False, cards=self.cards))
            
        # self.deck.print()

    def cards_check_exchange_add_weights(self):
        for self.player in self.players:
            self.player.print(False)
            self.player.arrangements.check_arrangement()
            self.player.arrangements.set_weights()
            self.player.arrangements.data_frame_ml = DataFrameML(self.player.arrangements.get_id(), 
                                                                 self.player.arrangements.get_weight())
            print()

            self.weights.append(self.player.arrangements.get_weight())
            #print(self.player.arrangements.get_weight())

            #self.exchange = str(input("Wymiana kart [T/N]: ")).lower()
            #self.exchange = choice(['t', 'n'])
            
            
            self.exchange = np.random.choice(['n', 't'], size=1, p=[float(self.root.root_object.internal_nodes[0][0].branches[0]),
                                                                    float(self.root.root_object.internal_nodes[0][0].branches[1])])    
            print(self.exchange)
            #self.exchange = 't'
            print("Wymiana kart: ", self.exchange)
            
            if self.exchange == 't':
                self.cards_exchange()
            if self.exchange == 'n':
                self.player.arrangements.data_frame_ml.exchange = self.exchange

            [self.player.arrangements.data_frame_ml.set_cards_exchanged(card.weight) for card in self.player.cards_exchanged]

            print()
            print("------------------------------------------------------------")
            print()

    def deal_cards(self):
        for idx in range(self.amount):
            self.player.take_cards(self.deck)

    def cards_exchange(self):
        #self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))
        #self.amount = choice(list(range(0, 6)))
        
        self.amount = np.random.choice([2, 3], size=1, p=[float(self.root.root_object.internal_nodes[1][0].branches[0]),
                                                          float(self.root.root_object.internal_nodes[1][0].branches[1])])    
          
        self.amount = int(self.amount)
        print("Ile kart do wymiany: ", self.amount)
        print()

        if self.amount == -1:
            return

        self.amount = self.player.return_to_croupier(self.amount)
        print(self.amount)
        self.deal_cards()

        self.player.arrangements.cards = self.player.cards

        print()
        print("------------------------------------------------------------")
        print()

        self.player.print(True)
        self.player.arrangements.check_arrangement()
        
        self.player.arrangements.set_weights()
        self.player.arrangements.data_frame_ml.exchange = self.exchange
        self.player.arrangements.init_data_frame_ml_after_ex()

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
                self.player.arrangements.set_cards(self.player.get_cards())
                self.player.win_or_not = True
                self.player.print(False)
                self.player.arrangements.check_arrangement()
            else:
                self.player.win_or_not = False

            self.player.arrangements.data_frame_ml.win_or_not = self.player.win_or_not

        for self.player in self.players:
            self.player.arrangements.get_data_frame_ml().print()
            self.player.arrangements.get_data_frame_ml().save_to_csv("poker_game.csv")







