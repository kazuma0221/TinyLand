# coding: UTF-8
import copy, csv
from dataclasses import dataclass

from const import const
from util import unitutil
from unit import Unit

@dataclass
class MapData:
    map: list[Unit] # Unitの1次元リスト。2次元ではないので注意
    width: int
    height: int

def makeMap(mapfile) -> MapData:
    '''mapディレクトリ内の指定ファイルからMapDataを作成する。
    :param mapfile: 読み込むマップのTSVファイル名。
    :param tilefile: 読み込むタイルの画像ファイル名。
    :rtype: MapData'''

    # ファイル読込
    filepath = 'map/' + mapfile
    with open(filepath, encoding='UTF-8', mode='r') as f:
        map = [line for line in csv.reader(f, delimiter='\t')]
    
    # 幅と高さを取得
    map_width = max([len(line) for line in map])
    map_height = len(map)

    # マップファイルの内容を1マスずつ処理
    mapList = []
    factory = unitutil.UnitFactory()
    for y, line in enumerate(map):
        mapList.extend([
            factory.make(int(unit), x, y)
            for x, unit in enumerate(line)
            if unit != const.MAP_EMPTY])
    return MapData(mapList, map_width, map_height)

def putMapIntoSpritesList(mapData, start_x):
    WholeMap = copy.copy(mapData.map)
    sprites = []
    for unit in WholeMap:
        if (unit.map_x < (start_x - 2)) or (unit.map_x > (start_x + const.DISPLAY_UNITS_X)):
            continue
        sprites.append(unit)
    return sprites

if __name__ == '__main__':
    # テスト用画面とマップデータを作成
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((const.DISPLAY_UNITS_X * const.MAP_UNIT_SIZE_X,
                                    const.DISPLAY_UNITS_Y * const.MAP_UNIT_SIZE_Y))
    mapdata = makeMap(const.MAP_FILES[0])
    print(f'Map size = ({mapdata.width}, {mapdata.height})')

    # スプライトグループを新規作成し、マップのスプライトをグループに登録する
    sprite_all = pygame.sprite.RenderUpdates()
    for unit in mapdata.map:
        unit.add(sprite_all)
    
    # ループ
    running = True
    while running:
        # 画面更新
        pygame.display.update()
        # イベント制御
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # スプライトの更新
        sprite_all.update()
        sprite_all.draw(screen)
        pygame.display.flip()
    pygame.quit()
