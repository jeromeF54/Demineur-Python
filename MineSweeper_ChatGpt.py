import random

class Demineur:
    def __init__(self, taille=9, mines=10):
        self.taille = taille
        self.mines = mines
        self.board = []
        self.mines_positions = set()
        self.revealed = set()
        self.flags = set()
        
        # Générer le tableau
        self.generate_board()

    def generate_board(self):
        """Génère le plateau avec mines et chiffres"""
        # Placer les mines
        while len(self.mines_positions) < self.mines:
            x, y = random.randint(0, self.taille - 1), random.randint(0, self.taille - 1)
            self.mines_positions.add((x, y))
        
        # Remplir les cases avec les chiffres
        self.board = [[' ' for _ in range(self.taille)] for _ in range(self.taille)]
        for x, y in self.mines_positions:
            self.board[x][y] = '*'
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if 0 <= i < self.taille and 0 <= j < self.taille and self.board[i][j] != '*':
                        if self.board[i][j] != '*':
                            self.board[i][j] = str(int(self.board[i][j] if self.board[i][j] != ' ' else 0) + 1)

    def display_board(self, reveal=False):
        """Affiche le plateau de manière lisible avec grille et alignement"""
        # Affichage des numéros de colonnes avec alignement
        print("    ", end="")
        for i in range(self.taille):
            print(f" {i:2} ", end="|")  # Séparateur pour les numéros de colonnes
        print()
        
        # Affichage de la grille avec les cases
        for i in range(self.taille):
            print("   +" + "----" * self.taille + "+")  # Ligne de séparation
            print(f" {i:2} |", end="")  # Affichage des numéros de lignes
            for j in range(self.taille):
                if (i, j) in self.revealed or reveal:
                    if self.board[i][j] == '*':
                        print(" *  ", end="|")  # Affichage des mines
                    else:
                        print(f" {self.board[i][j]}  ", end="|")  # Affichage des chiffres
                elif (i, j) in self.flags:
                    print(" 🚩 ", end="|")  # Affichage des drapeaux
                else:
                    print(" #  ", end="|")  # Affichage des cases non révélées
            print()
        print("   +" + "----" * self.taille + "+")  # Ligne de séparation finale
        print()

    def reveal(self, x, y):
        """Révéler une case"""
        if (x, y) in self.revealed or (x, y) in self.flags:
            return
        self.revealed.add((x, y))
        if self.board[x][y] == '*':
            return True  # Mine trouvée
        if self.board[x][y] == ' ':
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if 0 <= i < self.taille and 0 <= j < self.taille:
                        if (i, j) not in self.revealed:
                            self.reveal(i, j)
        return False

    def place_flag(self, x, y):
        """Placer un drapeau"""
        if (x, y) not in self.revealed:
            if (x, y) in self.flags:
                self.flags.remove((x, y))
            else:
                self.flags.add((x, y))
        else:
            print("Impossible de placer un drapeau sur une case déjà révélée.")

    def check_win(self):
        """Vérifier si le joueur a gagné"""
        for i in range(self.taille):
            for j in range(self.taille):
                if self.board[i][j] != '*' and (i, j) not in self.revealed:
                    return False
        return True

    def play(self):
        """Lancer le jeu"""
        while True:
            self.display_board(reveal=False)
            action = input("Choisissez une action (r = révéler, f = drapeau, q = quitter) : ").strip().lower()

            if action == 'q':
                print("Jeu terminé.")
                break
            elif action == 'r':
                try:
                    x, y = map(int, input("Entrez la ligne et la colonne (ex: 1 2) : ").split())
                    if self.reveal(x, y):
                        print("Vous avez trouvé une mine! Perdu!")
                        self.display_board(reveal=True)
                        break
                    if self.check_win():
                        print("Félicitations, vous avez gagné!")
                        self.display_board(reveal=True)
                        break
                except (ValueError, IndexError):
                    print("Coordonnées invalides. Essayez encore.")
            elif action == 'f':
                try:
                    x, y = map(int, input("Entrez la ligne et la colonne pour poser un drapeau (ex: 1 2) : ").split())
                    self.place_flag(x, y)
                except (ValueError, IndexError):
                    print("Coordonnées invalides. Essayez encore.")
            else:
                print("Action non reconnue. Essayez 'r', 'f' ou 'q'.")

# Créer une instance du jeu
jeu = Demineur()

# Démarrer la partie
jeu.play()
