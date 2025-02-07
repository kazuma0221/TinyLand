# coding: UTF-8
from pygame import sprite

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
            const.PATH_IMAGE + const.TILE_FILE,
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

def makeSprites(units:list):
    '''リストで渡されたスプライトを、描画更新用のスプライトグループに登録する。
    :param list[Unit] units: 描画する全スプライト（ユニット）のリスト。
    :rtype: None'''
    sprite_all = sprite.RenderUpdates()
    for unit in units:
        unit.add(sprite_all)
    return sprite_all

def makeChara(filename:str, num:int, x:int, y:int, width:int, height:int, isPassable:bool, direction:Direction=Direction.DOWN, name:str=None):
    '''指定の(x, y)に、サイズを(width, height)で指定した、ファイルのnum番目のキャラを生成して返す。
    :param str filename: ファイル名。imageフォルダ配下のみを対象とするためパス不要。
    :param int num: 画像内でどのキャラを表示するかのインデックス。
    :param int x: 表示するx座標。
    :param int y: 表示するy座標。
    :param int width: キャラ画像の幅。
    :param int height: キャラ画像の高さ。
    :param bool canJump: キャラのデフォルトでのジャンプ可否。
    :param Direction direction: キャラの向き。
    '''
    chara = Chara(pngutil.load_chip(const.PATH_IMAGE + filename,
                                    is_alpha=True,
                                    unit_width=width,
                                    unit_height=height),
                  num, x, y, name, isPassable, direction)
    return chara
