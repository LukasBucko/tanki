import pygame
import sys
import constants
from ui import UI


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("TANKI")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.state = constants.MENU
        self.running = True

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
                        if event.key == pygame.K_RIGHT: constants.tank_speed += 1
                        if event.key == pygame.K_LEFT: constants.tank_speed = max(1, constants.tank_speed - 1)
                    elif self.ui.selected_index == 1:
                        if event.key == pygame.K_RIGHT: constants.tank_lives += 1
                        if event.key == pygame.K_LEFT: constants.tank_lives = max(1, constants.tank_lives - 1)
                    elif event.key == pygame.K_RETURN and self.ui.selected_index == 2:  # Späť
                        self.state = constants.MENU
                        self.ui.selected_index = 1

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(constants.BLACK)

            if self.state == constants.MENU:
                self.ui.draw_main_menu()
            elif self.state == constants.SETTINGS:
                self.ui.draw_settings(constants.tank_speed, constants.tank_lives)
            elif self.state == constants.PLAYING:
                self.screen.fill(constants.GRAY)
                self.ui.draw_text("HRA PREBIEHA", self.ui.font_menu, constants.WHITE, constants.WIDTH // 2,
                                  constants.HEIGHT // 2)
                self.ui.draw_text("Stlač ESC pre návrat do menu", self.ui.font_info, constants.WHITE,
                                  constants.WIDTH // 2, constants.HEIGHT // 2 + 50)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]: self.state = constants.MENU

            pygame.display.flip()
            self.clock.tick(constants.FPS)
        pygame.quit()
        sys.exit()