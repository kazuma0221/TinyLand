# coding: UTF-8
from const import const, soundname
from pygame.mixer import Sound

def prepareSound() -> dict:
    '''使う効果音を新規登録して、効果音名とSoundのTypedDictサブクラスを返す。
    :returns: 効果音
    :rtype: dic'''
    path = const.PATH_SOUND
    dic = {soundname.JUMP: Sound(path + soundname.FILE_JUMP)}
    return dic