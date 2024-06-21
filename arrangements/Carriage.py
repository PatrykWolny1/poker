from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
import itertools
import random

class Carriage(object):
    cardmarkings = CardMarkings()   #Oznaczenia kart
    weight_gen = []                 #Tablica na wagi kart
    cards = []
    cards_2d = []
    indices_2d = []                 #Indeksy ukladow kart
    cards_5 = []
    cards_perm = []                 #Tablica na permutacje
    cards_all_permutations = []     #Tablica na permutacje - losowy uklad
    comb = []                       #Tablica na kombinacje - indeksy
    combs = []                      #Tablica na kombinacje
    cards_perm_weights = []
    num_arr = 0
    rand_int = 0
    if_perm_weights = True
    print_permutations = True       #Wyswietlanie wszystkich permutacji
    example = False                 #Jesli jest recznie wpisany uklad
    random = False                  #Jesli jest losowanie ukladu
    step_p = True
    str_1 = ""
    n_bar = 74880
    step_bar = int(n_bar / 20)          #Zwiekszanie dlugosci paska ladowania
    step_bar_finished = int(n_bar / 19) #Jaka czesc stanowia kropki (zaladowane)
    step_p = True

    #Funkcja dla przykladowego ukladu wpisanego recznie
    def set_cards(self, cards):
        self.cards_perm_weights = cards
        self.if_perm_weights = False
        self.example = True

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

    def print_arrengement(self):
        print()
        if self.example:
            print("Kareta: ", self.weight_arrangement, "Numer: ", self.rand_int)
        if self.random and self.example == False:
            print("Kareta: ", self.weight_arrangement)
        if self.random == False and self.example == False:
            print("Kareta: ", self.weight_arrangement, " Numer: ", self.num_arr)

        self.num_arr += 1

    def check_if_weights_larger(self):
        # Sprawdzanie czy wagi w wygenerowanych ukladach sa wieksze niz poprzedni uklad (min -> max)
        self.weight_gen = [ele for ele in self.weight_gen if ele != []]
        indices = []
        # print("Wagi: ")
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
            elif (self.weight_gen[idx2] > self.weight_gen[idx1]):
                # Dodawanie indeksow permutacji ktore nie pasuja (poprzednia wieksza od nastepnej)
                indices.append(idx2)
                indices.append(idx1)
            idx1 += 1

        # Wyswietlenie ukladow ktore nie pasuja
        for idx in range(0, len(indices)):
            for idx1 in range(0, len(self.cards_all_permutations[indices[idx]])):
                print(self.cards_all_permutations[indices[idx]][idx1].print_str(), end=" ")
                if idx1 == 4:
                    print(indices[idx])
            print()

    def random_arrangement(self):
        #Zerowanie pustych wierszy
        self.random = True
        self.cards_all_permutations = [ele for ele in self.cards_all_permutations if ele != []]

        self.rand_int = random.randint(0, len(self.weight_gen) - 1)

        print("Wylosowany uklad: ", self.rand_int)
        print("Ilosc ukladow: ", len(self.cards_all_permutations))

        self.cards_perm = self.cards_all_permutations[self.rand_int]
        self.carriage()

        return self.cards_all_permutations[self.rand_int]

    def get_indices_comb(self):
        size = len(self.comb)
        #self.indices_2d = []

        #Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        idx1 = 0
        idx3 = 0
        while idx1 < size - idx3:
            amount = 0
            for (index, card) in enumerate(self.comb[idx1]):
                indices = []
                for idx2 in range(0, len(self.comb[idx1])):
                    if card.name == self.comb[idx1][idx2].name:
                        indices.append(index)
                self.indices_2d.append(indices)
                #Jesli wystepuje wiecej niz 1 taka sama karta w ukladzie kart
                if len(indices) > 1:
                    amount += 1
            if amount > 1:
                del(self.comb[idx1])
                idx3 += 1
            else:
                idx1 += 1

    def get_indices(self, cards):
        size = len(cards)
        self.indices_2d = []

        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        for idx in range(0, size):
            indices = []
            for (index, card) in enumerate(cards):
                if card.name == cards[idx].name:
                    indices.append(index)
            self.indices_2d.append(indices)
        # print(self.indices_2d)

    def carriage(self):
        # Sprawdzanie czy uklad kart to kareta oraz przypisanie wagi do ukladu

        if self.if_perm_weights:
            self.cards_perm_weights = []
            # Sprawdzanie czy tablica indeksow nie jest pusta
            if len(self.indices_2d) != 0:
                for idx1 in self.cards_perm:
                    # Zapisanie ukladow w innej tablicy bo tablica self.cards_perm jest zerowana w check_generate_cards
                    self.cards_perm_weights.append(Card(idx1.name, idx1.color))
        else:
            self.get_indices(self.cards_perm_weights)

        size = len(self.indices_2d)

        if_carriage = 0
        weight_1 = 0
        weight_2 = 0

        # Waga ukladu
        self.weight_arrangement = 0

        for i in range(0, size):
            # print("Rozmiar: ", len(self.indeksy_2d[i]))
            # Jesli w wierszu tablicy znajduja sie 4 elementy | Indeksy powtorek, jesli jest kareta to dlugosc = 4
            if (len(self.indices_2d[i]) == 4):
                for j in range(0, len(self.indices_2d[i])):
                    weight_1 = pow(self.cards_perm_weights[self.indices_2d[i][j]].weight, 4)
                if_carriage += 1
            # Ostatnia karta
            if (len(self.indices_2d[i]) == 1):
                for j in range(0, len(self.indices_2d[i])):
                    weight_2 = self.cards_perm_weights[self.indices_2d[i][j]].weight * 1
            if (i == size - 1) and (if_carriage == 4):
                self.weight_arrangement = (weight_1 + weight_2) + 2221
                self.weight_gen.append(self.weight_arrangement)
                if self.example == True:
                    self.print_arrengement()

    def check_generate_cards(self, cards_2d):
        # Generowanie 5 kart oraz sprawdzanie jaki to uklad

        for idx1 in range(0, len(cards_2d)):
            for idx2 in range(0, len(cards_2d[idx1])):
                self.cards.append(cards_2d[idx1][idx2])
                # W tablicy kart przypisz uklad kart do nowej tablicy do czwartej karty
                if idx2 % 4 == 0 and idx2 > 0 and idx2 < 5:
                    self.cards_5 = self.cards[:]

                # for idx3 in range(0, len(self.cards_5)):
                #     self.cards_5[idx3].print()

                if idx2 > 3:
                    self.cards_5.pop()
                    self.cards_5.append(cards_2d[idx1][idx2])

                    self.perm = self.cards_5

                    self.combs = list(itertools.permutations(self.perm))

                    # for idx7 in range(0, len(self.combs)):
                    #     for idx8 in range(0, len(self.combs[idx7])):
                    #         self.combs[idx7][idx8].print()
                    #     print()

                    unique = set(self.combs)

                    for idx5 in unique:
                        self.cards_perm = []

                        for idx6 in range(0, len(idx5)):
                            self.cards_perm.append(idx5[idx6])

                        if self.print_permutations and self.random == False:
                            for idx7 in range(0, len(self.cards_perm)):
                                self.cards_perm[idx7].print()
                        else:
                            self.num_arr += 1
                            self.loading_bar()

                        self.cards_all_permutations.append(self.cards_perm)

                        self.get_indices(self.cards_perm)
                        self.carriage()
                        if self.random == False:
                            self.print_arrengement()
            self.cards = []

        self.check_if_weights_larger()

        return self.random_arrangement()

    def carriage_generating(self, random):
        #Zmienna uzywana do okreslenia czy uklad bedzie losowany
        self.random = random
        shift = 0

        #Iterowanie po figurach
        for i in range(0, len(self.cardmarkings.arrangements)):
            self.cards_1d = []
            #Iterowanie po kolorach
            for color in self.cardmarkings.colors:
                #Zapisanie do tablicy karty (figura i kolor)
                self.cards_1d.append(Card(self.cardmarkings.arrangements[i], color))
                #Ostatni kolor
                if color == 'Ka':
                    #To zapisanie 4 pierwszych figur o roznych kolorach
                    self.cards_2d.append(self.cards_1d)
                    #Zapisanie reszty kart
                    for color in range(0, len(self.cardmarkings.colors)):
                        for m in range(0, len(self.cardmarkings.arrangements)):
                            self.cards_1d.append(Card(self.cardmarkings.arrangements[m], self.cardmarkings.colors[color]))
                    #Usuwanie powtarzajacych sie kart w kolejnych partiach kart
                    z = 0
                    for idx in range(0, 3):
                        self.cards_1d.pop(17 + z + shift)
                        z += 12
                    #Usuwanie takiej samej karty jaka jest w ukladzie kareta np. 4 4 4 4  pop(4)
                    self.cards_1d.pop(4+shift)
                    #Zmienna pomocnicza poniewaz taka sama karta przesuwa sie co n indeksow
                    shift += 1

        #Ostateczna forma np.
        # 2Ki 2Tr 2Pi 2Ka 3Ki 4Ki ... AKi 3Tr 4Tr ... ATr 3Pi 4Pi ... APi 3Ka 4Ka ... AKa

        # for idx1 in range(0, len(self.cards_2d)):
        #     for idx2 in range(0, len(self.cards_2d[idx1])):
        #         self.cards_2d[idx1][idx2].print()
        #     print()

        return self.check_generate_cards(self.cards_2d)


