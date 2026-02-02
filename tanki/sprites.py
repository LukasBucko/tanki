import pygame
import math
import tanki.constants as constants


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(constants.WALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, color):
        super().__init__()
        # Malá guľatá strela (lepšie pre odrazy)
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, constants.YELLOW, (3, 3), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(constants.BULLET_SPEED, 0).rotate(-angle)

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        if not (0 <= self.pos.x <= constants.WIDTH and 0 <= self.pos.y <= constants.HEIGHT):
            self.kill()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls, bullet_group, wall_group, lives=None):
        super().__init__()
        self.color = color
        self.lives = lives if lives is not None else constants.tank_lives
        self.bullet_group = bullet_group
        self.wall_group = wall_group
        self.controls = controls
        self.cooldown_tracker = 0

        self.original_image = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (5, 9, 30, 26), border_radius=4)
        pygame.draw.rect(self.original_image, (60, 60, 60), (20, 19, 22, 6), border_radius=2)
        tower_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
        pygame.draw.circle(self.original_image, tower_color, (20, 22), 8)
        pygame.draw.circle(self.original_image, (40, 40, 40), (20, 22), 8, 2)

        self.image = self.original_image


        self.hitbox = pygame.Rect(0, 0, 20, 20)
        self.hitbox.center = (x, y)

        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0

    def shoot(self):
        if self.cooldown_tracker == 0:
            new_bullet = Bullet(self.pos.x, self.pos.y, self.angle, self.color)
            self.bullet_group.add(new_bullet)
            self.cooldown_tracker = constants.SHOOT_COOLDOWN

    def update(self):
        keys = pygame.key.get_pressed()

        # 1. Rotácia (mení len uhol, nie hitbox)
        if keys[self.controls['left']]: self.angle += 3.5
        if keys[self.controls['right']]: self.angle -= 3.5

        # Výpočet smeru
        direction = pygame.math.Vector2(1, 0).rotate(-self.angle)
        move_vec = pygame.math.Vector2(0, 0)
        if keys[self.controls['up']]: move_vec = direction * constants.tank_speed
        if keys[self.controls['down']]: move_vec = -direction * constants.tank_speed


        # Pohyb na osi X
        if move_vec.x != 0:
            self.pos.x += move_vec.x
            self.hitbox.centerx = self.pos.x
            # Kontrola kolízie hitboxu so stenami
            for wall in self.wall_group:
                if self.hitbox.colliderect(wall.rect):
                    if move_vec.x > 0: self.hitbox.right = wall.rect.left
                    if move_vec.x < 0: self.hitbox.left = wall.rect.right
                    self.pos.x = self.hitbox.centerx
                    break

        # Pohyb na osi Y
        if move_vec.y != 0:
            self.pos.y += move_vec.y
            self.hitbox.centery = self.pos.y
            for wall in self.wall_group:
                if self.hitbox.colliderect(wall.rect):
                    if move_vec.y > 0: self.hitbox.bottom = wall.rect.top
                    if move_vec.y < 0: self.hitbox.top = wall.rect.bottom
                    self.pos.y = self.hitbox.centery
                    break

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

        # Streľba a cooldown
        if keys[self.controls['shoot']]: self.shoot()
        if self.cooldown_tracker > 0: self.cooldown_tracker -= 1