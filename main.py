from classes.Croupier import Croupier
from classes.Player import Player
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
import time
import cProfile
import pstats
import pandas as pd

def main():
    start_time = time.time()
    cards_1, rand_int_1, all_comb_perm = Player().cards_permutations()
    
    for i in range(0, 1000):
        croupier = Croupier(all_comb_perm)
                
        croupier.play()
    
    end_time = time.time() - start_time
    with open("time.txt", "w") as file:
        file.write(str(end_time) + " sec\n")
    
    print()    
    print(end_time, " sec")
    
    df = pd.read_csv('poker_game.csv', on_bad_lines='skip', engine='python')
    print(df)

if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()