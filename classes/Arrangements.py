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
from arrangements.HelperArrangement import HelperArrangement

import itertools
class Arrangements(object):
    cards = []
    weights = []
    part_weights = []
    ids_arr = []
    arrangements = []
    data_frame_ml = DataFrameML()
    helper_arrangement = HelperArrangement()
    
    
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
        
        self.arrangements = [self.high_card, self.one_pair, self.two_pairs, self.three_of_a_kind,
                          self.straight, self.color, self.full, self.carriage, self.straight_royal_flush] 
               

    def set_cards(self, cards):                
        for x in self.arrangements:
            x.set_cards(cards)

    def set_weights(self):
        self.weights = []
        
        for x in self.arrangements:
            self.weights.append(x.get_weight())

        # Zwraca None, gdy niema potrzeby okreslania czesciowej wagi ukladu
        self.part_weights = []
        
        for x in self.arrangements:
            self.part_weights.append(x.get_part_weight())
        
        print(self.part_weights)
        
    def check_arrangement(self):
        self.ids_arr = []
        
        for x in self.arrangements:
            x.set_rand_int(self.rand_int)
            self.ids_arr.append(x.arrangement_recogn()) 
        
        print(self.ids_arr)

    def set_rand_int(self, rand_int):
        self.rand_int = rand_int
        
    def get_cards(self):
        return self.cards

    def get_data_frame_ml(self):
        return self.data_frame_ml

    def set_data_frame_ml(self, data_frame_ml = DataFrameML()):
        self.data_frame_ml = data_frame_ml

    def init_data_frame_ml_before_ex(self):          
        self.data_frame_ml.set_id_arr_after(self.get_id())
        self.data_frame_ml.set_weight_after_ex(self.get_weight())
        self.data_frame_ml.set_which_cards(self.get_part_weight())
        self.data_frame_ml.set_weight_ex(self.get_part_weight_sum(self.part_weights))

    def init_data_frame_ml_after_ex(self):          
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
        if not part_cards:
            return 0

        part_weight = part_cards.pop()
        
        if part_weight is None:
            return 0
        
        return part_weight + self.get_part_weight_sum(part_cards)

    def get_id(self):
        for id_arr in self.ids_arr:
            if id_arr is not None:
                return id_arr

    def print(self):
        for idx in self.cards:
            idx.print()