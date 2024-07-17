from classes.Croupier import Croupier
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
import time
import cProfile
import pstats
import pandas as pd
import numpy as np

def main():
    start_time = time.time()

    for i in range(0, 1):
        croupier = Croupier()
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
    print(df)

if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()