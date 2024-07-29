import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from classes.Croupier import Croupier
from classes.Player import Player
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
import time
import cProfile
import pstats
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from machine_learning.M_learning import M_learning 

def main():
    start_time = time.time()
    
    
   
    while(choice := input("Wybierz opcje (1 - Permutacje Kart | 2 - Gra)")):
        if choice == '1':
            cards_1, rand_int_1, all_comb_perm = Player().cards_permutations()
            Player().arrangements.cards_all_permutations = 0

        if choice == '2':
            for i in range(0, 1):
                croupier = Croupier(all_comb_perm)
                #print(i)
                croupier.play()
    
    #model_ml = M_learning()
    #model_ml.pre_processing()
    #model_ml.ml_learning_and_prediction()
    
        
    end_time = time.time() - start_time
    with open("time.txt", "w") as file:
        file.write(str(end_time) + " sec\n")
    
    print()    
    print(end_time, " sec")
    
if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()