# coding: UTF-8
from const import const
from const.direction import Direction
'''Charaクラスの動きを制御するモジュール。
引数charaとmapは、循環参照を防ぐため型指定はない。'''

def isPushing(chara, unit) -> bool:
    '''キャラが他ユニットに接触しているとき、そのユニットを押しているかどうか（＝移動可否）を判定する。
    当たっている辺の長さを計算し、キャラの向きに対応する辺が当たっていたら押しており（移動不可）、Trueとする。
    :param Chara chara: 動かすキャラ。
    :param Unit unit: 判定対象のユニット。
    :returns: 当たりに行っていたらTrue、いなかったらFalseを返す。
    :rtype: bool'''
    # 辺の座標の事前計算
    chara_left, chara_right = chara.rect.x, (chara.rect.x + chara.rect.w - 1)
    chara_top, chara_bottom = chara.rect.y, (chara.rect.y + chara.rect.h - 1)
    unit_left, unit_right = unit.rect.x, (unit.rect.x + unit.rect.w - 1)
    unit_top, unit_bottom = unit.rect.y, (unit.rect.y + unit.rect.h - 1)
    # print(f'Chara: ({chara_left}, {chara_top}), ({chara_right}, {chara_bottom})')
    # print(f'Unit: ({unit_left}, {unit_top}), ({unit_right}, {unit_bottom})')

    horizontal_touch, vertical_touch = -1, -1
    directions = [direction for direction in Direction]
    # 当たっている長さ（上下の辺）：左,x
    if unit_left <= chara_left <= unit_right:
        horizontal_touch = unit_right - chara_left
        directions.remove(Direction.RIGHT)
    # 当たっている長さ（上下の辺）：右,x
    elif unit_left <= chara_right <= unit_right:
        horizontal_touch = chara_right - unit_left
        directions.remove(Direction.LEFT)
    # 当たっている長さ（側面の辺）：上,y
    if unit_top <= chara_top <= unit_bottom:
        vertical_touch = unit_bottom - chara_top
        directions.remove(Direction.DOWN)
    # 当たっている長さ（側面の辺）：下,y
    elif unit_top <= chara_bottom <= unit_bottom:
        vertical_touch = chara_bottom - unit_top
        directions.remove(Direction.UP)
    
    # ユニットがキャラに完全に入っていたら、移動不可
    if (horizontal_touch >= unit.rect.w) and (vertical_touch >= unit.rect.h):
        return False
    
    # キャラの左右が当たる
    if (chara.direction in directions) and \
       (chara.direction in [Direction.LEFT, Direction.RIGHT]) and \
       (vertical_touch > horizontal_touch >= 0):
        return True
    # キャラの上下が当たる
    elif (chara.direction in directions) and \
         (chara.direction in [Direction.UP, Direction.DOWN]) and \
         (horizontal_touch > vertical_touch >= 0):
        return True
    else:
        # 移動なし（このパス通る？）
        return False

def walk(chara, mapdata):
    '''キャラを歩かせる。
    :param Chara chara: 動かすキャラ。
    :param MapData mapdata: 当たり判定の対象とするマップデータ。
    :param Direction direction: 歩く方向。
    :rtype: None'''
    # 接触している移動不可ユニットに向かっては移動できない
    for unit in mapdata.map:
        if not unit.isPassable and chara.isTouching(unit):
            # print(f'{chara.name} is touching {unit.name}')
            if chara.isPushing(unit):
                return
    # 移動量の計算
    direction = chara.direction
    offset_x = int(const.MAP_MOVE_AMOUNT * (direction - 1)) if (direction % 2 == 0) else 0
    offset_y = int(const.MAP_MOVE_AMOUNT * (direction - 2) * -1) if (direction % 2 == 1) else 0
    # print(f'offset: ({offset_x}, {offset_y})')
    # 普通のキャラの場合、単純に1マス動かす
    if chara.name != const.PLAYER_NAME:
        chara.rect.x += offset_x
        chara.rect.y += offset_y
        return
    # 主人公の場合、背景を逆方向に動かして、キャラの移動量と連動させる
    for unit in mapdata.map:
        unit.rect.x -= offset_x
        unit.rect.y -= offset_y
    chara.map_x += offset_x
    chara.map_y += offset_y