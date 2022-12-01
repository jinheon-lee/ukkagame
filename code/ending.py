import pygame.font
from settings import *
from game_data import levels
from player import Player


class Ending:
    def __init__(self, display_surface, create_levelselect):
        self.frame = 0

        # 스크린 설정
        self.display_surface = display_surface
        self.display_surface.fill('black')

        # 연출용 플레이어 생성
        self.player = Player((-10, 400))

        # 폰트 설정
        self.font = pygame.font.Font('../graphics/font/neodgm.ttf', 60)
        self.font2 = pygame.font.Font('../graphics/font/neodgm.ttf', 120)
        self.font3 = pygame.font.Font('../graphics/font/neodgm.ttf', 40)

        # 시간계산용 프레임 설정
        self.firstframe = 140
        self.secondframe = 170

        # 엔딩 끝난 후 버튼 설정
        self.button = EndButton((screen_width / 2, 500))

        # 버튼 누를 때 실행하는 함수
        self.create_levelselect = create_levelselect

    def button_check(self):
        """버튼 누르는 것 체크"""
        self.button.text = self.font.render('Return', False, 'white')
        if self.button.rect.collidepoint(pygame.mouse.get_pos()):
            self.button.text = self.font.render('Return', False, 'green')
            if pygame.mouse.get_pressed()[0]:
                self.__init__(self.display_surface, self.create_levelselect)
                self.create_levelselect(len(levels) - 1)
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            self.__init__(self.display_surface, self.create_levelselect)
            self.create_levelselect(len(levels) - 1)

    def run(self):
        """엔딩 실행"""
        self.display_surface.fill('black')
        # 프레임을 기준으로 행동 실행

        # 플레이어 움직임
        if self.frame < 120:
            self.player.rect.x += 5
            self.display_surface.blit(self.player.image, self.player.rect)

        if 120 < self.frame < self.firstframe:
            self.display_surface.blit(self.player.image, self.player.rect)

        # 텍스트 연출
        if self.firstframe <= self.frame < self.firstframe + self.secondframe:
            text1 = '모든 억까를 이겨내고'
            self.key1 = (self.frame - self.firstframe) // 3  # 텍스트 연출 사용 위한 키
            text = self.font.render(text1[:self.key1], False, 'white')
            self.display_surface.blit(text, (100, 200))
            if self.firstframe + 40 <= self.frame:
                text2 = '주인공은 목적지에 도달했다!'
                self.key2 = (self.frame - (self.firstframe + 40)) // 3
                text = self.font.render(text2[:self.key2], False, 'white')
                self.display_surface.blit(text, (100, 300))

        if self.firstframe + self.secondframe < self.frame:
            text = self.font2.render('Game Clear', False, 'white')
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
            self.display_surface.blit(text, text_rect)
            if self.firstframe + self.secondframe + 40 < self.frame:
                text1 = 'Thanks for playing'
                self.key1 = (self.frame - (self.firstframe + self.secondframe + 40)) // 3
                text = self.font3.render(text1[:self.key1], False, 'white')
                text_rect = text.get_rect(center=(screen_width / 2, 330))
                self.display_surface.blit(text, text_rect)

        # 돌아가는 버튼 추가
        if self.firstframe + self.secondframe + 150 < self.frame:
            pygame.mouse.set_visible(True)
            self.display_surface.blit(self.button.text, self.button.rect)
            self.button_check()

        self.frame += 1


class EndButton(pygame.sprite.Sprite):
    """레벨셀렉트로 돌아가는 버튼"""
    def __init__(self, pos):
        super().__init__()
        self.font = pygame.font.Font('../graphics/font/neodgm.ttf', 60)
        self.text = self.font.render('Return', False, 'white')
        self.rect = self.text.get_rect()
        self.rect.center = pos
