# coding: UTF-8
import pygame
from pygame.locals import *

from const import const
import map
from util import unitutil
from screen import Screen

class App(Screen):

    def __init__(self):
        '''初期化と画面作成。'''
        super().__init__()
        self.Player = unitutil.makeChara(filename=const.CHARA_FILE, num=0,
                                         x=const.START_X, y=const.START_Y,
                                         width=const.CHARA_SIZE_X, height=const.CHARA_SIZE_Y,
                                         isPassable=False, name=const.PLAYER_NAME)

    def updateScreen(self):
        '''画面更新。キャラ位置に対して必要なスプライトを描画する。'''
        start_x = 0
        self.sprites = map.putMapIntoSpritesList(self.mapdata, start_x)
        self.sprites.append(self.Player)
        super().updateScreen()

    def main(self):
        '''メインルーチン'''
        running = True
        while running:
            self.playMusic('village.mid')
            self.startingDraw()
            # イベント
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False # 終了
                if self.confirmButton(event):
                    pass
            # 移動
            direction = self.getDirection(pygame.key.get_pressed(), self.CM.getLeftStick())
            if direction is not None:
                self.Player.walk(self.mapdata, direction)
            self.updateScreen()
        self.quit()

if __name__ == "__main__":
    App().main()