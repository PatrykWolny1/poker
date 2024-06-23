from classes.Player import Player
from classes.Deck import Deck
from classes.Card import Card
from classes.Arrangements import Arrangements
class Croupier(object):
    cards = []
    player1 = None
    player2 = None
    player = None
    players = []
    weight = []
    amount = 0

    def __init__(self):
        self.deck = Deck()
        self.cards = [Card("4", "Ka"),
                      Card("2", "Pi"),
                      Card("K", "Tr"),
                      Card("K", "Ka"),
                      Card("K", "Ki")]

        self.player1 = Player('Nick', self.deck, True)
        self.player2 = Player('Tom', self.deck, True)

    ###############################################ZROBIC KOMENTARZE DO HIGH_CARD I ONE_PAIR I THREE_OF_A_KIND

    def play(self):
        print()

        idx_players = int(input("Ilu graczy: "))

        for idx in range(idx_players):
            nick = str(input("Pseudonim gracza: "))
            self.players.append(Player(nick, self.deck, True))

        #self.player1.give_cards(0, self.cards)
        #print("Deck: ", len(self.deck.cards))
        #self.deck.print()

        print()

        for self.player in self.players:
            self.player.print_arrangement()
            self.player.check_arrengement()
            self.weight.append(self.player.get_weight())
            print()
            exchange = str(input("Wymiana kart [T/N]: "))

            if exchange.lower() == 't':
                self.cards_exchange()
            if exchange.lower() == 'n':
                break

        print(self.weight)

    def deal_cards(self):
        for idx in range(self.amount):
            self.player.take_cards(self.deck)

    def cards_exchange(self, loop = True):
        while (loop):
            self.amount = int(input("Ile kart do wymiany [0-5][-1 COFNIJ]: "))
            print()

            if self.amount == -1:
                continue

            self.amount = self.player.return_to_croupier(self.amount)
            print(self.amount)

            if self.amount == -1:
                continue

            self.deal_cards()
            self.player.print_arrangement()
            self.player.check_arrengement()

            break

    def compare_players_cards(self):
        pass
        pass

