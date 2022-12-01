import pygame

from game_data import levels
from player import Player
from settings import tile_size, screen_width, screen_height
from support import import_csv_layout, import_imagedict
from tiles import *
pygame.font.init()
font = pygame.font.Font('../graphics/font/big-shot.ttf', 80)


class Level:
    def __init__(self, current_level, surface, create_levelselect, create_level):
        # level setup
        self.current_level = current_level  # 현재 레벨
        self.display_surface = surface  # 스크린
        level_data = levels[current_level]  # game_data에서 가져온 레벨의 데이터
        self.map_data = import_csv_layout(level_data['map'])  # 지도(2차원 리스트)
        self.new_max_level = level_data['unlock']  # 이 레벨을 클리어 시 열리는 레벨

        self.create_level = create_level  # 레벨 시작 함수(부활시 사용)
        self.create_levelselect = create_levelselect  # 레벨 선택 시작 함수(승리시 사용)
        self.world_shift = 0  # 플레이어가 고정되어 있고 타일이 움직이게 할 때 사용하는 변수

        self.deathcount = 0  # 죽은 횟수
        self.alive = False  # 부활 화면 실행 여부 판단
        self.counter = 60  # 부활 화면 기능 실행용 카운터
        self.starttime = 0  # 레벨 시작 시간

        self.setup_level(self.map_data)  # 지도 데이터를 이용해 스프라이트들을 생성

    def setup_level(self, layout):
        """
        주어진 2차원 맵 데이터를 이용해 스프라이트들의 그룹에 스프라이트를 추가한다

        :param layout:list[list[int]]
        :return:
        """
        tile_img_dict = import_imagedict('../graphics/tile')  # 이미지를 dict의 형태로 받아옴
        self.tiles = pygame.sprite.Group() # 바닥 타일 그룹
        self.player = pygame.sprite.GroupSingle()  # 플레이어 싱글 그룹
        self.goal = pygame.sprite.GroupSingle()  # 골인 지점 싱글 그룹
        self.thorns = pygame.sprite.Group()  # 가시 그룹
        self.checkpoints = pygame.sprite.Group()  # 체크포인트 그룹
        self.enemys = pygame.sprite.Group()  # 적 그룹
        self.mysteryblocks = pygame.sprite.Group()  # 랜덤박스 그룹
        # 2차원 리스트를 훑으면서 리스트의 값에 따라 그룹에 해당하는 좌표의 타일 추가하기
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                # 땅
                if cell == '4':
                    tile = Tile((x, y), tile_size, tile_img_dict['ground.png'])
                    self.tiles.add(tile)

                # 땅 위의 잔디
                if cell == '7':
                    tile = Tile((x, y), tile_size, tile_img_dict['topground.png'])
                    self.tiles.add(tile)

                # 플레이어 초기시작 위치
                if cell == '10':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                    self.checkpoint = (x, y)
                    self.startx = x

                # 가시
                if cell == '6':
                    sprite = Tile((x, y), tile_size, tile_img_dict['spike.png'])
                    self.thorns.add(sprite)

                # 골인점
                if cell == '3':
                    sprite = Tile((x, y), tile_size, tile_img_dict['goal.png'])
                    self.goal.add(sprite)

                # 체크포인트
                if cell == '0':
                    sprite = CheckpointTile((x, y), tile_size, tile_img_dict['checkpoint.png'])
                    self.checkpoints.add(sprite)

                # 적
                if cell == '12':
                    sprite = Enemy((x, y), tile_size, tile_img_dict['enemy'], -4)
                    self.enemys.add(sprite)

                # 랜덤박스(미완성)
                if cell == '1234':
                    sprite = Enemy((x,y),tile_size,tile_img_dict['mysterybox'])
                    self.MysteryBlock.add(sprite)

    def scroll_x(self):
        """화면의 위치에 따라  플레이어를 움직일 것인지 화면을 움직일 것인지 결정"""
        playerx = self.player.sprite
        player_x = playerx.rect.centerx
        direction_x = playerx.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            playerx.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            playerx.speed = 0
        else:
            self.world_shift = 0
            playerx.speed = 8

    def horizental_movement_collision(self):
        """플레이어의 좌우이동과 충돌 판정"""
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # 바닥 타일의 그룹들 과 플레이어의 충돌을 판정하고 위치를 바꾼다
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def enemy_horizental_update(self):
        """enemy의 좌우이동"""
        for enemy in self.enemys.sprites():
            enemy.rect.x += enemy.direction.x
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        enemy.direction.x *= -1
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                        enemy.direction.x *= -1

    def enemy_vertical_update(self):
        """enemy의 상하 이동 판정"""
        for enemy in self.enemys.sprites():
            enemy.apply_gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0

    def vertical_movement_collision(self):
        """플레이어의 상하 이동과 충돌 판정"""
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        # 랜덤 블록(개발중)
        for sprite in self.mysteryblocks.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    sprite.index = 1

    def check_win(self):
        """골인 지점 도달 체크"""
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.time = pygame.time.get_ticks()
            print("level", self.current_level, "time: ", self.time - self.starttime)
            print("time:", self.time)
            print("start_time:",self.starttime)
            levels[self.current_level]['scoreboard'].append(self.time - self.starttime)
            self.create_levelselect(self.new_max_level)

    def check_checkpoint(self):
        """체크리스트 갱신"""
        checklist = pygame.sprite.spritecollide(self.player.sprite, self.checkpoints, False)
        if checklist:
            self.checkpoint = (checklist[0].pos[0], checklist[0].pos[1])

    def check_die(self):
        """가시, 적으로 죽는 것 체크"""
        if pygame.sprite.spritecollide(self.player.sprite, self.thorns, False):
            self.kill_player()
        if pygame.sprite.spritecollide(self.player.sprite, self.enemys, False):
            self.kill_player()

    def check_fall(self):
        """떨어져 죽는 것 체크"""
        if self.player.sprite.check_death():
            self.kill_player()

    def kill_player(self):
        """플레이어 죽이고 레벨 리셋"""
        self.deathcount += 1
        self.alive = False
        print(self.deathcount)
        self.create_level(self.current_level, self.checkpoint, self.deathcount)  # 체크포인트 이용해 레벨 재생성

    def startscreen(self):
        """부활 시에 보이는 화면"""
        if self.counter >= 0:
            self.display_surface.fill('black')
        elif self.counter <= 0:
            self.alive = True

        text1 = font.render(f'x{3-self.deathcount}',False,'white')  # 데스카운트 표시
        text2 = font.render(f'Level {self.current_level+1}',False,'white')  # 레벨 표시
        text2_rect = text2.get_rect(center=(screen_width / 2, screen_height / 2-50))  # 텍스트 중앙정렬용 직사각형
        a = self.player.sprite.image.get_rect()  # 플레이어 이미지 가져오기
        a.topright = (screen_width/2-30,screen_height-285) # 플레이어 이미지 배치
        self.display_surface.blit(self.player.sprite.image, a)
        self.display_surface.blit(text1, (screen_width/2-10, screen_height-300))
        self.display_surface.blit(text2, text2_rect)

        self.counter -= 1

    def updatetile(self, world_shift):
        """
        타일 위치 업데이트

        :param world_shift:int
        :return: None
        """
        self.goal.update(world_shift)
        self.tiles.update(world_shift)
        self.checkpoints.update(world_shift)
        self.thorns.update(world_shift)
        self.enemys.update(world_shift)

    def run(self):
        """레벨 실행"""
        if self.alive:
            self.scroll_x()
            self.player.sprite.update()
            self.updatetile(self.world_shift)
            self.horizental_movement_collision()
            self.enemy_horizental_update()
            self.enemy_vertical_update()

            self.check_checkpoint()
            self.check_die()
            self.check_fall()
            self.check_win()
            self.vertical_movement_collision()

            self.goal.draw(self.display_surface)
            self.tiles.draw(self.display_surface)
            self.thorns.draw(self.display_surface)
            self.checkpoints.draw(self.display_surface)
            self.player.draw(self.display_surface)
            self.enemys.draw(self.display_surface)
        else:
            self.startscreen()
            self.vertical_movement_collision()
