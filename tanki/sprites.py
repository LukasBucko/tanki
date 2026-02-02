import pygame
import math
import tanki.constants as constants


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls, lives=None):
        super().__init__()


        self.lives = lives if lives is not None else constants.tank_lives


        self.original_image = pygame.Surface((45, 30), pygame.SRCALPHA)
        # Telo tanku
        pygame.draw.rect(self.original_image, color, (0, 0, 40, 30))

        pygame.draw.rect(self.original_image, (50, 50, 50), (35, 10, 15, 10))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Pozícia a rotácia
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.controls = controls

    def update(self):
        keys = pygame.key.get_pressed()

        #Rotácia
        if keys[self.controls['left']]:
            self.angle += 3
        if keys[self.controls['right']]:
            self.angle -= 3

        direction = pygame.math.Vector2(1, 0).rotate(-self.angle)

        #POHYB
        if keys[self.controls['up']]:
            self.pos += direction * constants.tank_speed
        if keys[self.controls['down']]:
            self.pos -= direction * constants.tank_speed

        #Aktualizácia obrázka a obdĺžnika
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        #Voliteľné: Hranice obrazovky (aby tank neodletel preč)
        self.pos.x = max(0, min(constants.WIDTH, self.pos.x))
        self.pos.y = max(0, min(constants.HEIGHT, self.pos.y))