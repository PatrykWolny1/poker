from arrangements.HelperArrangement import HelperArrangement
from classes.Card import Card
from arrangements.LoadingBar import LoadingBar
from arrangements.CardMarkings import CardMarkings
from itertools import permutations, combinations

class OnePair(HelperArrangement):
    
    def __init__(self):
        self.cardmarkings:CardMarkings = CardMarkings()  # Oznaczenia kart
        self.high_card:Card = Card()             # Wysoka karta
        self.limit_rand:int = 1000              # Ograniczenie dla liczby obliczen
        self.one_iter:int = 120
        self.loading_bar:LoadingBar = LoadingBar(self.one_iter * self.limit_rand - 1, 40, 40)          #Permutacje: 131 788 800
        self.file = open("one_pair.txt", "w")

        self.perm:list = []                      # Lista na permutacje
        self.weight_arrangement_part:list  = []   # Lista na wagi pozostalych kart

        self.weight_arrangement:int = 0         # Waga ukladu
        self.c_idx1:int = 0                     # Zapisywanie aktualnego indeksu z petli for
        self.num_arr:int = 0                    # Numer ukladu
        self.rand_iter:int = 0

        self.random:bool = False
        self.example:bool = False

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = True
    
    def set_rand_int(self, rand_int):
        self.rand_int = rand_int
        
    def get_weight(self):
        # Jesli to jest to aktualny uklad to zwroc wage ukladu
        if self.weight_arrangement > 0:
            return self.weight_arrangement

    def get_part_weight(self):
        if sum(self.weight_arrangement_part) > 0:
            return self.weight_arrangement_part

    def print_arrengement(self):
        if self.random == False:
            print("Jedna Para: ", self.weight_arrangement, "Wysoka karta: ", self.high_card.print_str(),  "Numer: ", self.num_arr)
        if self.example == True:
            print("Jedna Para: ", self.weight_arrangement, "Wysoka karta: ", self.high_card.print_str(),  "Numer: ", self.rand_int)

    def remove_multiples(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for i in range(0, len(HelperArrangement().get_indices_2d_1())):
            if len(HelperArrangement().get_indices_2d_1()[i]) in range(2, 4):  # Jesli w wierszu tablicy znajduja sie 2 lub 3 takie same elementy
                return True

        return False

    def remove_multiples_more_4(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for i in range(0, len(HelperArrangement().get_indices_2d_1())):
            if len(HelperArrangement().get_indices_2d_1()[i]) > 4:  # Jesli w wierszu tablicy znajduja sie wiecej niz 4 takie same elementy
                return True

        return False

    def remove_multiples_more_2(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for i in range(0, len(HelperArrangement().get_indices_2d_1())):
            if len(HelperArrangement().get_indices_2d_1()[i]) > 2:  # Jesli w wierszu tablicy znajduja sie wiecej niz 2 takie same elementy
                return True

        return False

    def arrangement_recogn(self):
        one_count_1 = 0     # Licznik na uklad wysoka karta
        one_count_2 = 0     # Licznik na uklad para
        once_1 = False      # Zmienne ktore sluza do wykonania petli jeden raz
        once_2 = False
        once_3 = False
        one_weight = 0          # Waga ukladu
        cards_max_sort = []     # Lista na karty do okreslenie najwyzszej karty (na pojedyncze karty)
        self.weight_arrangement_part = []
        
        if len(HelperArrangement().dim(self.perm)) == 1:
            self.perm = [self.perm]
            self.c_idx1 = 0
        
        
        HelperArrangement().clear_indices_2d_1()
        HelperArrangement().get_indices_1(self.perm[self.c_idx1])
        
        for idx in range(0, len(HelperArrangement().get_indices_2d_1())):
            if len(HelperArrangement().get_indices_2d_1()[idx]) == 2:
                one_count_2 += 1

                # Warunek wykonywany jeden raz
                if once_1 == False:
                    # Obliczenia dla jednej karty i drugiej (para)
                    one_weight += pow(self.perm[self.c_idx1][HelperArrangement().get_indices_2d_1()[idx][0]].weight, 6)
                    one_weight += pow(self.perm[self.c_idx1][HelperArrangement().get_indices_2d_1()[idx][1]].weight, 6)

                    once_1 = True

            if len(HelperArrangement().get_indices_2d_1()[idx]) == 1:
                # Dodanie do listy karty ktorej wystapienie pojawia sie 1 raz w ukladzie
                cards_max_sort.append(self.perm[self.c_idx1][HelperArrangement().get_indices_2d_1()[idx][0]])
                one_count_1 += 1

                # Wyszukiwanie w kolejnych petlach kart ktore wystepuja 1 raz w ukladzie
                for idx1 in range(idx + 1, len(HelperArrangement().get_indices_2d_1())):

                    if once_2 == False:

                        if len(HelperArrangement().get_indices_2d_1()[idx1]) == 1:
                            cards_max_sort.append(self.perm[self.c_idx1][HelperArrangement().get_indices_2d_1()[idx1][0]])

                            for idx2 in range(idx1 + 1, len(HelperArrangement().get_indices_2d_1())):
                                if len(HelperArrangement().get_indices_2d_1()[idx2]) == 1:
                                    cards_max_sort.append(self.perm[self.c_idx1][HelperArrangement().get_indices_2d_1()[idx2][0]])

                                    if once_3 == False:
                                        cards_max_sort.sort(key=lambda x: x.weight)

                                        # Znalezienie minimalnej i maksymalnej wagi karty z posrod 3 kart
                                        min_card = cards_max_sort.index(min(cards_max_sort))
                                        self.high_card = cards_max_sort.index(max(cards_max_sort))

                                        # Wyszukanie srodkowej wagi karty z posrod 3 kart (wyszukiwanie po indeksach)
                                        for idx3 in range(0, len(cards_max_sort)):
                                            # Jesli indeks idx3 nie jest rowny indeksom min i max to jest to waga srodkowa
                                            if idx3 not in [min_card, self.high_card]:
                                                mid_card = cards_max_sort[idx3]
                                                one_weight += pow(mid_card.weight, 3)
                                            #cards_max_sort[idx3].print()
                                        #print()

                                        self.high_card = max(cards_max_sort)
                                        min_card = min(cards_max_sort)

                                        one_weight += pow(min_card.weight, 2)
                                        one_weight += pow(self.high_card.weight, 4)

                                        # print("Min: ", min_card.print_str())
                                        # print("Mid: ", mid_card.print_str())
                                        # print("Max: ", self.high_card.print_str())

                                        cards_max_sort.clear()

                                        once_3 = True
                            once_2 = True

        # Jesli pojedyncza karta wystepuje 3 razy oraz wystepuje 1 para to zakoncz
        if one_count_1 == 3 and one_count_2 == 2:
            self.weight_arrangement = one_weight + 390079

            HelperArrangement().append_weight_gen(self.weight_arrangement)   # Tablica wag dla sprawdzania czy wygenerowane uklady maja wieksze
            
            if self.random == False:
                #self.print_arrengement()
                self.file.write("Jedna para: " + str(self.weight_arrangement) +
                                " Wysoka Karta: " + self.high_card.print_str() +
                                " Numer: " + str(self.num_arr) + "\n")
                                    
            self.num_arr += 1
                
            if self.example == True:
                self.print_arrengement()
                
                for idx in range(0, len(self.perm[self.c_idx1])):
                    with open("one_pair.txt", "a") as file:
                        file.write(self.perm[self.c_idx1][idx].print_str() + " ")
                        
                with open("one_pair.txt", "a") as file:
                    file.write("\n")
                
                with open("one_pair.txt", "a") as file:
                    file.write("Jedna Para: " + str(self.weight_arrangement) + " Wysoka karta: " +
                                    self.high_card.print_str() + " Numer: " + str(self.rand_int) + "\n")
                
                self.weight_arrangement_part.append(min_card.weight)
                self.weight_arrangement_part.append(mid_card.weight)
                self.weight_arrangement_part.append(self.high_card.weight)
                return 1

        else:
            self.weight_arrangement = 0
            self.weight_arrangement_part = []


    def one_pair_generating(self, random):
        self.random = random

        cards_2d = []
        cards_to_comb = []
        cards_to_comb_1 = []
        cards_to_comb_rest = []
        i_pair = 0      # Kolejne iteracje petli
        iter_ar = 0     # Kolejne iteracje dla kolejnych serii ukladow
        len_comb = 0    # Ilosc permutacji

        # Tworzenie talii kart
        for arrangement in self.cardmarkings.arrangements:
            for color in self.cardmarkings.colors:
                cards_2d.append(Card(arrangement, color))

        #while (True):
        # for idx in range(0 + iter_ar, 4 + iter_ar):
        #     cards_2d[idx].print()
        # print("###############################")

        cards_to_comb_rest.extend(cards_2d[0:52])

        # for idx in range(0, len(cards_to_comb_rest)):
        #     cards_to_comb_rest[idx].print()
        # print()

        # Tworzenie kombinacji 3 kart (maja byc pojedyncze)
        cards_comb_rest = list(combinations(cards_to_comb_rest, 3))

        cards_to_comb_rest.clear()

        for idx in range(0, len(cards_comb_rest)):
            # Tworzenie serii kart (od indeksu 0 do 3 itd.)
            cards_to_comb.extend(cards_2d[0 + iter_ar : 4 + iter_ar])

            cards_comb_rest[idx] = list(cards_comb_rest[idx])

            # for idx1 in range(0, len(cards_comb_rest[idx])):
            #     cards_comb_rest[idx][idx1].print()
            # print()
            
            HelperArrangement().get_indices_1(cards_comb_rest[idx])

            # Usuwanie powtorek powtarzajacych sie kart (2 lub 3)
            if_remove_comb_1 = self.remove_multiples(cards_comb_rest[idx])

            if if_remove_comb_1 == True:
                cards_comb_rest[idx] = []

            HelperArrangement().clear_indices_2d_1()

            # Dodanie do serii kart kolejnych 3 kart
            cards_to_comb.extend(cards_comb_rest[idx])
            cards_to_comb_1.append(cards_to_comb.copy())
            cards_to_comb.clear()

        cards_to_comb_1 = [x for x in cards_to_comb_1 if x != []]

        # for idx in range(0, len(cards_comb_rest)):
        #     for idx1 in range(0, len(cards_comb_rest[idx])):
        #         cards_comb_rest[idx][idx1].print()
        #     print()

        # for idx in range(0, len(cards_to_comb_1)):
        #     for idx1 in range(0, len(cards_to_comb_1[idx])):
        #         cards_to_comb_1[idx][idx1].print()
        #     print()

        for idx in range(0, len(cards_to_comb_1)):
            # Usuwanie kart ktorych wystapienia sa rowne 4
            if len(cards_to_comb_1[idx]) == 4:
                cards_to_comb_1[idx] = []

            HelperArrangement().get_indices_1(cards_comb_rest[idx])

            # usuwanie kart ktorych wystepienia sa wieksze od 4
            if_remove_comb_2 = self.remove_multiples_more_4(cards_to_comb_1[idx])

            if if_remove_comb_2 == True:
                cards_to_comb_1[idx] = []

            HelperArrangement().clear_indices_2d_1()

        cards_to_comb_1 = [x for x in cards_to_comb_1 if x != []]

        for idx in range(0, len(cards_to_comb_1)):
            cards_comb = list(combinations(cards_to_comb_1[idx], 5))
            
            # Usuwanie kart ktorych wystepienia sa wieksze od 2
            for idx1 in range(0, len(cards_comb)):
                HelperArrangement().get_indices_1(cards_comb[idx1])

                if_remove_comb_3 = self.remove_multiples_more_2(cards_comb[idx1])

                if if_remove_comb_3 == True:
                    cards_comb[idx1] = []

                HelperArrangement().clear_indices_2d_1()

            cards_comb = [x for x in cards_comb if x != []]

            for idx1 in range(0, len(cards_comb)):
                self.perm = list(permutations(cards_comb[idx1], 5))

                # for idx2 in range(0, len(cards_comb[idx1])):
                #     cards_comb[idx1][idx2].print()
                # print()

                for idx2 in range(0, len(self.perm)):
                    self.perm[idx2] = list(self.perm[idx2])

                    if self.random == False:
                        for idx3 in range(0, len(self.perm[idx2])):
                            #self.perm[idx2][idx3].print()
                            self.file.write(self.perm[idx2][idx3].print_str() + " ")
                        #print()
                        self.file.write("\n")
                    # Zapisanie indeksu uzywanego w funkcji one_pair()
                    self.c_idx1 = idx2
                    self.arrangement_recogn()

                    self.loading_bar.set_count_bar(self.num_arr)
                    self.loading_bar.display_bar()

                    HelperArrangement().append_cards_all_permutations(self.perm[idx2])
        
                    self.rand_iter += 1
                #print(self.rand_iter) 
        
                    if self.rand_iter == self.one_iter * self.limit_rand:
                        HelperArrangement().check_if_weights_larger(False)

                        self.file.close()

                        return HelperArrangement().random_arrangement()

        iter_ar += 4

        HelperArrangement().check_if_weights_larger(False)

        self.file.close()

        return HelperArrangement().random_arrangement()