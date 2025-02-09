# coding: UTF-8
from pygame import font

class Event:
    '''マップイベントの親クラス。'''
    pass

class MessageEvent(Event):
    '''メッセージ表示用のマップイベント。'''
    def __init__(self, message):
        font.init()
        self.font = font.SysFont(name='Noto Sans CJK JP', size=30)
        self.message = message
        self.strSurface = None
    
    def do(self):
        # 文字列のSurfaceを作る
        self.strSurface = self.font.render(self.message, True, (255, 255, 255))
        return self

class TurnEvent(Event):
    '''方向転換用のマップイベント。'''
    def do(self, unit, direction):
        unit.direction = direction
        return self

class CloseEvent(Event):
    '''マップイベントの終了用。'''
    def __init__(self):
        pass
    def do(self):
        return self