import os
import pygame
import sys
import time

class KnightsTour:

    def __init__(self):
        self.board_size = 8
        self.moves = [
              (1, 2),   # 2 up 1 right
              (-1, 2),  # 2 up 1 left
              (1, -2),    # 2 down 1 right
              (-1, -2),   # 2 down 1 left
              (-2, 1),  # 2 left 1 up
              (-2, -1),   # 2 left 1 down
              (2, 1),   # 2 right 1 up
              (2, -1)   # 2 right 1 down
        ]
    # ------------------------------------------------------------
    # SUCCESSOR FUNCTION
    # ------------------------------------------------------------
    def successor_fct(self, x, y, visited):
        successors = []
        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.board_size and
                0 <= ny < self.board_size and
                (nx, ny) not in visited
            ):
                successors.append((nx, ny))
        return successors

    # ------------------------------------------------------------
    # BACKTRACKING SIMPLE
    # ------------------------------------------------------------
    def backtracking(self, assignment):
        if len(assignment) == 64:
            return assignment

        x, y = assignment[-1]
        visited = set(assignment)
        successors = self.successor_fct(x, y, visited)
    
        for nx, ny in successors:
            assignment.append((nx, ny))
            result = self.backtracking(assignment)
            if result:
                return result
            assignment.pop()

        return None

    # ------------------------------------------------------------
    # MRV : Minimum Remaining Values
    # ------------------------------------------------------------
    def MRV(self, successors, visited):
        scored = []
        for x, y in successors: # pour chaque mouvement posible
            temp_visited = visited.copy() # copier les case déjà visités
            temp_visited.add((x, y)) # ajouter le mouvement actue aux visités
            onward = self.successor_fct(x, y, temp_visited) # Trouver les successeurs du mouvement actuel
            scored.append((len(onward), x, y)) # Stocker le nombre de successeurs

        scored.sort() # Trier par nombre de successeurs (croissant)
        best = scored[0][0]  # plus petit nombre de successeur
        return [(x, y) for s, x, y in scored if s == best] # Retourner les mouvements avec le plus petit nombre de successeurs


    # ------------------------------------------------------------
    # LCV : Least Constraining Value
    # ------------------------------------------------------------
    def LCV(self, successors, visited):
        scored = []
        for x, y in successors:
            temp = visited.copy()
            temp.add((x, y))

            impact = 0
            for nx, ny in self.successor_fct(x, y, temp):
                temp2 = temp.copy()
                temp2.add((nx, ny))
                impact += len(self.successor_fct(nx, ny, temp2))

            scored.append((impact, x, y))

        scored.sort(reverse=True)
        return [(x, y) for impact, x, y in scored]

    # ------------------------------------------------------------
    # BACKTRACKING AVEC MRV + LCV
    # ------------------------------------------------------------
    def backtracking_with_heuristics(self, assignment):
        if len(assignment) == 64:
            return assignment

        x, y = assignment[-1]
        visited = set(assignment)
        successors = self.successor_fct(x, y, visited)

        if not successors:
            return None

        # 1. MRV : réduire la branche
        successors = self.MRV(successors, visited)

        # 2. LCV : essayer les valeurs les moins contraignantes d’abord
        successors = self.LCV(successors, visited)

        for nx, ny in successors:
            assignment.append((nx, ny))
            result = self.backtracking_with_heuristics(assignment)
            if result:
                return result
            assignment.pop()

        return None

