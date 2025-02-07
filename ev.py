# coding: UTF-8
import numpy as np
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature
from const import const
from const.direction import Direction
'''ゲームイベントを制御するモジュール。'''

def search(chara, mapdata):
    '''キャラの向いている方向にある、近くのイベントありユニットを探して返す。複数あれば近い方を優先する。
    :param Chara chara: 動かすキャラ。
    :param MapData mapdata: 探すマップデータ。
    :returns: 最も近いイベントありのUnitを返す。なければNoneを返す。
    :rtype: Unit'''
    # キャラの座標
    chara_left, chara_right = chara.rect.x, (chara.rect.x + chara.rect.w - 1)
    chara_top, chara_bottom = chara.rect.y, (chara.rect.y + chara.rect.h - 1)
    chara_center = (chara.rect.x + int(chara.rect.w / 2), chara.rect.y + int(chara.rect.h / 2))
    # print(f'Chara: ({chara_left}, {chara_top}), ({chara_right}, {chara_bottom})')

    # 向きに応じて探索範囲を設定する
    search_left, search_right = 0, (mapdata.width * const.MAP_UNIT_SIZE_X - 1)
    search_top, search_bottom = 0, (mapdata.height * const.MAP_UNIT_SIZE_Y - 1)
    if chara.direction == Direction.LEFT:
        search_left = chara_left + const.MAP_UNIT_SIZE_X
        search_right = chara_right
        search_top, search_bottom = chara_top, chara_bottom
    elif chara.direction == Direction.RIGHT:
        search_left = chara_left
        search_right = chara_right + const.MAP_UNIT_SIZE_X
        search_top, search_bottom = chara_top, chara_bottom
    elif chara.direction == Direction.UP:
        search_left, search_right = chara_left, chara_right
        search_top = chara_top + const.MAP_UNIT_SIZE_Y
        search_bottom = chara_bottom
    elif chara.direction == Direction.DOWN:
        search_top = chara_top
        search_bottom = chara_bottom + const.MAP_UNIT_SIZE_Y
        search_left, search_right = chara_left, chara_right
    polygon = Polygon([[(search_left, search_top), (search_right, search_top), (search_left, search_bottom), (search_right, search_bottom)]])
    
    # ユニットを総当たりし、探索範囲内で最も近いものを選ぶ
    closestUnit = None
    distance = const.CHARA_SIZE_X * 2
    for unit in mapdata.map:
        # ユニットが触っていなければ飛ばす
        if not chara.isTouching(unit):
            continue
        # ユニットの中心座標が探索範囲外であれば飛ばす
        unit_center = ((unit.rect.x + int(unit.rect.w / 2)), (unit.rect.y + int(unit.rect.h / 2)))
        if not boolean_point_in_polygon(Feature(geometry=Point(unit_center)), polygon):
            continue
        # ユニットが範囲に引っかかっていれば、距離を計算してユニットを保存
        chara_center_array = np.array(list(chara_center))
        unit_center_array = np.array(list(unit_center))
        if closestUnit is None:
            closestUnit = unit
            distance = np.linalg.norm(chara_center_array - unit_center_array)
            print(closestUnit)
        else:
            new_distance = np.linalg.norm(chara_center_array - unit_center_array)
            if new_distance < distance:
                closestUnit = unit
                distance = new_distance
    
    # 最も近いユニットを返す
    return closestUnit

class Event:
    pass

class MessageEvent(Event):
    def __init__(self, message):
        self.message = message
    def do(self):
        print(self.message)

class CloseEvent(Event):
    def __init__(self):
        pass
    def do(self):
        pass