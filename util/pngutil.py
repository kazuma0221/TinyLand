# coding: UTF-8
import pygame

# 画像分割
def split(surface:pygame.Surface, is_alpha:bool, unit_width:int, unit_height:int) -> list[pygame.Surface]:
    images = []
    w, h = surface.get_size()
    flag_src = pygame.SRCALPHA if is_alpha else 0
    
    for y in range(0, h, unit_height):
        for x in range(0, w, unit_width):
            piece = pygame.Surface((unit_width, unit_height), flag_src)
            piece.blit(surface, (0, 0), (x, y, unit_width, unit_height))
            images.append(piece)
    return images

# チップ読み込み
def load_chip(p: str, is_alpha: bool, unit_width:int, unit_height:int) -> list[pygame.Surface]:
    img = pygame.image.load(p)
    imgs = split(img, is_alpha, unit_width, unit_height)
    return imgs
