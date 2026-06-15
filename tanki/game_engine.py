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
        self.ip_address = "127.0.0.1"
        self.running = True
        self.current_map_matrix = None

    def setup_map(self):
        self.walls.empty()
        thick = 2
        ts = constants.TILE_SIZE

        self.current_map_matrix = random.choice(constants.MAPS)

        for r, row in enumerate(self.current_map_matrix):
            for c, cell in enumerate(row):
                if cell == 1:
                    x, y = c * ts, r * ts
                    if r > 0 and self.current_map_matrix[r - 1][c] == 0:
                        self.walls.add(Wall(x, y, ts, thick))
                    if r < len(self.current_map_matrix) - 1 and self.current_map_matrix[r + 1][c] == 0:
                        self.walls.add(Wall(x, y + ts - thick, ts, thick))
                    if c > 0 and self.current_map_matrix[r][c - 1] == 0:
                        self.walls.add(Wall(x, y, thick, ts))
                    if c < len(row) - 1 and self.current_map_matrix[r][c + 1] == 0:
                        self.walls.add(Wall(x + ts - thick, y, thick, ts))

    def start_game(self):
        self.tanks.empty()
        self.bullets.empty()
        self.setup_map()

        ts = constants.TILE_SIZE
        p1 = Tank(ts * 1.5, ts * 1.5, constants.GREEN, {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_SPACE
        }, self.bullets, self.walls, lives=constants.tank_lives, player_id=1)

        p2 = Tank(ts * 8.5, ts * 5.5, constants.RED, {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'shoot': pygame.K_RSHIFT
        }, self.bullets, self.walls, lives=constants.tank_lives, player_id=2)

        self.tanks.add(p1, p2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

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
                            self.state = constants.CONNECT
                            self.ui.selected_index = 0
                        elif self.ui.selected_index == 2:
                            self.state = constants.SETTINGS
                            self.ui.selected_index = 0
                        elif self.ui.selected_index == 3:
                            self.running = False

            elif self.state == constants.CONNECT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                        self.state = constants.PLAYING
                    elif event.key == pygame.K_BACKSPACE:
                        self.ip_address = self.ip_address[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.state = constants.MENU
                        self.ui.selected_index = 1
                    elif event.unicode and event.unicode in "0123456789.":
                        self.ip_address += event.unicode

            elif self.state == constants.SETTINGS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.ui.selected_index = (self.ui.selected_index - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.ui.selected_index = (self.ui.selected_index + 1) % 3

                    if self.ui.selected_index == 0:
                        if event.key == pygame.K_RIGHT: constants.tank_speed = min(5, constants.tank_speed + 1)
                        if event.key == pygame.K_LEFT: constants.tank_speed = max(1, constants.tank_speed - 1)
                    elif self.ui.selected_index == 1:
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

            elif self.state == constants.CONNECT:
                self.ui.draw_connect_menu(self.ip_address)

            elif self.state == constants.SETTINGS:
                self.ui.draw_settings(constants.tank_speed, constants.tank_lives)

            elif self.state == constants.PLAYING:
                self.screen.fill(constants.GRAY)

                # --- AKTUALIZÁCIA ---
                self.tanks.update()
                self.bullets.update()

                # --- LOGIKA KOLÍZIÍ (STRELY VS TANKY) ---
                for bullet in self.bullets:
                    # Skontrolujeme, či strela trafila nejaký tank
                    hit_tanks = pygame.sprite.spritecollide(bullet, self.tanks, False)
                    for tank in hit_tanks:
                        # Ak je to cudzí tank ALEBO tvoj vlastný po odraze (bounces > 0)
                        if bullet.owner != tank or getattr(bullet, 'bounces', 0) > 0:
                            tank.lives -= 1
                            bullet.kill()
                            if tank.lives <= 0:
                                tank.kill()
                            break  # Strela zmizne hneď po prvom zásahu

                # --- VYKRESLENIE ---
                self.walls.draw(self.screen)
                self.bullets.draw(self.screen)
                self.tanks.draw(self.screen)

                # --- HUD (Životy) ---
                tanks_list = sorted(self.tanks.sprites(), key=lambda t: (t.player_id is None, t.player_id if t.player_id is not None else 0))
                for index, tank in enumerate(tanks_list):
                    player_label = f"Hráč {tank.player_id} HP: {tank.lives}" if tank.player_id is not None else f"HP: {tank.lives}"
                    label_surface = self.ui.font_info.render(player_label, True, tank.color)
                    self.screen.blit(label_surface, (20, 20 + index * 30))

                # Detekcia konca kola
                alive_tanks = self.tanks.sprites()
                if len(alive_tanks) < 2:
                    if len(alive_tanks) == 1:
                        winner = alive_tanks[0]
                        msg = f"Hráč {winner.player_id} VYHRAL!" if winner.player_id is not None else "VYHRAL!"
                    else:
                        msg = "REMÍZA!"

                    self.ui.draw_text(msg, self.ui.font_title, constants.YELLOW, constants.WIDTH // 2,
                                      constants.HEIGHT // 2)
                    pygame.display.flip()

                    pygame.time.delay(1500)
                    self.start_game()

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.state = constants.MENU

            pygame.display.flip()
            self.clock.tick(constants.FPS)

        pygame.quit()
        sys.exit()