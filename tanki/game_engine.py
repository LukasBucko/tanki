import pygame
import sys
import tanki.constants as constants
from tanki.ui import UI
from tanki.sprites import Tank


class GameEngine:
    def __init__(self):
        pygame.init()
        # Nastavenie okna
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("Tank Battle Project")
        self.clock = pygame.time.Clock()

        self.ui = UI(self.screen)

        # Skupiny spritov
        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()  # Pridaná skupina pre strely

        # Predvolený stav
        self.state = constants.MENU
        self.running = True

    def start_game(self):
        self.tanks.empty()
        self.bullets.empty()  # Vyčistíme strely pri novom štarte

        # Hráč 1 - Pridaný 'shoot': SPACE a odkaz na skupinu striel
        p1 = Tank(200, 300, constants.GREEN, {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'shoot': pygame.K_SPACE
        }, self.bullets, lives=constants.tank_lives)

        # Hráč 2 - Pridaný 'shoot': RETURN (Enter) a odkaz na skupinu striel
        p2 = Tank(600, 300, constants.RED, {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_RETURN
        }, self.bullets, lives=constants.tank_lives)

        self.tanks.add(p1, p2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Logika pre HLAVNÉ MENU
            if self.state == constants.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.ui.selected_index = (self.ui.selected_index - 1) % len(self.ui.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.ui.selected_index = (self.ui.selected_index + 1) % len(self.ui.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.ui.selected_index == 0:  # ŠTART
                            self.start_game()
                            self.state = constants.PLAYING
                        elif self.ui.selected_index == 1:  # NASTAVENIA
                            self.state = constants.SETTINGS
                            self.ui.selected_index = 0
                        elif self.ui.selected_index == 2:  # KONIEC
                            self.running = False

            # Logika pre NASTAVENIA
            elif self.state == constants.SETTINGS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.ui.selected_index = (self.ui.selected_index - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.ui.selected_index = (self.ui.selected_index + 1) % 3

                    # Meníme globálne konštanty šípkami vľavo/vpravo
                    if self.ui.selected_index == 0:
                        if event.key == pygame.K_RIGHT:
                            constants.tank_speed = min(5, constants.tank_speed + 1)
                        if event.key == pygame.K_LEFT:
                            constants.tank_speed = max(1, constants.tank_speed - 1)

                    elif self.ui.selected_index == 1:
                        if event.key == pygame.K_RIGHT:
                            constants.tank_lives = min(5, constants.tank_lives + 1)
                        if event.key == pygame.K_LEFT:
                            constants.tank_lives = max(1, constants.tank_lives - 1)

                    elif event.key == pygame.K_RETURN and self.ui.selected_index == 2:
                        self.state = constants.MENU
                        self.ui.selected_index = 1

    def run(self):
        while self.running:
            self.handle_events()

            # Vykresľovanie podľa aktuálneho stavu
            if self.state == constants.MENU:
                self.ui.draw_main_menu()

            elif self.state == constants.SETTINGS:
                self.ui.draw_settings(constants.tank_speed, constants.tank_lives)

            elif self.state == constants.PLAYING:
                self.screen.fill(constants.GRAY)

                # --- AKTUALIZÁCIA ---
                self.tanks.update()
                self.bullets.update()  # Aktualizujeme pohyb striel

                # --- VYKRESLENIE ---
                self.tanks.draw(self.screen)
                self.bullets.draw(self.screen)  # Vykreslíme strely na obrazovku

                # --- ZOBRAZENIE ŽIVOTOV V ROHOCH ---
                tanks_list = self.tanks.sprites()
                if len(tanks_list) >= 2:
                    p1_lives_surf = self.ui.font_info.render(f"P1 Životy: {tanks_list[0].lives}", True, constants.GREEN)
                    self.screen.blit(p1_lives_surf, (20, 20))

                    p2_lives_surf = self.ui.font_info.render(f"P2 Životy: {tanks_list[1].lives}", True, constants.RED)
                    self.screen.blit(p2_lives_surf, (constants.WIDTH - p2_lives_surf.get_width() - 20, 20))

                # Návrat do menu pomocou ESC
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.state = constants.MENU

                self.ui.draw_text("ESC pre menu", self.ui.font_info, constants.WHITE,
                                  constants.WIDTH // 2, constants.HEIGHT - 30)

            pygame.display.flip()
            self.clock.tick(constants.FPS)

        pygame.quit()
        sys.exit()