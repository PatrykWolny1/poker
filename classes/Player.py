from classes.Arrangements import Arrangements
from random import choice
class Player(object):
    nick = None
    cards = None
    random = False
    amount = 0
    weight = 0
    index = 0
    cards = []
    all_combs = []
    combs_perm = False

    def __init__(self, deck, cards, nick = "Nick", index = 0, if_deck = False):
        self.nick = nick
        self.index = index
        deck.shuffling()
        self.arrangements = Arrangements()
        if if_deck:
            self.cards = []
            for idx in range(5):
                self.cards.append(deck.deal())
            self.arrangements.set_cards(self.cards)
        else:
            self.cards = cards
            self.arrangements.set_cards(self.cards)

    def return_to_croupier(self, amount = 0):
        self.amount = amount
        temp = self.cards.copy()

        if self.amount == 0:
            return self.amount

        for idx in range(self.amount):
            if idx == 0:
                self.print()

            if self.amount != 5:
                #which_card = input("Ktora karta[1-5]: ")
                which_card = choice(list(range(1, 5)))

                print("Ktora karta: ", which_card)

                print()
                which = int(which_card)

                temp.pop(which - 1)
            else:
                temp.pop()

            self.cards = temp
            self.print()

        if self.amount == 5:
            self.arrangements.set_cards(self.cards)

        print()

        return self.amount

    def take_cards(self, deck):
        self.cards.append(deck.deal())

    def cards_permutations(self):
        print("Wybierz rodzaj permutacji (1 - ALL | 2 - RANDOM): ")

        #if_all_perm = input()
        if_rand = "1"

        if if_rand == "1":
            self.random = False
        elif if_rand == "2":
            self.random = True

        if_combs_perm = "2"

        if if_combs_perm == "1":
            self.combs_perm = False
        elif if_combs_perm == "2":
            self.combs_perm = True

        print("Wybierz uklad do wygenerowania:\n"
              "(1 - POKER KROLEWSKI)\n"
              "(2 - KARETA)\n"
              "(3 - FULL)\n"
              "(4 - KOLOR)\n"
              "(5 - STRIT)\n"
              "(6 - TROJKA\n"
              "(7 - DWIE PARY)\n"
              "(8 - JEDNA PARA)\n"
              "(9 - WYSOKA KARTA)\n")

        #arrangement = input()
        arrangement = "6"

        if arrangement == "1":
            self.cards = self.arrangements.straight_royal_flush.straight_royal_flush_generating(self.random)
        if arrangement == "2":
            self.cards = self.arrangements.carriage.carriage_generating(self.random)
        if arrangement == "3":
            self.cards = self.arrangements.full.full_generating(self.random)
        if arrangement == "4":
            self.cards = self.arrangements.color.color_generating(self.random)
        if arrangement == "5":
            self.cards = self.arrangements.straight.straight_generating(self.random)
        if arrangement == "6":
            self.cards, self.all_combs = self.arrangements.three_of_a_kind.three_of_a_kind_generating(self.random, self.combs_perm)
        if arrangement == "7":
            self.cards, self.all_combs = self.arrangements.two_pairs.two_pairs_generating(self.random, self.combs_perm)
        if arrangement == "8":
            self.cards = self.arrangements.one_pair.one_pair_generating(self.random)
        if arrangement == "9":
            self.cards = self.arrangements.high_card.high_card_generating(self.random)

        self.cards = list(self.cards)

        self.arrangements.set_cards(self.cards)

    def get_arrangements(self):
        return self.arrangements

    def get_weight(self):
        self.weight = self.arrangements.set_get_weights()
        return self.weight

    def get_cards(self):
        return self.cards

    def set_cards(self, cards):
        self.cards = cards

    def print(self):
        print(self.nick)
        for idx in self.cards:
            idx.print()
        print()
