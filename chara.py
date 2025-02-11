# coding: UTF-8
from pygame import mixer, Surface

from const import const
from const.direction import Direction
import move, unit

class Chara(unit.AnimationUnit):
    '''キャラクタのクラス。AnimationUnitに自分の動きを追加している。'''
    def __init__(self, images:list[Surface], x:int, y:int, name:str, isPassable:bool, eventlist:list=None, direction:Direction=Direction.DOWN):
        super().__init__(images, x, y, name, isPassable, eventlist, direction, animation=True)
    
    def getMapX_inGrid(self):
        return int(self.map_x / const.MAP_UNIT_SIZE_X)

    def getMapY_inGrid(self):
        return int(self.map_y / const.MAP_UNIT_SIZE_Y)

    def walk(self, mapdata, direction:Direction):
        '''キャラが歩く。
        :param MapData mapdata: 当たり判定の対象とするマップデータ。
        :param Direction direction: 歩く方向。
        :rtype: None'''
        self.direction = direction
        move.walk(self, mapdata)
    
    def isPushing(self, unit:unit.Unit):
        '''キャラがユニットに接触しているとき、そのユニットを押しているかどうか（＝移動可否）を判定する。
        :param Unit unit: 処理する対象のユニット。
        :returns: 押していればTrue、押していなければFalseを返す。
        :rtype: bool'''
        return move.isPushing(self, unit)
