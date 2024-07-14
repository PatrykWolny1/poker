import csv
import pandas as pd

class DataFrameML(object):

    
    def __init__(self, id_arr = 0, weight = 0, exchange = '', id_arr_after = -1, which_cards = [], win_or_not = None):
        self.id_arr = id_arr
        self.weight = weight
        self.idx = 0
        self.idx_ex = 0
        self.weight_ex = 0
        self.weight_after_ex = 0
        self.id_arr_after = 0
        self.cards_exchanged = {}

        self.exchange = ''

        self.cards_after = {}

        self.win_or_not = None
        
    def set_win_or_not(self, win_or_not):
        self.win_or_not = win_or_not

    def set_weight_after_ex(self, weight_after_ex):
        self.weight_after_ex = weight_after_ex

    def set_weight_ex(self, weight_ex):
        self.weight_ex = weight_ex

    def set_exchange(self, exchange):
        self.exchange = exchange

    def set_id_arr_after(self, id_arr_after):
        self.id_arr_after = id_arr_after

    def set_cards_after(self, cards_after):
        self.idx += 1
        self.cards_after.update({"Cards After " + str(self.idx) : cards_after})
    
    def set_cards_exchanged(self, cards):
        self.idx_ex += 1
        self.cards_exchanged.update({"Cards Exchanged " + str(self.idx_ex) : cards})
    
    def clear_dict_idx(self):
        self.which_cards.clear()
        self.idx = 0

    def print(self):
        print(self.id_arr, self.weight, self.exchange, self.id_arr_after, 
              self.weight_after_ex, self.cards_after, self.win_or_not)
        
    def save_to_csv(self, filename):
        data = {"Arrangement ID" : self.id_arr, 
                "Weight" : self.weight,
                "Exchange" : self.exchange, 
                "Arrangement ID (After)" : self.id_arr_after, 
                "Weight (After)" : self.weight_after_ex, 
                "Win" : self.win_or_not
               }
        data.update(self.cards_after)
        data.update(self.cards_exchanged)

        df = pd.DataFrame([data])
        temp = df.pop("Win")
        df.insert(len(data) - 1, "Win", temp)
        
        pd.set_option('display.max_columns', 16)

        print(df)
                
        csv_file_path = filename 
    
        df.to_csv(csv_file_path, mode = 'a', index=False, header = False)        
                
        

