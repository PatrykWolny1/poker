from classes.Croupier import Croupier
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
import time
import cProfile
import pstats

def main():
    start_time = time.time()

    
    # for i in range(0, 3):
    #     croupier = Croupier()
    #     croupier.play()

    cards = [1, 1, 2, 11, 12]
    OnePairStructureStrategy(cards)
    
    end_time = time.time() - start_time
    # with open("full.txt", "a") as file:
    #     file.write(str(end_time) + " sec\n")

    
    
    
    # print()    
    print(end_time, " sec")

if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()