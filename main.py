from classes.Croupier import Croupier
from classes.Player import Player
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
import time
import cProfile
import pstats
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def main():
    start_time = time.time()
    cards_1, rand_int_1, all_comb_perm = Player().cards_permutations()
    
    for i in range(0, 1):
        croupier = Croupier(all_comb_perm)
                
        croupier.play()
    
    end_time = time.time() - start_time
    with open("time.txt", "w") as file:
        file.write(str(end_time) + " sec\n")
    
    print()    
    print(end_time, " sec")
    
    df = pd.read_csv('poker_game.csv', on_bad_lines='skip', engine='python')
    pd.set_option('display.max_columns', 16)
    
    pd.options.display.float_format = '{:,.0f}'.format
    df = df.fillna('0')
    # df['Exchange'] = df['Exchange'].replace({'[\'t\']': True, '[\'n\']': False})
    
    df.loc[df['Exchange'] == '[\'t\']', 'Exchange'] = True
    df.loc[df['Exchange'] == '[\'n\']', 'Exchange'] = False


    df.loc[df['Exchange Amount'] == '[0]', 'Exchange Amount'] = 0
    
    df.loc[df[' Cards Exchanged 1'] == '', ' Cards Exchanged 1'] = 0
    df.loc[df[' Cards Exchanged 2'] == '', ' Cards Exchanged 2'] = 0
    df.loc[df[' Cards Exchanged 3'] == '', ' Cards Exchanged 3'] = 0



    #print(df.head().corr())
    df = df.rename(columns={' Card After 1': 'Card After 1', ' Card After 2': 'Card After 2', ' Card After 3': 'Card After 3', 
                            ' Card After 4': 'Card After 4', ' Card After 5': 'Card After 5',
                            ' Cards Exchanged 1': 'Cards Exchanged 1', ' Cards Exchanged 2': 'Cards Exchanged 2',
                            ' Cards Exchanged 3': 'Cards Exchanged 3'})
    #df = df.head()
    
    df = pd.get_dummies(df, drop_first=False, columns=['Exchange', 'Exchange Amount', 'Arrangement ID (After)'])
   
    df = df.drop(columns=['Card After 1', 'Card After 2', 'Card After 3', 'Card After 4', 'Card After 5',
                          'Cards Exchanged 1', 'Cards Exchanged 2', 'Cards Exchanged 3',])


    
    df.to_excel('poker_game_out.xlsx', index=True)
    df.to_csv('poker_game_out.csv', index=True)
    
    # X = df.drop("Weight", axis=1)
    # X = df.drop("Weight (After)", axis=1)
    
    X = df.drop("Win", axis=1)
    y = df["Win"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    
    #print(X.head())

    #df = df.head().corr()
    #df.to_excel('corr.xlsx', index=False)

if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()