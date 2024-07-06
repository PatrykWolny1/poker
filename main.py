from classes.Croupier import Croupier
import time


file = open("one_pair.txt", "a")

start_time = time.time()

croupier = Croupier()

croupier.play()

print()
end_time = time.time() - start_time
print(end_time, " sec")

file.write((str(end_time)) + " sec\n")
file.close()
