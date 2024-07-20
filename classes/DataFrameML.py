import csv
import pandas as pd

class DataFrameML(object):
    
    def __init__(self, id_arr = 0, weight = 0, exchange = '', id_arr_after = 0, which_cards = [], win_or_not = None):
        self.id_arr:int = id_arr
        self.weight:int = weight
        self.idx:int = 0
        self.idx_ex:int = 0
        self.idx_bef:int = 0
        self.weight_ex:int = 0
        self.weight_after_ex:int = 0
        self.id_arr_after:int = 0
        self.exchange_amount:int = 0
        
        self.cards_before:dict = {}
        self.cards_exchanged:dict = {}
        self.cards_after:dict = {}
        
        self.exchange:str = ''
        self.win_or_not:bool = None

    def set_cards_after(self, cards_after):
        self.idx += 1
        #print(cards_after)
        self.cards_after.update({"Card After " + str(self.idx) : cards_after})
    
    def set_cards_exchanged(self, cards):
        self.idx_ex += 1
        self.cards_exchanged.update({"Cards Exchanged " + str(self.idx_ex) : cards})
    
    def set_cards_before(self, cards_before):
        self.idx_bef += 1
        self.cards_before.update({"Cards Before " + str(self.idx_bef) : cards_before})

    def set_exchange_amount(self, amount):
        self.exchange_amount = amount

    def set_id_arr_after(self, id_arr_after):
        self.id_arr_after = id_arr_after
    
    def print(self):
        print(self.id_arr, self.weight, self.cards_before, self.exchange, self.exchange_amount, self.id_arr_after, 
              self.weight_after_ex, self.cards_after, self.cards_exchanged, self.win_or_not)
        
    def save_to_csv(self, filename):
        data = {# "Arrangement ID" : self.id_arr, 
                # "Weight" : self.weight,
                "Exchange" : self.exchange,
                "Exchange Amount" : self.exchange_amount, 
                # "Arrangement ID (After)" : self.id_arr_after, 
                # "Weight (After)" : self.weight_after_ex, 
                "Win" : self.win_or_not
               }
        data.update(self.cards_before)
        # data.update(self.cards_after)
        data.update(self.cards_exchanged)

        df = pd.DataFrame([data])
        temp = df.pop("Win")
        df.insert(len(data) - 1, "Win", temp)
        
        pd.set_option('display.max_columns', 16)

        #print(df)
                
        csv_file_path = filename 
    
        df.to_csv(csv_file_path, mode = 'a', index=False, header = False)        
                
        

