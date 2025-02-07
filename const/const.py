# coding: UTF-8
'''定数定義'''

# 画面・画像
DISPLAY_UNITS_X, DISPLAY_UNITS_Y = 21, 21    # 画面の大きさをマス数で定義
PATH_IMAGE = 'image/'
CHARA_FILE = 'Player.png'
MAP_FILES = ['map_test.txt']
TILE_FILE = 'tiles_01.png'
COLOR_SKYBLUE = (120, 120, 255)

# 音声
PATH_SOUND = 'sound/'

# メッセージ用
MESSAGE_BACK_FILE = 'message_window_back.png'

# マップ用
MAP_UNIT_SIZE_X, MAP_UNIT_SIZE_Y, MAP_MOVE_AMOUNT = 32, 32, 1
MAP_EMPTY = '0'
MAP_BLOCK = '103'
BLOCK_NAME_DICT = {16:'Grass', 21:'Water'}
PASSABLE_BLOCK_LIST = [16]

# キャラクタ制御
CHARA_SIZE_X, CHARA_SIZE_Y = 32, 32 # キャラクタのサイズ
START_X, START_Y = 10, 10 # 主人公の基準位置
PLAYER_NAME = 'Player'
SIDE_MOVE_AMOUNT = 2