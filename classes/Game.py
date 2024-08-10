import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import time
import shutil
from classes.Player import Player
from classes.Croupier import Croupier
from machine_learning.M_learning import M_learning 
import re
import sys
import atexit


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def cleanup():
    # with open('ml_data/poker_game_one_pair_combs_all.csv', 'r+') as infile:
    #     infile.truncate(0)  
    pass

atexit.register(cleanup)

class Game(object):
        
    def __init__(self):
        self.Game()
    
    def Game(self): 
        all_combs_with_duplicates = 'ml_data/poker_game_one_pair_combs_all_duplicates.csv'
        all_combs_update_with_duplicates = 'ml_data/poker_game_one_pair_combs_all_to_update_duplicates.csv' 
        
        file_all_to_update = 'ml_data/poker_game_one_pair_combs_all_to_update.csv'
        file_one_pair_combs_all = 'ml_data/poker_game_one_pair_combs_all.csv'  
               
        while(choice_1 := input("\n" + 
                "(1)\n" +
                "- Zbieranie rozgrywek do pliku\n" +
                "- Gra (Ukladem Jedna Para) - AI vs Player, AI vs AI, Player vs Player)\n\n" + 
                "(2)\n" + 
                "- Gra miedzy graczami (Wszystkie uklady)\n" +
                "- Permutacje kart\n" +
                "- Aktualizacja modelu ML\n" +
                "- Uczenie maszynowe\n\n")):
            
            if choice_1 == '1':
                # Line used when gather data or play game with AI; Better performance in case of games gathering; OnePair so far
                cards_1, rand_int_1, all_comb_perm = Player().cards_permutations(combs_gen=True)
            if choice_1 == '2':
                all_comb_perm = []
        
            while(choice := input("Wybierz opcje: \n" + 
                                "(1) - Permutacje Kart\n" +
                                "(2) - Gra (Ukladem Jedna Para)\n" +
                                "(3) - Gra (Wszystkie uklady)\n" + 
                                "(4) - Zbieranie rozgrywek do pliku\n" + 
                                "(5) - Uczenie Maszynowe\n" +
                                "(6) - Aktualizacja modelu ML\n" +
                                "(7) - Usuwanie zawartosci plikow '... all_to_update.csv' oraz '... all.csv' po aktualizacjach\n" +
                                "(8) - Wroc\n" +
                                "(9) - Wyjscie\n")):
                
                if choice == '1':
                    Player().cards_permutations()
                
                if choice == '2':
                    croupier = Croupier(all_comb_perm=all_comb_perm, game_visible=True, tree_visible=False)
                    croupier.play()
                
                if choice == '3':
                    croupier = Croupier(game_visible=True, tree_visible=False)
                    croupier.play()
                
                if choice == '4':
                    n = int(input("Podaj ilosc rozgrywek do zapisania: "))
                    for i in range(0, n):
                        croupier = Croupier(all_comb_perm=all_comb_perm, game_visible=False, tree_visible=False)
                        # print(i)
        
                        try:
                            croupier.play()
                        except IndexError:
                            print("Uzyc opcji (1) z wstepnego menu")
                            break
                        except KeyboardInterrupt:
                            print("Przerwany program. Powrot do menu.")
                            print(i)
                            break
                    
                    try:
                        header = "Player ID,Exchange,Exchange Amount,Cards Before 1,Cards Before 2,Cards Before 3,Cards Before 4,Cards Before 5,Card Exchanged 1,Card Exchanged 2,Card Exchanged 3,Win"

                        if os.path.getsize(file_all_to_update) == 0:
                            with open(file_all_to_update, 'w') as outfile:
                                outfile.write(header + "\n")
                            print("Dodano naglowek do pliku ", file_all_to_update)                    
                        else:
                            print("Plik nie jest pusty")                   
                                    
                    except FileNotFoundError:
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")  
                    
                    # try:
                        # Usuwane sa powtarzajace sie linie
                        
                        # with open(all_combs_update_with_duplicates, 'r') as infile, open(file_all_to_update, 'a') as outfile:
                        #     # Create a set to store unique lines
                        #     seen_lines = set()
                        #     for line in infile:
                        #         # If the line is not in the set, write it to the output file and add it to the set
                        #         if line not in seen_lines:
                        #             outfile.write(line)
                        #             seen_lines.add(line)
                        # print("Plik ", all_combs_update_with_duplicates, " i jego unikalne wartosci zostaly skopiowane do pliku ",
                        #       file_all_to_update)   
                                                
                                    
                    # except FileNotFoundError:
                    #     print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")                    
          
                    try:
                        with open(all_combs_update_with_duplicates, 'r') as infile:
                            lines = infile.readlines()
                            
                        # Write the remaining lines back to the file
                        with open(all_combs_with_duplicates, 'a') as outfile:
                            outfile.writelines(lines)
                            
                        unique_pairs = set()
                        for i in range(0, len(lines), 2):
                            if i+1 < len(lines):
                                pair = (lines[i].strip(), lines[i+1].strip())
                                unique_pairs.add(pair) 

                        with open(file_all_to_update, 'a') as outfile:
                            for pair_w in unique_pairs:
                                outfile.write(pair_w[0] + '\n')
                                outfile.write(pair_w[1] + '\n')
                                
                            
                        print("Plik ", all_combs_update_with_duplicates, " zostal skopiowany do pliku ",
                            all_combs_with_duplicates)
                        print("Plik ", all_combs_update_with_duplicates, " i jego unikalne wartosci zostaly skopiowane do pliku ",
                              file_all_to_update)
                    
                    except FileNotFoundError:   
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")                           

                    try:
                        with open(all_combs_with_duplicates, 'r') as infile, open(file_one_pair_combs_all, 'w') as outfile:
                            # Usuwane sa powtarzajace sie pary 
                            with open(all_combs_with_duplicates, 'r') as infile:
                                lines = infile.readlines()

                            unique_pairs = set()
                            for i in range(0, len(lines), 2):
                                if i+1 < len(lines):
                                    pair = (lines[i].strip(), lines[i+1].strip())
                                    unique_pairs.add(pair) 

                            with open(file_one_pair_combs_all, 'r') as infile, open(file_one_pair_combs_all, 'a') as outfile:
                                for pair_w in unique_pairs:
                                    outfile.write(pair_w[0] + '\n')
                                    outfile.write(pair_w[1] + '\n')
                            
                                if os.path.getsize(file_one_pair_combs_all) == 0:
                                    outfile.write(header + "\n")
                                    print("Dodano naglowek do pliku ", file_one_pair_combs_all)                    
                                        
                        print("Plik ", all_combs_with_duplicates, " i jego unikalne wartosci zostaly skopiowane do pliku ",
                              file_one_pair_combs_all)                    
                                    
                    except FileNotFoundError:
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")      
              
                    try:
                        with open(all_combs_update_with_duplicates, 'r+') as file:
                            file.truncate(0)
                        print("Plik ", all_combs_update_with_duplicates, " zostal wyczyszczony")
                    except FileNotFoundError:   
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")    

                if choice == '5':
                    while(choice_2 := input("\n(1) - Wygrane/Przegrane\n" + 
                                            "(2) - Ilosc kart do wymiany zeby zwiekszyc szanse na wygrana\n" +
                                            "(3) - Wroc:\n")):
                        if choice_2 == '1':
                            model_ml = M_learning(win_or_not=True, exchange_or_not=False, file_path_csv='ml_data/poker_game_one_pair_combs_all.csv')
                        
                        if choice_2 == '2':
                            model_ml = M_learning(win_or_not=False, exchange_or_not=True, file_path_csv='ml_data/poker_game_one_pair_combs_all.csv')            

                        if choice_2 == '3':
                            break
                        
                        model_ml.pre_processing()
                        model_ml.ml_learning_and_prediction()

                if choice == '6':
                    while(choice_3 := input("\n(1) - Wygrane/Przegrane\n" + 
                                            "(2) - Ilosc kart do wymiany zeby zwiekszyc szanse na wygrana\n" +
                                            "(3) - Wroc:\n")):
                        
                        file_all_to_update = 'ml_data/poker_game_one_pair_combs_all_to_update.csv'
                        file_one_pair_combs_all = 'ml_data/poker_game_one_pair_combs_all.csv'                    
                        
                        if choice_3 == '1':
                            try:
                                model_ml_up = M_learning(win_or_not=True, exchange_or_not=False, file_path_csv=file_all_to_update)
                            except FileNotFoundError:
                                print("Plik z rozgrywkami nie istnieje.")
                                break
                            
                            with open('models_prediction/path_to_model_WIN.txt', 'r') as file:
                                filename_updated_model_path = file.readline()
                                filename_updated_weights_path = file.readline()
                                
                            if os.path.exists(filename_updated_model_path):
                                model_ml_up.update_model(base_model_path=filename_updated_model_path, weights_model_path=filename_updated_weights_path)
                                print("Wykorzystano UPDATE MODEL")
                                
                            else:
                                directory = "models_prediction"
                                prefix = "model_base_WIN"
                                extension = "hdf5"
                                pattern = rf"^{prefix}.*\.{extension}$"
                                matching_file1 = [filename for filename in os.listdir(directory) if re.match(pattern, filename)]
                                
                                directory = "models_prediction"
                                prefix = "weights_model_base_WIN"
                                extension = "weights.h5"
                                pattern = rf"^{prefix}.*\.{extension}$"
                                matching_file2 = [filename for filename in os.listdir(directory) if re.match(pattern, filename)]
                                
                                base_model_path = directory + '/' + matching_file1[0]
                                weight_model_path = directory + '/' + matching_file2[0]                               

                                model_ml_up.update_model(base_model_path=base_model_path, weights_model_path=weight_model_path)
                                print("Wykorzystano BASE MODEL")
                        
                        if choice_3 == '2':
                            try:
                                model_ml_up = M_learning(win_or_not=False, exchange_or_not=True, file_path_csv=file_all_to_update)      
                            except FileNotFoundError:
                                print("Plik z rozgrywkami nie istnieje.")
                                break
                            
                            with open('models_prediction/path_to_model_EX_AMOUNT.txt', 'r') as file:
                                filename_updated_model_path = file.readline()                           
                                filename_updated_weights_path = file.readline()

                            if os.path.exists(filename_updated_model_path):
                                model_ml_up.update_model(base_model_path=filename_updated_model_path, weights_model_path=filename_updated_weights_path)
                                print("Wykorzystano UPDATE MODEL")
                                
                            else:
                                directory = "models_prediction"
                                prefix = "model_base_EX_AMOUNT"
                                extension = "hdf5"
                                pattern = rf"^{prefix}.*\.{extension}$"
                                matching_file1 = [filename for filename in os.listdir(directory) if re.match(pattern, filename)]
                                
                                directory = "models_prediction"
                                prefix = "weights_model_base_EX_AMOUNT"
                                extension = "weights.h5"
                                pattern = rf"^{prefix}.*\.{extension}$"
                                matching_file2 = [filename for filename in os.listdir(directory) if re.match(pattern, filename)]
                                
                                base_model_path = directory + '/' + matching_file1[0]
                                weight_model_path = directory + '/' + matching_file2[0]
                                
                                model_ml_up.update_model(base_model_path=base_model_path, weights_model_path=weight_model_path)
                                print("Wykorzystano BASE MODEL")
                                
                            if choice_3 == '3':
                                break
                
                if choice == '7':
                    with open(file_all_to_update, 'r+') as infile:
                        infile.truncate(0)     
                    with open(file_one_pair_combs_all, 'r+') as infile:
                        infile.truncate(0)  
                    print("Usunieto!")

                if choice == '8':
                    break
                    
                if choice == '9':
                    exit()