# coding: UTF-8
import pygame
from pygame.locals import *

from const import const
import ev, map
from util import unitutil
from screen import Screen

class App(Screen):

    def __init__(self):
        '''初期化と画面作成。'''
        super().__init__()
        self.testNPC = unitutil.makeChara(filename=const.CHARA_FILE, num=0,
                                         x=5, y=6,
                                         width=const.CHARA_SIZE_X, height=const.CHARA_SIZE_Y,
                                         isPassable=False, name='テストNPC',
                                         eventlist=[ev.MessageEvent('これはテストです。'), ev.CloseEvent()])

        self.mapdata.map.append(self.testNPC)
        self.Player = unitutil.makeChara(filename=const.CHARA_FILE, num=0,
                                         x=const.START_X, y=const.START_Y,
                                         width=const.CHARA_SIZE_X, height=const.CHARA_SIZE_Y,
                                         isPassable=False, name=const.PLAYER_NAME,
                                         eventlist=None)
        
    def updateScreen(self):
        '''画面更新。キャラ位置に対して必要なスプライトを描画する。'''
        start_x = 0
        self.sprites = map.putMapIntoSpritesList(self.mapdata, start_x)
        self.sprites.append(self.Player)
        super().updateScreen()

    def main(self):
        '''メインルーチン'''
        # 制御変数
        running = True
        processing = False
        eventUnit = None
        print(self.testNPC.eventlist)

        # ループ
        while running:
            self.playMusic('village.mid')
            self.startingDraw()
            # イベント
            for event in pygame.event.get():
                # 終了
                if event.type == pygame.QUIT:
                    running = False
                # 決定キー
                if self.confirmButton(event):
                    if not processing:
                        eventUnit = ev.search(self.Player, self.mapdata)
                        if eventUnit is not None:
                            processing = eventUnit.start()
                    else:
                        processing = eventUnit.next()
            
            # イベント処理中でなければ移動
            if not processing:
                direction = self.getDirection(pygame.key.get_pressed(), self.CM.getLeftStick())
                if direction is not None:
                    self.Player.walk(self.mapdata, direction)
            self.updateScreen()
        self.quit()

if __name__ == "__main__":
    App().main()