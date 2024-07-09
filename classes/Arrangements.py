from arrangements.StraightRoyalFlush import StraightRoyalFlush
from arrangements.Carriage import Carriage
from arrangements.Full import Full
from arrangements.Color import Color
from arrangements.Straight import Straight
from arrangements.ThreeOfAKind import ThreeOfAKind
from arrangements.TwoPairs import TwoPairs
from arrangements.OnePair import OnePair
from arrangements.HighCard import HighCard
from classes.DataFrameML import DataFrameML

import itertools
class Arrangements(object):
    cards = []
    weights = []
    part_weights = []
    ids_arr = []
    data_frame_ml = DataFrameML()
    
    rand_int = 0    
    def __init__(self, cards = []):
        self.id_arr = 0
        self.data_frame_ml = DataFrameML()
        self.cards = cards

        self.high_card = HighCard()
        self.one_pair = OnePair()
        self.two_pairs = TwoPairs()
        self.three_of_a_kind = ThreeOfAKind()
        self.straight = Straight()
        self.color = Color()
        self.full = Full()
        self.carriage = Carriage()
        self.straight_royal_flush = StraightRoyalFlush()        

    def set_cards(self, cards):
        self.cards = cards
        self.straight_royal_flush.set_cards(self.cards)
        self.carriage.set_cards(self.cards)
        self.full.set_cards(self.cards)
        self.color.set_cards(self.cards)
        self.straight.set_cards(self.cards)
        self.three_of_a_kind.set_cards(self.cards)
        self.two_pairs.set_cards(self.cards)
        self.one_pair.set_cards(self.cards)
        self.high_card.set_cards(self.cards)

    def set_weights(self):
        self.weights = []
        self.weights.append(self.high_card.get_weight())
        self.weights.append(self.one_pair.get_weight())
        self.weights.append(self.two_pairs.get_weight())
        self.weights.append(self.three_of_a_kind.get_weight())
        self.weights.append(self.straight.get_weight())
        self.weights.append(self.color.get_weight())
        self.weights.append(self.full.get_weight())
        self.weights.append(self.carriage.get_weight())
        self.weights.append(self.straight_royal_flush.get_weight())


        # Zwraca None, gdy niema potrzeby okreslania czesciowej wagi ukladu
        self.part_weights = []
        self.part_weights.append(self.high_card.get_part_weight())
        self.part_weights.append(self.one_pair.get_part_weight())
        self.part_weights.append(self.two_pairs.get_part_weight())
        self.part_weights.append(self.three_of_a_kind.get_part_weight())
        self.part_weights.append(self.straight.get_part_weight())
        self.part_weights.append(self.color.get_part_weight())
        self.part_weights.append(self.full.get_part_weight())
        self.part_weights.append(self.carriage.get_part_weight())
        self.part_weights.append(self.straight_royal_flush.get_part_weight())
        print(self.part_weights)

    def check_arrangement(self):
        self.ids_arr = []
        
        
        self.ids_arr.append(self.high_card.high_card())
        
        
        self.ids_arr.append(self.one_pair.one_pair(True))
        
        self.two_pairs.set_rand_int(self.rand_int)
        self.ids_arr.append(self.two_pairs.two_pairs())
        
        self.three_of_a_kind.set_rand_int(self.rand_int)
        self.ids_arr.append(self.three_of_a_kind.three_of_a_kind())
        
        self.straight.set_rand_int(self.rand_int)
        self.ids_arr.append(self.straight.straight())
        
        self.color.set_rand_int(self.rand_int)
        self.ids_arr.append(self.color.color())
        
        self.full.set_rand_int(self.rand_int)
        self.ids_arr.append(self.full.full())
        
        self.carriage.set_rand_int(self.rand_int)
        self.ids_arr.append(self.carriage.carriage())
        
        self.straight_royal_flush.set_rand_int(self.rand_int)
        self.ids_arr.append(self.straight_royal_flush.straight_royal_flush())
        
        print(self.ids_arr)

    def set_rand_int(self, rand_int):
        self.rand_int = rand_int
        
    def get_cards(self):
        return self.cards

    def get_data_frame_ml(self):
        return self.data_frame_ml

    def set_data_frame_ml(self, data_frame_ml = DataFrameML()):
        self.data_frame_ml = data_frame_ml

    def init_data_frame_ml_after_ex(self):          ###########copy()
        self.data_frame_ml.set_id_arr_after(self.get_id())
        self.data_frame_ml.set_weight_after_ex(self.get_weight())
        self.data_frame_ml.set_which_cards(self.get_part_weight())
        self.data_frame_ml.set_weight_ex(self.get_part_weight_sum(self.part_weights))

    def get_weight(self):
        for weight in self.weights:
            if weight is not None:
                return weight

    def get_part_weight(self):
        for part_weight in self.part_weights:
            if part_weight is not None:
                return part_weight

    def get_part_weight_sum(self, part_cards):
        if not part_cards[self.get_id()]:
            return 0

        part_weight = part_cards[self.get_id()].pop()

        return part_weight + self.get_part_weight_sum(part_cards)

    def get_id(self):
        for id_arr in self.ids_arr:
            if id_arr is not None:
                return id_arr

    def print(self):
        for idx in self.cards:
            idx.print()