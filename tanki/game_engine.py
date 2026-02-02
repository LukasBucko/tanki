import pygame
import sys
import random
import tanki.constants as constants
from tanki.ui import UI
from tanki.sprites import Tank, Wall


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("TANKI")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)

        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.state = constants.MENU
        self.running = True
        self.current_map_matrix = None

    def setup_map(self):
        self.walls.empty()
        thick = 2
        ts = constants.TILE_SIZE

        # Výber náhodnej mapy zo zoznamu piatich máp
        self.current_map_matrix = random.choice(constants.MAPS)

        for r, row in enumerate(self.current_map_matrix):
            for c, cell in enumerate(row):
                if cell == 1:
                    x, y = c * ts, r * ts
                    # Kreslíme čiary len tam, kde stena susedí s prázdnym priestorom (0)
                    if r > 0 and self.current_map_matrix[r - 1][c] == 0:
                        self.walls.add(Wall(x, y, ts, thick))
                    if r < len(self.current_map_matrix) - 1 and self.current_map_matrix[r + 1][c] == 0:
                        self.walls.add(Wall(x, y + ts - thick, ts, thick))
                    if c > 0 and self.current_map_matrix[r][c - 1] == 0:
                        self.walls.add(Wall(x, y, thick, ts))
                    if c < len(row) - 1 and self.current_map_matrix[r][c + 1] == 0:
                        self.walls.add(Wall(x + ts - thick, y, thick, ts))

    def start_game(self):
        """Inicializuje kolo, mapu a tanky s ohľadom na nastavené životy."""
        self.tanks.empty()
        self.bullets.empty()
        self.setup_map()

        ts = constants.TILE_SIZE
        # Hráč 1 - Spawn vľavo hore (bezpečná zóna 1,1)
        p1 = Tank(ts * 1.5, ts * 1.5, constants.GREEN, {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_SPACE
        }, self.bullets, self.walls, lives=constants.tank_lives)

        # Hráč 2 - Spawn vpravo dole (bezpečná zóna 8,5)
        p2 = Tank(ts * 8.5, ts * 5.5, constants.RED, {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'shoot': pygame.K_RETURN
        }, self.bullets, self.walls, lives=constants.tank_lives)

        self.tanks.add(p1, p2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # --- Logika pre MENU ---
            if self.state == constants.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.ui.selected_index = (self.ui.selected_index - 1) % len(self.ui.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.ui.selected_index = (self.ui.selected_index + 1) % len(self.ui.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.ui.selected_index == 0:
                            self.start_game()
                            self.state = constants.PLAYING
                        elif self.ui.selected_index == 1:
                            self.state = constants.SETTINGS
                            self.ui.selected_index = 0
                        elif self.ui.selected_index == 2:
                            self.running = False

            # --- Logika pre SETTINGS ---
            elif self.state == constants.SETTINGS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.ui.selected_index = (self.ui.selected_index - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.ui.selected_index = (self.ui.selected_index + 1) % 3

                    if self.ui.selected_index == 0:  # Rýchlosť
                        if event.key == pygame.K_RIGHT: constants.tank_speed = min(5, constants.tank_speed + 1)
                        if event.key == pygame.K_LEFT: constants.tank_speed = max(1, constants.tank_speed - 1)
                    elif self.ui.selected_index == 1:  # Životy
                        if event.key == pygame.K_RIGHT: constants.tank_lives = min(5, constants.tank_lives + 1)
                        if event.key == pygame.K_LEFT: constants.tank_lives = max(1, constants.tank_lives - 1)
                    elif event.key == pygame.K_RETURN and self.ui.selected_index == 2:
                        self.state = constants.MENU
                        self.ui.selected_index = 1

    def run(self):
        while self.running:
            self.handle_events()

            if self.state == constants.MENU:
                self.ui.draw_main_menu()

            elif self.state == constants.SETTINGS:
                self.ui.draw_settings(constants.tank_speed, constants.tank_lives)

            elif self.state == constants.PLAYING:
                self.screen.fill(constants.GRAY)

                # --- AKTUALIZÁCIA ---
                self.tanks.update()
                self.bullets.update()

                # --- VYKRESLENIE ---
                self.walls.draw(self.screen)
                self.bullets.draw(self.screen)
                self.tanks.draw(self.screen)

                # --- HUD (Životy) ---
                tanks_list = self.tanks.sprites()
                if len(tanks_list) >= 2:
                    p1_lives = self.ui.font_info.render(f"P1 HP: {tanks_list[0].lives}", True, constants.GREEN)
                    self.screen.blit(p1_lives, (20, 20))
                    p2_lives = self.ui.font_info.render(f"P2 HP: {tanks_list[1].lives}", True, constants.RED)
                    self.screen.blit(p2_lives, (constants.WIDTH - p2_lives.get_width() - 20, 20))

                # Detekcia konca kola (ak jeden hráč vyhrá)
                if len(self.tanks) < 2:
                    pygame.time.delay(1000)
                    self.start_game()

                # ESC pre návrat do menu
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.state = constants.MENU

            pygame.display.flip()
            self.clock.tick(constants.FPS)

        pygame.quit()
        sys.exit()