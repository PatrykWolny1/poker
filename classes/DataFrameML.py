import csv
import pandas as pd

class DataFrameML(object):
    idx = 0
    id_arr = 0
    weight = 0
    weight_ex = 0
    weight_after_ex = 0
    id_arr_after = 0

    exchange = ''

    which_cards = {}

    win_or_not = None
    
    def __init__(self, id_arr = 0, weight = 0, exchange = '', id_arr_after = -1, which_cards = [], win_or_not = None):
        self.id_arr = id_arr
        self.weight = weight

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

    def set_which_cards(self, which_cards):
        self.idx += 1
        self.which_cards.update({"Cards Exchanged " + str(self.idx) : which_cards})
        
    def clear_dict_idx(self):
        self.which_cards.clear()
        self.idx = 0

    def print(self):
        print(self.id_arr, self.weight, self.exchange, self.id_arr_after, 
              self.weight_after_ex, self.which_cards, self.win_or_not)
        
    def save_to_csv(self, filename):
        data = {"Arrangement ID" : self.id_arr, 
                "Weight" : self.weight,
                "Exchange" : self.exchange, 
                "Arrangement ID (After)" : self.id_arr_after, 
                "Weight (After)" : self.weight_after_ex, 
                "Win" : self.win_or_not
               }
        data.update(self.which_cards)

        df = pd.DataFrame([data])
        temp = df.pop("Win")
        df.insert(len(data) - 1, "Win", temp)

        print(df)
        
        csv_file_path = filename 
                
        df.to_csv(csv_file_path, mode = 'a', index=True, index_label= "Index", header = False)
    
        self.idx += 1
        
                
        

