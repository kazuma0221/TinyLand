# coding: UTF-8

class Event:
    '''マップイベントの親クラス。'''
    pass

class MessageEvent(Event):
    '''メッセージ表示用のマップイベント。'''
    def __init__(self, message):
        self.message = message
    
    def do(self):
        print(self.message)
        return self

class CloseEvent(Event):
    '''マップイベントの終了用。'''
    def __init__(self):
        pass
    def do(self):
        return self