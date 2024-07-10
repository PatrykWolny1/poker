from classes.Croupier import Croupier
import time
import cProfile
import pstats

def main():
    start_time = time.time()

    croupier = Croupier()

    croupier.play()

    end_time = time.time() - start_time
    with open("full.txt", "a") as file:
        file.write(str(end_time) + " sec\n")

    print()    
    print(end_time, " sec")

if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()