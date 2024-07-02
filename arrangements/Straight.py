from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
import itertools
import random
import time

class Straight(object):
    cardmarkings = CardMarkings()   #Oznaczenia kart
    weight_gen = []                 #Tablica na wagi
    cards = []                      #Tablica na karty
    cards_2d = []                   #Tablica do przetwarzania
    cards_perm_weights = []         #Tablica na permutacje do wag
    perm = []                       #Tablica na permutacje do wag - posortowana
    cards_perm = []                 #Tablica na permutacje
    indices_2d_name = []            #Tablica na indeksy nazwa
    indices_2d_color = []           #Tablica na indeksy kolor
    cards_all_permutations = []     #Tablica do wyswietlania losowego ukladu
    num_arr = 0                     #Liczenie ukladow kart w kolejnych iteracjach
    weight_arrangement = 0          #Zmienna pomocnicza do sumowania wagi ukladu
    rand_int = 0                    #Przechowywanie numeru losowego ukladu
    straight_iter = 0               #Liczenie ile iteracji zostalo wykonanych
    c_idx6 = 0
    c_idx6_iter = 0

    if_perm_weights = True
    random = False                  #Jesli jest losowanie ukladu
    example = False                 #Jesli jest recznie wpisany uklad
    print_permutations = True       #Wyswietlenie wszystkich permutacji

    step_p = True
    str_1 = ""
    n_bar = 1224000
    step_bar = int(n_bar / 40)         # Zwiekszanie dlugosci paska ladowania
    step_bar_finished = int(n_bar / 40)  # Jaka czesc stanowia kropki (zaladowane)

    def set_cards(self, cards):
        self.perm = cards
        self.if_perm_weights = False
        self.example = True
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
        if self.step_p == False and (self.straight_iter % self.step_bar_finished) == 0:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")
            # os.system('cls')
        if self.num_arr == self.n_bar - 1:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")

    def print_arrengement(self):
        if self.random == False:
            print("Strit: ", self.weight_arrangement, " Numer: ", self.num_arr)
        if self.random == True:
            print("Strit: ", self.weight_arrangement, " Numer: ", self.rand_int)

        self.num_arr += 1

    def random_arrangement(self):
        self.cards_all_permutations = [ele for ele in self.cards_all_permutations if ele != []]

        self.rand_int = random.randint(0, len(self.weight_gen) - 1)

        print("Wylosowany uklad: ", self.rand_int)
        print("Ilosc ukladow: ", len(self.cards_all_permutations))

        return self.cards_all_permutations[self.rand_int]

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

        for idx in range(0, len(indices)):
            for idx1 in range(0, len(self.cards_all_permutations[indices[idx]])):
                if idx1 < 5:
                    print(self.cards_all_permutations[indices[idx]][idx1].print_str(), end=" ")
            print(indices[idx])
            print()

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

    def get_indices_color(self, cards):
        self.indices_2d_color = []

        #Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for idx in range(0, len(cards)):
            indices = []
            for (index, card) in enumerate(cards):
                if card.color == cards[idx].color:
                    indices.append(index)
            self.indices_2d_color.append(indices)
        #print(self.indices_2d)

    def remove_royal_flush(self, cards_comb_list):
        # Pobranie indeksow kolorow czyli okreslenie indeksow w jakich wystepuja
        self.get_indices_color(cards_comb_list)

        for idx1 in range(0, len(self.indices_2d_color)):
            #Jesli wystepuje 5 kolorow w ukladzie
            if len(self.indices_2d_color[idx1]) == 5:
                return True

        return False

    def remove_more_1(self, cards_comb_list):
        #Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        self.get_indices_name(cards_comb_list)

        for i in range(0, len(self.indices_2d_name)):
            if (len(self.indices_2d_name[i]) > 1):  # Jesli w wierszu tablicy znajduje sie wiecej niz 1 element
                return True

        return False

    def dim(self, a):
        # Jesli to nie jest lista to zwroc pusty zbior
        if not type(a) == list:
            return []
        # Rekurencja. Dodawanie kolejno dlugosci kolejnych tablic np. [1 5 10 15] czyli 4-wymiarowa
        return [len(a)] + self.dim(a[0])

    def straight(self):
        if len(self.dim(self.perm)) == 1:
            self.perm = [self.perm]
            self.c_idx6 = 0
            self.c_idx6_iter = (120 * 1020)

        # Przygotowanie tablicy do sortowania. Sortowanie jest uzywane zeby ulatwic okreslenie czy jest to strit
        self.perm[self.c_idx6] = sorted(self.perm[self.c_idx6], key=lambda x: x.weight)

        # Pobranie indeksow gdzie wystepuja powtorzenia kolorow lub pojedynczy kolor
        self.get_indices_color(self.perm[self.c_idx6])
        self.get_indices_name(self.perm[self.c_idx6])


        # for idx1 in range(0, len(self.perm[self.c_idx6])):
        #     self.perm[self.c_idx6][idx1].print()
        # print()

        weight_iter = 0
        straight_weight = 0
        calc_weights = True
        idx1 = 0
        idx2 = 1

        while (calc_weights):

            # Dla posortowanej tablicy sprawdz czy waga jest mniejsza od kolejnej
            for idx3, idx4 in zip(range(0, len(self.indices_2d_color)), range(0, len(self.indices_2d_name))):
                # Jesli jest 5 takich samych kolorow to powrot z funkcji (poker krolewski)
                if len(self.indices_2d_color[idx3]) == 5:
                    return
                if len(self.indices_2d_name[idx4]) > 1:
                    return

            if idx1 == 4:
                break

            # Jesli waga pierwszej karty jest mniejsza od drugiej ... do 5 karty to jest to strit
            if ((self.perm[self.c_idx6][idx2].weight - self.perm[self.c_idx6][idx1].weight == 1) or
                    (self.perm[self.c_idx6][4].weight == 13 and (self.perm[self.c_idx6][idx2].weight - self.perm[self.c_idx6][idx1].weight) == 9)):

                if self.c_idx6_iter in range((120 * 1020) + 1): #120*1020
                    #print(idx1 + 2, self.perm[self.c_idx6][idx1].print_str())
                    straight_weight += pow(self.perm[self.c_idx6][idx1].weight, idx1 + 2)
                    weight_iter += 1

                    if self.perm[self.c_idx6][idx2].weight == 13:
                        #print("1", self.perm[self.c_idx6][idx2].print_str())
                        straight_weight += pow(self.perm[self.c_idx6][idx2].weight, 1) - 10
                        weight_iter += 1

                    if self.perm[self.c_idx6][idx2].weight == 5:
                        #print("1", self.perm[self.c_idx6][idx2].print_str())
                        straight_weight += pow(self.perm[self.c_idx6][idx2].weight, 1)
                        weight_iter += 1

                else:
                    #print(idx1 + 1, self.perm[self.c_idx6][idx1].print_str())
                    straight_weight += pow(self.perm[self.c_idx6][idx1].weight, idx1 + 1)
                    weight_iter += 1

                    if idx2 == 4:
                        #print(idx2 + 1, self.perm[self.c_idx6][idx2].print_str())
                        straight_weight += pow(self.perm[self.c_idx6][idx2].weight, idx2 + 1)
                        weight_iter += 1

                # Jesli jest strit to weight_iter == 4. Liczono od 0
                if weight_iter == 5:
                    self.weight_arrangement = straight_weight + 11242224
                    self.weight_gen.append(self.weight_arrangement)
                    calc_weights = False

                    if self.random == False or self.example == True:
                        self.print_arrengement()

                    return 4

            idx1 += 1
            idx2 += 1

    def straight_generating(self, random):
        self.random = random

        cards_2d = []
        m = 0
        for iter in range(0, 10):
            cards_1d = []
            if iter > 1:
                m += 1
            for color in self.cardmarkings.colors:
                for idx1, idx2 in zip(range(0, len(self.cardmarkings.arrangements)), range(0, 5)):
                    if iter == 0:
                        if idx1 == 0:
                            cards_1d.append(Card(self.cardmarkings.arrangements[len(self.cardmarkings.arrangements) - 1], color))
                        if idx1 < 4:
                            cards_1d.append(Card(self.cardmarkings.arrangements[idx1], color))
                    else:
                        cards_1d.append(Card(self.cardmarkings.arrangements[idx1 + m], color))
                if color == 'Ka':
                    cards_2d.append(cards_1d[:])

        # for idx3 in range(0, len(cards_2d)):
        #     for idx4 in range(0, len(cards_2d[idx3])):
        #         cards_2d[idx3][idx4].print()
        #     print()

        return self.check_generate_cards(cards_2d)

    def check_generate_cards(self, cards_2d):
        #Generowanie 5 kart oraz sprawdzanie jaki to uklad
        cards_comb_list = []

        self.permutation = True

        for idx1 in range(0, len(cards_2d)):
            self.cards.clear()
            for idx2 in range(0, len(cards_2d[idx1])):
                self.cards.append(cards_2d[idx1][idx2])
                if idx2 == 19:
                    if self.permutation:
                        cards_comb = list(itertools.combinations(self.cards, 5))

                        cards_comb_list.clear()

                        for idx5 in cards_comb:
                            cards_comb_list.append(list(idx5))

                        #Usuwanie z tablicy kombinacji kart o ilosci wiekszej od 1

                        for idx5 in range(0, len(cards_comb_list)):
                            # Usuwanie ukladow gdzie wystepuje wiecej niz 1 taka sama karta
                            if_remove = self.remove_more_1(cards_comb_list[idx5])
                            #Usuwanie pokera krolewskiego z permutacji ukladow
                            if_remove_rf = self.remove_royal_flush(cards_comb_list[idx5])

                            if if_remove == True or if_remove_rf == True:
                                cards_comb_list[idx5] = []

                        cards_comb_list = [ele for ele in cards_comb_list if ele != []]

                        # for idx5 in range(0, len(cards_comb_list)):
                        #     for idx6 in range(0, len(cards_comb_list[idx5])):
                        #         cards_comb_list[idx5][idx6].print()
                        #     print()

                        #print(len(cards_comb_list))

                        for idx5 in cards_comb_list:
                            self.perm = list(itertools.permutations(idx5, 5))

                            for idx6 in range(0, len(self.perm)):
                                self.perm[idx6] = list(self.perm[idx6])

                                self.get_indices_name(self.perm[idx6])

                                if self.random == False:
                                    for idx7 in range(0, len(self.perm[idx6])):
                                        self.perm[idx6][idx7].print()
                                    print()

                                self.c_idx6 = idx6
                                self.straight()

                                if self.random == True:
                                    self.loading_bar()
                                    self.straight_iter += 1

                                self.cards_all_permutations.append(self.perm[idx6])

                                self.c_idx6_iter += 1

        self.check_if_weights_larger()

        return self.random_arrangement()
