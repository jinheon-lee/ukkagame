import pygame
from settings import screen_height

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.on_ground = True

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_speed
            self.on_ground = False

    def update(self):
        self.get_input()

    def check_death(self):
        if self.rect.y > screen_height:
            return True
        else:
            return False
