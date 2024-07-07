from classes.Card import Card
from arrangements.HelperArrangement import HelperArrangement
from arrangements.CardMarkings import CardMarkings
from arrangements.LoadingBar import LoadingBar
from itertools import permutations, combinations
from operator import itemgetter
from itertools import chain

class Color(HelperArrangement):
    cardmarkings = CardMarkings()  #Oznaczenia kart
    loading_bar_1 = LoadingBar(611519, 40, 39)
    loading_bar_2 = LoadingBar(5095, 40, 39)

    cards_2d = []           # Przygotowanie listy do wstepnego przetwarzania
    perm = []               # Lista na permutacje
    perm_unsort = []        # Nieposortowana lista na permutacje

    high_card = None        # Zmienna na wysoka karte

    color_weight = 0        # Waga karty
    color_sum = 0           # Suma ukladu
    num_arr = 0             # Licznik
    count = 0               # Licznik pomocniczy do funkcji temp_lambda()
    count_1 = 0             # Licznik do loading_bar()
    count_2 = 0             # Licznik do loading_bar()

    random = False
    example = False

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = True

    def get_weight(self):
        if self.color_sum > 0:
            return self.color_sum

    def get_part_weight(self):
        return None

    def temp_lambda(self, t1):
        #Jesli koniec sekwencji wag i sumy [[Card int] [Card int] ... [Card int] sum][[Card int] ... [Card int] sum]
        if self.count == 6:
            return

        self.count += 1

        #Zamiana indeksu kart (LISTA!) na string (SAMA LICZBA) (czyli self.count < 6, gdzie poczatek self.count zaczyna sie od 1)
        if self.count < 6:
            t2 = ''.join(map(str, t1[1]))
            if int(t2) < 5:
                return t1[1]
        #Zamiana wagi calego ukladu na string (bez listy)
        elif self.count == 6:
            t3 = ''.join(map(str, t1))
            if int(t3) > 4:
                return t1

    def print_arrengement(self):
        if self.random == False:
            print("Kolor:", self.color_sum, "Wysoka Karta:", self.high_card.print_str(), "Numer:", self.num_arr)
        elif self.random == True:
            print("Kolor:", self.color_sum, "Wysoka Karta:", self.high_card.print_str(), "Numer:", self.rand_int)

        self.num_arr += 1

    def check_if_straight_royal_flush(self):
        #Sprawdzanie czy w ukladach kart znajduje sie Poker lub Poker Krolewski (do eliminacji)
        count = 0
        for idx, idx1 in zip(range(0, len(self.perm) - 1), range(1, len(self.perm))):
            #Karty musza byc poukladane od najmniejszej do najwiekszej w odstepie wartosci wagi wynoszacej 1
            #As jest traktowany jako najwyzsza karta lub najnizsza wtedy roznica miedzy A, a 2 wynosi 9
            if (self.perm[idx1].weight - self.perm[idx].weight == 1 or
                    (self.perm[0].weight == 1 and self.perm[4].weight == 13 and self.perm[4].weight - self.perm[3].weight == 9)):
                count += 1
            if count == 4:
                return True

    def remove_straight_royal_flush(self):
        #Usuwanie Pokera oraz Pokera Krolewskiego

        calc_weights = True
        if_begin = False

        idx1 = 0
        idx2 = 0
        idx3 = 1
        straight_flush_iter = 0
        len_straight_flush_iter = 0
        len_iter = 0

        while (calc_weights):
            if straight_flush_iter == 0 and if_begin == True:
                idx2 = 0
                idx3 = 1
                if_begin = False
            elif if_begin == True:
                idx2 = 0
                idx3 = 1
                straight_flush_iter = 0
                if_begin = False

            #Dla posortowanej tablicy sprawdz czy waga jest mniejsza od kolejnej
            #Wykrywanie tych samych kart oraz strita
            if ((self.cards_2d[idx1][idx3].weight - self.cards_2d[idx1][idx2].weight == 1) or
                    #Wykrywanie kombinacji kart A 2 3 4 5
                    (self.cards_2d[idx1][0].weight == 1 and self.cards_2d[idx1][4].weight == 13 and self.cards_2d[idx1][4].weight - self.cards_2d[idx1][3].weight == 9)):
                straight_flush_iter += 1

            #Jesli zostaly sprawdzone 4 uklady to usun dany wiersz kart
            if straight_flush_iter == 4 and idx2 == 3:
                # for idx in range(0, len(self.cards_2d[idx1])):
                #     self.cards_2d[idx1][idx].print()
                # print()
                self.cards_2d.remove(self.cards_2d[idx1])

                idx2 = 0
                idx3 = 1
                straight_flush_iter = 0
                len_straight_flush_iter += 1
                if_begin = True

            elif idx2 == 3 and straight_flush_iter < 4:
                idx1 += 1
                idx2 = 0
                idx3 = 1
                if_begin = True
                straight_flush_iter = 0

            # print("cards_2d: ", len(self.cards_2d) * len(self.cardmarkings.colors))
            # print("len_iter: ", len_iter)
            # print("len_straight_flush_iter: ", len_straight_flush_iter)

            #Wyjscie z funkcji
            if ((len_iter + 1) - (len(self.cards_2d) * len(self.cardmarkings.colors))
                    == (len_straight_flush_iter * len(self.cardmarkings.colors))):
                calc_weights = False

            idx2 += 1
            idx3 += 1
            len_iter += 1

    def color(self):
        self.all_permutations = True

        #Obliczenia dla wyswietlenia ukladu losowego lub okreslonego (przykladowego)
        if self.random == True and self.example == True:

            self.perm_unsorted = self.perm.copy()

            self.perm.sort()

            if self.check_if_straight_royal_flush():
                return

            self.color_weight = 0
            self.color_sum = 0
            HelperArrangement().clear_indices_2d_color()
            #Pobranie indeksow tablicy, gdzie wystepuja takie same kolory
            HelperArrangement().get_indices_color(self.perm)
            print(HelperArrangement().get_indices_2d_color())

            #Lista ma dlugosc 1 w ktorej znajduje sie kolejna lista z kartami, a dalej z waga ukladu
            for idx1 in range(0, len(HelperArrangement().get_indices_2d_color()) - 4):
                #Jesli wystepuje 5 kolorow to jest to uklad Kolor
                if len(HelperArrangement().get_indices_2d_color()[idx1]) == 5:
                    for idx in range(0, len(self.perm)):
                        #Dla kart innych niz najwyzsza policz czesciowo wage ukladu
                        if self.perm[idx] != max(self.perm):
                            #Potega od 1 do 4
                            self.color_weight = pow(sorted(self.perm)[idx].weight, idx + 1)
                            self.color_sum += self.color_weight
                            print(self.color_sum)
                    self.high_card = max(self.perm)
                    self.color_weight = pow(self.high_card.weight, 5)

                    #Calkowita suma ukladu
                    self.color_sum += self.color_weight + 12007274
            
                    # print()
                    # for idx in range(0, len(self.perm_unsorted)):
                    #     self.perm_unsorted[idx].print()
                    # print()

                    self.print_arrengement()
                    return 5
            return

        #Obliczenia dla wyswietlenia wszystkich permutacji ukladu Kolor
        #Jesli tablica jest jednowymiarowa to dodaj jeden wymiar w celu uruchomienia nastepnej petli
        if len(HelperArrangement().dim(self.perm)) == 1:
            self.perm = [self.perm]
            HelperArrangement().clear_indices_2d_color()
        
        HelperArrangement().get_indices_color(self.perm)

        for idx in range(0, len(self.perm)):

            for idx1 in range(0, len(HelperArrangement().get_indices_2d_color()) - 4):
                if len(HelperArrangement().get_indices_2d_color()[idx1]) == 5:
                    for idx2 in range(0, len(self.perm[idx])):
                        self.color_weight = 0
                        self.color_sum = 0

                        # for k in range(0, len(self.perm[idx][idx2])):
                        #     self.perm[idx][idx2][k].print()
                        # print()

                        HelperArrangement().append_cards_all_permutations(self.perm[idx][idx2])


                        if self.random == True:
                            self.loading_bar_1.set_count_bar(self.count_1)
                            self.loading_bar_1.display_bar()
                            self.count_1 += 1

                        #Dodanie indeksow do nowej tablicy zlozonej z tablicy glownej w celu powrotu ze
                        # stanu posortowanego do nieposortowanego
                        i = 0
                        j = 0
                        b = []
                        t = []
                        check = True
                        while check:
                            t.append([self.perm[idx][idx2][j], [i]])
                            i += 1
                            j += 1
                            if j == 5:
                                b.append(t.copy())
                                check = False

                        #Usuniecie wymiaru z tablicy oraz przypisanie do tablicy nieposortowanej
                        perm_unsorted = list(chain.from_iterable(b))

                        #print(perm_unsorted)
                        # print("perm_unsorted: [", end="")
                        # for idx22 in range(0, len(perm_unsorted)):
                        #     print("[", end="")
                        #     print((perm_unsorted[idx22][1]), end = ", ")
                        #     print(perm_unsorted[idx22][0].print_str(), end = "")
                        #     print("]", end=" ")
                        # print()

                        #Sortowanie wedlug klucza (t1[0] == Card) czyli wedlug samych kart bez indeksow
                        perm_sorted = sorted(perm_unsorted, key = lambda t1: t1[0])
                        # print("perm_sorted: [", end="")
                        # for idx22 in range(0, len(perm_sorted)):
                        #     print("[", end="")
                        #     print((perm_sorted[idx22][1]), end=", ")
                        #     print(perm_sorted[idx22][0].print_str(), end="")
                        #     print("]", end=" ")
                        # print()

                        #print(perm_sorted)
                        for idx3 in range(0, len(perm_sorted)):
                            if perm_sorted[idx3][0] != max(perm_sorted, key = lambda t3: t3[0])[0]:
                                self.color_weight = pow(perm_sorted[idx3][0].weight, idx3 + 1)
                                self.color_sum += self.color_weight

                        self.high_card = max(perm_sorted, key = lambda t4: t4[0])
                        self.color_weight = pow(self.high_card[0].weight, 5)
                        self.color_sum += self.color_weight

                        if self.random == True:
                            HelperArrangement().append_weight_gen(self.color_sum)

                        #print("SUM: ", self.color_sum)

                        #Zrobic z perm unsorted i dodac do self.perm_temp
                        #Dodanie wagi calego ukladu jako tablica
                        perm_sorted.append([self.color_sum])
                        # print("perm_sorted: ", end="")
                        # for idx22 in range(0, len(perm_sorted)):
                        #     if idx22 == 5:
                        #         print("sum:", perm_sorted[idx22])
                        #     else:
                        #         print("[", end= "")
                        #         print((perm_sorted[idx22][1]), end=", ")
                        #         print(perm_sorted[idx22][0].print_str(), end="")
                        #         print("]", end=" ")

                        #Uzywane w funkcji temp_lambda()
                        self.count = 0

                        #Sortowanie z kluczem (czyli wedlug dodanych indeksow)
                        self.perm_unsort.append(sorted(perm_sorted.copy(), key=self.temp_lambda))

                        # print("perm_unsort: ", end="")
                        #
                        # for idx11 in range(0, len(self.perm_unsort)):
                        #     for idx22 in range(0, len(self.perm_unsort[idx11])):
                        #         if idx22 == 5:
                        #             print("sum:", self.perm_unsort[idx11][idx22])
                        #         else:
                        #             #print("[", end= "")
                        #             print((self.perm_unsort[idx11][idx22][1]), end="-")
                        #             print(self.perm_unsort[idx11][idx22][0].print_str(), end=" ")
                        #             #print("]", end=" ")
                        #     print()

                if self.random == False:
                    self.loading_bar_2.set_count_bar(self.count_2)
                    self.loading_bar_2.display_bar()
                    self.count_2 += 1

                HelperArrangement().clear_indices_2d_color()

                break

    def color_generating(self, random):
        self.random = random

        self.cards_2d = []

        for idx in range(0, len(self.cardmarkings.colors)):
            self.cards_2d = []

            #Sprowadzenie kart do ukladu - 2Ki 3Ki 4Ki 5Ki 6Ki 7Ki 8Ki 9Ki 10Ki JKi QKi KKi AKi
            #                                                   ...
            for idx1 in self.cardmarkings.arrangements:
                self.cards_2d.append(Card(idx1, self.cardmarkings.colors[idx]))

            # for idx2 in range(0, len(self.cards_2d)):
            #     self.cards_2d[idx2].print()
            # print()

            self.cards_2d = list(combinations(self.cards_2d, 5))

            #Konwertowanie tuple do list
            self.cards_2d = [list(i) for i in self.cards_2d]

            #Usuwanie pokera oraz pokera krolewskiego
            self.remove_straight_royal_flush()

            # Wyswietlanie kombinacji wszystkich kart z ukladem kolor
            # for idx1 in range(0, len(self.cards_2d)):
            #     for idx2 in range(0, len(self.cards_2d[idx1])):
            #         self.cards_2d[idx1][idx2].print()
            #     print()

            #Kazda iteracja zawiera 1278 kart dla kazdego koloru
            for idx1 in range(0, len(self.cards_2d)):
                self.perm.append(list(permutations(self.cards_2d[idx1], 5)))

                #Zamiana tuple na list w dwuwymiarowej tablicy
                self.perm = [[list(j) for j in row[0:]] for row in self.perm]

                #print(len(self.perm))
                # for idx11 in range(0, len(self.perm)):
                #     for idx22 in range(0, len(self.perm[idx11])):
                #         for idx33 in range(0, len(self.perm[idx11][idx22])):
                #             self.perm[idx11][idx22][idx33].print()
                #             pass
                #         print()


                self.color()
                self.perm.clear()

        #Jesli losowanie nie wybrane to nastepuje sortowanie wag ukladow (od najmniejszej do najwiekszej)
        if self.random == False:
            self.perm_unsort.sort(key=itemgetter(5))

            #print("perm_unsort: ", end="")
            #print(self.perm_unsort)
            for idx11 in range(0, len(self.perm_unsort)):
                for idx22 in range(0, len(self.perm_unsort[idx11])):
                    if idx22 == 5:
                        #print("sum:", self.perm_unsort[idx11][idx22])
                        self.color_sum = self.perm_unsort[idx11][idx22]
                        HelperArrangement().append_weight_gen(self.color_sum)
                    else:
                        pass
                        #print("[", end="")
                        #print((self.perm_unsort[idx11][idx22][1]), end="-")
                        print(self.perm_unsort[idx11][idx22][0].print_str(), end=" ")
                        #print("]", end=" ")

                #Usuwanie wagi przed wybraniem maksymalnej figury
                self.perm_unsort[idx11].pop()
                #Wyszukiwanie najwyzszej karty [Card idx][Card idx] ... [Card idx]
                self.high_card = max(self.perm_unsort[idx11])[0]
                # for idx33 in range(0, len(self.perm_unsort[idx11])):
                #     HelperArrangement.append_cards_all_permutations(self.perm_unsort[idx11][idx33][0])

                self.print_arrengement()

            self.num_arr = 0

        HelperArrangement().check_if_weights_larger()

        return HelperArrangement().random_arrangement()