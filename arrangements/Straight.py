from classes.Card import Card
from arrangements.HelperArrangement import HelperArrangement
from arrangements.LoadingBar import LoadingBar
from arrangements.CardMarkings import CardMarkings
import itertools

class Straight(HelperArrangement):
    cardmarkings = CardMarkings()   #Oznaczenia kart
    loading_bar = LoadingBar(1224000, 40, 40)

    cards = []                      #Tablica na karty
    perm = []                       #Tablica na permutacje do wag - posortowana

    num_arr = 0                     #Liczenie ukladow kart w kolejnych iteracjach
    weight_arrangement = 0          #Zmienna pomocnicza do sumowania wagi ukladu
    straight_iter = 0               #Liczenie ile iteracji zostalo wykonanych
    c_idx6 = 0
    c_idx6_iter = 0

    random = False                  #Jesli jest losowanie ukladu
    example = False                 #Jesli jest recznie wpisany uklad

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
        if self.random == False:
            print("Strit: ", self.weight_arrangement, " Numer: ", self.num_arr)
        if self.random == True:
            print("Strit: ", self.weight_arrangement, " Numer: ", self.rand_int)

        self.num_arr += 1

    def remove_royal_flush(self, cards_comb_list):
        # Pobranie indeksow kolorow czyli okreslenie indeksow w jakich wystepuja
        HelperArrangement().get_indices_color(cards_comb_list)

        for idx1 in range(0, len(self.get_indices_2d_color())):
            #Jesli wystepuje 5 kolorow w ukladzie
            if len(self.get_indices_2d_color()[idx1]) == 5:
                return True

        return False

    def remove_more_1(self, cards_comb_list):
        #Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        HelperArrangement().get_indices_1(cards_comb_list)

        for i in range(0, len(HelperArrangement().get_indices_2d_1())):
            if (len(HelperArrangement().get_indices_2d_1()[i]) > 1):  # Jesli w wierszu tablicy znajduje sie wiecej niz 1 element
                return True

        return False

    def straight(self):
        if len(HelperArrangement().dim(self.perm)) == 1:
            self.perm = [self.perm]
            self.c_idx6 = 0
            self.c_idx6_iter = (120*1020) + 1
            if sorted(self.perm[self.c_idx6])[4].weight == 13 and sorted(self.perm[self.c_idx6])[3].weight == 4:
                self.c_idx6_iter = 0      
            HelperArrangement().clear_indices_2d_1()
            HelperArrangement().clear_indices_2d_color()

        
        # Przygotowanie tablicy do sortowania. Sortowanie jest uzywane zeby ulatwic okreslenie czy jest to strit
        #self.perm[self.c_idx6] = sorted(self.perm[self.c_idx6], key=lambda x: x.weight)
        # Pobranie indeksow gdzie wystepuja powtorzenia kolorow lub pojedynczy kolor

        HelperArrangement().get_indices_color(self.perm[self.c_idx6], random = True, example = True)
        HelperArrangement().get_indices_1(self.perm[self.c_idx6])

        # for idx1 in range(0, len(self.perm[self.c_idx6])):
        #     sorted(self.perm[self.c_idx6])[idx1].print()
        # print()

        weight_iter = 0
        straight_weight = 0
        calc_weights = True
        idx1 = 0
        idx2 = 1

        while (calc_weights):

            # Dla posortowanej tablicy sprawdz czy waga jest mniejsza od kolejnej
            for idx3, idx4 in zip(range(0, len(HelperArrangement().get_indices_2d_color())), range(0, len(HelperArrangement().get_indices_2d_1()))):
                # Jesli jest 5 takich samych kolorow to powrot z funkcji (poker krolewski)
                if len(HelperArrangement().get_indices_2d_color()[idx3]) == 5:
                    return
                if len(HelperArrangement().get_indices_2d_1()[idx4]) > 1:
                    return

            if idx1 == 4:
                break
            # Jesli waga pierwszej karty jest mniejsza od drugiej ... do 5 karty to jest to strit
            if ((sorted(self.perm[self.c_idx6])[idx2].weight - sorted(self.perm[self.c_idx6])[idx1].weight == 1) or
                    (sorted(self.perm[self.c_idx6])[4].weight == 13 and ((sorted(self.perm[self.c_idx6])[4].weight - sorted(self.perm[self.c_idx6])[3].weight) == 9))):

                if self.c_idx6_iter in range((120 * 1020) + 1): #120*1020
                    print(idx1 + 2, sorted(self.perm[self.c_idx6])[idx1].print_str())
                    straight_weight += pow(sorted(self.perm[self.c_idx6])[idx1].weight, idx1 + 2)
                    weight_iter += 1

                    if sorted(self.perm[self.c_idx6])[idx2].weight == 13:
                        print("1", sorted(self.perm[self.c_idx6])[idx2].print_str())
                        straight_weight += pow(sorted(self.perm[self.c_idx6])[idx2].weight, 1)
                        weight_iter += 1

                else:
                    #print(idx1 + 1, sorted(self.perm[self.c_idx6])[idx1].print_str())
                    straight_weight += pow(sorted(self.perm[self.c_idx6])[idx1].weight, idx1 + 1)
                    weight_iter += 1
                    #print(straight_weight)

                    if idx2 == 4:
                        #print(idx2 + 1, sorted(self.perm[self.c_idx6])[idx2].print_str())
                        straight_weight += pow(sorted(self.perm[self.c_idx6])[idx2].weight, idx2 + 1)
                        weight_iter += 1
                        #print(straight_weight)

                # Jesli jest strit to weight_iter == 4. Liczono od 0
                if weight_iter == 5:
                    self.weight_arrangement = straight_weight + 11242224
                    HelperArrangement().append_weight_gen(self.weight_arrangement)

                    if self.random == False:
                        self.print_arrengement()
                    if self.example == True:
                        self.print_arrengement()

                    calc_weights = False

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

                            HelperArrangement().clear_indices_2d_1()
                            HelperArrangement().clear_indices_2d_color()

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

                                HelperArrangement().get_indices_1(self.perm[idx6])

                                if self.random == False:
                                    for idx7 in range(0, len(self.perm[idx6])):
                                        self.perm[idx6][idx7].print()
                                    print()

                                self.c_idx6 = idx6
                                self.straight()

                                HelperArrangement().clear_indices_2d_1()

                                if self.random == True:
                                    self.loading_bar.set_count_bar(self.straight_iter)
                                    self.loading_bar.display_bar()
                                    self.straight_iter += 1

                                HelperArrangement().append_cards_all_permutations(self.perm[idx6])

                                self.c_idx6_iter += 1

        HelperArrangement().check_if_weights_larger()

        return HelperArrangement().random_arrangement()
