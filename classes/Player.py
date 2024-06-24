from classes.Arrangements import Arrangements
class Player(object):
    nick = None
    cards = None
    random = False

    def __init__(self, nick, deck, if_deck):
        self.cards = []
        self.nick = nick
        deck.shuffling()
        self.arrangements = Arrangements()
        if if_deck:
            for idx in range(5):
                self.cards.append(deck.deal())
            self.arrangements.set_cards(self.cards)

    def give_cards(self, amount = 0, cards = []):
        for idx in range(amount):
            self.print()
            print()
            which_card = input("Ktora karta[1-5][-1 WYJSCIE]: ")
            which = int(which_card)
            if which == -1:
                break
            self.cards.pop(which - 1)
        print()

        if amount == 0:
            self.cards = cards

        self.arrangements.set_cards(self.cards)

    def cards_permutations(self):
        print("Wybierz rodzaj permutacji (1 - ALL | 2 - RANDOM): ")

        #if_all_perm = input()
        if_all_perm = "2"

        if if_all_perm == "1":
            self.random = False
        elif if_all_perm == "2":
            self.random = True

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
        arrangement = "9"

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
            self.cards = self.arrangements.three_of_a_kind.three_of_a_kind_generating(self.random)
        if arrangement == "7":
            self.cards = self.arrangements.two_pairs.two_pairs_generating(self.random)
        if arrangement == "8":
            self.cards = self.arrangements.one_pair.one_pair_generating(self.random)
        if arrangement == "9":
            self.cards = self.arrangements.high_card.high_card_generating(self.random)

        self.cards = list(self.cards)

        self.arrangements.set_cards(self.cards)

    def print_arrangement(self):
        self.arrangements.print()
        self.arrangements.check_arrangement()

<<<<<<< Updated upstream
=======
    def set_cards(self, cards):
        self.arrangements.set_cards(cards)

    def get_cards(self):
        return self.cards

    def get_weight(self):
        return self.arrangements.get_weight()

>>>>>>> Stashed changes
    def print(self):
        print(self.nick)
        for idx in self.cards:
            idx.print()
        print()
