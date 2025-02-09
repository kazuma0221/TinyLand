# coding: UTF-8
from pygame import sprite, Surface

class Window(sprite.Sprite):
    '''ウィンドウのクラス。'''
    def __init__(self, image:Surface, x:int, y:int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y