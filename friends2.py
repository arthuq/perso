class Team():
    def __init__(self, n_player:int, cat:list, qpc:int, number:int):
        self.n = n_player #nombre de joueurs

        self.cat = cat #liste des catégories
        self.n_cat = len(cat) #nombre de categories
        self.qpc = qpc #question par catégories (int)

        self.score = 0 #score
        self.next = 0 #prochain joueur

        self.questions = [[]] * self.n_cat #liste de questions

        # Setting up name
        self.name = input(f"Nom de l'équipe {number}: ")

        # Setting up players
        self.players = []
        for i in range(n_player):
            tmp = input(f"Nom du joueur {i+1} : ")
            self.players.append(tmp)
        print("\n")

    def get_score(self):
        print(f"Le score de l'équipe << {self.name} >> est de {self.score} !")

    def next_player(self):
        tmp = self.players[self.next]
        print(f"Au tour de {tmp} se jouer!")
        self.next = (self.next + 1) % self.n
        return tmp

    def up_score(self):
        self.score += 1

    def check_n_qu(self):
        return sum( [len(cat) for cat in self.questions] )

    def init_questions(self):
        print("\n"*50)
        print(f"Au tour de l'équipe  << {self.name} >> de renseigner ses questions.\n")
        for j in self.players:
            input(f"{j}, c'est à toi ! Appuie sur entrée quand tu es prêt ...")
            for c, cat in enumerate(self.cat) :
                print(f"\nDans la catégorie : {cat} :")
                for i in range(self.qpc):
                    q = input(f"Question {i+1} : tapes ta question : ")
                    r = input("Tapes la réponse à ta question : ")
                    self.questions[c].append( (j, q, r) )
                    print("\n")

    def print_cat(self, adv, count:bool=False):
        print("Les catégories sont les suivantes : ")
        for i, cat in enumerate(adv.cat) :
            if count:
                print(f" {i+1} - {cat} ({len(adv.questions[i])})")
            else:
                print(f" {i+1} - {cat}")
        print("\n")

    def choose_question(self, adv):
        # Choix de la catégorie
        self.print_cat(adv, True)
        while True :
            try:
                c = int(input("Choississez une catégorie : ")) - 1
                if len(adv.questions[c]) > 0 and c>=0 and c < adv.n_cat :
                    break
                else:
                    print("Plus de questions dans cette catégorie...")
            except :
                print("Chiffre invalide.")

        # Choix de la question
        try :
            q_number = random.randint(0, len(adv.questions[c]) - 1)
            j, q, r = adv.questions[c][q_number]
            del adv.questions[c][q_number]
            return j, q, r

        except:
            print("Opération invalide.")

#

import random

def sep(symbol:str="*", n:int=25):
    print(f"{symbol}"*n)

def display_question(j, q, r):
    print(f"\nLa question porte sur : {j}. Donne ta réponse à l'oral!")
    print(f"> {q}\n")
    input("Appuie sur entrée quand tu as répondu.")
    print(f"La réponse était : {r}\n")

def good_ans(j):
    while True:
        tmp = input(f"Est-ce que {j} a eu juste ? (o/n) : ")
        if tmp in ["o", "n"]:
            break
    if tmp == "o":
        return True
    return False

def end_game(t1, t2):
    print("La partie est finie !!!!")
    print("Bilan des scores :")
    print(f"Equipe << {t1.name} >> : {t1.score} points.")
    print(f"Equipe << {t2.name} >> : {t2.score} points.\n")
    if t1.score > t2.score :
        print(f"L'équipe << {t1.name} >> gagne !!!")
    elif t2.score > t1.score :
        print(f"L'équipe << {t2.name} >> gagne !!!")
    else:
        print("Il y a égalité ... Merci d'avoir joué !'")

def choose_n_players():
    while True:
        try :
            N = int(input("Commencons ! Combien y a t-il de joueurs ? : "))
            if N >= 2:
                break
            print("Il faut 2 joueurs minimum.")
        except ValueError:
            print("Entrée invalide...")
    return N

def choose_categories():
    while True :
        tmp = input("Jouer avec les catégories par défaut ? (o/n) : ")
        if tmp in ["o", "n"]:
            break
    if tmp == "o" :
        categories = ["Peurs et phobies", "Histoire ancienne", "Literature", "Tout est relatif"]

    else:
        categories = []
        while True:
            try:
                n_c = int(input("Avec combien de catégories voulez vous jouer ? : "))
                break
            except ValueError:
                print("Entrée invalide...")
        for i in range(n_c) :
            categories.append(input(f"Catégorie {i+1} : "))
        print("\n")

    return categories


def choose_n_questions():
    while True:
        try :
            q_per_cat = int(input("Combien de questions par joueur et par catégorie ? : "))
            if q_per_cat > 0 :
                break
        except ValueError:
                print("Entrée invalide...")
    return q_per_cat


def play() :
    # Choix du nombre de joueurs
    N = choose_n_players()

    # Choix du nombre de questions
    q_per_cat = choose_n_questions()

    # Choix des catégories
    categories = choose_categories()

    # Initialisation des deux équipes
    t1 = Team(N//2, categories, q_per_cat, 1)
    t2 = Team(N - N//2, categories, q_per_cat, 2)

    # Initialisation des questions
    t1.init_questions()
    t2.init_questions()
    print("\n"*50)

    # Lancement du jeu
    while t1.check_n_qu() + t2.check_n_qu() > 0 :
        # Décidez qui est qui (joueur et adversaire)
        for team in range(2):
            if team == 0:
                eq, adv = t1, t2
            else:
                eq, adv = t2, t1

            # Skip si plus de quetion pour cette equipe
            if adv.check_n_qu() == 0:
                continue

            # Introduction
            sep("* ", 25)
            print(f"Au tour de l'equipe << {eq.name} >> de répondre !")
            sep("* ", 25)
            print('\n')

            # Poser la question
            j0 = eq.next_player()
            j1, q, r = eq.choose_question(adv)
            display_question(j1, q, r)

            # Mise à jour des scores
            if good_ans(j0) :
                eq.up_score()
            eq.get_score()

            # Suite du jeu
            input("Appuyez sur entrer pour continuer... ")
            sep("\n", 50)

    # Fin de jeu
    end_game(t1, t2)


play()