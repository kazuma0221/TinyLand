# coding: UTF-8
from const import const, soundname
from pygame import mixer

def prepareSound() -> dict:
    '''使う効果音を新規登録して、効果音名とSoundのTypedDictサブクラスを返す。
    :returns: 効果音
    :rtype: dic'''
    # 初期化とパス
    mixer.init()
    path = const.PATH_SOUND
    # 効果音の名前とファイル名の紐づけ
    dic = {soundname.MESSAGE: mixer.Sound(path + soundname.FILE_MESSAGE)}

    return dic