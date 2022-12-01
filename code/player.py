import pygame

from settings import screen_height


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))  # 플레이어 이미지
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)  # 플레이어 직사각형
        self.direction = pygame.math.Vector2(0, 0)  # 플레이어 방향벡터(x는 x축 방향설정, y는 y축 속력)
        self.speed = 8  # 플레이어 x방향 속력
        self.gravity = 0.8  # 플레이어에 적용되는 중력
        self.jump_speed = -16  # 플렝이어 점프 시 바뀌는 y방향 속도
        self.on_ground = True  # 땅에 있는지 여부

    def get_input(self):
        """키 입력받아서 방향벡터 수정"""
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
        """중력 적용"""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.on_ground = False

    def jump(self):
        """플레이어 점프"""
        if self.on_ground:
            self.direction.y = self.jump_speed
            self.on_ground = False

    def update(self):
        """인풋 받음 """
        self.get_input()

    def check_death(self):
        if self.rect.y > screen_height:
            return True
        else:
            return False
