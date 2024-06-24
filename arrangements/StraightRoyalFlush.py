from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
from itertools import permutations
import random

class StraightRoyalFlush(object):
    cardmarkings = CardMarkings()  #Oznaczenia kart
    weight_gen = []                #Tablica na wagi
    cards = []                     #Tablica na karty
    cards_2d = []                  #Tablica do przetwarzania
    perm = []                      #Tablica na permutacje do wag
    cards_perm = []                #Tablica na permutacje
    indices_2d_name = []           #Tablica na indeksy - figury
    indices_2d_color = []          #Tablica na indeksy - kolory
    cards_all_permutations = []    #Tablica do wyswietlania losowego ukladu
    perm_sorted = []               #Tablica na posortowana tablice permutacji
    perm_sorted_print = []         #Tablica na posortowane tablice permuacji - wyswietlanie
    weight_arrangement = 0         #Tablica na wage ukladu
    print_permutations = True      #Wyswietlenie wszystkich permutacji
    print_random = True            #Jesli jest wyswietlanie losowego ukladu
    random = False                 #Jesli jest losowanie ukladu
    example = False                #Jesli jest recznie wpisany uklad
    if_royal_flush = False         #Jesli jest poker krolewski (prawda) lub poker (falsz)
    num_arr = 0                    #Liczenie ukladow kart w kolejnych iteracjach
    rand_int = 0                   #Przechowywanie numeru losowego ukladu

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = True

    def get_weight(self):
        if self.weight_arrangement > 0:
            return self.weight_arrangement

    def print_arrengement(self):
        if self.num_arr == len(self.cards_all_permutations):
            self.random = True

        if self.random == False and self.if_royal_flush == False:
            print("Poker: ", self.weight_arrangement, " Numer: ", self.num_arr)
        elif self.random == True and self.if_royal_flush == False:
           print("Poker: ", self.weight_arrangement, " Numer: ", self.rand_int)
        elif self.random == False and self.if_royal_flush == True:
            print("Poker Krolewski: ", self.weight_arrangement, "Numer: ", self.num_arr)
        elif self.random == True and self.if_royal_flush == True:
            print("Poker Krolewski: ", self.weight_arrangement, "Numer: ", self.rand_int)

        self.num_arr += 1

    def random_arrangement(self):
        self.cards_all_permutations = [ele for ele in self.cards_all_permutations if ele != []]

        self.rand_int = random.randint(0, len(self.cards_all_permutations) - 1)

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
                    print(self.cards_all_permutations[indices[idx]][idx1][0].print_str(), end=" ")
                if idx1 == 5:
                    print(self.cards_all_permutations[indices[idx]][idx1], end=" ")
                    print(indices[idx])
            print()

    def get_indices_name(self, cards):
        self.indices_2d_name = []

        #Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart
        indices = []
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
        #print(self.indices_2d_color)

    def straight_royal_flush_recognition(self, cards):
        #Czy jest 5 takich samych kolorow
        color_5 = False
        for idx in range(0, len(self.indices_2d_color)):
            if len(self.indices_2d_color[idx]) == 5:
                color_5 = True

        #Czy 5 wag zostalo sprawdzonych
        weight_5 = 0
        for idx2 in range(0, len(cards)):
            # Sprawdzanie wag dla kart o wagach od 9 do 13 (Poker Krolewski) 10...A
            if cards[idx2].weight in [9, 10, 11, 12, 13]:
                weight_5 += 1
            # Prawda dla Pokera Krolewskiego
            if color_5 == True and idx2 == 4 and weight_5 == 5:
                return True

        return False

    def arrangement_recognition_weights(self):
        #Rozpoznawanie ukladu oraz obliczanie wagi

        count = 0
        weight_iter = 0
        straight_weight = 0
        calc_weights = True

        if self.example == True:
            self.get_indices_name(self.perm)
            self.get_indices_color(self.perm)

            for idx1 in range(0, len(self.perm_sorted)):
                for idx2, idx3 in zip(range(1, len(self.perm_sorted[idx1])), range(0, len(self.perm_sorted[idx1]) - 1)):
                    if (((self.perm_sorted[idx1][idx2].weight - self.perm_sorted[idx1][idx3].weight) == 1) or
                        (self.perm_sorted[idx1][4].weight == 13 and self.perm_sorted[idx1][idx2].weight - self.perm_sorted[idx1][idx3].weight == 9)):
                        count += 1

                self.if_royal_flush = self.straight_royal_flush_recognition(self.perm_sorted[idx1])

            if count != 4:
                return

        #Dziala dla tablicy o 0 rozmiarze i wiekszym (120)
        for idx4 in range(0, len(self.perm_sorted)):
            #Obliczanie wag
            while (calc_weights):
                #Sprawdzanie par kart 1-2, 2-3, 3-4, 4-5
                idx2 = 0
                idx3 = 1

                for idx33 in range(0, len(self.indices_2d_name)):
                    #Jesli jest wiecej kart o takich samych figurach od 1 to powrot z funkcji
                    if len(self.indices_2d_name[idx33]) > 1:
                        return
                for idx55 in range(0, len(self.indices_2d_color)):
                    #Jesli jest mniej niz 5 kolorow to powrot z funkcji
                    if len(self.indices_2d_color[idx55]) != 5:
                        return

                self.if_royal_flush = False

                if idx2 < 4 and idx3 < 5:
                    #Dla posortowanej tablicy sprawdz czy waga jest mniejsza od kolejnej
                    if (self.perm_sorted[idx4][idx3].weight - self.perm_sorted[idx4][idx2].weight) == 1:
                        straight_weight += self.perm_sorted[idx4][idx2].weight

                    if weight_iter == 3:
                        straight_weight += self.perm_sorted[idx4][idx3].weight

                        #Zapisanie wagi do tablicy wag
                        self.weight_arrangement = straight_weight
                        self.weight_gen.append(self.weight_arrangement)

                        #Pobranie indeksow gdzie znajduja sie takie same kolory
                        self.get_indices_color(self.perm_sorted[idx4])
                        #Wykrycie Pokera (False) lub Pokera Krolewskiego (True) oraz zwrocenie wartosci logicznej
                        self.if_royal_flush = self.straight_royal_flush_recognition(self.perm_sorted[idx4])

                        self.print_arrengement()
                        calc_weights = False
                        break
                weight_iter += 1
                idx2 += 1
                idx3 += 1
                continue
    def straight_royal_flush(self):
        #Sortowanie tablicy permutacji w celu ulatwienia ustalenia ukladu kart
        self.perm_sorted = []
        self.perm_sorted_print = []

        for idx1 in range(0, len(self.perm)):
            if self.random == False and self.example == False:
                #Dodawanie do tablicy posortowanych kart
                self.perm_sorted.append(sorted(self.perm[idx1], key=lambda x: x.weight))
                #Tablica dla wyswietlania posortowanych wynikow
                self.perm_sorted_print.append(self.perm[idx1])

        if self.random == False and self.example == True:
            self.perm_sorted.append(sorted(self.perm, key=lambda x: x.weight))
            self.perm_sorted_print.append(self.perm)

        if self.random == True and self.example == True:
            self.perm_sorted.append(sorted(self.perm, key=lambda x: x.weight))
            self.perm_sorted_print.append(self.perm)

        if self.print_permutations and self.example == False:
            for idx1 in range(0, len(self.perm_sorted_print)):
                for idx2 in range(0, len(self.perm_sorted_print[idx1])):
                    #Ustalanie ukladu: poker lub poker krolewski
                    self.perm_sorted_print[idx1][idx2].print()
                print()
                #Liczenie wag dla tablicy kart
                self.arrangement_recognition_weights()
        else:
            self.arrangement_recognition_weights()

    def straight_royal_flush_generating(self, random):
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
                            cards_1d.append(
                                Card(self.cardmarkings.arrangements[len(self.cardmarkings.arrangements) - 1],
                                     color))
                        if idx1 < 4:
                            cards_1d.append(Card(self.cardmarkings.arrangements[idx1], color))
                    else:
                        cards_1d.append(Card(self.cardmarkings.arrangements[idx1 + m], color))

                if color == 'Ka':
                    cards_2d.append(cards_1d[:])

        return self.check_generate_cards(cards_2d)

    def check_generate_cards(self, cards_2d):
        #Generowanie 5 kart oraz sprawdzanie jaki to uklad

        # for idx3 in range(0, len(cards_2d)):
        #     for idx4 in range(0, len(cards_2d[idx3])):
        #         cards_2d[idx3][idx4].print()
        #     print()

        #Konwertowanie tablicy kart do tymczasowej dwuwymiarowej tablicy
        for idx1 in range(0, len(cards_2d)):
            self.temp = []
            for idx2 in range(0, len(cards_2d[idx1])):
                self.cards.append(cards_2d[idx1][idx2])
            self.temp.append(self.cards)

        # for idx1 in range(0, len(self.temp)):
        #     for idx2 in range(0, len(self.temp[idx1])):
        #         self.temp[idx1][idx2].print()
        #     print()

        self.perm_temp = []
        self.perm = []

        #Konwertowanie tymczasowej tablicy do tablicy na permutacje
        for idx1 in range(0, len(self.temp)):
            for step1, step2 in zip(range(0, len(self.temp[idx1]), 5), range(5, len(self.temp[idx1]) + 1, 5)):
                self.perm_temp.append(self.temp[idx1][step1:step2])

        # for idx1 in range(0, len(self.perm)):
        #     for idx2 in range(0, len(self.perm[idx1])):
        #         self.perm[idx1][idx2].print()
        #     print()

        for idx1 in range(0, len(self.perm_temp)):
            #Generowanie tablicy permutacji
            self.perm = list(permutations(self.perm_temp[idx1]))

            # for idx1 in range(0, len(self.perm)):
            #     for idx2 in range(0, len(self.perm[idx1])):
            #         self.perm[idx1][idx2].print()
            #     print()

            for idx2 in range(0, len(self.perm)):
                self.cards_all_permutations.append(self.perm[idx2])

            if self.random == False:
                self.straight_royal_flush()

        if self.random == False:
            self.check_if_weights_larger()

        return self.random_arrangement()




