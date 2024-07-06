from arrangements.HelperArrangement import HelperArrangement
from classes.Card import Card
from arrangements.LoadingBar import LoadingBar
from arrangements.CardMarkings import CardMarkings
from itertools import permutations, combinations
import random
import time

class OnePair(HelperArrangement):
    cardmarkings = CardMarkings()  # Oznaczenia kart
    indices_2d_name = []           # Lista na indeksy figur
    perm = []                      # Lista na permutacje
    cards_all_permutations = []    # Lista na wszystkie permutacje
    weight_gen = []                # Lista na wagi
    weight_arrangement_part = []   # Lista na wagi pozostalych kart

    high_card = None               # Wysoka karta

    weight_arrangement = 0         # Waga ukladu
    c_idx1 = 0                     # Zapisywanie aktualnego indeksu z petli for
    num_arr = 0                    # Numer ukladu
    rand_int = 0                   # Losowy numer

    random = False
    example = False

    idx_bar = 0
    loading_bar = LoadingBar(10137600, 40, 39)

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = False

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
        if self.random == True:
            print("Jedna Para: ", self.weight_arrangement, "Wysoka karta: ", self.high_card.print_str(),  "Numer: ", self.rand_int)

        self.num_arr += 1

    def check_if_weights_larger(self):
        # Sprawdzanie czy wagi w wygenerowanych ukladach sa wieksze niz poprzedni uklad (min -> max)
        self.weight_gen = [ele for ele in self.weight_gen if ele != []]
        indices = []
        count_all_weights = 0
        idx1 = 1
        for idx2 in range(0, len(self.weight_gen)):
            if (idx1 == len(self.weight_gen)):
                print("Dlugosc tablicy: ", len(self.weight_gen))
                print("Wszystkie liczby sprawdzone: ", count_all_weights)
                break
            if (self.weight_gen[idx2] <= self.weight_gen[idx1]):
                #print(self.weight_gen[idx2], "[", idx2, "]", "<=", self.weight_gen[idx1], "[", idx1, "]")
                count_all_weights += 1
            else:
                indices.append(idx2)
                indices.append(idx1)
            idx1 += 1

        for idx in range(0, len(indices)):
            for idx1 in range(0, len(self.cards_all_permutations[indices[idx]])):
                print(self.cards_all_permutations[indices[idx]][idx1].print_str(), end=" ")
            print()
            print(indices[idx])

    def random_arrangement(self):
        self.cards_all_permutations = [ele for ele in self.cards_all_permutations if ele != []]

        self.rand_int = random.randint(0, len(self.weight_gen) - 1)

        print("Wylosowany uklad: ", self.rand_int)
        print("Ilosc ukladow: ", len(self.cards_all_permutations))

        return self.cards_all_permutations[self.rand_int]

    def dim(self, a):
        # Jesli to nie jest lista to zwroc pusty zbior
        if not type(a) == list:
            return []
        # Rekurencja. Dodawanie kolejno dlugosci kolejnych tablic np. [1 5 10 15] czyli 4-wymiarowa
        return [len(a)] + self.dim(a[0])

    def get_indices_name(self, cards):
        self.indices_2d_name = []

        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for idx in range(0, len(cards)):
            indices = []
            for (index, card) in enumerate(cards):
                if card.name == cards[idx].name:
                    indices.append(index)
            self.indices_2d_name.append(indices)
        #print(self.indices_2d_name)

    def remove_multiples(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        self.get_indices_name(cards_comb)

        for i in range(0, len(self.indices_2d_name)):
            if len(self.indices_2d_name[i]) in range(2, 4):  # Jesli w wierszu tablicy znajduja sie 2 lub 3 takie same elementy
                return True

        return False

    def remove_multiples_more_4(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        self.get_indices_name(cards_comb)

        for i in range(0, len(self.indices_2d_name)):
            if len(self.indices_2d_name[i]) > 4:  # Jesli w wierszu tablicy znajduja sie wiecej niz 4 takie same elementy
                return True

        return False

    def remove_multiples_more_2(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        self.get_indices_name(cards_comb)

        for i in range(0, len(self.indices_2d_name)):
            if len(self.indices_2d_name[i]) > 2:  # Jesli w wierszu tablicy znajduja sie wiecej niz 2 takie same elementy
                return True

        return False

    def one_pair(self):
        one_count_1 = 0     # Licznik na uklad wysoka karta
        one_count_2 = 0     # Licznik na uklad para
        once_1 = False      # Zmienne ktore sluza do wykonania petli jeden raz
        once_2 = False
        once_3 = False
        one_weight = 0          # Waga ukladu
        cards_max_sort = []     # Lista na karty do okreslenie najwyzszej karty (na pojedyncze karty)
        self.weight_arrangement_part = []


        if len(self.dim(self.perm)) == 1:
            self.perm = [self.perm]
            self.c_idx1 = 0

        self.get_indices_name(self.perm[self.c_idx1])

        for idx in range(0, len(self.indices_2d_name)):
            if len(self.indices_2d_name[idx]) == 2:
                one_count_2 += 1

                # Warunek wykonywany jeden raz
                if once_1 == False:
                    # Obliczenia dla jednej karty i drugiej (para)
                    one_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][0]].weight, 6)
                    one_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][1]].weight, 6)

                    once_1 = True

            if len(self.indices_2d_name[idx]) == 1:
                # Dodanie do listy karty ktorej wystapienie pojawia sie 1 raz w ukladzie
                cards_max_sort.append(self.perm[self.c_idx1][self.indices_2d_name[idx][0]])
                one_count_1 += 1

                # Wyszukiwanie w kolejnych petlach kart ktore wystepuja 1 raz w ukladzie
                for idx1 in range(idx + 1, len(self.indices_2d_name)):

                    if once_2 == False:

                        if len(self.indices_2d_name[idx1]) == 1:
                            cards_max_sort.append(self.perm[self.c_idx1][self.indices_2d_name[idx1][0]])

                            for idx2 in range(idx1 + 1, len(self.indices_2d_name)):
                                if len(self.indices_2d_name[idx2]) == 1:
                                    cards_max_sort.append(self.perm[self.c_idx1][self.indices_2d_name[idx2][0]])

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
                                            # cards_max_sort[idx3].print()
                                        # print()

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
            self.weight_gen.append(self.weight_arrangement)   # Tablica wag dla sprawdzania czy wygenerowane uklady maja wieksze
            if self.random == False:
                self.print_arrengement()

            self.weight_arrangement_part.append(min_card.weight)
            self.weight_arrangement_part.append(mid_card.weight)
            self.weight_arrangement_part.append(self.high_card.weight)

            return 1

        else:
            self.weight_arrangement = 0
            self.weight_arrangement_part = []


    def one_pair_generating(self, random):
        start_time = time.time()

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

        while (True):
            for idx in range(0 + iter_ar, 4 + iter_ar):
                cards_2d[idx].print()
            print("###############################")

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

                # Usuwanie powtorek powtarzajacych sie kart (2 lub 3)
                if_remove_comb_1 = self.remove_multiples(cards_comb_rest[idx])

                if if_remove_comb_1 == True:
                    cards_comb_rest[idx] = []

                # Dodanie do serii kart kolejnych 3 kart
                cards_to_comb.extend(cards_comb_rest[idx])
                cards_to_comb_1.append(cards_to_comb.copy())
                cards_to_comb.clear()

            cards_comb_rest = [x for x in cards_comb_rest if x != []]
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

                # usuwanie kart ktorych wystepienia sa wieksze od 4
                if_remove_comb_2 = self.remove_multiples_more_4(cards_to_comb_1[idx])

                if if_remove_comb_2 == True:
                    cards_to_comb_1[idx] = []

            cards_to_comb_1 = [x for x in cards_to_comb_1 if x != []]

            for idx in range(0, len(cards_to_comb_1)):
                cards_comb = list(combinations(cards_to_comb_1[idx], 5))

                # Usuwanie kart ktorych wystepienia sa wieksze od 2
                for idx1 in range(0, len(cards_comb)):
                    if_remove_comb_3 = self.remove_multiples_more_2(cards_comb[idx1])

                    if if_remove_comb_3 == True:
                        cards_comb[idx1] = []

                cards_comb = [x for x in cards_comb if x != []]

                for idx1 in range(0, len(cards_comb)):
                    self.perm = list(permutations(cards_comb[idx1], 5))

                    # for idx2 in range(0, len(cards_comb[idx1])):
                    #     cards_comb[idx1][idx2].print()
                    # print()

                    for idx1 in range(0, len(self.perm)):
                        self.perm[idx1] = list(self.perm[idx1])

                        if self.random == False:
                            for idx2 in range(0, len(self.perm[idx1])):
                                self.perm[idx1][idx2].print()
                            print()

                        # Zapisanie indeksu uzywanego w funkcji one_pair()
                        self.c_idx1 = idx1
                        self.one_pair()

                        if self.random == True:
                            self.loading_bar.set_count_bar(self.idx_bar)
                            self.loading_bar.display_bar()
                            self.idx_bar += 1

                        self.cards_all_permutations.append(self.perm[idx1])

                len_comb += len(cards_comb)

            print(len_comb)

            cards_to_comb_1.clear()

            i_pair += 1
            iter_ar += 4

            self.step_p = True
            self.idx_bar = 0
            self.str_1 = ""

            if i_pair == 1:
                print(len(self.cards_all_permutations))
                break

        self.check_if_weights_larger()

        return self.random_arrangement()