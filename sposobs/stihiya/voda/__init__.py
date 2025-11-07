import os
import sys
from typing import Any

import instruments
from sposobs.stihiya.voda.voda_h import TIMER_FOR_S_OBRAT, TIMER_FOR_S_VERTIK, VERTIK_CHANGE_Y, POGRESHOST, VERTIK_KOEF, \
    VVERH_KOEF, VVERH_CHANGE_Y, SUMMA_RAZNICA, VVERH_RAZNICA, VERTIK_ANGLE, VVERH_ANGLE, FALL_CHANGE, \
    FIRST_GRANICA_Y_EJECTION, FIRST_CHANGE_Y_EJECTION, SECOND_GRANICA_Y_EJECTION, SECOND_CHANGE_Y_EJECTION, \
    THIRD_GRANICA_Y_EJECTION, THIRD_CHANGE_Y_EJECTION, ELSE_CHANGE_Y_EJECTION, CHANGE_X_EJECTION, VVERH_KOEF_CHANGE_X, \
    VodohodState

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import sposobs
from sposobs import stihiya, dvizh
import arcade.texture.transforms
from sposobs.stihiya.voda import voda_h

V_LIST = []
'''list[str]'''

class Voda(stihiya.Stihiya):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list)
        self.voda = True
        self.podklass = sposobs.VODA

        self.minus_v = self.minus_max_v = minus_v
        self.v_max_minus = False
        self.s_v_max_minus = 0
        self.kritik = False

    def update_v(self):
        if self.s == 1:
            s = 0
            for pers in V_LIST:
                if pers.v >= self.minus_v and pers == self.pers:
                    pers.v -= self.minus_v
                else:
                    s += 1

            if s == len(V_LIST):
                self.action = False
                self.s += self.timer_for_s

        for pers in V_LIST:
            if self.v_max_minus and self.s_v_max_minus == 0:
                self.s_v_max_minus = 1
                pers.v_max -= self.minus_max_v
                pers.v -= self.minus_max_v
            elif not self.v_max_minus and self.s_v_max_minus == 1:
                self.s_v_max_minus = 0
                pers.v_max += self.minus_max_v
                pers.v += self.minus_max_v
            elif self.v_max_minus and self.s_v_max_minus == 1 and pers.kritik:
                self.v_max_minus = False
                self.s_v_max_minus = 0
                pers.v_max += self.minus_max_v
                pers.v += self.minus_max_v

            if pers.v < 0:
                pers.v *= 0

            if pers.v < pers.v_max:
                pers.v += pers.v_plus
            elif pers.v > pers.v_max:
                pers.v = pers.v_max

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        if self.pers.block.block:
            self.action = False

    # def func_for_init(self):
    #     self.scale = self.minus_v / 100


class VodaFight(Voda, stihiya.StihiyaFight, dvizh.DvizhSprite):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.tip = sposobs.VODA_FIGHT

        self.degree_block = 0.2
        self.force_for_block = -1
        self.minus_for_block = -1
        self.probit_block = True

        self.minus_max_v = 0
        self.v_max_minus = False
        self.s_v_max_minus = 0
        self.kritik = False

    def sbiv(self, sprite):
        if not sprite.smert:
            sprite.sbiv = True
            sprite.fizika.update_poly = True
            # sprite.position_new = True
            # sprite.new_position = (sprite.center_x, 160)


