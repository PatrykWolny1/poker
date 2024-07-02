from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
from itertools import permutations, combinations, chain
from operator import itemgetter
import random
#import numpy as np
import time

class TwoPairs(object):
    cardmarkings = CardMarkings()  # Oznaczenia kart
    cards_2d = []                  # Przygotowanie listy pod kombinacje i permutacje
    cards_2d_acc = []              # Lista pomocnicza
    cards_begin = []               # Lista pomocnicza
    cards_comb = []                # Lista na kombinacje
    perm = []                      # Lista na permutacje
    perm_unsort = []               # Lista po odsortowaniu
    indices_2d_name = []           # Lista na indeksy tych samych kart (figury)
    two_pairs_sum = 0              # Suma wag
    all_perm_size = 0              # Liczba wszystkich permutacji dla danej iteracji
    high_card = None               # Wysoka karta
    count = 0                      # Licznik do funkcji temp_lambda()

    random = False
    example = False
    if_not_two_pairs = False

    num_arr = 0                    # Licznik ukladow
    idx_high_c = 0                 # Zmienna pomocnicza do dodania kolumny z wysoka karta
    rand_iter = 0                  # Ile iteracji zostalo wykonanych w celu ograniczenia liczby obliczen
    rand_int = 0                   # Wylosowany uklad
    limit_rand = 2                 # Ograniczenie dla liczby obliczen
    all_perm_rand = []             # Wszystkie permutacje do wylosowania ukladu
    weight_gen = []                # Lista na wagi

    #loading_bar()
    step_p = True
    str_1 = ""
    n_bar = 14826240                        # Ilosc ukladow (trzeba uruchomic program i policzyc)
    step_bar = int(n_bar / 42)            # Ilosc punktow ladowania (40 - dzielnik)
    step_bar_finished = int(n_bar / 7)   # Ilosc zaladowanych punktow (co jeden) [.####][..###]
    count_bar = 0

    def set_cards(self, cards):
        self.perm = cards
        self.example = True

    def get_weight(self):
        if self.two_pairs_sum > 0:
            return self.two_pairs_sum

    def loading_bar(self):
        # Pasek postepu

        # Pierwsza wartosc step_p to prawda
        # Tworzony jest pasek postepu stworzony ze znakow "#"
        if self.step_p:
            for i in range(0, self.n_bar, self.step_bar):
                self.str_1 += "#"
        # Tutaj nastepuje wyswietlenie paska ze znakow "#"
        if self.step_p:
            print("[", end="")
            print(self.str_1, end="]\n")
            # os.system('cls')
            self.step_p = False
        # Zamiana znaku "#" na ".", co okreslona liczbe iteracji
        if self.step_p == False and (self.count_bar % self.step_bar_finished) == 0:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")
            # os.system('cls')
        # Ostatnia iteracja zamiana znaku
        if self.count_bar == self.n_bar - 1:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")

    def print_arrengement(self):
        if self.random == False:
            print("Dwie pary:", self.two_pairs_sum, "Wysoka Karta:", self.high_card[0].print_str(), "Numer:", self.num_arr)
        if self.random == True:
            print("Dwie pary:", self.two_pairs_sum, "Wysoka Karta:", self.high_card[0].print_str(), "Numer:", self.rand_int)

        self.num_arr += 1

    def dim(self, a):
        #Jesli to nie jest lista to zwroc pusty zbior
        if not type(a) == list:
            return []
        #Rekurencja. Dodawanie kolejno dlugosci kolejnych tablic np. [1 5 10 15] czyli 4-wymiarowa
        return [len(a)] + self.dim(a[0])

    def get_indices(self, cards):
        if len(self.dim(cards)) == 1:
            cards = [cards]

        self.indices_2d_name = []

        for idx in range(0, len(cards)):
            for idx1 in range(0, len(cards[idx])):
                indices = []
                for idx2 in range(0, len(cards[idx])):
                    if cards[idx][idx1].name == cards[idx][idx2].name:
                        indices.append(idx2)
                self.indices_2d_name.append(indices)
        #print(self.indices_2d_name)

    def filter_func(self, list_comb):
        #Filtruje liste o permutacje ktore nie sa dwiema parami
        self.get_indices(list_comb)

        count = 0

        for idx in range(0, len(self.indices_2d_name)):
            #Jesli wiecej niz 2 takie same karty to zwroc falsz
            if len(self.indices_2d_name[idx]) > 2:
                count += 1
        if count > 0:
            return False
        else:
            return True

    # def moving_average(a, n=3):
    #     ret = np.cumsum(a, dtype=float)
    #     ret[n:] = ret[n:] - ret[:-n]
    #     return ret[n - 1:] / n

    def temp_lambda(self, t1):
        # Jesli koniec sekwencji wag i sumy [[Card int] [Card int] ... [Card int] sum][[Card int] ... [Card int] sum]
        if self.count == 7:
            self.count = 0
            return

        self.count += 1

        # Zamiana indeksu kart (LISTA!) na string (SAMA LICZBA) (czyli self.count < 6, gdzie poczatek self.count zaczyna sie od 1)
        if self.count < 6:
            t2 = ''.join(map(str, t1[1]))
            if int(t2) < 5:
                return t1[1]
        # Zamiana wagi calego ukladu na string (bez listy)
        elif self.count == 6:
            # t3 = ''.join(map(str, t1))
            # if int(t3) > 4:
            return t1

    def check_if_weights_larger(self):
        # Sprawdzanie czy wagi w wygenerowanych ukladach sa wieksze niz poprzedni uklad (min -> max)
        self.weight_gen = [ele for ele in self.weight_gen if ele != []]
        indices = []
        # print("Wagi: ")
        count_all_weights = 0
        idx1 = 1
        for idx2 in range(0, len(self.weight_gen)):
            if (idx1 == len(self.weight_gen) - 1):
                print("Dlugosc tablicy: ", len(self.weight_gen))
                print("Wszystkie liczby sprawdzone: ", count_all_weights)
                break
            if (self.weight_gen[idx2] <= self.weight_gen[idx1]):
                #print(self.weight_gen[idx2], "[", idx2, "]", "<=", self.weight_gen[idx1], "[", idx1, "]")
                count_all_weights += 1
            else:
                #Dodawanie indeksow permutacji ktore nie pasuja (poprzednia wieksza od nastepnej)
                indices.append(idx2)
                indices.append(idx1)
            idx1 += 1

        #Wyswietlenie ukladow ktore nie pasuja
        for idx in range(0, len(indices)):
            for idx1 in range(0, len(self.all_perm_rand[indices[idx]])):
                if idx1 < 5:
                    print(self.all_perm_rand[indices[idx]][idx1][0].print_str(), end=" ")
                if idx1 == 5:
                    print(self.all_perm_rand[indices[idx]][idx1], end=" ")
                    print(indices[idx])
            print()

    def random_arrangement(self):
        self.rand_int = random.randint(0, len(self.all_perm_rand) - 1)

        print("Wylosowany uklad: ", self.rand_int)
        print("Ilosc ukladow: ", len(self.all_perm_rand))

        for idx2 in range(0, len(self.all_perm_rand[self.rand_int])):
            #Jesli karty od 1 do 5
            if idx2 < 5:
                #Usuwanie indeksow kart od 1 do 5
                self.all_perm_rand[self.rand_int][idx2][1].pop()
                #self.perm_unsort[self.rand_int][idx2][1].pop()
            #Jesli indeks jest rowny elementowi suma wag dwoch par
            if idx2 == 5:
                #Dodaj do zmiennej sume wag
                self.two_pairs_sum = self.all_perm_rand[self.rand_int][idx2]
            #Jesli indeks rowny elementowi wysoka karta
            if idx2 == 6:
                #Dodaj do zmiennej element wysoka karta
                self.high_card = self.all_perm_rand[self.rand_int][idx2]
            #Usuwanie sumy wag oraz wysokiej karty zeby zostaly same karty przygotowane do dalszego przetwarzania
            if idx2 in [5, 6]:
                self.all_perm_rand[self.rand_int][idx2] = [self.all_perm_rand[self.rand_int][idx2]]
                self.all_perm_rand[self.rand_int][idx2].pop()

        # Usuwanie podwojnej tablicy do pojedynczej
        self.all_perm_rand[self.rand_int] = list(chain.from_iterable(self.all_perm_rand[self.rand_int]))
        # Usuwanie pustych list z listy
        self.all_perm_rand[self.rand_int] = [ele for ele in self.all_perm_rand[self.rand_int] if ele != []]


        if self.random != True:
            # Wyswietlenie kart
            for idx2 in range(0, len(self.all_perm_rand[self.rand_int])):
                print(self.all_perm_rand[self.rand_int][idx2].print_str(), end=" ")

            self.print_arrengement()

        return self.all_perm_rand[self.rand_int]

    def two_pairs(self, cards_perm = []):
        two_pairs_weight = 0    # Tymczasowa zmienna na wage
        perm_unsorted = []      # Lista nieposortowana
        perm_unsort = []        # Lista odsortowana
        count_two_pairs = 0     # Zmienna potrzebna do okreslenie czy sa dwie pary
        c_two_pairs = False     # Zmienna tymczasowa (pomocnicza)
        pow_two_pairs = 4       # Potega dla jednej i drugiej pary [4 6]
        self.two_pairs_sum = 0  # Zmienna zawierajaca sume wag tymczasowych

        # Jesli podany jest przykladowy uklad
        if self.example == True:
            cards_perm = self.perm # Lista prawdopodobnie nie potrzebna cards_perm

        # Dodanie indeksow do nowej tablicy zlozonej z tablicy glownej w celu powrotu ze
        # stanu posortowanego do nieposortowanego
        i = 0
        j = 0
        b = []
        t = []
        check = True
        while check:
            t.append([cards_perm[j], [i]])
            i += 1
            j += 1
            if j == 5:
                b.append(t.copy())
                check = False

        cards_perm.sort()

        self.get_indices(cards_perm)

        # Usuniecie wymiaru z tablicy oraz przypisanie do tablicy nieposortowanej
        perm_unsorted = list(chain.from_iterable(b))

        # Sortowanie wedlug klucza (t1[0] == Card) czyli wedlug samych kart bez indeksow
        perm_sorted = sorted(perm_unsorted, key=lambda t1: t1[0])

        # Okreslenie czy uklad to dwie pary
        for idx in range(0, len(self.indices_2d_name)):
            # Jesli wystepuje 1 karta to jest to wysoka karta
            if len(self.indices_2d_name[idx]) == 1:
                #Przypisanie wysokiej karty z posortowanej tablicy
                self.high_card = perm_sorted[self.indices_2d_name[idx][0]]
                two_pairs_weight = pow(perm_sorted[self.indices_2d_name[idx][0]][0].weight, 2)
                # Sumowanie tymczasowej wagi wysokiej karty
                self.two_pairs_sum += two_pairs_weight

            # Jesli wystepuja dwie takie same karty to jest to para
            if len(self.indices_2d_name[idx]) == 2:
                # Dla pierwszej iteracji (jednej pary) count_two_pairs != 0
                # if c_two_pairs == True:
                #     c_two_pairs = False
                #     count_two_pairs = 0
                count_two_pairs += 1

                # Jesli jedna para z tablicy self.indices_2d_name czyli [1, 1][1, 1]
                if count_two_pairs == 4:
                    # print(perm_sorted[self.indices_2d_name[idx][0]][0].weight)
                    # print(perm_sorted[self.indices_2d_name[idx][1]][0].weight)
                    two_pairs_weight = pow(perm_sorted[self.indices_2d_name[idx][0]][0].weight, pow_two_pairs)
                    self.two_pairs_sum += two_pairs_weight
                    two_pairs_weight = pow(perm_sorted[self.indices_2d_name[idx][1]][0].weight, pow_two_pairs)
                    self.two_pairs_sum += two_pairs_weight
                    # Zwiekszenie potegi do 6 dla nastepnej pary (wyzszej)
                    pow_two_pairs = 6
                    # Pierwsza iteracja zakonczona
                    c_two_pairs = True

            if len(self.indices_2d_name[idx]) == 3:
                return True

        self.two_pairs_sum += 10069253
        perm_sorted.append([self.two_pairs_sum])

        if self.example == True and c_two_pairs == True:
            self.print_arrengement()
        # for idx1 in range(0, len(perm_sorted)):
        #     if idx1 != 5:
        #         print(perm_sorted[idx1][0].print_str(), end=" ")
        #     else:
        #         print(perm_sorted[idx1])
        #         print(self.high_card[0].print_str())
        #print(self.perm_unsort)

        else:
            self.two_pairs_sum = 0

        self.count = 0
        # Odsortowanie tablicy za pomoca indeksow
        self.perm_unsort.append(sorted(perm_sorted.copy(), key = self.temp_lambda))

        # Dodawanie wysokiej karty do tablicy
        self.perm_unsort[self.idx_high_c].append([self.high_card[0]])

        # Indeks dla nieposortowanej tablicy
        self.idx_high_c += 1

        # for idx1 in range(0, len(perm_unsort)):
        #     if idx1 != 5:
        #         print(self.perm_unsort[idx1][0].print_str(), end=" ")
        #     else:
        #         print(self.perm_unsort[idx1])
        #         print(self.high_card[0].print_str())

        #Calkowita suma ukladu
        #print("WAGA UKLADU: ", self.two_pairs_sum, " WYSOKA KARTA: ", self.high_card[0].print_str())

    def combinations_generating(self):
        perm_size = 0

        self.cards_comb = list(combinations(self.cards_begin, 5))

        self.cards_comb = [list(i) for i in self.cards_comb]

        # Filtrowanie listy z niepotrzebnych ukladow kart
        self.cards_comb = list(filter(self.filter_func, self.cards_comb)).copy()

        #print("Ilosc kombinacji: ", len(self.cards_comb))

        # for idx in range(0, len(self.cards_comb)):
        #     for idx1 in range(0, len(self.cards_comb[idx])):
        #         self.cards_comb[idx][idx1].print()
        #     print()

        for idx1 in range(0, len(self.cards_comb)):
            self.perm.append(list(permutations(self.cards_comb[idx1], 5)))

        # Zamiana tuple na list
        self.perm = [[list(j) for j in row[0:]] for row in self.perm]

        #print(self.perm)

        for idx in range(0, len(self.perm)):
            for idx1 in range(0, len(self.perm[idx])):
                if_not_two_pairs = self.two_pairs(self.perm[idx][idx1])
                if if_not_two_pairs:
                    return None
                for idx2 in range(0, len(self.perm[idx][idx1])):
                    pass
                    #self.count_bar += 1
                    #self.loading_bar()
                    #self.perm[idx][idx1][idx2].print()
                #print()

        # Sortowanie z kluczem (wedlug wag)
        self.perm_unsort.sort(key = itemgetter(5))


        #print(self.perm_unsort)
        for idx1 in range(0, len(self.perm_unsort)):
            for idx2 in range(0, len(self.perm_unsort[idx1])):
                self.count_bar += 1
                self.loading_bar()
                pass
                # if idx2 < 5:
                #     print(self.perm_unsort[idx1][idx2][0].print_str(), end = " ")
                # if idx2 == 5:
                #     self.perm_unsort[idx1][idx2] = int(''.join(map(str, self.perm_unsort[idx1][idx2])))
                #     self.two_pairs_sum = self.perm_unsort[idx1][idx2]
                #     print(self.perm_unsort[idx1][idx2], end = " ")
                # if idx2 == 6:
                #     self.high_card = self.perm_unsort[idx1][idx2]
                #     self.print_arrengement()

            self.weight_gen.append(self.two_pairs_sum)
            self.all_perm_rand.append(self.perm_unsort[idx1].copy())
            #print()

        # print("------------------------------------------------------------------")
        # print("##################################################################")
        # print("------------------------------------------------------------------")

        perm_size = len(self.perm[0])

        #print("Ilosc permutacji: ", len(self.perm) * len(self.perm[0]))

        self.all_perm_size += len(self.cards_comb) * perm_size

        #print("Ilosc permutacji: ", self.all_perm_size)
        #print("comb_size * perm_size", perm_size, len(self.cards_comb))
        #print("Ilosc permutacji: ", len(self.cards_comb) * perm_size)
        #14826240

        if self.rand_iter == self.limit_rand and self.random == True:

            # for idx1 in range(0, len(self.weight_gen)):
            #     print(self.weight_gen[idx1])

            self.check_if_weights_larger()

            return self.random_arrangement()

        self.rand_iter += 1

        self.idx_high_c = 0
        self.perm_unsort.clear()
        self.perm.clear()
        self.cards_comb.clear()

    def two_pairs_generating(self, random):
        self.random = random

        self.cards_2d = []
        cards = []

        p = True
        q = False
        z = False

        idx = 0  # Do figur kart
        idx2 = 0  # While
        idx4 = 0  # Do pierwszych 8 kart
        limit_1 = 8  # Zakres kart w odniesieniu do calej talii
        limit_2 = 12
        count_1 = 0  # Pomocnicza do pierwszych 8 kart
        count_2 = 0  # Do iterowania zwieksza sie
        iter_count_2 = 11  # zmniejsza sie
        step = 0  # Krok do zakresu kart (limit_1 i limit_2)
        count_11 = 0  # Pomocnicza,
        count_all = 0  # Zwiekszana co iteracje do wyboru kart od danego ukladu 4 kart
        count_all_1 = 1  # Liczy uklady
        iter_count_1 = 12  # Zmienna okreslajaca ilosc figur uzytych w algorytmie (iteracje)
        iter_count_11 = 13  # Zmienna okreslajaca ilosc figur uzytych w algorytmie oznaczajaca
        # uklad znajdujacy sie o jedna iterecje nizej od iter_count_1
        i = 0  # Zmienna pomocnicza, inkrementowana do figur kart (idx)
        j = 0  # Zmienna pomocnicza, dekrementowana
        k = 9  # Zmienna okreslajaca koniec sprawdzanych ukladow
        x = False  # Zmienna uzywana do powtorzenia danej iteracji
        y = False  # Zmienna uzywana do powtorzenia danej iteracji
        l = 0  # Do iterowania (oznacza rozmiar ukladow), zwiekszana
        l_1 = -2  # Zmienna pomocnicza, zmniejszana

        while (p):
            m = len(self.cardmarkings.colors)
            while idx2 < m:
                # Dodawanie kart idx zwiekszany z kazda iteracja po to by nie powtarzaly sie karty
                self.cards_2d.append(Card(self.cardmarkings.arrangements[idx], self.cardmarkings.colors[idx2]))
                idx2 += 1
                idx4 += 1
                # Jesli dodawanie wszystkich 4 kolorow zakonczone
                if idx2 == 4:
                    idx += 1
                    idx2 = 0
                    count_1 += 1

                # Dodaje poczatek ukladu kart np. 2Ki 2Tr 2Pi 2Ka 3Ki 3Tr 3Pi 3Ka  || 3Ki 3Tr 3Pi 3Ka 4Ki 4Tr 4Pi 4Ka
                if count_1 == 2 and idx4 == 8:
                    self.cards_begin = self.cards_2d.copy()
                    # for idx11 in range(0, len(self.cards_begin)):
                    #     self.cards_begin[idx11].print()
                    # print()
                # Dodaje karty co 4 iteracje na poczatek sekwencji np. 2Ki 2Tr 2Pi 2Ka ... 4Ki 4Tr 4Pi 4Ka 5Ki 5Tr ... || ... 3Ki 3Tr ... 7Ki 7Tr 7Pi 7Ka ...
                if (((count_all + 1) % 8) == 0) or count_1 == 13 - count_11:
                    for idx11 in range(0, len(self.cards_2d)):
                        # self.cards_2d[idx11].print()
                        self.cards_2d_acc.append(self.cards_2d[idx11])
                    self.cards_2d = []

                    # for idx11 in range(0, len(self.cards_2d_acc)):
                    #     self.cards_2d_acc[idx11].print()
                    # print()
                    # print("COUNT_1", count_11)

                    if count_11 == 11:
                        self.check_if_weights_larger()
                        return self.random_arrangement()

                    # Jesli jest ostatnia karta to zacznij operacje A ... K ... Q ... J ... 10 ...
                    if count_1 == 13 - count_11:

                        # print()
                        # print()
                        # print("------------------------------------------------------------------")
                        # print("##################################################################")
                        # print("------------------------------------------------------------------")

                        while (True):

                            # for idx11 in range(0, len(self.cards_2d_acc)):
                            #     self.cards_2d_acc[idx11].print()

                            # print()
                            # print()

                            # print()

                            # for idx11 in range(0, len(self.cards_begin)):
                            #     self.cards_begin[idx11].print()
                            # print()

                            # for idx11 in range(0, len(self.cards_2d_acc)):
                            #     self.cards_2d_acc[idx11].print()
                            # print()

                            # print("count_all_1: ", count_all_1)

                            # Dla 1 karty omin zwiekszanie limitow
                            if count_all_1 == 1:
                                pass
                            else:
                                limit_1 += 4
                                limit_2 += 4

                            # Jesli zmiana iteracji sekwencji np. 2Ki 2Tr 2Pi 2Ka (1) ... AKi ATr APi AKa || 3Ki 3Tr 3Pi 3Ka (67) ... 4Ka 5Ki 5Tr 5Pi 5Ka
                            if count_all_1 in [67, 122, 167, 203, 231, 251, 267, 277]:
                                iter_count_1 += 1

                            # Zwieksz limit o krok jesli zmiana iteracji sekwencji (poziom nizej od powyzszej)(zbior)
                            if count_all_1 == iter_count_11 and z == True:
                                #print("------------------------------------------")
                                limit_1 = 8 + step
                                limit_2 = 16 + step

                            # Zmien limit
                            if count_all_1 == iter_count_1 and z == True:
                                limit_1 = limit_2 - 4

                            # Dla pierwszej iteracji nie zmieniaj kroku
                            if q:
                                step += 4
                                q = False

                            # Algorytm dla ustalenia wartosci iter_count_1 oraz iter_count_11
                            if (count_all_1 == iter_count_1 and z == True):
                                # iter_count_11 jest zawsze mniejszy o 1 od iter_count_1
                                iter_count_11 = iter_count_1 - 1

                                # print("##########################################")
                                # print("iter_COUNT_1: ", iter_count_1)
                                # print("J: ", j)
                                # print("K-1: ", k - 1)
                                # print("L: ", l)
                                if iter_count_11 in [67, 122, 168, 203]:
                                    pass
                                else:
                                    pass
                                    # print("iter_COUNT_11: ", iter_count_11)
                                    # print("##########################################")

                                if l in [2, 3]:
                                    iter_count_1 -= 1
                                if l in [4, 5, 6, 7, 8, 9]:
                                    iter_count_1 -= l_1

                                iter_count_1 += 10 - j

                                if j == k - 1:
                                    if x == True:
                                        k -= 1
                                    x = True
                                    j = 0

                                    if l in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                        y = False

                                    l += 1
                                    l_1 += 1

                                    if l in [2, 4, 5, 6, 7, 8, 9]:
                                        iter_count_11 -= 1
                                    if l == 3:
                                        iter_count_1 += 1

                                j += 1

                                if j == 1 and (k - 1) in [8, 7, 6, 5, 4, 3, 2, 1, 0] and y == False:
                                    j = 0
                                    y = True

                                iter_count_11 = iter_count_1 - 1

                                if l in [3, 4, 5, 6, 7, 8, 9]:
                                    iter_count_11 -= 1
                                    iter_count_1 -= 1

                            # Dla pierszej iteracji
                            if count_all_1 == 12 and z == False:
                                # print("##########################################")
                                # print("iter_COUNT_1: ", iter_count_1)
                                # print("J: ", j)
                                # print("K-1: ", k - 1)
                                # print("L: ", l)
                                # print("iter_COUNT_11: ", iter_count_11)
                                # print("##########################################")

                                limit_1 = 8
                                limit_2 = 16
                                iter_count_1 += 1
                            # Dla pierwszej iteracji
                            if count_all_1 == 13 and z == False:
                                # print("##########################################")
                                # print("iter_COUNT_1: ", iter_count_1)
                                # print("J: ", j)
                                # print("K-1: ", k - 1)
                                # print("L: ", l)
                                # print("iter_COUNT_11: ", iter_count_11)
                                # print("##########################################")

                                limit_1 = limit_2 - 4
                                iter_count_1 += 10
                                j += 1
                                z = True
                                iter_count_11 = iter_count_1 - 1

                            # Dla limitu powyzej liczby kart
                            if limit_1 == 52:
                                limit_1 = 12
                                limit_2 = 20

                            # Na podstawie wyliczonego limitu dodaj karty z tablicy o okreslonej liczbie kart
                            for idx11 in range(limit_1, limit_2):
                                self.cards_begin.append(self.cards_2d_acc[idx11])

                            # print("limit1: ", limit_1)
                            # print("limit2: ", limit_2)
                            # for idx11 in range(0, len(self.cards_begin)):
                            #     self.cards_begin[idx11].print()
                            # print()

                            #####################################TUTAJ UMIESCIC RESZTE
                            cards = self.combinations_generating()
                            if cards:
                                return cards

                            for idx11 in range(0, 4):
                                self.cards_begin.pop()

                            # for idx11 in range(0, len(self.cards_begin)):
                            #     self.cards_begin[idx11].print()
                            # print()

                            count_1 += 1
                            count_2 += 1

                            count_all_1 += 1

                            # Kolejna iteracja
                            if count_2 == iter_count_2:
                                # Usun karty z tablicy zeby dodac nastepne
                                for idx11 in range(0, 4):
                                    self.cards_begin.pop()
                                iter_count_2 -= 1
                                count_2 = 0
                                q = True

                                # for idx11 in range(0, len(self.cards_begin)):
                                #     self.cards_begin[idx11].print()
                                # print()

                                # Nowa iteracja (nastepna)
                                if iter_count_2 == 0:
                                    self.count_bar = 0
                                    q = False
                                    step = 0
                                    iter_count_2 = 10 - i
                                    i += 1
                                    idx = i
                                    idx2 = 0
                                    idx4 = 0
                                    count_1 = 0
                                    count_11 += 1
                                    count_all = -1
                                    limit_1 = 4
                                    limit_2 = 8
                                    self.rand_iter += 1
                                    self.cards_begin.clear()
                                    self.cards_2d_acc.clear()
                                    break
                                else:
                                    continue
                count_all += 1