# ============================================================
# INTERFACE GRAPHIQUE PYGAME
# ============================================================
class GameGUI:
    def __init__(self):
        pygame.init()
        
        # Dimensions
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 700
        self.SQUARE_SIZE = 70
        self.BOARD_OFFSET_X = 50
        self.BOARD_OFFSET_Y = 50
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.BUTTON_COLOR = (70, 130, 180)
        self.BUTTON_HOVER = (100, 160, 210)
        self.SUCCESS_COLOR = (76, 175, 80)
        self.TEXT_COLOR = (50, 50, 50)
        self.PATH_COLOR = (220, 50, 50, 128)
        self.HIGHLIGHT_COLOR = (255, 255, 0, 100)
        
        # Fenêtre
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Knight's Tour Problem")
        self.clock = pygame.time.Clock()
        
        # Solver
        self.knight_solver = KnightsTour()
        
        # État
        self.solution = None
        self.current_move = 0
        self.animating = False
        self.solving = False
        self.stats = None
        self.animation_speed = 1000  # millisecondes entre chaque mouvement
        self.last_move_time = 0
        
        # Polices
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        
        # Charger l'image du cavalier
        self.load_knight_image()
        
        # Boutons
        self.buttons = {
            'simple': pygame.Rect(650, 100, 500, 60),
            'heuristic': pygame.Rect(650, 180, 500, 60),
            'animate': pygame.Rect(650, 260, 240, 60),
            'reset': pygame.Rect(910, 260, 240, 60)
        }
    
    def load_knight_image(self):
        """Charge l'image du cavalier depuis le répertoire courant"""
        try:
            # Chercher l'image du cavalier dans le répertoire courant
            possible_names = ['knight.png', 'cavalier.png', 'horse.png', 'Knight.png']
            knight_path = None
            
            for name in possible_names:
                if os.path.exists(name):
                    knight_path = name
                    break
            
            if knight_path:
                self.knight_image = pygame.image.load(knight_path)
                # Redimensionner l'image pour qu'elle tienne dans une case
                self.knight_image = pygame.transform.scale(
                    self.knight_image, 
                    (int(self.SQUARE_SIZE * 0.8), int(self.SQUARE_SIZE * 0.8))
                )
                print(f"✓ Image du cavalier chargée: {knight_path}")
            else:
                # Si aucune image n'est trouvée, créer une image avec le symbole Unicode
                self.knight_image = None
                print("⚠ Aucune image de cavalier trouvée. Utilisation du symbole Unicode.")
        except Exception as e:
            print(f"⚠ Erreur lors du chargement de l'image: {e}")
            self.knight_image = None
    
    def draw_board(self):
        """Dessine l'échiquier"""
        for row in range(8):
            for col in range(8):
                x = self.BOARD_OFFSET_X + col * self.SQUARE_SIZE
                y = self.BOARD_OFFSET_Y + row * self.SQUARE_SIZE
                
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.rect(self.screen, self.BLACK, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)
    
    def draw_path(self):
        """Dessine le chemin parcouru jusqu'au mouvement actuel"""
        if not self.solution or self.current_move < 1:
            return
        
        # Surface transparente pour le chemin
        path_surface = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Dessiner les lignes du chemin
        for i in range(min(self.current_move, len(self.solution) - 1)):
            row1, col1 = self.solution[i]
            row2, col2 = self.solution[i + 1]
            
            x1 = self.BOARD_OFFSET_X + col1 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            y1 = self.BOARD_OFFSET_Y + row1 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            x2 = self.BOARD_OFFSET_X + col2 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            y2 = self.BOARD_OFFSET_Y + row2 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            
            pygame.draw.line(path_surface, self.PATH_COLOR, (x1, y1), (x2, y2), 4)
        
        self.screen.blit(path_surface, (0, 0))
        
        # Dessiner les numéros des cases visitées
        for i in range(min(self.current_move + 1, len(self.solution))):
            row, col = self.solution[i]
            x = self.BOARD_OFFSET_X + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            y = self.BOARD_OFFSET_Y + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            
            color = (150, 0, 0) if i == 0 else self.TEXT_COLOR
            text = self.small_font.render(str(i), True, color)
            text_rect = text.get_rect(center=(x, y + 20))
            self.screen.blit(text, text_rect)
    
    def draw_knight(self):
        """Dessine le cavalier à sa position actuelle"""
        if not self.solution or self.current_move >= len(self.solution):
            return
        
        row, col = self.solution[self.current_move]
        x = self.BOARD_OFFSET_X + col * self.SQUARE_SIZE
        y = self.BOARD_OFFSET_Y + row * self.SQUARE_SIZE
        
        # Surligner la case actuelle
        highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surface, self.HIGHLIGHT_COLOR, (0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
        self.screen.blit(highlight_surface, (x, y))
        
        # Dessiner le cavalier
        if self.knight_image:
            # Centrer l'image du cavalier
            img_rect = self.knight_image.get_rect()
            img_rect.center = (x + self.SQUARE_SIZE // 2, y + self.SQUARE_SIZE // 2)
            self.screen.blit(self.knight_image, img_rect)
        else:
            # Utiliser le symbole Unicode si pas d'image
            knight_text = self.title_font.render("♞", True, (150, 0, 0))
            knight_rect = knight_text.get_rect(center=(x + self.SQUARE_SIZE // 2, y + self.SQUARE_SIZE // 2 - 10))
            self.screen.blit(knight_text, knight_rect)
    
    def draw_button(self, name, text, rect):
        """Dessine un bouton"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        
        color = self.BUTTON_HOVER if is_hover and not self.solving else self.BUTTON_COLOR
        if self.solving or (self.animating and name != 'reset'):
            color = (150, 150, 150)
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, rect, 2, border_radius=10)
        
        text_surf = self.font.render(text, True, self.WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def draw_ui(self):
        """Dessine l'interface utilisateur"""
        # Titre
        title = self.title_font.render("Knight's Tour Problem", True, self.TEXT_COLOR)
        self.screen.blit(title, (self.WINDOW_WIDTH // 2 - title.get_width() // 2, 10))
        
        # Sous-titre
        subtitle = self.small_font.render("", True, self.TEXT_COLOR)
        self.screen.blit(subtitle, (self.WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 55))
        
        # Boutons
        self.draw_button('simple', "Backtracking Simple", self.buttons['simple'])
        self.draw_button('heuristic', "Backtracking + Heuristiques", self.buttons['heuristic'])
        self.draw_button('animate', "Animer", self.buttons['animate'])
        self.draw_button('reset', "Reset", self.buttons['reset'])
        
        # Zone de statistiques
        stats_y = 350
        if self.solving:
            solving_text = self.font.render("Résolution en cours...", True, self.TEXT_COLOR)
            self.screen.blit(solving_text, (670, stats_y))
        
        if self.animating:
            anim_text = self.font.render(f"Animation: {self.current_move}/64", True, self.TEXT_COLOR)
            self.screen.blit(anim_text, (670, stats_y + 40))
        
        if self.stats:
            # Cadre des statistiques
            stats_rect = pygame.Rect(650, stats_y, 500, 250)
            pygame.draw.rect(self.screen, (240, 240, 240), stats_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.BLACK, stats_rect, 2, border_radius=10)
            
            # Titre
            stats_title = self.font.render("Statistiques", True, self.TEXT_COLOR)
            self.screen.blit(stats_title, (670, stats_y + 10))
            
            # Méthode
            method_label = self.small_font.render("Méthode:", True, self.TEXT_COLOR)
            self.screen.blit(method_label, (670, stats_y + 50))
            method_text = self.tiny_font.render(self.stats['method'], True, self.TEXT_COLOR)
            self.screen.blit(method_text, (680, stats_y + 75))
            
            # Temps
            time_text = self.small_font.render(f"Temps: {self.stats['time']:.3f} secondes", True, self.TEXT_COLOR)
            self.screen.blit(time_text, (670, stats_y + 110))
            
            # Mouvements
            moves_text = self.small_font.render(f"Mouvements: {self.stats['moves']}/64", True, self.TEXT_COLOR)
            self.screen.blit(moves_text, (670, stats_y + 145))
            
            # Message de succès
            if self.stats['moves'] == 64:
                success_text = self.font.render("✓ Solution trouvée!", True, self.SUCCESS_COLOR)
                self.screen.blit(success_text, (670, stats_y + 185))
        
        # Informations sur les heuristiques
        info_y = 620
        info_title = self.small_font.render("Heuristiques CSP:", True, self.TEXT_COLOR)
        self.screen.blit(info_title, (650, info_y))
        
        mrv_text = self.tiny_font.render("• MRV: Minimum Remaining Values", True, self.TEXT_COLOR)
        self.screen.blit(mrv_text, (660, info_y + 30))
        
        lcv_text = self.tiny_font.render("• LCV: Least Constraining Value", True, self.TEXT_COLOR)
        self.screen.blit(lcv_text, (660, info_y + 55))
    
    def solve(self, use_heuristics=False):
        """Résout le problème"""
        self.solving = True
        self.solution = None
        self.stats = None
        self.current_move = 0
        self.animating = False
        
        # Mise à jour de l'écran
        self.draw()
        pygame.display.flip()
        
        # Résolution
        start_time = time.time()
        assignment = [(0, 0)]
        
        if use_heuristics:
            solution = self.knight_solver.backtracking_with_heuristics(assignment)
            method = "Backtracking + MRV + LCV"
        else:
            solution = self.knight_solver.backtracking(assignment)
            method = "Backtracking Simple"
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        self.solution = solution
        self.stats = {
            'method': method,
            'time': elapsed,
            'moves': len(solution) if solution else 0
        }
        self.solving = False
    
    def start_animation(self):
        """Démarre l'animation de la solution"""
        if self.solution:
            self.animating = True
            self.current_move = 0
            self.last_move_time = pygame.time.get_ticks()
    
    def update_animation(self):
        """Met à jour l'animation"""
        if not self.animating or not self.solution:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.animation_speed:
            self.current_move += 1
            self.last_move_time = current_time
            
            if self.current_move >= len(self.solution):
                self.current_move = len(self.solution) - 1
                self.animating = False
    
    def reset(self):
        """Réinitialise l'application"""
        self.solution = None
        self.stats = None
        self.solving = False
        self.animating = False
        self.current_move = 0
    
    def handle_click(self, pos):
        """Gère les clics de souris"""
        if self.solving:
            return
        
        if self.buttons['simple'].collidepoint(pos) and not self.animating:
            self.solve(use_heuristics=False)
        elif self.buttons['heuristic'].collidepoint(pos) and not self.animating:
            self.solve(use_heuristics=True)
        elif self.buttons['animate'].collidepoint(pos):
            self.start_animation()
        elif self.buttons['reset'].collidepoint(pos):
            self.reset()
    
    def draw(self):
        """Dessine tout"""
        self.screen.fill(self.WHITE)
        self.draw_board()
        self.draw_path()
        self.draw_knight()
        self.draw_ui()
    
    def run(self):
        """Boucle principale"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            # Mettre à jour l'animation
            self.update_animation()
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


# Programme principal
if __name__ == "__main__":
    print("""ici
    """)
    
    gui = GameGUI()
    gui.run()


















