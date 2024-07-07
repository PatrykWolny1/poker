from classes.Card import Card
from arrangements.HelperArrangement import HelperArrangement
from arrangements.LoadingBar import LoadingBar
from arrangements.CardMarkings import CardMarkings
from itertools import permutations

class StraightRoyalFlush(HelperArrangement):
    cardmarkings = CardMarkings()  #Oznaczenia kart

    loading_bar = LoadingBar(4799, 40, 39)

    cards = []                     #Tablica na karty
    perm = []                      #Tablica na permutacje do wag

    weight_arrangement = 0         #Tablica na wage ukladu
    num_arr = 0                    #Liczenie ukladow kart w kolejnych iteracjach

    random = False                 #Jesli jest losowanie ukladu
    example = False                #Jesli jest recznie wpisany uklad
    if_royal_flush = False         #Jesli jest poker krolewski (prawda) lub poker (falsz)
    calc_weights = True            #Zakonczenie petli while oraz identyfikacja czy jest to poker lub poker krolewski

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = True

    def get_weight(self):
        if self.weight_arrangement > 0:
            return self.weight_arrangement

    def get_part_weight(self):
        return None

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

    def straight_royal_flush_recognition(self, cards):
        #Czy jest 5 takich samych kolorow
        color_5 = False
        for idx in range(0, len(self.get_indices_2d_color())):
            if len(self.get_indices_2d_color()[idx]) == 5:
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
        self.calc_weights = True

        if self.example == True:
            HelperArrangement().get_indices_1(self.perm)
            HelperArrangement().get_indices_color(self.perm)

            self.perm = [self.perm]

            for idx1 in range(0, len(sorted(self.perm))):
                for idx2, idx3 in zip(range(1, len(sorted(self.perm[idx1]))), range(0, len(sorted(self.perm[idx1])) - 1)):
                    if (((sorted(self.perm[idx1])[idx2].weight - sorted(self.perm[idx1])[idx3].weight) == 1) or
                            (sorted(self.perm[idx1])[4].weight == 13 and sorted(self.perm[idx1])[4].weight - sorted(self.perm[idx1])[3].weight == 9)):
                        count += 1

                self.if_royal_flush = self.straight_royal_flush_recognition(sorted(self.perm[idx1]))

     

            if count != 4:
                HelperArrangement().clear_indices_2d_1()
                HelperArrangement().clear_indices_2d_color()
                return

        #Dziala dla tablicy o 0 rozmiarze i wiekszym (120)
        for idx4 in range(0, len(sorted(self.perm))):
            #Obliczanie wag
            while (self.calc_weights):
                #Sprawdzanie par kart 1-2, 2-3, 3-4, 4-5
                idx2 = 0
                idx3 = 1

                for idx33 in range(0, len(HelperArrangement().get_indices_2d_1())):
                    #Jesli jest wiecej kart o takich samych figurach od 1 to powrot z funkcji
                    if len(HelperArrangement().get_indices_2d_1()[idx33]) > 1:
                        return
                for idx55 in range(0, len(HelperArrangement().get_indices_2d_color())):
                    #Jesli jest mniej niz 5 kolorow to powrot z funkcji
                    if len(HelperArrangement().get_indices_2d_color()[idx55]) != 5:
                        return

                self.if_royal_flush = False

                if idx2 < 4 and idx3 < 5:
                    #Dla posortowanej tablicy sprawdz czy waga jest mniejsza od kolejnej
                    if (sorted(self.perm[idx4])[idx3].weight - sorted(self.perm[idx4])[idx2].weight) == 1:
                        straight_weight += sorted(self.perm[idx4])[idx2].weight

                    if weight_iter == 3:
                        straight_weight += sorted(self.perm[idx4])[idx3].weight

                        #Zapisanie wagi do tablicy wag
                        self.weight_arrangement = straight_weight + 12448474
                        HelperArrangement().append_weight_gen(self.weight_arrangement)

                        #Pobranie indeksow gdzie znajduja sie takie same kolory
                        HelperArrangement().get_indices_color(sorted(self.perm[idx4]))
                        #Wykrycie Pokera (False) lub Pokera Krolewskiego (True) oraz zwrocenie wartosci logicznej
                        self.if_royal_flush = self.straight_royal_flush_recognition(sorted(self.perm[idx4]))

                        HelperArrangement().clear_indices_2d_color()
                        if self.example == True or self.random == False:
                            self.print_arrengement()
                        self.calc_weights = False
                        break
                weight_iter += 1
                idx2 += 1
                idx3 += 1
                continue


    def straight_royal_flush(self):
        self.arrangement_recognition_weights()

        if self.if_royal_flush == True and self.calc_weights == False:
            return 9
        elif self.if_royal_flush == False and self.calc_weights == False:
            return 8

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
            temp = []
            for idx2 in range(0, len(cards_2d[idx1])):
                self.cards.append(cards_2d[idx1][idx2])
            temp.append(self.cards)

        # for idx1 in range(0, len(temp)):
        #     for idx2 in range(0, len(temp[idx1])):
        #         temp[idx1][idx2].print()
        #     print()

        # for idx1 in range(0, len(self.perm)):
        #     for idx2 in range(0, len(self.perm[idx1])):
        #         self.perm_temp[idx1][idx2].print()
        #     print()


        #Konwertowanie tymczasowej tablicy do tablicy na permutacje
        for idx1 in range(0, len(temp)):
            for step1, step2 in zip(range(0, len(temp[idx1]), 5), range(5, len(temp[idx1]) + 1, 5)):
            #Generowanie tablicy permutacji
                self.perm = list(permutations(temp[idx1][step1:step2]))
                #print(self.perm)

                self.perm = [list(i) for i in self.perm]

                for idx2 in range(0, len(self.perm)):


                    if self.random == False:
                        for idx3 in range(0, len(self.perm[idx1])):
                            self.perm[idx1][idx3].print()
                        print()

                    self.straight_royal_flush()

                    HelperArrangement().append_cards_all_permutations(self.perm[idx2])
                    self.loading_bar.set_count_bar(self.num_arr)
                    self.loading_bar.display_bar()
                    self.num_arr += 1

        HelperArrangement().check_if_weights_larger()

        return HelperArrangement().random_arrangement()