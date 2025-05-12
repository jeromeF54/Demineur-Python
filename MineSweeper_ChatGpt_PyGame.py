import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
TAILLE_FENETRE = 600
TILE_SIZE = TAILLE_FENETRE // 9  # 9x9 cases

# Couleurs
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
BLEU = (70, 70, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)

# Configuration de la fenêtre
screen = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Démineur")

# Classe Demineur
class Demineur:
    def __init__(self, taille=9, mines=10):
        self.taille = taille
        self.mines = mines
        self.board = []
        self.mines_positions = set()
        self.revealed = set()
        self.flags = set()
        self.moves = 0
        self.time_start = time.time()
        self.generate_board()

    def generate_board(self):
        """Génère le plateau avec mines et chiffres"""
        while len(self.mines_positions) < self.mines:
            x, y = random.randint(0, self.taille - 1), random.randint(0, self.taille - 1)
            self.mines_positions.add((x, y))
        
        self.board = [[' ' for _ in range(self.taille)] for _ in range(self.taille)]
        for x, y in self.mines_positions:
            self.board[x][y] = '*'
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if 0 <= i < self.taille and 0 <= j < self.taille and self.board[i][j] != '*':
                        if self.board[i][j] != '*':
                            self.board[i][j] = str(int(self.board[i][j] if self.board[i][j] != ' ' else 0) + 1)

    def reveal(self, x, y):
        """Révéler une case"""
        if (x, y) in self.revealed or (x, y) in self.flags:
            return
        self.revealed.add((x, y))
        self.moves += 1
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

    def check_win(self):
        """Vérifier si le joueur a gagné"""
        for i in range(self.taille):
            for j in range(self.taille):
                if self.board[i][j] != '*' and (i, j) not in self.revealed:
                    return False
        return True

    def get_time(self):
        """Retourner le temps écoulé"""
        return round(time.time() - self.time_start, 2)

# Fonction pour dessiner la grille
def draw_grid(demineur):
    for i in range(demineur.taille):
        for j in range(demineur.taille):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRIS, rect, 0 if (i, j) in demineur.revealed else 2)
            if (i, j) in demineur.revealed:
                if demineur.board[i][j] == '*':
                    pygame.draw.circle(screen, NOIR, rect.center, TILE_SIZE // 3)
                elif demineur.board[i][j] != ' ':
                    font = pygame.font.Font(None, 36)
                    text = font.render(demineur.board[i][j], True, NOIR)
                    screen.blit(text, (j * TILE_SIZE + TILE_SIZE // 3, i * TILE_SIZE + TILE_SIZE // 3))
            elif (i, j) in demineur.flags:
                pygame.draw.line(screen, ROUGE, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, ROUGE, rect.bottomleft, rect.topright, 2)

# Fonction pour dessiner des boutons avec texte souligné
def draw_button(text, x, y, width, height, font_size=36):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, NOIR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    
    # Dessiner le bouton
    pygame.draw.rect(screen, GRIS, (x, y, width, height))
    pygame.draw.rect(screen, NOIR, (x, y, width, height), 2)  # Bordure du bouton
    
    # Afficher le texte souligné (souligner la première lettre)
    screen.blit(text_surface, text_rect)
    pygame.draw.line(screen, NOIR, (text_rect.x, text_rect.y + font_size // 4), 
                     (text_rect.x + text_rect.width, text_rect.y + font_size // 4), 2)

# Fonction pour afficher le menu stylisé
def draw_menu():
    screen.fill(BLEU)
    font = pygame.font.Font(None, 48)
    title = font.render("Démineur", True, JAUNE)
    screen.blit(title, (TAILLE_FENETRE // 4, TAILLE_FENETRE // 4))

    # Dessiner les boutons
    draw_button("Start", TAILLE_FENETRE // 4, TAILLE_FENETRE // 2, 300, 50)
    draw_button("Quit", TAILLE_FENETRE // 4, TAILLE_FENETRE // 1.5, 300, 50)

    pygame.display.flip()

# Fonction pour démarrer le jeu
def start_game():
    game_loop()

# Fonction principale du jeu
def game_loop():
    demineur = Demineur()
    running = True
    while running:
        screen.fill(BLANC)
        draw_grid(demineur)
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Temps: {demineur.get_time()}s", True, NOIR)
        moves_text = font.render(f"Coups: {demineur.moves}", True, NOIR)
        screen.blit(timer_text, (10, TAILLE_FENETRE - 40))
        screen.blit(moves_text, (10, TAILLE_FENETRE - 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE
                if event.button == 1:  # Clic gauche pour révéler
                    if demineur.reveal(row, col):
                        print("Mine touchée !")
                        draw_menu()  # Montrer le menu après la perte
                        running = False
                elif event.button == 3:  # Clic droit pour poser un drapeau
                    demineur.place_flag(row, col)

        if demineur.check_win():
            print("Vous avez gagné !")
            draw_menu()  # Montrer le menu après la victoire
            running = False

        pygame.display.flip()

# Affichage du menu principal
draw_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Vérifier si le clic est sur le bouton "Start"
            if TAILLE_FENETRE // 4 <= x <= TAILLE_FENETRE // 4 + 300 and TAILLE_FENETRE // 2 <= y <= TAILLE_FENETRE // 2 + 50:
                start_game()  # Démarrer le jeu
            # Vérifier si le clic est sur le bouton "Quit"
            elif TAILLE_FENETRE // 4 <= x <= TAILLE_FENETRE // 4 + 300 and TAILLE_FENETRE // 1.5 <= y <= TAILLE_FENETRE // 1.5 + 50:
                running = False  # Quitter le jeu
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Quitter le jeu
                running = False
            elif event.key == pygame.K_s:  # Commencer une nouvelle partie
                start_game()

pygame.quit()
