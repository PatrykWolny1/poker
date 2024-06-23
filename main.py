from classes.Croupier import Croupier
import time

start_time = time.time()

croupier = Croupier()

croupier.play()

print()
print(((time.time() - start_time)), " sec")


