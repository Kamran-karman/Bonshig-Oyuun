import math
import sys

import arcade
from arcade import Texture

from arcade.geometry import is_point_in_polygon

PNG = '.png'


class TextureList:
    def __init__(self):
        self.__list: list[Texture] = []

    def __getitem__(self, item):
        return self.__list[item]

    def __setitem__(self, key, value):
        self.__list[key] = value

    def __len__(self):
        return len(self.__list)

    def append(self, texture: Texture | tuple[Texture, Texture]):
        self.__list.append(texture)

    def remove(self, texture: Texture | tuple[Texture, Texture]):
        self.__list.remove(texture)

    def extend(self, texture_list: list[Texture | tuple[Texture, Texture]]):
        for texture in texture_list:
            self.append(texture)

    def load_textures(self, kol_vo: int, main_patch: str, rasshir: str, texture_pair=True):
        for i in range(kol_vo):
            if texture_pair:
                texture = arcade.load_texture_pair(f'{main_patch}{i}{rasshir}')
            else:
                texture = arcade.load_texture(f'{main_patch}{i}{rasshir}')
            self.append(texture)


def nearest_pers(sprite: arcade.Sprite, sprite_list_1: arcade.SpriteList, neobhodimo_rast=-1, kol_vo: int = 1):
    rast_slovar = {}
    sprite_list = arcade.SpriteList()
    min_rast_list = []
    s = 0
    for sprite_1 in sprite_list_1:
        rast_x = abs(sprite.center_x - sprite_1.center_x)
        rast_y = abs(sprite.center_y - sprite_1.center_y)
        rast = math.hypot(rast_x, rast_y)
        rast_slovar.update({sprite_1: rast})

    copy_rast_slovar = rast_slovar.copy()
    while s < kol_vo:
        min_rast = min(copy_rast_slovar.values())
        min_rast_list.append(min_rast)
        for sprite_1 in copy_rast_slovar:
            if copy_rast_slovar[sprite_1] == min_rast:
                copy_rast_slovar.pop(sprite_1)
                break
        s += 1

    if neobhodimo_rast != -1:
        for rast in min_rast_list:
            if rast > neobhodimo_rast:
                min_rast_list.remove(rast)
        for sprite_1 in rast_slovar:
            if rast_slovar[sprite_1] in min_rast_list:
                sprite_list.append(sprite_1)
    else:
        for sprite_1 in rast_slovar:
            if rast_slovar[sprite_1] in min_rast_list:
                sprite_list.append(sprite_1)
    if kol_vo == 1:
        return sprite_list[0]
    else:
        return sprite_list


MIN_SDVIG_PIXEL = 7
MAX_SDVIG_PIXEL = MIN_SDVIG_PIXEL + 50
IT_SDVIG_PIXEL = 5


def nearest(point: tuple[float, float], input_sprite_list: arcade.SpriteList):
    rast_slovar = {}
    output_sprite_list = arcade.SpriteList()

    def sdvig(point_list, sdvig_x: int, sdvig_y: int):
        # print(point[0] + sdvig_x, point[1] - sdvig_y, point_list)
        return is_point_in_polygon(point[0] + sdvig_x, point[1] - sdvig_y, point_list)

    sdvig_pixel = MIN_SDVIG_PIXEL

    while len(rast_slovar) == 0 and sdvig_pixel < MAX_SDVIG_PIXEL:
        for sprite in input_sprite_list:
            sdvig_list = [
                (0, -sdvig_pixel), (sdvig_pixel, -sdvig_pixel), (sdvig_pixel, 0), (sdvig_pixel, sdvig_pixel),
                (0, sdvig_pixel), (-sdvig_pixel, sdvig_pixel), (-sdvig_pixel, 0), (-sdvig_pixel, -sdvig_pixel)
            ]

            rast_list = []

            for i in sdvig_list:
                if sdvig(sprite.hit_box.get_adjusted_points(), *i):
                    rasst = math.hypot(abs(point[0] + i[0] + sprite.center_x),  abs(point[1] + i[1] + sprite.center_y))
                    rast_list.append(rasst)

            if len(rast_list) > 0:
                rast_slovar.update({min(rast_list): sprite})

        sdvig_pixel += IT_SDVIG_PIXEL

    # print(rast_slovar)
    for i in range(len(rast_slovar)):
        output_sprite_list.append(rast_slovar[min(rast_slovar.keys())])
        rast_slovar.pop(min(rast_slovar.keys()))

    return output_sprite_list


def poisk_path(key_slovo: str = "Igra"):
    list_path = sys.path
    for path in list_path:
        slovo = ""
        for i in range(-4, 0):
            slovo += path[i]
        if slovo == key_slovo:
            return path.replace("\\", '/')
    return ''


def preobraz(a, in_min, in_max, out_min, out_max):
    return (a - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