class VodaBlock(Voda, stihiya.StihiyaBlock):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.tip = sposobs.VODA_BLOCK

        self.s_block_texture = 0
        self.block_texture_list = []

        self.s_body_type = 0

        self.fizika = None

    def block_animation(self, speed=0.1):
        # if self.avto_block:
        #     self.texture = self.pers.animations.jump_texture[self.pers.storona]
        if self.block:
            if self.s_block_texture < 2:
                self.texture = self.block_texture_list[round(self.s_block_texture)][self.pers.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.s_block_texture += speed
            else:
                self.texture = self.block_texture[self.pers.storona]
                self.hit_box._points = self.texture.hit_box_points
            self.draw()
        else:
            self.s_block_texture = 0


class VodaImitation(VodaFight, stihiya.StihiyaImitation):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.podtip = sposobs.VODA_IMITATION

        self.baff_uron = 3
        self.kombo_baff_uron = 6

        self.kombo_texture_list = instruments.TextureList()
        self.obich_texture = None
        self.kol_vo_udar_textures = 0
        self.kol_vo_kombo_textures = 0

        self.kombo = False
        self.s_kombo = 0
        self.s_kombo_texture = 0
        self.s_udar_texture = -1
        self.kol_vo_udars = 0
        self.sprite_udar = arcade.Sprite()

        self.fight = False

    def update_kombo(self):
        if self.s == 1:
            self.func_mana()
        if self.kombo:
            self.s = 3

        if not self.action:
            self.sprite_udar = arcade.Sprite()
            if self.s_kombo >= self.kol_vo_udars:
                self.s_kombo = 0
                self.kombo = True

    def atak(self, sprite, physics_engine: arcade.PymunkPhysicsEngine):
        if self.sprite_udar != sprite:
            if not self.kombo:
                self.s_kombo += 1
            self.sprite_udar = sprite
        if self.kombo:
            if self.s_kombo_texture < 3:
                self.udar(sprite, self.uron * self.baff_uron)
            else:
                self.udar(sprite, self.uron * self.kombo_baff_uron)
        else:
            self.udar(sprite)
        self.oglush(sprite)
        self.dvizh_sprite_func(sprite, physics_engine)


class VodoHod(VodaFight):
    def __init__(self, pers, sprite_list, minus_v, igrok=False):
        super().__init__(pers, sprite_list, minus_v)
        self.podtip = sposobs.VODOHOD
        self.igrok = igrok

        self.storona = 0

        self.obrat = False
        self.s_obrat = 0
        self.timer_for_s_obrat = TIMER_FOR_S_OBRAT
        self.s_vertik = 0
        self.timer_for_s_vertik = TIMER_FOR_S_VERTIK
        self.vverh = False
        self.vertik = False
        self.big = False

        self.fizika: arcade.PymunkPhysicsEngine = Any

        self.state = VodohodState.OBICH
        self.last_s_state = 0

    def hod(self, change_x: float, walls_list: arcade.SpriteList, storona: int):
        if self.pers.oglush:
            self.action = False
        if self.action:

            def set_angle(angle: int):
                if self.pers.storona == 1:
                    self.pers.angle = self.angle = angle
                else:
                    self.pers.angle = self.angle = -angle

            height = self.height / 2
            self.storona = storona

            if arcade.check_for_collision_with_list(self, walls_list):
                s = 0
                for wall in walls_list:
                    if arcade.check_for_collision(self, wall):
                        if wall.height >= height * VVERH_KOEF and wall.top > self.center_y - height * 0.85:
                            s += 1
                            if wall.height >= height * VERTIK_KOEF and wall.top > self.center_y - height * 0.85:
                                if self.s_vertik < self.timer_for_s_vertik:
                                    self.change_x = change_x * 0.4
                                    if self.state != VodohodState.VERTIK:
                                        self.state = VodohodState.VERTIK
                                    set_angle(45)
                                    self.s_vertik += 1
                                else:
                                    set_angle(90)
                                    self.change_x = 0
                                    self.change_y = VERTIK_CHANGE_Y
                            else:
                                self.s_vertik = 0
                                if self.state != VodohodState.VVERH:
                                    set_angle(45)
                                    self.state = VodohodState.VVERH
                                self.change_x = change_x * VVERH_KOEF_CHANGE_X
                                self.change_y = VVERH_CHANGE_Y
                            break
                        else:
                            if self.last_s_state == 0:
                                set_angle(0)
                                self.state = VodohodState.OBICH
                                self.s_vertik = 0
                                self.change_y = 0
                                self.change_x = change_x
                self.last_s_state = s
            else:
                set_angle(0)
                self.s_vertik = 0
                self.change_x = change_x
                self.change_y = FALL_CHANGE

    def update_pers_body_type(self):
        if self.action:
            self.pers.position = self.position
            self.s_kd = 0
            if self.s == 0:
                self.fizika.remove_sprite(self.pers)
                # self.fizika.sprites[self.pers].body.body_type = self.fizika.KINEMATIC
            self.s += 1
        else:
            self.s = 0
            self.s_kd += 1
            if self.s_kd == 1:
                self.pers.angle = 0
                self.fizika.add_sprite(self.pers, 1, 1,
                                       max_vertical_velocity=2000,
                                       max_horizontal_velocity=300,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.fizika = physics_engine
        self.update_sposob()
        self.update_v()
        self.update_mor()
        self.update_pers_body_type()

        if self.action and not self.kritik:
            self.pers.toggle = True
            self.func_mana()
            self.v_max_minus = True

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and self.change_x != 0:
                    self.oglush(sprite)
                    self.dvizh_sprite_func(sprite, physics_engine, 1)
                    self.udar(sprite)
                    self.sbiv(sprite)
        else:
            self.pers.angle = self.angle = 0
            self.pers.toggle = False
            self.bottom = self.pers.bottom
            self.center_x = self.pers.center_x
            self.v_max_minus = False

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite(physics_engine)

