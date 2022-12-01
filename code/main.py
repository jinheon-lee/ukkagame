import sys

import pygame

from game_data import levels
from level import Level
from levelselect import Levelselect
from settings import *
from ending import Ending
from intro import Intro


def read_scoreboard():
    """레벨의 수만큼 스코어 보드 텍스트 파일을 읽어 game_data.py의 각 레벨의 scoreboard에 저장"""
    for i in range(len(levels)):
        try:
            with open(f'../userscore/scoreboard{i}.txt', 'r') as f:
                lines = f.readlines()
                for j in lines:
                    try:
                        score = j.strip()
                        levels[i]['scoreboard'].append(score)

                    # 스코어보드 파일이 잘못 되었을 경우 초기화
                    except ValueError as err:
                        levels[i]['scoreboard'] = {}
                        break
        # 스코어보드 파일이 존재하지 않을 경우 생성 후 초기화
        except IOError:
            with open(f'../userscore/scoreboard{i}.txt', 'w') as f:
                pass


class Game:
    """
    전체 게임 클래스
    """

    def __init__(self):
        self.unlocked_level = 1  # 해금된 레벨(0~self.unlocked_level)
        self.levelselect = Levelselect(self.unlocked_level, screen, self.create_level)  # 레벨 선택 클래스
        self.ending = Ending(screen, self.create_levelselect)  # 엔딩 선택 장면
        self.intro = Intro(screen)  # 인트로
        self.status = 'intro'  # 게임에서 실행중인 것(인트로, 레벨선택, 레벨, 엔딩 등)
        self.deathcount = 0  # 죽은 횟수
        self.starttime = 0  # 레벨 시작 시간

    def run(self):
        """
        self.status 따라 장면 실행

        :return: None
        """
        if self.status == 'intro':
            self.intro.run()
            if self.intro.intro_over:
                self.status = 'levelselect'
        elif self.status == 'levelselect':
            self.levelselect.run()
        elif self.status == 'level':
            self.level.run()
        elif self.status == 'ending':
            self.ending.run()
        elif self.status == 'scoreboard':
            pass

    def create_level(self, current_level, pos = None, deathcount = 0):
        """
        입력받은 pos 위치에 플레이어가 있는 새 레벨 생성\n
        입력받은 pos 없으면 맵의 기본값으로 설정

        :param current_level: int
        :param pos: tuple
        :param deathcount: int
        :return: None
        """
        self.starttime = self.levelselect.starttime
        self.deathcount = deathcount
        self.status = 'level'
        self.level = Level(current_level, screen, self.create_levelselect, self.create_level)
        if pos != None:  # pos가 주어졌다면 플레이어의 위치를 새롭게 지정, 체크포인트에 사용
            '''
            여기서 self.level.startx는 레벨에 들어왔을 때 플레이어가 스폰되는 x좌표
            pos를 받은 경우 체크포인트가 보이는 위치의 x좌표가 이 startx가 되게 화면을 이동
            ->pos[0]-self.level.startx만큼 왼쪽으로 world_shift
            그 뒤 화면 기준 startx에에 플레이어 소환
            '''
            self.level.updatetile(-pos[0] + self.level.startx)
            self.level.player.sprite.rect.midleft = (self.level.startx, pos[1])
        self.level.deathcount = self.deathcount

    def create_levelselect(self, new_unlocked_level):
        """
        레벨 셀렉트 클래스 만듦

        :param new_unlocked_level: int
        :return:
        """
        # 만약 마지막 스테이지를 깨 new_unlocked_level 인덱스가 레벨의 수와 같으면 엔딩 실행
        if new_unlocked_level == len(levels):
            self.status = 'ending'
            return
        # new_max_level이 기존의 max_level다 작으면 새로운 unlocked_level 업데이트
        if new_unlocked_level > self.unlocked_level:
            self.unlocked_level = new_unlocked_level
        self.levelselect = Levelselect(self.unlocked_level, screen, self.create_level)
        self.status = 'levelselect'


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()
read_scoreboard()
pygame.display.set_caption('ukkagame')  # 게임 창 이름
pygame.display.flip()


while True:
    for event in pygame.event.get():
        # 게임 닫을 때 세이브데이터 저장하기
        if event.type == pygame.QUIT:
            for i in range(len(levels)):
                with open(f'../userscore/scoreboard{i}.txt', 'w') as ff:
                    for j in sorted(map(int, levels[i]['scoreboard'])):
                        ff.write(str(j) + '\n')
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # esc 누르면 게임 끄기
                if game.status == 'level' or 'ending':  # 레벨이나 엔딩 중이면 레벨 선택하는 곳으로 돌아가기
                    game.ending.__init__(screen, game.create_levelselect)  # Ending 클래스 초기화
                    game.status = 'levelselect'
                else:
                    pygame.quit()
                    sys.exit()
    screen.fill('skyblue')
    game.run()  # 게임 실행

    pygame.display.update()
    clock.tick(60)
