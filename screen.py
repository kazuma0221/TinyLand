# coding: UTF-8
import pygame
from pygame.mixer import music
from pygame.locals import *

from const import const #, soundname
from const.direction import Direction
from controller import ControllerManager
from window import Window
import map
# from sound import sound

class Screen:

    def __init__(self):
        '''初期化と画面作成。'''
        pygame.init()
        self.disp_x, self.disp_y = (const.DISPLAY_UNITS_X * const.MAP_UNIT_SIZE_X), (const.DISPLAY_UNITS_Y * const.MAP_UNIT_SIZE_Y)
        self.screen = pygame.display.set_mode((self.disp_x, self.disp_y))
        # self.sounds_dic = sound.prepareSound()
        self.CM = ControllerManager()

        # スプライトグループへの初期登録
        self.mapdata = map.makeMap(const.MAP_FILES[0])
        self.sprites = map.putMapIntoSpritesList(self.mapdata, 0)
        self.sprite_all = pygame.sprite.RenderUpdates()

        # メッセージの初期処理：枠を読み込んで透明にし、文字列のSurfaceを初期化する
        self.message_window = Window(pygame.image.load(const.PATH_IMAGE + const.MESSAGE_BACK_FILE),
                                     x=const.MESSAGE_WIN_X,
                                     y=const.MESSAGE_WIN_Y)
        self.message_window.image.set_alpha(0)
        self.strSurface = None

        # 制御変数
        self.processing = False
        self.eventUnit = None

    def confirmButton(self, event)->bool:
        '''決定ボタンが押されたかどうかの判定。'''
        # スペースキー入力
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True
        # コントローラのAボタン
        if self.CM.getButtonA():
            return True
        return False

    def getDirection(self, pressed, tilted)->Direction:
        '''方向キー判定。tilted[0]はコントローラ左スティックのX軸変化量、[1]はY軸変化量。'''
        if pressed[pygame.K_LEFT] or (tilted is not None and tilted[0] < -5000):
            return Direction.LEFT
        elif pressed[pygame.K_RIGHT] or (tilted is not None and tilted[0] > 5000):
            return Direction.RIGHT
        elif pressed[pygame.K_DOWN] or (tilted is not None and tilted[1] < -5000):
            return Direction.DOWN
        elif pressed[pygame.K_UP] or (tilted is not None and tilted[1] > 5000):
            return Direction.UP
        return None

    def startingDraw(self):
        '''ループ冒頭の描画処理。'''
        pygame.display.update()
        self.screen.fill(pygame.Color(const.COLOR_SKYBLUE))
    
    def updateScreen(self):
        '''画面更新。スプライトを描画し、画面フリップする。'''
        # メッセージ枠
        self.sprites.append(self.message_window)
        # 全ユニットのスプライト
        if not self.processing:
            self.sprite_all.empty()
            for unit in self.sprites:
                unit.add(self.sprite_all)
        self.sprite_all.update()
        self.sprite_all.draw(self.screen)
        # メッセージがあればテキストを表示、なければ空にする
        if self.strSurface is not None:
            self.screen.blit(self.strSurface, (const.MESSAGE_START_X, const.MESSAGE_START_Y))
        else:
            empty_surface = pygame.surface.Surface(size=(self.disp_x, const.MESSAGE_WIN_HEIGHT))
            empty_surface.set_alpha(0)
            self.screen.blit(empty_surface, (0, const.MESSAGE_WIN_HEIGHT))
        # フリップ
        pygame.display.flip()

    def playMusic(self, name:str):
        '''曲が演奏中でなければ、指定した曲を再生する。'''
        if music.get_busy():
            return
        music.load('music/' + name)
        music.play()
    
    def showMessageWindow(self):
        self.message_window.image.set_alpha(255)

    def hideMessageWindow(self):
        self.strSurface = None
        self.message_window.image.set_alpha(0)

    def main(self):
        '''メインルーチン。'''
        running = True
        while running:
            self.startingDraw()
            # イベント
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False # 終了
            self.updateScreen()
        self.quit()

    def quit(self):
        '''ゲーム終了時の処理。'''
        music.stop()
        pygame.quit()

if __name__ == "__main__":
    Screen().main()