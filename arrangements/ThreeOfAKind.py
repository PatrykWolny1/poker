from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
from itertools import permutations, combinations
import random

class ThreeOfAKind(object):
    cardmarkings = CardMarkings()  # Oznaczenia kart
    cards_2d = []
    indices_2d_name = []
    perm = []
    cards_all_permutations = []
    weight_gen = []

    high_card = None

    weight_arrangement = 0
    c_idx1 = 0
    num_arr = 0
    rand_int = 0

    random = False
    example = False

    step_p = True
    str_1 = ""
    n_bar = 6589440
    step_bar = int(n_bar / 40)              # Zwiekszanie dlugosci paska ladowania
    step_bar_finished = int(n_bar / 39)     # Jaka czesc stanowia kropki (zaladowane)

    def set_cards(self, cards):
        self.perm = cards
        self.example = True
        self.random = False

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
        if self.step_p == False and ((self.num_arr + 1) % self.step_bar_finished) == 0:
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
            print("Trojka: ", self.weight_arrangement, "Wysoka karta: ", self.high_card.print_str(),  "Numer: ", self.num_arr)
        if self.random == True:
            print("Trojka: ", self.weight_arrangement, "Wysoka karta: ", self.high_card.print_str(),  "Numer: ", self.rand_int)

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
                print(self.cards_all_permutations[indices[idx]][idx1].print_str(), indices[idx], end=" ")
            print()

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
            if len(self.indices_2d_name[i]) == 2:  # Jesli w wierszu tablicy znajduja sie 2 takie same elementy
                return True

        return False

    def remove_multiples_more_3(self, cards_comb):
        # Sprawdzanie oraz zapisanie indeksow powtarzajacych sie kart

        self.get_indices_name(cards_comb)

        for i in range(0, len(self.indices_2d_name)):
            if len(self.indices_2d_name[i]) > 3:  # Jesli w wierszu tablicy znajduja sie 2 takie same elementy
                return True

        return False

    def three_of_a_kind(self):
        three_count_3 = 0
        three_count_1 = 0
        once_2 = False
        once_1 = False
        three_weight = 0

        if len(self.dim(self.perm)) == 1:
            self.perm = [self.perm]
            self.c_idx1 = 0

        self.get_indices_name(self.perm[self.c_idx1])

        for idx in range(0, len(self.indices_2d_name)):

            if len(self.indices_2d_name[idx]) == 3:
                three_count_3 += 1

                if once_1 == False:
                    three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][0]].weight, 5)
                    three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][1]].weight, 5)
                    three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][2]].weight, 5)

                    once_1 = True

            if len(self.indices_2d_name[idx]) == 1:
                three_count_1 += 1

                if once_2 == False:
                    for idx1 in range(idx + 1, len(self.indices_2d_name)):
                        if len(self.indices_2d_name[idx1]) == 1:
                            if self.perm[self.c_idx1][self.indices_2d_name[idx][0]] < self.perm[self.c_idx1][self.indices_2d_name[idx1][0]]:
                                self.high_card = self.perm[self.c_idx1][self.indices_2d_name[idx1][0]]
                                three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][0]].weight, 2)
                                three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx1][0]].weight, 3)

                            else:
                                self.high_card = self.perm[self.c_idx1][self.indices_2d_name[idx][0]]
                                three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx][0]].weight, 3)
                                three_weight += pow(self.perm[self.c_idx1][self.indices_2d_name[idx1][0]].weight, 2)

                    once_2 = True

        if three_count_3 == 3 and three_count_1 == 2:
            self.weight_arrangement = three_weight
            self.weight_gen.append(self.weight_arrangement)   # Tablica wag dla sprawdzania czy wygenerowane uklady maja wieksze
            if self.random == False:
                self.print_arrengement()

    def three_of_a_kind_generating(self, random):
        self.random = random

        cards_2d = []
        cards_to_comb = []
        cards_to_comb_1 = []
        cards_to_comb_rest = []
        i_three = 0
        iter_ar = 0
        len_comb = 0

        for arrangement in self.cardmarkings.arrangements:
            for color in self.cardmarkings.colors:
                cards_2d.append(Card(arrangement, color))

        while (True):
            # for idx in range(0 + iter_ar, 4 + iter_ar):
            #     cards_2d[idx].print()
            # print("###############################")

            cards_to_comb_rest.extend(cards_2d[0:52])


            # for idx in range(0, len(cards_to_comb_rest)):
            #     cards_to_comb_rest[idx].print()
            # print()

            cards_comb_rest = list(combinations(cards_to_comb_rest, 2))

            cards_to_comb_rest.clear()

            for idx in range(0, len(cards_comb_rest)):
                cards_to_comb.extend(cards_2d[0 + iter_ar : 4 + iter_ar])

                cards_comb_rest[idx] = list(cards_comb_rest[idx])

                # for idx1 in range(0, len(cards_comb_rest[idx])):
                #     cards_comb_rest[idx][idx1].print()
                # print()

                cards_to_comb.extend(cards_comb_rest[idx])

                cards_to_comb_1.append(cards_to_comb.copy())

                cards_to_comb.clear()

            for idx in range(0, len(cards_to_comb_1)):
                if_remove_comb_1 = self.remove_multiples(cards_to_comb_1[idx])

                if if_remove_comb_1 == True:
                    cards_to_comb_1[idx] = []

            cards_to_comb_1 = [x for x in cards_to_comb_1 if x != []]


            # for idx in range(0, len(cards_to_comb_1)):
            #     for idx1 in range(0, len(cards_to_comb_1[idx])):
            #         cards_to_comb_1[idx][idx1].print()
            #     print()

            for idx in range(0, len(cards_to_comb_1)):
                cards_comb = list(combinations(cards_to_comb_1[idx], 5))

                for idx1 in range(0, len(cards_comb)):
                    if_remove_comb_2 = self.remove_multiples_more_3(cards_comb[idx1])

                    if if_remove_comb_2 == True:
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

                        self.c_idx1 = idx1
                        self.three_of_a_kind()

                        if self.random == True:
                            self.loading_bar()
                            self.num_arr += 1

                        self.cards_all_permutations.append(self.perm[idx1])

                len_comb += len(cards_comb)

            #print(len_comb)

            cards_to_comb_1.clear()

            i_three += 1
            iter_ar += 4

            if i_three == 13:
                break

        if self.random == False:
            self.check_if_weights_larger()

        return self.random_arrangement()