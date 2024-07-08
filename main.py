from classes.Croupier import Croupier
import time

start_time = time.time()

croupier = Croupier()

croupier.play()

end_time = time.time() - start_time

with open("straight_royal_flush.txt", "a") as file:
    file.write(str(end_time) + " sec\n")

print()    
print(end_time, " sec")
