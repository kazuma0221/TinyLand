# coding: UTF-8
import numpy as np
import csv, random
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

import ev
from unit import Unit
from chara import Chara
from util import pngutil
from const import const
from const.direction import Direction

class UnitFactory():
    '''ユニット画像を登録しておき、make()で番号に応じたユニットを作成する。'''

    # シングルトン定義
    instance = None
    def __new__(self):
        '''ユニットの画像ファイルを分割読み込みし、リストに格納する。
        :param str filename: ファイル名。imageフォルダ配下のみを対象とするためパス不要。
        '''
        if self.instance is None:
            self.instance = super().__new__(self)
        self.imageList = pngutil.load_chip(
            const.DIR_IMAGE + const.TILE_FILE,
            is_alpha=True,
            unit_width=const.MAP_UNIT_SIZE_X,
            unit_height=const.MAP_UNIT_SIZE_Y)
        return self.instance
    
    def make(self, num:int, x:int, y:int):
        '''指定の(x, y)に、numで指定した番号のユニットを生成して返す。
        :param int num: ユニットの番号。
        :param int x: 画面上のx座標マス数。
        :param int y: 画面上のy座標マス数。
        '''
        name = f'[{const.BLOCK_NAME_DICT[num]} ({x}, {y})]'
        unit = Unit(self.imageList[num], x, y, name, (num in const.PASSABLE_BLOCK_LIST))
        return unit

def makeChara(filename:str, x:int, y:int, width:int=const.CHARA_SIZE_X, height:int=const.CHARA_SIZE_Y,
              isPassable:bool=False, direction:Direction=Direction.DOWN, name:str=None,
              eventlist:list=None):
    '''指定の(x, y)に、サイズを(width, height)で指定した、ファイルのnum番目のキャラを生成して返す。
    :param str filename: ファイル名。imageフォルダ配下のみを対象とするためパス不要。
    :param int x: 表示するx座標。
    :param int y: 表示するy座標。
    :param int width: キャラ画像の幅。
    :param int height: キャラ画像の高さ。
    :param bool canJump: キャラのデフォルトでのジャンプ可否。
    :param Direction direction: キャラの向き。
    :param list eventlist: 実行するEventのリスト。
    '''
    chara = Chara(pngutil.load_chip(const.DIR_IMAGE + filename,
                                    is_alpha=True,
                                    unit_width=width,
                                    unit_height=height),
                  x, y, name, isPassable, eventlist, direction)
    return chara

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
        search_left = chara_left - const.MAP_UNIT_SIZE_X
        search_right = chara_right
        search_top, search_bottom = chara_top, chara_bottom
    elif chara.direction == Direction.RIGHT:
        search_left = chara_left
        search_right = chara_right + const.MAP_UNIT_SIZE_X
        search_top, search_bottom = chara_top, chara_bottom
    elif chara.direction == Direction.UP:
        search_left, search_right = chara_left, chara_right
        search_top = chara_top - const.MAP_UNIT_SIZE_Y
        search_bottom = chara_bottom
    elif chara.direction == Direction.DOWN:
        search_top = chara_top
        search_bottom = chara_bottom + const.MAP_UNIT_SIZE_Y
        search_left, search_right = chara_left, chara_right
    polygon = Polygon([[(search_left, search_top), (search_right, search_top), (search_right, search_bottom), (search_left, search_bottom)]])
    
    # ユニットを総当たりし、探索範囲内で最も近いものを選ぶ
    closestUnit = None
    distance = const.CHARA_SIZE_X * 2
    for unit in mapdata.map:
        # イベントがなければ飛ばす
        if unit.eventlist is None:
            continue
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
        else:
            new_distance = np.linalg.norm(chara_center_array - unit_center_array)
            if new_distance < distance:
                closestUnit = unit
                distance = new_distance
    
    # 最も近いユニットを返す
    return closestUnit

def makeTestNPC(x:int, y:int, filename:str=const.CHARA_FILE_PLAYER, direction:Direction=Direction.DOWN, message:str=u'これはテストです。'):
    return makeChara(filename=filename, x=x, y=y, name='テストNPC', direction=direction,
                     eventlist=[ev.TurnEvent(), ev.MessageEvent(message), ev.CloseEvent()])

def readNPC(mapdata):
    # NPCのデータファイルから、mapdataのidに一致するデータに限り、各NPCを辞書として持つリストを読み込む。
    # 戻り値はCharaのリストとして返す。
    NPCFilePath = const.DIR_MAP + const.NPC_FILE
    with open(NPCFilePath, encoding='UTF-8', mode='r') as f:
        NPCs = [line for line in csv.DictReader(f, delimiter='\t') if line['mapid'] == mapdata.id]
    
    # 当該マップのNPCを順に生成する
    # TODO: NPCの向きをtsvファイルのdirectionから読めるようにする→ファイルに整数値をもたせる？
    return [makeTestNPC(x=int(npc['x']), y=int(npc['y']),
                     filename='chara_'+npc['graphic']+'.png',
                     direction=random.randint(0, 3),
                     message=npc['message']) for npc in NPCs]