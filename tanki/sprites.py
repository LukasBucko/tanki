import pygame
import math
import tanki.constants as constants


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, color):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(constants.YELLOW)  # Farba strely
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(x, y))

        # Výpočet smeru letu na základe rotácie tanku
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(constants.BULLET_SPEED, 0).rotate(-angle)

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

        # Odstránenie strely, ak vyletí z obrazovky
        if not (0 <= self.pos.x <= constants.WIDTH and 0 <= self.pos.y <= constants.HEIGHT):
            self.kill()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls, bullet_group, lives=None):
        super().__init__()
        self.color = color  # Uložíme si farbu pre strely
        self.lives = lives if lives is not None else constants.tank_lives
        self.bullet_group = bullet_group  # Skupina, kam sa pridávajú strely

        self.original_image = pygame.Surface((45, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (0, 0, 40, 30))
        pygame.draw.rect(self.original_image, (50, 50, 50), (35, 10, 15, 10))

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.controls = controls

        self.cooldown_tracker = 0  # Sledovanie času do ďalšieho výstrelu

    def shoot(self):
        if self.cooldown_tracker == 0:
            # Vytvoríme strelu na pozícii tanku s jeho uhlom
            new_bullet = Bullet(self.pos.x, self.pos.y, self.angle, self.color)
            self.bullet_group.add(new_bullet)
            self.cooldown_tracker = constants.SHOOT_COOLDOWN

    def update(self):
        keys = pygame.key.get_pressed()

        # Rotácia
        if keys[self.controls['left']]:
            self.angle += 3
        if keys[self.controls['right']]:
            self.angle -= 3

        direction = pygame.math.Vector2(1, 0).rotate(-self.angle)

        # POHYB
        if keys[self.controls['up']]:
            self.pos += direction * constants.tank_speed
        if keys[self.controls['down']]:
            self.pos -= direction * constants.tank_speed

        # STREĽBA
        if keys[self.controls['shoot']]:
            self.shoot()

        # Znižovanie cooldownu
        if self.cooldown_tracker > 0:
            self.cooldown_tracker -= 1

        # Aktualizácia obrázka a obdĺžnika
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        self.pos.x = max(0, min(constants.WIDTH, self.pos.x))
        self.pos.y = max(0, min(constants.HEIGHT, self.pos.y))