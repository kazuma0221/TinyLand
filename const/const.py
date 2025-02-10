# coding: UTF-8
'''定数定義'''

# 画面・画像全般
DISPLAY_UNITS_X, DISPLAY_UNITS_Y = 21, 21    # 画面の大きさをマス数で定義
PATH_IMAGE = 'image/'
COLOR_SKYBLUE = (120, 120, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# メッセージ
MESSAGE_BACK_FILE = 'message_window.png'
MESSAGE_WIN_X = 16
MESSAGE_WIN_Y = 462
MESSAGE_WIN_HEIGHT = 200
MESSAGE_START_X = 36
MESSAGE_START_Y = 478
MESSAGE_FONT_NAME = 'Noto Sans CJK JP'
MESSAGE_FONT_SIZE = 26

# マップ
MAP_UNIT_SIZE_X, MAP_UNIT_SIZE_Y, MAP_MOVE_AMOUNT = 32, 32, 1
MAP_FILES = ['map_test.txt']
TILE_FILE = 'tiles_01.png'
MAP_EMPTY = '0'
MAP_BLOCK = '103'
BLOCK_NAME_DICT = {16:'Grass', 21:'Water'}
PASSABLE_BLOCK_LIST = [16]

# キャラ画像
CHARA_SIZE_X, CHARA_SIZE_Y = 32, 32 # キャラクタのサイズ
CHARA_FILE_PLAYER = 'Player.png'
CHARA_FILE_F03 = 'chara_f_03.png'
CHARA_FILE_M12 = 'chara_m_12.png'

# プレイヤー制御
START_X, START_Y = 10, 10 # 主人公の基準位置
PLAYER_NAME = 'Player'
SIDE_MOVE_AMOUNT = 2

# 音声
PATH_SOUND = 'sound/'
SOUND_MESSAGE_NEXT = 'cursor_02.mp3'