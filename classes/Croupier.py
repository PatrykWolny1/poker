from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.DataFrameML import DataFrameML
from decision_tree_structure.Node import Node
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
from operator import itemgetter
from random import choice
import numpy as np
import sys
import os


    
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
        self.game_visible:bool = False
        self.tree_visible:bool = True
            
    def play(self):        
        print()
        

        #self.set_cards()
        self.set_players_nicknames()
            
        print()
        
        #########################################################

        # # Dla testowania wybranych uklaldow
        # self.set_cards()
        # player1 = Player(self.deck, cards = self.cards)
        # player1.arrangements.set_cards(self.cards)
        # player1.print()
        # player1.arrangements.check_arrangement()

        #########################################################

        # player1 = Player(deck=self.deck, if_show_perm=True)
        # player1.cards_permutations()

        # # for idx in range(0, len(player1.all_combs)):
        # #     for idx1 in range(0, len(player1.all_combs[idx])):
        # #         player1.all_combs[idx][idx1].print()
        # #     print()

        # player1.arrangements.print()
        # print()
        # player1.arrangements.check_arrangement()

        #########################################################
        #########################################################
        #enablePrint()
        self.weights_cards = []
        
        self.one_pair_strategy = []
        self.num = 0
        self.amount_list = []
        self.exchange_list = []
        
        for self.player in self.players:
            if self.game_visible == True or self.game_visible == True:
                self.player.print(False)    
            self.player.arrangements.check_arrangement()

            self.player.arrangements.set_weights()
            
            self.weights_cards.append(self.player.arrangements.get_part_weight())

            self.one_pair_strategy.append(OnePairStructureStrategy(cards=self.weights_cards[self.num]))
            
            self.num += 1
        
        self.num = 0
        
        for strategy in self.one_pair_strategy:
            strategy.set_root(visited=False)
            strategy.build_tree()
            
            if self.game_visible == True:
                print(str(strategy.root))

        
        self.cards_check_exchange_add_weights()
        
        if self.game_visible == True:
            print()
            print("------------------------------------------------------------")
            print("------------------------------------------------------------")
            print()
        
        for self.player in self.players:
            if self.game_visible == True:
                self.player.print(False)
            self.player.arrangements.check_arrangement()
            self.player.arrangements.set_weights()
        
        if self.game_visible == True:
            print("Wagi ukladow graczy: ", self.weights)
            
        self.compare_players_weights()
        
        # self.one_pair_strategy[self.num].set_root(visited=True, amount=self.amount, exchange=self.exchange)
        # self.one_pair_strategy.build_tree()
        # print(str(self.one_pair_strategy.root))
        
        num_1 = 0

        if self.tree_visible == True:
            print("-"*100)
        #for amount, exchange in self.amount_list, self.exchange_list:
        for strategy in self.one_pair_strategy:
            if self.tree_visible == True:
                print("Liczba wymienionych kart: " + str(self.amount_list[num_1]) 
                    + "\nCzy wymienic? " + str(self.exchange_list[num_1]))
                print("\n")
                
            strategy.set_root(visited=True, amount=self.amount_list[num_1], exchange=self.exchange_list[num_1])
            strategy.build_tree()
            
            if self.tree_visible == True:
                print(str(strategy.root))
            
            if self.tree_visible == True:
                print("\n")
                print("-"*100)
            num_1 += 1

    def set_cards(self):
        self.cards = [[Card("2", "Ka"),
                      Card("5", "Pi"),
                      Card("9", "Ka"),
                      Card("2", "Tr"),
                      Card("7", "Ki")],
                      [Card("8", "Ka"),
                      Card("8", "Pi"),
                      Card("9", "Tr"),
                      Card("10", "Tr"),
                      Card("6", "Ki")]]
        
    def set_players_nicknames(self):
        #self.idx_players = int(input("Ilu graczy: "))
        self.idx_players = 2
    
        self.deck = Deck()
        
        cards, rand_int = Player().cards_permutations()

        for idx in range(int(self.idx_players)):
            #nick = str(input("Pseudonim gracza: "))
            if idx == 0:
                nick = 'Nick'
            if idx == 1:                                           
                nick = 'Adam'
                
            self.players.append(Player(deck=self.deck, perm=True, nick=nick, index=idx, cards=cards[idx],
                                       if_deck=False, if_show_perm=False))
            #self.deck.print()

    def cards_check_exchange_add_weights(self):
        for self.player in self.players:
            if self.game_visible == True:
                self.player.print(False)
                
            self.player.arrangements.check_arrangement()
            self.player.arrangements.set_weights()
            self.player.arrangements.data_frame_ml = DataFrameML(self.player.arrangements.get_id(), 
                                                                 self.player.arrangements.get_weight())
            if self.game_visible == True:
                print()

            #print(self.player.arrangements.get_weight())

            #self.exchange = str(input("Wymiana kart [T/N]: ")).lower()
            #self.exchange = choice(['t', 'n'])
            
            
            self.exchange = np.random.choice(['n', 't'], size=1, p=[float(self.one_pair_strategy[self.num].root.internal_nodes[0][0].branches[0]),
                                                                    float(self.one_pair_strategy[self.num].root.internal_nodes[0][0].branches[1])])    
            #self.exchange = 't'
            self.exchange_list.append(self.exchange)

            if self.game_visible == True:
                print(self.exchange)
                print("Wymiana kart: ", self.exchange)  
            

            if self.exchange == 't':
                self.cards_exchange()
            if self.exchange == 'n':
                self.player.arrangements.data_frame_ml.exchange = self.exchange
                self.amount_list.append(None)
            
            self.num += 1

            self.weights.append(self.player.arrangements.get_weight())
            [self.player.arrangements.data_frame_ml.set_cards_exchanged(card.weight) for card in self.player.cards_exchanged]

            if self.game_visible == True:
                print()
                print("------------------------------------------------------------")
                print()

    def deal_cards(self, cards_list:list = []):
        for idx in range(self.amount):
            self.player.take_cards(self.deck, cards_list)

    def cards_exchange(self):
        #self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))
        #self.amount = choice(list(range(0, 6)))
        
        self.amount = np.random.choice([2, 3], size=1, p=[float(self.one_pair_strategy[self.num].root.internal_nodes[1][0].branches[0]),
                                                          float(self.one_pair_strategy[self.num].root.internal_nodes[1][0].branches[1])])    
          
        self.amount = int(self.amount)
        self.amount_list.append(self.amount)
        
        if self.game_visible == True:
            print("Ile kart do wymiany: ", self.amount)
            print()

        if self.amount == -1:
            return

        self.amount = self.player.return_to_croupier(self.amount, 
                                                     self.player.arrangements.get_part_weight(), game_visible=False)
        if self.game_visible == True:
            print(self.amount)
        self.deal_cards()

        self.player.arrangements.set_cards(self.player.cards)
        
        if self.game_visible == True:
            print()
            print("------------------------------------------------------------")
            print()

            self.player.print(False)
            
        self.player.arrangements.check_arrangement()
        self.player.arrangements.set_weights()
        
        self.player.arrangements.data_frame_ml.exchange = self.exchange
        self.player.arrangements.init_data_frame_ml_after_ex()

    def compare_players_weights(self):
        max_weight = list(max(enumerate(self.weights), key = itemgetter(1)))
        
        if self.game_visible == True:
            print("Wieksza waga: ", max_weight)

            print()
            print("------------------------------------------------------------")
            print("------------------------------------------------------------")
            print()

        for self.player in self.players:

            if self.player.index == max_weight[0]:
                if self.game_visible == True:
                    print("WYGRANA")
                
                self.player.arrangements.set_cards(self.player.cards)
                self.player.win_or_not = True
                
                if self.game_visible == True:
                    self.player.print(False)
                
                self.player.arrangements.check_arrangement()
            else:
                self.player.win_or_not = False

            self.player.arrangements.data_frame_ml.win_or_not = self.player.win_or_not

        for self.player in self.players:
            if self.game_visible == False or self.game_visible == True:
                self.player.arrangements.get_data_frame_ml().print()
            self.player.arrangements.get_data_frame_ml().save_to_csv("poker_game.csv")







