from constants import *


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Impact", 80)
        self.font_menu = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_info = pygame.font.SysFont("Arial", 25)
        self.menu_options = ["ŠTART HRY", "NASTAVENIA", "KONIEC"]
        self.selected_index = 0

    def draw_text(self, text, font, color, x, y):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw_main_menu(self):
        self.screen.fill(BLACK)
        self.draw_text("TANKI", self.font_title, GREEN, WIDTH // 2, HEIGHT // 4)

        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_index else WHITE
            text_str = f"> {option} <" if i == self.selected_index else option
            self.draw_text(text_str, self.font_menu, color, WIDTH // 2, HEIGHT // 2 + i * 60)

    def draw_settings(self, speed, lives):
        self.screen.fill(BLACK)
        self.draw_text("NASTAVENIA", self.font_title, GREEN, WIDTH // 2, HEIGHT // 5)

        options = [f"Rýchlosť tankov: {speed}", f"Počet životov: {lives}", "Späť"]
        for i, opt in enumerate(options):
            color = YELLOW if i == self.selected_index else WHITE
            self.draw_text(opt, self.font_menu, color, WIDTH // 2, HEIGHT // 2 + i * 60)

        self.draw_text("Šípkami vľavo/vpravo meníš hodnoty", self.font_info, GRAY, WIDTH // 2, HEIGHT - 50)