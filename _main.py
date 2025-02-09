# coding: UTF-8
import pygame
from pygame.locals import *

from const import const
from const.direction import Direction
import ev, map
from util import unitutil
from screen import Screen

class App(Screen):

    def __init__(self):
        '''初期化と画面作成。'''
        super().__init__()
        self.mapdata.map.append(unitutil.makeTestNPC(x=5, y=6, message=u'鉱山には　オバケが　出るんです。こわいなあ。'))
        self.mapdata.map.append(unitutil.makeTestNPC(x=10, y=14, direction=Direction.LEFT, message=u'武器屋なら　ここから　東ですよ。'))
        self.Player = unitutil.makeChara(filename=const.CHARA_FILE, num=0,
                                         x=const.START_X, y=const.START_Y, name=const.PLAYER_NAME,
                                         eventlist=None)
        
    def updateScreen(self):
        '''画面更新。キャラ位置に対して必要なスプライトを描画する。'''
        start_x = 0
        self.sprites = map.putMapIntoSpritesList(self.mapdata, start_x)
        self.sprites.append(self.Player)
        super().updateScreen()

    def checkMapEvent(self):
        # イベント処理中でなければ、イベントユニットを検索し、なければ戻る
        if not self.processing:
            self.eventUnit = unitutil.search(self.Player, self.mapdata)
            if self.eventUnit is None:
                return False
            # イベントユニットがあれば、開始処理を行って次に行く
            self.eventUnit.start()
        
        # 次のイベントを取得し、タイプに応じて切り分け
        next = self.eventUnit.next()
        if type(next) is ev.CloseEvent:
            self.hideMessageWindow()
            self.processing = False
            return
        if type(next) is ev.MessageEvent:
            self.showMessageWindow()
            self.strSurface = next.do().strSurface
        if type(next) is ev.TurnEvent:
            next.do(self.eventUnit, self.Player.direction.reverse())
        self.processing = True
    
    def main(self):
        '''メインルーチン'''
        running = True
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
                    self.checkMapEvent()
            # イベント処理中でなければ移動
            if not self.processing:
                direction = self.getDirection(pygame.key.get_pressed(), self.CM.getLeftStick())
                if direction is not None:
                    self.Player.walk(self.mapdata, direction)
            self.updateScreen()
        self.quit()

if __name__ == "__main__":
    App().main()