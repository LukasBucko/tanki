import pygame
import sys
import random
import os
import tanki.constants as constants
from tanki.ui import UI
from tanki.sprites import Tank, Wall


class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("TANKI")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)

        # --- OPRAVA CIEST K ASSETOM ---
        # Zistíme cestu k priečinku, kde je tento súbor (game_engine.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Priečinok assets je o úroveň vyššie (v root priečinku projektu)
        project_root = os.path.dirname(current_dir)
        assets_path = os.path.join(project_root, "assets")

        # Načítanie zvukových efektov
        try:
            self.shoot_sound = pygame.mixer.Sound(os.path.join(assets_path, "shoot.mp3"))
            self.hit_sound = pygame.mixer.Sound(os.path.join(assets_path, "hit.mp3"))
            self.shoot_sound.set_volume(0.3)
            self.hit_sound.set_volume(0.5)
        except:
                self.shoot_sound = None
                self.hit_sound = None

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
        # Odovzdáme shoot_sound tankom
        p1 = Tank(ts * 1.5, ts * 1.5, constants.GREEN, {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_SPACE
        }, self.bullets, self.walls, shoot_sound=self.shoot_sound, lives=constants.tank_lives)

        p2 = Tank(ts * 8.5, ts * 5.5, constants.RED, {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'shoot': pygame.K_RSHIFT
        }, self.bullets, self.walls, shoot_sound=self.shoot_sound, lives=constants.tank_lives)

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
                            self.state = constants.SETTINGS
                            self.ui.selected_index = 0
                        elif self.ui.selected_index == 2:
                            self.running = False

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

            elif self.state == constants.SETTINGS:
                self.ui.draw_settings(constants.tank_speed, constants.tank_lives)

            elif self.state == constants.PLAYING:
                self.screen.fill(constants.GRAY)

                self.tanks.update()
                self.bullets.update()

                # LOGIKA KOLÍZIÍ (STRELY VS TANKY) + ZVUK ZÁSAHU
                for bullet in self.bullets:
                    hit_tanks = pygame.sprite.spritecollide(bullet, self.tanks, False)
                    for tank in hit_tanks:
                        if bullet.owner != tank or getattr(bullet, 'bounces', 0) > 0:
                            # Prehraj zvuk zásahu
                            if self.hit_sound:
                                self.hit_sound.play()

                            tank.lives -= 1
                            bullet.kill()
                            if tank.lives <= 0:
                                tank.kill()
                            break

                self.walls.draw(self.screen)
                self.bullets.draw(self.screen)
                self.tanks.draw(self.screen)

                # HUD
                tanks_list = self.tanks.sprites()
                p1 = next((t for t in tanks_list if t.color == constants.GREEN), None)
                p2 = next((t for t in tanks_list if t.color == constants.RED), None)

                if p1:
                    p1_lives = self.ui.font_info.render(f"P1 HP: {p1.lives}", True, constants.GREEN)
                    self.screen.blit(p1_lives, (20, 20))
                if p2:
                    p2_lives = self.ui.font_info.render(f"P2 HP: {p2.lives}", True, constants.RED)
                    self.screen.blit(p2_lives, (constants.WIDTH - p2_lives.get_width() - 20, 20))

                if len(self.tanks) < 2:
                    msg = "REMIZA!"
                    if p1:
                        msg = "P1 VYHRAL!"
                    elif p2:
                        msg = "P2 VYHRAL!"
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