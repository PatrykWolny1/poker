from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
from itertools import permutations, combinations
import random
from operator import itemgetter
from itertools import chain

class Color(object):
    cardmarkings = CardMarkings()  #Oznaczenia kart
    cards_2d = []
    perm = []
    weight_gen = []
    cards_all_permutations = []
    high_card = None
    color_weight = 0
    color_sum = 0
    num_arr = 0
    rand_int = 0
    perm_final_2 = []
    all_permutations = False
    count = 0
    perm_unsort = []
    random = False
    example = False
    step_p = True
    count = 0
    count_1 = 0
    count_2 = 0
    str_1 = ""
    n_bar = 611519                             #Ilosc ukladow (trzeba uruchomic program i policzyc)
    n_bar_2 = 5095
    step_bar = int(n_bar / 40)                 #Ilosc punktow ladowania (40 - dzielnik)
    step_bar_2 = int(n_bar_2 / 30)
    step_bar_finished = int(n_bar / 40)        #Ilosc zaladowanych punktow (co jeden) [.####][..###]
    step_bar_finished_2 = int(n_bar_2 / 31)

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = True

    def get_weight(self):
        if self.color_sum > 0:
            return self.color_sum

    def loading_bar(self):
        #Pasek postepu
        #Jesli random = True to wybierana jest wartosc pierwsza
        #Przyklad count_1_2_func to funkcja przyjmujaca argument random

        count_1_2_func = lambda random: self.count_1 if self.random else self.count_2
        n_bar_func = lambda random: self.n_bar if self.random else self.n_bar_2
        step_bar_func = lambda random: self.step_bar if self.random else self.step_bar_2
        step_bar_finished_func = lambda random: self.step_bar_finished if self.random else self.step_bar_finished_2

        #Pierwsza wartosc step_p to prawda
        #Tworzony jest pasek postepu stworzony ze znakow "#"
        if self.step_p:
            for i in range(0, n_bar_func(self.random), step_bar_func(self.random)):
                self.str_1 += "#"
        #Tutaj nastepuje wyswietlenie paska ze znakow "#"
        if self.step_p:
            print("[", end="")
            print(self.str_1, end="]\n")
            # os.system('cls')
            self.step_p = False
        #Zamiana znaku "#" na ".", co okreslona liczbe iteracji
        if self.step_p == False and (count_1_2_func(self.random) % step_bar_finished_func(self.random)) == 0:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")
            # os.system('cls')
        #Ostatnia iteracja zamiana znaku
        if self.count_1 == n_bar_func(self.random) - 1:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")

    def dim(self, a):
        #Jesli to nie jest lista to zwroc pusty zbior
        if not type(a) == list:
            return []
        #Rekurencja. Dodawanie kolejno dlugosci kolejnych tablic np. [1 5 10 15] czyli 4-wymiarowa
        return [len(a)] + self.dim(a[0])

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
            for idx1 in range(0, len(self.perm_unsort[indices[idx]])):
                if idx1 < 5:
                    print(self.perm_unsort[indices[idx]][idx1][0].print_str(), end=" ")
                if idx1 == 5:
                    print(self.perm_unsort[indices[idx]][idx1], end=" ")
                    print(indices[idx])
            print()

    def random_arrangement(self):
        self.perm_unsort = [ele for ele in self.perm_unsort if ele != []]

        self.rand_int = random.randint(0, len(self.perm_unsort) - 1)

        print("Wylosowany uklad: ", self.rand_int)
        print("Ilosc ukladow: ", len(self.perm_unsort))

        #Usuwanie indeksow do sortowania tablicy zeby zostaly same karty
        for idx in range(0, len(self.perm_unsort[self.rand_int])):
            self.perm_unsort[self.rand_int][idx].pop()

        #Usuwanie podwojnej tablicy do pojedynczej
        self.perm_unsort[self.rand_int] = list(chain.from_iterable(self.perm_unsort[self.rand_int]))

        self.high_card = max(self.perm_unsort[self.rand_int])

        self.random = True

        return self.perm_unsort[self.rand_int]

    def print_arrengement(self):
        if self.random == False:
            print("Kolor:", self.color_sum, "Wysoka Karta:", self.high_card.print_str(), "Numer:", self.num_arr)
        elif self.random == True:
            print("Kolor:", self.color_sum, "Wysoka Karta:", self.high_card.print_str(), "Numer:", self.rand_int)

        self.num_arr += 1

    def get_indices_color(self, cards):
        self.indices_2d_color = []

        if self.random == True and self.example == True:
            for idx in range(0, len(cards)):
                indices = []
                for (index, card) in enumerate(cards):
                    if card.color == cards[idx].color:
                        indices.append(index)
                self.indices_2d_color.append(indices)
            #print(self.indices_2d_color)
            return

        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart
        for idx in range(0, len(cards)):
            for idx1 in range(0, len(cards[idx])):
                indices = []
                for (index, card) in enumerate(cards[idx]):
                    if card.color == cards[idx][idx1].color:
                        indices.append(index)
                self.indices_2d_color.append(indices)
        #print(self.indices_2d_color)

    def check_if_straight_royal_flush(self):
        #Sprawdzanie czy w ukladach kart znajduje sie Poker lub Poker Krolewski (do eliminacji)
        count = 0
        for idx, idx1 in zip(range(0, len(self.perm) - 1), range(1, len(self.perm))):
            #Karty musza byc poukladane od najmniejszej do najwiekszej w odstepie wartosci wagi wynoszacej 1
            #As jest traktowany jako najwyzsza karta lub najnizsza wtedy roznica miedzy A, a 2 wynosi 9
            if (self.perm[idx1].weight - self.perm[idx].weight == 1 or
                    (self.perm[4].weight == 13 and self.perm[idx1].weight - self.perm[idx].weight == 9)):
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
            if ((self.cards_2d[idx1][idx3].weight - self.cards_2d[idx1][idx2].weight < 2) or
                    #Wykrywanie kombinacji kart A 2 3 4 5
                    (self.cards_2d[idx1][4].weight == 13 and self.cards_2d[idx1][idx3].weight - self.cards_2d[idx1][idx2].weight == 9)):
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

            #Pobranie indeksow tablicy, gdzie wystepuja takie same kolory
            self.get_indices_color(self.perm)

            #Lista ma dlugosc 1 w ktorej znajduje sie kolejna lista z kartami, a dalej z waga ukladu
            for idx1 in range(0, len(self.indices_2d_color) - 4):
                #Jesli wystepuje 5 kolorow to jest to uklad Kolor
                if len(self.indices_2d_color[idx1]) == 5:
                    for idx in range(0, len(self.perm)):
                        #Dla kart innych niz najwyzsza policz czesciowo wage ukladu
                        if self.perm[idx] != max(self.perm):
                            #Potega od 1 do 4
                            self.color_weight = pow(self.perm[idx].weight, idx + 1)
                            self.color_sum += self.color_weight

                    self.high_card = max(self.perm)
                    self.color_weight = pow(self.high_card.weight, 5)

                    #Calkowita suma ukladu
                    self.color_sum += self.color_weight + 12007274

                    # print()
                    # for idx in range(0, len(self.perm_unsorted)):
                    #     self.perm_unsorted[idx].print()
                    # print()

                    self.print_arrengement()
                    return
            return

        #Obliczenia dla wyswietlenia wszystkich permutacji ukladu Kolor
        #Jesli tablica jest jednowymiarowa to dodaj jeden wymiar w celu uruchomienia nastepnej petli
        if len(self.dim(self.perm)) == 1:
            self.perm = [self.perm]

        for idx in range(0, len(self.perm)):
            self.get_indices_color(self.perm[idx])

            for idx1 in range(0, len(self.indices_2d_color) - 4):
                if len(self.indices_2d_color[idx1]) == 5:
                    for idx2 in range(0, len(self.perm[idx])):
                        self.color_weight = 0
                        self.color_sum = 0

                        # for k in range(0, len(self.perm[idx][idx2])):
                        #     self.perm[idx][idx2][k].print()
                        # print()

                        if self.random == True:
                            self.count_1 += 1
                            self.loading_bar()

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

                        #print("SUM: ", self.color_sum)

                        #Zrobic z perm unsorted i dodac do self.perm_temp
                        if self.all_permutations:
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

                self.count_2 += 1
                self.loading_bar()
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
        if self.random != True:
            self.perm_unsort.sort(key=itemgetter(5))

            #print("perm_unsort: ", end="")
            #print(self.perm_unsort)
            for idx11 in range(0, len(self.perm_unsort)):
                for idx22 in range(0, len(self.perm_unsort[idx11])):
                    if idx22 == 5:
                        print("sum:", self.perm_unsort[idx11][idx22])
                        self.color_sum = self.perm_unsort[idx11][idx22]
                        self.weight_gen.append(self.color_sum)
                    else:
                        #print("[", end="")
                        #print((self.perm_unsort[idx11][idx22][1]), end="-")
                        print(self.perm_unsort[idx11][idx22][0].print_str(), end=" ")
                        #print("]", end=" ")

                #Usuwanie wagi przed wybraniem maksymalnej figury
                self.perm_unsort[idx11].pop()
                #Wyszukiwanie najwyzszej karty [Card idx][Card idx] ... [Card idx]
                self.high_card = max(self.perm_unsort[idx11])[0]
                self.print_arrengement()

            self.num_arr = 0

        self.check_if_weights_larger()

        return self.random_arrangement()