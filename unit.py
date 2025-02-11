# coding: UTF-8
from pygame import sprite, time, Surface
import copy
from const import const
from const.direction import Direction

class Unit(sprite.Sprite):
    '''画面ユニットのクラス。'''
    def __init__(self, image:Surface, x:int, y:int, name:str, isPassable:bool, eventlist:list=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.map_x, self.map_y = x, y
        self.rect.x, self.rect.y = (x * const.MAP_UNIT_SIZE_X), (y * const.MAP_UNIT_SIZE_Y)
        self.name = name
        self.isPassable = isPassable
        self.eventlist = eventlist
    
    def isAbove(self, other):
        '''自分が相手よりも高いかどうかを判定する。
        :param other: 判定する相手ユニット。
        :rtype: bool'''
        return (self.rect.y + self.rect.h - 1) < other.rect.y
    
    def isBelow(self, other):
        '''自分が相手よりも低いかどうかを判定する。
        :param other: 判定する相手ユニット。
        :rtype: bool'''
        return self.rect.y > (other.rect.y + other.rect.h - 1)
    
    def isLeftTo(self, other):
        '''自分が相手よりも左にいるかどうかを判定する。
        :param other: 判定する相手ユニット。
        :rtype: bool'''
        return (self.rect.x + self.rect.w - 1) < other.rect.x
    
    def isRightTo(self, other):
        '''自分が相手よりも右にいるかどうかを判定する。
        :param other: 判定する相手ユニット。
        :rtype: bool'''
        return self.rect.x > (other.rect.x + other.rect.h - 1)
    
    def isTouching(self, other):
        '''自分が相手と接触しているかどうかを判定する。
        :param other: 判定する相手ユニット。
        :rtype: bool'''
        return (    not self.isAbove(other)
                and not self.isBelow(other)
                and not self.isLeftTo(other)
                and not self.isRightTo(other)
        )
    
    def start(self):
        if self.eventlist is None:
            return False
        self.tempEventlist = copy.copy(self.eventlist)

    def next(self):
        if len(self.tempEventlist) < 1:
            return None
        return self.tempEventlist.pop(0)

class AnimationUnit(Unit):
    '''アニメーションするユニットのクラス。'''
    def __init__(self, images:list[Surface], x:int, y:int, name:str, isPassable:bool, eventlist:list, direction:Direction, animation:bool=False):
        self.images = images
        super().__init__(images[0], x, y, name, isPassable, eventlist)
        self.direction = direction
        self.animation = animation
    
    def update(self):
        '''ユニットをアニメーションする。
        :rtype: None'''
        if not self.animation:
            return
        t = time.get_ticks() # 経過時間
        i = t // 500 % 3 + (self.direction * 3) # 足踏み
        self.image = self.images[i]
