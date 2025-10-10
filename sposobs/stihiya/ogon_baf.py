import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


import arcade
import sposobs
from sposobs import stihiya
from sposobs.stihiya import ogon


class OgonBaf(ogon.Ogon):
    def __init__(self, pers, sprite_list, baf_texture):
        super().__init__(pers, sprite_list)
        self.tip = sposobs.OGON_BAF

        self.__baf_texture = baf_texture

        self.baf = False

    def baf_animations(self):
        if self.action and not self.block and self.baf:
            self.texture = self.__baf_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points


class BafColdOr(OgonBaf):
    def __init__(self, pers, sprite_list, baf_texture):
        super().__init__(pers, sprite_list, baf_texture)
        self.sposob = sposobs.OGON_BAF_COLD_ORUZHIE




