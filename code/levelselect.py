import pygame

from game_data import levels
from support import import_imagelist


class Levelselect:  # 레벨 선택 클래스
    def __init__(self, unlocked_level, surface, create_level):
        self.lastlevel = len(levels)  # 레벨 수
        self.selected_level = 0  # 선택된 레벨
        self.unlocked_level = unlocked_level  # 해금된 레벨
        self.buttons = pygame.sprite.Group()  # 버튼 클래스 그룹
        self.display_surface = surface  # 스크린
        self.create_level = create_level  # 레벨 생성 함수
        self.starttime = 0  # 게임 시작시부터 시간을 측정하기 위한 변수
        self.cnt = 10  # 키보드 연속입력 제한을 위한 카운터

        for i in range(self.lastlevel):
            # 레벨 개수만큼 버튼 만들기
            pos = levels[i]['pos']
            imgpath = levels[i]['selectimgpath']
            img = import_imagelist(imgpath)
            if i <= self.unlocked_level:
                status = 'available'
            else:
                status = 'locked'
            self.buttons.add(Button(pos, status, img))

    def displaybutton(self):
        """버튼 상태를 지정하고 버튼 그리기"""
        for i, button in enumerate(self.buttons.sprites()):
            if button.status != 'locked':
                if i == self.selected_level:
                    button.status = 'selected'
                else:
                    button.status = 'unselected'
            else:
                button.status = 'locked'
            button.update()
        self.buttons.draw(self.display_surface)

    def update(self):
        """버튼 누르는 것 확인"""

        # 키보드 입력 확인
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.starttime = pygame.time.get_ticks()
            print("start:", self.starttime)
            self.create_level(self.selected_level)
            pygame.mouse.set_visible(False)
        elif keys[pygame.K_UP]:
            if self.selected_level >= 1 and self.cnt <= 0:
                self.selected_level -= 1
                self.cnt = 10

        elif keys[pygame.K_DOWN]:
            if self.selected_level < self.unlocked_level and self.cnt <= 0:
                self.selected_level += 1
                self.cnt = 10

        # 마우스 입력 확인
        mousepos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.buttons.sprites()):
            if sprite.rect.collidepoint(mousepos):
                if i <= self.unlocked_level:
                    self.selected_level = i
                if pygame.mouse.get_pressed()[0] and i <= self.unlocked_level and self.cnt <= 0:
                    self.starttime = pygame.time.get_ticks()
                    print("start:", self.starttime)
                    pygame.mouse.set_visible(False)
                    self.create_level(i)
                    self.cnt = 10
        # 연속입력 방지 카운터
        if self.cnt > 0:
            self.cnt -= 1

    def run(self):
        """Levelselect 실행"""
        pygame.mouse.set_visible(True)
        self.update()
        self.displaybutton()

    # 아래


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, status, imglist):
        super().__init__()
        self.imglist = imglist  # [선택 X 이미지, 선택 이미지, 잠김 이미지]
        self.image = self.imglist[0]  # 선택 안되어있을 때 이미지
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.index = 0
        self.status = status

    def update(self):
        if self.status == 'selected':  # 선택됨
            self.index = 1
        elif self.status == 'unselected':  # 선택 안됨
            self.index = 2
        else:  # 잠김
            self.index = 0

        self.image = self.imglist[self.index]  # 버튼 이미지 업데이트
