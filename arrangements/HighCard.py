from classes.Card import Card
from arrangements.CardMarkings import CardMarkings
from itertools import permutations, combinations
import random
import time

class HighCard(object):
    cardmarkings = CardMarkings()  # Oznaczenia kart
    cards_2d = []
    indices_2d_name = []
    perm = []
    cards_all_permutations = []
    weight_gen = []

    weight_arrangement = 0
    c_idx1 = 0
    num_arr = 0
    rand_int = 0
    iter_pair = 0

    random = False
    example = False

    step_p = True
    str_1 = ""
    n_bar = 10137600 #1 098 240 - number of combinations (all) | 84480 (1 iter) | permutations - 131 788 800 | 10 137 600 (1 iter)
    step_bar = int(n_bar / 40)              # Zwiekszanie dlugosci paska ladowania
    step_bar_finished = int(n_bar / 39)     # Jaka czesc stanowia kropki (zaladowane)
    idx_bar = 0

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
        if self.step_p == False and ((self.idx_bar + 1) % self.step_bar_finished) == 0:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")
            # os.system('cls')
        if self.idx_bar == self.n_bar - 1:
            print("[", end="")
            self.str_1 = self.str_1.replace("#", ".", 1)
            print(self.str_1, end="]\n")

    def print_arrengement(self):
        if self.random == False:
            print("Wysoka karta: ", self.weight_arrangement, "Wysoka karta: ", self.high_card_1.print_str(),  "Numer: ", self.num_arr)
        if self.random == True:
            print("Wysoka karta: ", self.weight_arrangement, "Wysoka karta: ", self.high_card_1.print_str(),  "Numer: ", self.rand_int)

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

        # for idx in range(0, len(indices)):
        #     for idx1 in range(0, len(self.cards_all_permutations[indices[idx]])):
        #         print(self.cards_all_permutations[indices[idx]][idx1].print_str(), end=" ")
        #     print()
        #     print("IDX: ", indices[idx])

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

    def get_indices_color(self, cards):
        self.indices_2d_color = []

        for idx in range(0, len(cards)):
            indices = []
            for (index, card) in enumerate(cards):
                if card.color == cards[idx].color:
                    indices.append(index)
            self.indices_2d_color.append(indices)
        # print(self.indices_2d_color)

    def card_max(self, perm_temp, pow_idx):
        if not perm_temp:
            return 0

        card_temp = max(perm_temp)
        self.high_card_weight = pow(card_temp.weight, pow_idx)
        perm_temp.remove(card_temp)

        pow_idx -= 1

        return self.high_card_weight + self.card_max(perm_temp, pow_idx)

    def high_card(self):
        if len(self.dim(self.perm)) == 1:
            self.perm = [self.perm]
            self.c_idx1 = 0

        straight_iter = 0

        for idx2, idx1 in zip(range(1, len(self.perm[self.c_idx1])), range(0, len(self.perm[self.c_idx1]))):
            if ((self.perm[self.c_idx1][idx2].weight - self.perm[self.c_idx1][idx1].weight == 1) or
             (self.perm[self.c_idx1][4].weight == 13 and (self.perm[self.c_idx1][idx2].weight - self.perm[self.c_idx1][idx1].weight) == 9)):
                straight_iter += 1

            if straight_iter == 4:
                return

        self.get_indices_name(self.perm[self.c_idx1])
        self.get_indices_color(self.perm[self.c_idx1])

        for idx3, idx4 in zip(range(0, len(self.indices_2d_color)), range(0, len(self.indices_2d_name))):
            # Jesli jest 5 takich samych kolorow to powrot z funkcji (poker krolewski)
            if len(self.indices_2d_color[idx3]) == 5:
                return
            if len(self.indices_2d_name[idx4]) > 1:
                return

        self.high_card_1 = max(self.perm[self.c_idx1].copy())

        perm_temp = self.perm[self.c_idx1].copy()

        self.weight_arrangement = self.card_max(perm_temp, 5)

        self.weight_gen.append(self.weight_arrangement)

        if self.random == False:
            self.print_arrengement()

    def high_card_generating(self, random):
        self.random = random

        cards_2d = []
        cards_to_comb_rest = []
        cards_comb_rest_sorted = []
        count = 0

        for arrangement in self.cardmarkings.arrangements:
            for color in self.cardmarkings.colors:
                cards_2d.append(Card(arrangement, color))

        while (True):
            start_time = time.time()

            cards_to_comb_rest.extend(cards_2d[0:52])

            # for idx in range(0, len(cards_to_comb_rest)):
            #     cards_to_comb_rest[idx].print()
            # print()

            cards_comb_rest = list(combinations(cards_to_comb_rest, 5))

            cards_to_comb_rest.clear()

            for idx in range(0, len(cards_comb_rest)):

                cards_comb_rest[idx] = list(cards_comb_rest[idx])

                cards_comb_rest_sorted.append(sorted(cards_comb_rest[idx].copy(), key = lambda x: x.weight))

                self.get_indices_name(cards_comb_rest_sorted[idx])
                self.get_indices_color(cards_comb_rest_sorted[idx])

                for idx1 in range(0, len(self.indices_2d_name)):
                    if len(self.indices_2d_name[idx1]) != 1:
                        cards_comb_rest[idx] = []
                    if len(self.indices_2d_color[idx1]) == 5:
                        cards_comb_rest[idx] = []

                #print(idx)

                if cards_comb_rest_sorted[idx] != []:
                    for idx2, idx3 in zip(range(1, len(cards_comb_rest_sorted[idx])),
                                          range(0, len(cards_comb_rest_sorted[idx]) - 1)):

                        if (((cards_comb_rest_sorted[idx][idx2].weight - cards_comb_rest_sorted[idx][idx3].weight) == 1) or
                                (cards_comb_rest_sorted[idx][4].weight == 13 and cards_comb_rest_sorted[idx][idx2].weight -
                                 cards_comb_rest_sorted[idx][idx3].weight == 9)):
                            count += 1

                        if count == 4:
                            cards_comb_rest[idx] = []

                    count = 0

            cards_comb_rest = [x for x in cards_comb_rest if x != []]

            # for idx in range(0, len(cards_comb_rest)):
            #     for idx1 in range(0, len(cards_comb_rest[idx])):
            #         cards_comb_rest[idx][idx1].print()
            #     print()

            #print(len(cards_comb_rest))

            for idx in range(0, len(cards_comb_rest)):
                self.perm = list(permutations(cards_comb_rest[idx], 5))

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
                    self.high_card()

                    #print(int(time.time() - start_time))

                    self.cards_all_permutations.append(self.perm[idx1])

                    if self.random == True:
                        self.loading_bar()
                        self.idx_bar += 1

                    self.iter_pair += 1

                    if int(time.time() - start_time) == 160:
                        pass

                    if self.iter_pair == self.n_bar:
                        self.check_if_weights_larger()
                        return self.random_arrangement()

            print(len(self.cards_all_permutations))

        self.check_if_weights_larger()

        return self.random_arrangement()