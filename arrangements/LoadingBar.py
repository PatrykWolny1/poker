class LoadingBar(object):
    # loading_bar()
    step_p = True
    str_1 = ""
    n_bar = 0               # Ilosc ukladow (trzeba uruchomic program i policzyc)
    step_bar = 0            # Ilosc punktow ladowania (40 - dzielnik)
    step_bar_finished = 0   # Ilosc zaladowanych punktow (co jeden) [.####][..###]
    count_bar = 0

    def __init__(self, n_bar, points_step, points_finished):
        self.step_p = True
        self.str_1 = ""
        self.n_bar = n_bar
        self.step_bar = int(self.n_bar / points_step)
        self.step_bar_finished = int(self.n_bar / points_finished)
        self.count_bar = 0

    def set_count_bar(self, count_bar):
        self.count_bar = count_bar

    def display_bar(self):
        # Pasek postepu
        # Pierwsza wartosc step_p to prawda
        # Tworzony jest pasek postepu stworzony ze znakow "#"
        if self.step_p:
            for i in range(0, self.n_bar, self.step_bar):
                self.str_1 += "#"
        # Tutaj nastepuje wyswietlanie paska ze znakow "#"
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
