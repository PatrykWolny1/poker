from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
import itertools
import random


class Full(object):
    cardmarkings = CardMarkings()   #Oznaczenia kart
    weight_gen = []                 #Tablica na wagi
    cards = []                      #Tablica na karty
    cards_2d = []                   #Tablica do przetwarzania ukladow
    cards_1d = []                   #Tablica do przetwarzania ukladow
    cards_1d_comb = []              #Tablica do przetwarzania ukladow kombinacje
    cards_comb_perm = []            #Tablica do przetwarzania ukladow permutacje
    cards_comb_perm_print = []      #Tablica do wyswietlenia ukladow permutacje
    indices_2d = []                 #Tablica na indeksy powtarzajacych sie kart
    cards_perm_weights = []         #Tablica na permutacje do wyliczenia wag ukladow
    cards_2d_5 = []                 #Tablica do wyswietlania (testy)
    cards_2d_5_list = []            #Tablica do wyswietlania (testy)
    cards_all_permutations = []     #Tablica do losowania ukladu
    num_arr = 0                     #Liczenie ukladow kart w kolejnych iteracjach
    c_idx6 = 0
    rand_int = 0
    perm = []

    if_perm_weights = True
    random = False                  #Jesli jest losowanie ukladu
    example = False                 #Jesli jest recznie wpisany uklad
    print_permutations = True       #Czy wyswietlic wszystkie permutacje

    step_p = True
    str_1 = ""
    n_bar = 449280
    step_bar = int(n_bar / 20)          #Zwiekszanie dlugosci paska ladowania
    step_bar_finished = int(n_bar / 19) #Jaka czesc stanowia kropki (zaladowane)

    def set_cards(self, cards):
        self.perm = cards
        self.random = True

    def get_weight(self):
        if self.weight_arrangement > 0:
            return self.weight_arrangement

    def loading_bar(self):
        if self.step_p:
            for i in range(0, self.n_bar, self.step_bar):
                self.str_1 += "#"
        if self.step_p:
            print("[", end="")
            print(self.str_1, end="]\n")
            # os.system('cls')
            self.step_p = False
        if self.step_p == False and (self.num_arr % self.step_bar_finished) == 0:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")
            # os.system('cls')
        if self.num_arr == self.n_bar - 1:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")

    #Przykladowy losowy uklad
    def random_arrangement(self):
        self.cards_all_permutations = [ele for ele in self.cards_all_permutations if ele != []]

        self.rand_int = random.randint(0, len(self.cards_all_permutations) - 1)

        print("Wylosowany uklad: ", self.rand_int)
        print("Ilosc ukladow: ", len(self.cards_all_permutations))

        return self.cards_all_permutations[self.rand_int]

    def print_arrengement(self):
        if self.random == False:
            print("Full: ", self.weight_arrangement, "Numer: ", self.num_arr)
        if self.random == True:
            print("Full: ", self.weight_arrangement, "Numer: ", self.rand_int)

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
                # print(self.weight_gen[idx2], "[", idx2, "]", "<=", self.weight_gen[idx1], "[", idx1, "]")
                count_all_weights += 1
            else:
                indices.append(idx2)
                indices.append(idx1)
            idx1 += 1

        # for idx in range(0, len(self.cards_all_permutations)):
        #     for idx2 in range(0, len(self.cards_all_permutations[idx])):
        #         self.cards_all_permutations[idx][idx2].print()
        #     print()

        for idx in range(0, len(indices)):
            for idx1 in range(0, len(self.cards_all_permutations[indices[idx]])):
                pass
                print(self.cards_all_permutations[indices[idx]][idx1].print_str(), end=" ")
            print(indices[idx])

    def dim(self, a):
        # Jesli to nie jest lista to zwroc pusty zbior
        if not type(a) == list:
            return []
        # Rekurencja. Dodawanie kolejno dlugosci kolejnych tablic np. [1 5 10 15] czyli 4-wymiarowa
        return [len(a)] + self.dim(a[0])

    def get_indices_name(self, cards):
        self.indices_2d = []

        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for idx in range(0, len(cards)):
            indices = []
            for (index, card) in enumerate(cards):
                if card.name == cards[idx].name:
                    indices.append(index)
            self.indices_2d.append(indices)
        #print(self.indices_2d)

    def remove_repeats_full(self):
        #Usuwanie tych samych kart ktorych liczba jest wieksza od 3

        #print(self.indices_2d)
        for i in range(0, len(self.indices_2d)):
            if (len(self.indices_2d[i]) == 4):  # Jesli w wierszu tablicy znajduja sie 3 elementy
                return True

    def full(self):
        # Sprawdzanie czy uklad kart to full oraz przypisanie wagi do ukladu

        self.if_full = 0  # Sumowanie tych samych kart
        weight_1 = 0
        weight_2 = 0
        indices_1 = False
        indices_2 = False

        self.weight_arrangement = 0

        if self.random == True:
            self.get_indices_name(self.perm)
            self.c_idx6 = 0
            self.perm = [self.perm]


        for i in range(0, len(self.indices_2d)):
            #print("Rozmiar: ", len(self.indices_2d[i]))
            if ((len(self.indices_2d[i]) == 3) and indices_1 == False):  # Jesli w wierszu tablicy znajduja sie 3 elementy
                for j in range(0, len(self.indices_2d[i])):
                    weight_1 += pow(self.perm[self.c_idx6][self.indices_2d[i][j]].weight, 3)
                indices_1 = True
                self.if_full += 1
            if ((len(self.indices_2d[i]) == 2) and indices_2 == False):  # Jesli w wierszu tablicy znajduja sie 2 elementy
                for k in range(0, len(self.indices_2d[i])):
                    weight_2 += self.perm[self.c_idx6][self.indices_2d[i][k]].weight * 2
                indices_2 = True
                self.if_full += 1

        if (self.if_full == 2):
            self.weight_arrangement = (weight_1 + weight_2)
            self.weight_gen.append(self.weight_arrangement)  # Tablica wag dla sprawdzania czy wygenerowane uklady maja wieksze
            self.print_arrengement()

    def full_generating(self, random):
        self.cards_2d = []
        self.random = random

        for i in self.cardmarkings.arrangements:        #Iteracja po oznaczeniach
            self.cards_1d = []
            for idx1 in range(0, 4):                    #Dodanie 4 pierwszych kart
                self.cards_1d.append(Card(i, self.cardmarkings.colors[idx1]))   #

            self.cards_1d_comb = list(itertools.combinations(self.cards_1d, 4))

            #Iteracja po tablicy z kombinacjami
            for idx2 in self.cards_1d_comb:
                self.cards_1d = []
                #Dazenie do tablicy postaci AKi ATr APi 2Ki 3Ki 4Ki 5Ki 6Ki ...
                for idx3 in range(0, len(idx2)):
                    self.cards_1d.append(Card(idx2[idx3].name, idx2[idx3].color))
                    if idx3 == 2:
                        for idx4 in self.cardmarkings.colors:
                            for idx5 in range(0, len(self.cardmarkings.arrangements)):
                                self.cards_1d.append(Card(self.cardmarkings.arrangements[idx5], idx4))
                        self.cards_2d.append(self.cards_1d)

        #Tablica ma byc postaci AKi ATr APi 2Ki 3Ki 4Ki 5Ki 6Ki ... QKi KKi AKi 2Tr 3Tr 4Tr ... KTr ATr
        # for idx6 in range(0, len(self.cards_2d)):
        #     for idx7 in range(0, len(self.cards_2d[idx6])):
        #         self.cards_2d[idx6][idx7].print()
        #     print()

        #Filtracja kart o takich samych kolorach
        #Przed: 2Ki 2Tr 2Pi 2Ki 3Ki ... KKi AKi 2Tr 3Tr ...
        #Po: 2Ki 2Tr 2Pi 3Ki ... KKi AKi 3Tr 4Tr ...
        shift1 = 0
        shift2 = 12
        shift3 = 24
        shift4 = 36
        for idx1 in range(0, len(self.cards_2d)):
            self.cards_2d[idx1].pop(3 + shift1)
            self.cards_2d[idx1].pop(3 + shift2)
            self.cards_2d[idx1].pop(3 + shift3)
            self.cards_2d[idx1].pop(3 + shift4)
            if ((idx1 + 1) % 1 == 0):
                shift1 += 1
                shift2 += 1
                shift3 += 1
                shift4 += 1

        shift5 = 1
        shift6 = 0

        # for idx11 in range(0, len(self.cards_1d)):
        #     self.cards_1d[idx11].print()

        #Sortowanie do postaci: 2Ki 2Tr 2Pi 2Ka 3Ki 3Tr 3Pi 3Ka 4Ki 4Tr 4Pi ...
        for idx1 in range(0, len(self.cards_2d)):
            self.cards_2d[idx1].sort()

        # for idx6 in range(0, len(self.cards_2d)):
        #     for idx7 in range(0, len(self.cards_2d[idx6])):
        #         self.cards_2d[idx6][idx7].print()
        #     print()

        for idx1 in range(0, len(self.cards_2d)):
            for idx2 in range(0, len(self.cards_2d[idx1])):
                if idx2 == 8:
                    for idx6 in range(0, len(self.cards_2d[idx1])):
                        if idx2 == len(self.cards_2d[idx1]):
                            shift6 += 1
                        #Usuwanie powtorek np. 2Ki 2Tr 2Pi 2Ki 3Ki ... AKi 2Tr 3Tr ... ATr
                        if (idx1 > 4) and (idx2 > 4 + shift6) and (idx2 < 7 + shift6):
                            self.cards_2d[idx1].insert(0, self.cards_2d[idx1].pop(idx2))
                            shift5 += 1
                        if ((idx1 + 1) % 4 == 0) and (idx1 != 0) and (idx1 > 4):
                            shift6 += 4

        # for idx6 in range(0, len(self.cards_2d)):
        #     for idx7 in range(0, len(self.cards_2d[idx6])):
        #         self.cards_2d[idx6][idx7].print()
        #     print()

        step = 0
        step2 = 0
        step3 = 0

        iter_comb = 0
        for idx in range(0, 13):
            for idx1 in range(0, len(self.cards_2d)):

                cards_2d_temp = []
                cards_2d_6 = []

                for idx2 in range(0, len(self.cards_2d[idx1])):
                    if (idx2 >= step2) and (idx2 < 4 + step2):
                        cards_2d_temp.append(self.cards_2d[idx1][idx2])
                    if (idx2 > 3 + step + step3 and idx2 < 8 + step + step3): #or (idx2 > 5 + step and idx2 < 8 + step):
                        cards_2d_temp.append(self.cards_2d[idx1][idx2])
                    #Filtracja kart do postaci 2Ki 2Tr 2Pi 2Ka 3Ki 3Tr 3Pi 3Ka w celu utworzenia tablicy kombinacji kart
                    if idx2 == 7 + step + step3:
                        cards_2d_6.append(cards_2d_temp)
                        # print("#######################################")
                        # for idx3 in range(0, len(cards_2d_6)):
                        #     pass
                        #     for idx33 in range(0, len(cards_2d_6[idx3])):
                        #         cards_2d_6[idx3][idx33].print()
                        #     print()

                        self.cards_2d_5.clear()

                        for idx3 in range(0, len(cards_2d_6)):
                            #Utworzenie tablicy z kombinacjami kart (48 * 78 = 3744 kombinacji kart po przetwarzaniu)
                            self.cards_2d_5.append(list(itertools.combinations(cards_2d_6[idx3], 5)))

                            self.cards_2d_5_list.clear()

                            for idx4 in self.cards_2d_5[0]:
                                self.cards_2d_5_list.append(list(idx4).copy())

                            for idx5 in range(0, len(self.cards_2d_5_list)):
                                # Pobranie indeksow z tablicy permutacji w ktorych wystepuje FULL np. [1, 3, 4][2, 5]
                                self.get_indices_name(self.cards_2d_5_list[idx5])

                                # Usuwanie liczby kart wiekszych od 3
                                if_remove = self.remove_repeats_full()

                                if if_remove == True:
                                    self.cards_2d_5_list[idx5] = []

                            self.cards_2d_5_list = [ele for ele in self.cards_2d_5_list if ele != []]

                            # for idx55 in range(0, len(self.cards_2d_5_list)):
                            #     for idx66 in range(0, len(self.cards_2d_5_list[idx55])):
                            #         self.cards_2d_5_list[idx55][idx66].print()
                            #     print()

                            #print(len(self.cards_2d_5_list))

                            self.perm.clear()

                            for iter_1 in range(0, len(self.cards_2d_5_list)):
                                perm_temp = list(itertools.permutations(self.cards_2d_5_list[iter_1], 5))
                                #print(perm_temp)
                                for idx6 in perm_temp:
                                    self.perm.append(list(idx6).copy())

                            for idx6 in range(0, len(self.perm)):
                                self.get_indices_name(self.perm[idx6])

                                if self.random == False:
                                    for idx7 in range(0, len(self.perm[idx6])):
                                        self.perm[idx6][idx7].print()
                                    self.c_idx6 = idx6
                                    self.full()

                                if self.random == True:
                                    self.num_arr += 1
                                    self.loading_bar()


                                #Tablica permutacji do wylosowania ukladu
                                self.cards_all_permutations.append(self.perm[idx6])

                step += 4

            step = 0
            step2 += 4
            step3 += 4

        self.check_if_weights_larger()

        return self.random_arrangement()
