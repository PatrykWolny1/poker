import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from classes.Player import Player
from classes.Croupier import Croupier
from machine_learning.M_learning import M_learning 

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
                "- Uczenie maszynowe\n\n")):
            
            if choice_1 == '1':
                # Line used when gather data or play game with AI; Better performance in case of games gathering; OnePair so far
                cards_1, rand_int_1, all_comb_perm = Player().cards_permutations(combs_gen=True)
            if choice_1 == '2':
                all_comb_perm = []
        
            while(choice := input("Wybierz opcje: \n" + 
                                "(1) - Permutacje Kart\n" +
                                "(2) - Gra \n" +
                                "(3) - Zbieranie rozgrywek do pliku\n(4) - Uczenie Maszynowe\n" + 
                                "(5) - Wroc:\n" +
                                "(6) - Wyjscie\n")):
                
                if choice == '1':
                    Player().cards_permutations()
                
                if choice == '2':
                    for i in range(0, 1):
                        croupier = Croupier(all_comb_perm, game_visible=True, tree_visible=False)
                        #print(i)
                        croupier.play()
                        
                if choice == '3':
                    n = input("Podaj ilosc rozgrywek do zapisania: ")
                    #n = 1
                    for i in range(0, n):
                        croupier = Croupier(game_visible=False, tree_visible=False)
                        print(i)
                        croupier.play()
                        
                if choice == '4':
                    model_ml = M_learning()
                    model_ml.pre_processing()
                    model_ml.ml_learning_and_prediction()
                    
                if choice == '5':
                    break
                
                if choice == '6':
                    exit()