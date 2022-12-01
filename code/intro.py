from settings import *
import pygame
import time

class Intro:
    def __init__(self,display_surface):
        # whitescreen은 게임 화면 규격의 하얀 바탕
        # companylogo는 팀 이름 있는 게임 화면 규격의 이미지
        # logo는 게임 타이틀 있는 게임 화면 규격 이미지
        # 로비는 메뉴 사진

        whitescreenog = pygame.image.load('../graphics/intro/whitescreen.png')
        self.whitescreen = pygame.transform.scale(whitescreenog, (screen_width, screen_height))

        companylogoog = pygame.image.load('../graphics/intro/companylogo.png')
        self.companylogo = pygame.transform.scale(companylogoog, (screen_width, screen_height))

        logoog = pygame.image.load('../graphics/intro/logo.png')
        self.logo = pygame.transform.scale(logoog, (screen_width, screen_height))

        lobbyog = pygame.image.load('../graphics/intro/lobby.png')
        self.lobby = pygame.transform.scale(lobbyog, (screen_width, screen_height))

        self.screen = display_surface
        self.intro_over = False
        self.screen.fill('white')
        self.timesettrue = 0

    def run(self):
        """인트로 실행"""
        self.playtime = time.time()
        self.whitescreen.set_alpha(40)
        self.screen.fill('white')
        # 처음 시작할 때 로고 나오기, 클릭하면 시작
        if self.timesettrue == 0:
            self.t0 = self.playtime
            self.timesettrue = 1
        if 0 <= self.playtime - self.t0 < 1:
            self.screen.fill('white')
            self.screen.blit(self.whitescreen, (0, 0))
        if 3 <= self.playtime - self.t0 < 5:
            self.screen.fill('white')
            self.companylogo.set_alpha(255 * (self.playtime - self.t0 - 3) / 2)
            self.screen.blit(self.companylogo, (0, 0))
        if 7 <= self.playtime - self.t0 < 9:
            self.screen.fill('white')
            self.companylogo.set_alpha(255 * (9 - self.playtime + self.t0) / 2)
            self.screen.blit(self.companylogo, (0, 0))

        if 10 <= self.playtime - self.t0 < 11:
            self.screen.fill('white')

        if 11 <= self.playtime - self.t0 < 13:
            self.screen.fill('white')
            self.logo.set_alpha(255 * (self.playtime - self.t0 - 11) / 2)
            self.screen.blit(self.logo, (0, 0))

        if 13 <= self.playtime - self.t0:
            self.screen.blit(self.logo, (0, 0))
            if pygame.mouse.get_pressed()[0]:
                self.timesettrue = 0
                self.intro_over = True

        pygame.display.update()