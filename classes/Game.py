import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from classes.Player import Player
from classes.Croupier import Croupier
from machine_learning.M_learning import M_learning 
import sys

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

class Game(object):
        
    def __init__(self):
        self.Game()
    
    def Game(self):    
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
                        croupier.play()
                        
                if choice == '5':
                    while(choice_2 := input("\n(1) - Wygrane lub przegrane\n" + 
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
                    file_all_to_update = 'ml_data/poker_game_one_pair_combs_all_to_update.csv'
                    
                    model_ml_up = M_learning(file_path_csv=file_all_to_update)
                   
                    if os.path.exists(model_ml_up.filename_updated):
                        model_ml_up.update_model(
                            base_model_path=model_ml_up.filename_updated)
                        
                    else:
                        model_ml_up.update_model(
                            base_model_path='models_prediction/model_base_WIN_Adam_00001_test_acc=0.666_test_loss=0.155.keras')
                     
                    if os.path.exists(file_all_to_update):
                        os.remove(file_all_to_update)
                        print("File deleted successfully.")
                    else:
                        print("The file does not exist.")
                        
                if choice == '7':
                    break
                
                if choice == '8':
                    exit()