import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import shutil

from classes.Player import Player
from classes.Croupier import Croupier
from machine_learning.M_learning import M_learning 
import sys
import atexit


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def cleanup():
    pass
    # file_all_to_update_duplicates = 'ml_data/poker_game_one_pair_combs_all_to_update_duplicates.csv'
    # file_one_pair_combs_all_duplicates = 'ml_data/poker_game_one_pair_combs_all_duplicates.csv'                    

    # if os.path.exists(file_all_to_update_duplicates):
    #     with open(file_all_to_update_duplicates, 'r') as file:
    #         lines = file.readlines()

    #     # Write the remaining lines back to the file
    #     with open(file_all_to_update_duplicates, 'w') as file:
    #         file.writelines(lines[1:])
    
    #     with open(file_all_to_update_duplicates, 'r') as src, open(file_one_pair_combs_all_duplicates, 'a') as dst:
    #         shutil.copyfileobj(src, dst) 
        
    #     print("Plik ", file_all_to_update_duplicates, " zostal skopiowany do pliku glownego.")
    # else:
    #     print("Plik nie istnieje.")    

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
                                "(7) - Wroc:\n" +
                                "(8) - Wyjscie\n")):
                
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
                        print(i)
        
                        try:
                            croupier.play()
                        except IndexError:
                            print("Uzyc opcji (1) z wstepnego menu")
                            break
                        except KeyboardInterrupt:
                            print("Przerwany program. Powrot do menu.")
                            break
                    
                    try:
                        header = "Player ID,Exchange,Exchange Amount,Cards Before 1,Cards Before 2,Cards Before 3,Cards Before 4,Cards Before 5,Card Exchanged 1,Card Exchanged 2,Card Exchanged 3,Win"

                        if os.path.getsize(file_all_to_update) == 0:
                            with open(file_all_to_update, 'w') as file:
                                file.write(header + "\n")
                            print("Dodano naglowek do pliku ", file_all_to_update)                    
                        else:
                            print("Plik nie jest pusty")
                            
                            with open(file_all_to_update, 'r') as file:
                                lines = file.readlines()
                                if lines[0] != header:
                                    lines.insert(0, header + "\n")
                            
                            with open(file_all_to_update, 'w') as file:
                                file.writelines(lines)
                                    
                            print("Dodano naglowek do pliku ", file_all_to_update)                    
                                    
                    except FileNotFoundError:
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")  
                    
                    try:
                        with open(all_combs_update_with_duplicates, 'r') as infile, open(file_all_to_update, 'a') as outfile:
                            # Create a set to store unique lines
                            seen_lines = set()
                            for line in infile:
                                # If the line is not in the set, write it to the output file and add it to the set
                                if line not in seen_lines:
                                    outfile.write(line)
                                    seen_lines.add(line)
                        print("Plik ", all_combs_update_with_duplicates, " i jego unikalne wartosci zostaly skopiowane do pliku ",
                              file_all_to_update)                    
                                    
                    except FileNotFoundError:
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")                    

                    try:
                        with open(all_combs_with_duplicates, 'r') as infile, open(file_one_pair_combs_all, 'w') as outfile:
                            # Create a set to store unique lines
                            seen_lines = set()
                            outfile.write("Player ID,Exchange,Exchange Amount," +
                                            "Cards Before 1,Cards Before 2,Cards Before 3," +
                                            "Cards Before 4,Cards Before 5,Card Exchanged 1," +
                                            "Card Exchanged 2,Card Exchanged 3,Win")
                            for line in infile:
                                # If the line is not in the set, write it to the output file and add it to the set
                                if line not in seen_lines:
                                    outfile.write(line)
                                    seen_lines.add(line)
                        print("Plik ", all_combs_with_duplicates, " i jego unikalne wartosci zostaly skopiowane do pliku ",
                              file_one_pair_combs_all)                    
                                    
                    except FileNotFoundError:
                        print("Plik ", all_combs_update_with_duplicates, " nie istnieje.")      
                        
                    if os.path.exists(all_combs_update_with_duplicates):
                        with open(all_combs_update_with_duplicates, 'r+') as file:
                            lines = file.readlines()
                            #file.truncate(0)

                        # Write the remaining lines back to the file
                        with open(all_combs_with_duplicates, 'a') as file:
                            file.writelines(lines[1:])
                            
                        print("Plik ", all_combs_update_with_duplicates, " zostal skopiowany do pliku ",
                            all_combs_with_duplicates)
                    else:
                        print("Plik nie istnieje.") 

                if choice == '5':
                    while(choice_2 := input("\n(1) - Wygrane/Przegrane\n" + 
                                            "(2) - Ilosc kart do wymiany zeby zwiekszyc szanse na wygrana\n" +
                                            "(3) - Wroc:\n")):
                        if choice_2 == '1':
                            model_ml = M_learning(win_or_not=True, exchange_or_not=False, file_path_csv='ml_data/poker_game_one_pair_combs_all_duplicates.csv')
                        
                        if choice_2 == '2':
                            model_ml = M_learning(win_or_not=False, exchange_or_not=True, file_path_csv='ml_data/poker_game_one_pair_combs_all_duplicates.csv')            

                        if choice_2 == '3':
                            break
                        
                        model_ml.pre_processing()
                        model_ml.ml_learning_and_prediction()

                if choice == '6':
                    while(choice_3 := input("\n(1) - Wygrane/Przegrane\n" + 
                                            "(2) - Ilosc kart do wymiany zeby zwiekszyc szanse na wygrana\n" +
                                            "(3) - Wroc (Skopiuj rozgrywki do glownego pliku po douczeniu WSZYSTKICH modeli oraz usun plik tymczasowy):\n")):
                        
                        file_all_to_update = 'ml_data/poker_game_one_pair_combs_all_to_update.csv'
                        file_one_pair_combs_all = 'ml_data/poker_game_one_pair_combs_all.csv'                    
                        
                        if choice_3 == '1':
                            try:
                                model_ml_up = M_learning(win_or_not=True, exchange_or_not=False, file_path_csv=all_combs_update_with_duplicates)
                            except FileNotFoundError:
                                print("Plik z rozgrywkami nie istnieje.")
                                break
                            
                            with open('models_prediction/path_to_model_WIN.txt', 'r') as file:
                                filename_updated_model_path = file.readline()
                                
                            if os.path.exists(filename_updated_model_path):
                                model_ml_up.update_model(base_model_path=filename_updated_model_path)
                                print("USING UPDATE MODEL")
                                
                            else:
                                model_ml_up.update_model(base_model_path='models_prediction/model_base_WIN_Adam_00001_test_acc=0.664_test_loss=0.155_2024-08-05_10-52-44.keras')
                                print("USING BASE MODEL")
                        
                        if choice_3 == '2':
                            try:
                                model_ml_up = M_learning(win_or_not=False, exchange_or_not=True, file_path_csv=all_combs_update_with_duplicates)      
                            except FileNotFoundError:
                                print("Plik z rozgrywkami nie istnieje.")
                                break
                            
                            with open('models_prediction/path_to_model_EX_AMOUNT.txt', 'r') as file:
                                filename_updated_model_path = file.readline()                           
                            
                            if os.path.exists(filename_updated_model_path):
                                model_ml_up.update_model(base_model_path=filename_updated_model_path)
                                print("USING UPDATE MODEL")
                                
                            else:
                                model_ml_up.update_model(base_model_path='models_prediction/model_base_EX_AMOUNT_Adam_00001_test_acc=0.736_test_loss=0.089_2024-08-05_18-27-44.keras')
                                print("USING BASE MODEL")
                                
                            if choice_3 == '3':
                                os.remove(file_all_to_update) 
                                os.remove(all_combs_update_with_duplicates)                         
                                break
                
                if choice == '7':
                    break
                
                if choice == '8':
                    exit()