import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import hit_box_and_radius
import math

MOL_BLUE = (44, 117, 255, 255)

FIZ_SPOSOB = 10000

SHCHITS = 11000
SHCHIT = 11001

COLD_ORUZHIE = 12000
OBICH_MECH = 12001
MECH_OGON = 12002
DVURUCH_MECH = 12002
VILA = 12004
TOPOR = 12005
MECH_BRENDA = 12006

DAL_ORUZH = 1300

RUKOPASH = 1400
UDAR = 1401

RIVOKS = 31100
RIVOK = 31110

# __________________

STIHIYA = 20000

STIHIYA_FIGHT = 21000
MOLNIAY = 21100
CEPNAYA_MOLNIYA = 21101
GNEV_TORA = 21102
STRELI_PERUNA = 21103
SHAR_MOLNIYA = 21104
UDAR_ZEVSA = 21105

VODA = 21200
SPUTNIK = 21201
SPUTNIKI = 21202
VOLNA = 21203
RECHNOY_DRAKON = 21204
UDAR_KITA = 21205
TAYFUN = 21206
HLIST = 21207
VODA_UDAR = 21208
VODA_UDARS = 21209
VODOHOD = 21210
TECHENIE = 21211

ZEMLYA = 21300

VETER = 21400

OGON = 21500
FIRE_BALL = 21501
YAZIKI_OGNYA = 21502
KULAK_OGNYA = 21503
MINI_FIRE_BALL = 21504


# ___CepnayaMolniay___
URON_CEP_MOLNIAY = 300
MINUS_MANA_CEP_MOLNIAY = 20

S_KD_CEP_MOLNIAY = 360

S_OGLUSH_CEP_MOLNIAY = 90
# ______________________


# ___GnevTora___
URON_GNEV_TORA = 400
MINUS_MANA_GNEV_TORA = 30

S_KD_GENV_TORA = 600

S_OGLUSH_GNEV_TORA = 240
# ______________________


# ___StreliPeruna___
URON_STRELI_PERUNA = 150
MINUS_MANA_STRLI_PERUNA = 4

S_KD_STRELI_PERUNA = 45

S_OGLUSH_STRELI_PERUNA = 45
# ______________________


# ___SharMolniay___
SKOROST_SHAR_MOL = 20
URON_SHAR_MOL = 35
URON1_SHAR_MOL = URON_SHAR_MOL / 5

S_KD_SHAR_MOL = 300
MAX_S_ZARYAD_SHAR_MOL = 360
MAX_BAF_S_ZARYAD_SHAR_MOL = 300
S_DO_PROMAH_SHAR_MOL = 45

VZRIV_BAF_URON_SHAR_MOL = 1.5
PROMAH_DEBAF_URON_SHAR_MOL = 1.5
BAF_URON_SHAR_MOL = 19.067

S_OGLUSH_SHAR_MOL = 6
DEBAF_FOR_OGLUSH_SHAR_MOL = 2
BAF_FOR_OGLUSH_SHAR_MOL = 294
VZRIV_BAF_OGLUSH_SHAR_MOL = 1.5
# ______________________


# ___UdarZevsa___
URON_UDAR_ZEVSA = 20
BAF_URON_UDAR_ZEVSA = 1.5

S_KD_UDAR_ZEVSA = 600
S_UDAR_ZEVSA = 300

S_OGLUSH_UDAR_ZEVSA = 12
BAF_FOR_OGLUSH_UDAR_ZEVSA = 1.4788
# ______________________


# ___Sputnik___
URON_SPUTNIK = 50
SPUTNIK_CHANGE = 18
SPUTNIK_CHANGE_UDAR = 27
S_SPUNNIK = 180
S_KD_SPUTNIK = 240
SPUTNIK_MINUS_MANA = 1
# ______________________


# ___Rivok___
S_KD_RIVOK = 60
# ______________________


# ___Shcit___
URON_SHCHIT = 80
# ______________________


# ___DvuruchMech___
URON_DVURUCH_MECH = 120
# ______________________


# ___Vila___
URON_VILA = 40
# ______________________


# ___Topor___
URON_TOPOR = 50
# ______________________


# ___MechBrenda___
URON_MECH_BRENDA = 180
# ______________________


class Sposob(arcade.Sprite):
    def __init__(self, pers, sprite_list):
        super().__init__()
        self.pers = pers
        self.sprite_list = sprite_list

        self.action = False
        self.action_2 = False

        self.timer_for_s = 0
        self.timer_for_s_2 = 0
        self.timer_for_s_kd = 0
        self.timer_for_s_oglush = 0

        self.s = 0
        self.s_2 = 0
        self.s_kd = 0

        self.fight_sposob = False
        self.block_sposob = False
        self.dvizh_sposob = False

        self.klass = 0
        self.podklass = 0
        self.tip = 0
        self.podtip = 0
        self.sposob = 0

    def update_sposob(self):
        for sprite in self.sprite_list:
            if sprite.hp <= 0:
                self.sprite_list.remove(sprite)

        if self.pers.hp <= 0 or self.pers.oglush:
            self.s += self.timer_for_s

    def oglush(self, sprite):
        if not sprite.oglush:
            sprite.oglush = True
            sprite.timer_for_s_oglush = self.timer_for_s_oglush
            sprite.s_oglush = 0


class FizSposob(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.klass = FIZ_SPOSOB

        self.minus_stamina = 0
        self.stamina = False

    def func_stamina(self, minus_stamina=-1):
        if self.pers.stamina > 0:
            if minus_stamina == -1:
                if self.pers.stamina >= self.minus_stamina:
                    self.pers.stamina -= self.minus_stamina
                    self.stamina = True
                else:
                    self.pers.stamina -= self.minus_stamina
                    self.stamina = False
                    self.s += self.timer_for_s
            else:
                if self.pers.stamina >= minus_stamina:
                    self.pers.stamina -= minus_stamina
                    self.stamina = True
                else:
                    self.pers.stamina -= minus_stamina
                    self.stamina = False
                    self.s += self.timer_for_s
        else:
            self.s += self.timer_for_s


class Stihiya(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.klass = STIHIYA

        self.minus_mana = 0
        self.mana = True

    def func_mana(self, minus_mana=float(-1)):
        if self.pers.mana > 0:
            if minus_mana != -1:
                if self.pers.mana >= self.minus_mana:
                    self.mana = True
                    self.pers.mana -= self.minus_mana
                else:
                    self.s += self.timer_for_s
                    self.mana = False
                    self.pers.mana -= self.minus_mana
            else:
                if self.pers.mana >= minus_mana:
                    self.mana = True
                    self.pers.mana -= minus_mana
                else:
                    self.s += self.timer_for_s
                    self.mana = False
                    self.pers.mana -= minus_mana
        else:
            self.s += self.timer_for_s


class Fight(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.fight_sposob = True

        self.uron = 0
        self.degree_block = 0
        self.probit_block = False

        self.slovar = {}
        self.kd = False

    def update_slovar(self):
        if len(self.slovar) < len(self.sprite_list):
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
        while len(self.slovar) > len(self.sprite_list):
            for i in self.slovar:
                s = 0
                for sprite in self.sprite_list:
                    if sprite == i:
                        s += 1
                if s == 0:
                    self.slovar.pop(i)
                    return
        if not self.action:
            for i in self.slovar:
                self.slovar[i] = False

    def update_position(self):
        self.position = self.pers.position

    def udar(self, sprite, uron=-1., popal=True):
        for i in self.slovar:
            if i == sprite and not self.slovar[i]:
                self.slovar[i] = popal
                if uron == -1:
                    sprite.hp -= round(self.uron)
                else:
                    sprite.hp -= round(uron)

    def kd_timer_stamina(self):
        if self.s_kd < self.timer_for_s_kd and self.s >= self.timer_for_s:
            self.kd = True
        elif self.s_kd >= self.timer_for_s_kd:
            self.kd = False

        if self.kd:
            self.action = False
            self.s_kd += 1

        if self.s >= self.timer_for_s:
            self.action = False
            self.s = 0

        if self.action:
            self.s += 1
        if self.action and self.s == 1:
            self.s_kd = 0

    def kd_timer_mana(self):
        self.s_kd += 1

        if self.s_kd <= self.timer_for_s_kd:
            self.kd = True
            self.action = False
        else:
            self.kd = False

        if self.s >= self.timer_for_s:
            self.action = False
            self.action_2 = False
            self.kd = True
            self.s_kd = 0
            self.s = 0
            self.s_2 = 0

        if self.action:
            self.kd = False
            self.s += 1

    def udar_or_block(self, sprite, popal=True):
        if not sprite.avto_block_func(self.pers):
            self.udar(sprite, popal=popal)
            return True
        else:
            for sposob in sprite.sposob_list:
                if sposob.sposob == UDAR and sposob.block:
                    self.udar(sprite, self.uron, popal)
                    return False
                if self.sposob == UDAR:
                    if sposob.sposob == self.sposob and sposob.block:
                        self.udar(sprite, self.uron * 0.5, popal)
                        return False
                    return False
            self.udar(sprite, self.uron * self.degree_block, popal)
            return False


class Block(Sposob):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.block_sposob = True

        self.block_texture = None

        self.main_block = False
        self.block = False
        self.avto_block = False
        self.s_avto_block = 0
        self.timer_for_s_ab = 30

    def update_block(self):
        if self.main_block:
            self.block = self.pers.block.block
            self.avto_block = self.pers.block.avto_block
        if self.action:
            self.avto_block = self.block = self.pers.block.block = self.pers.block.avto_block = False
            return
        if self.avto_block or self.block:
            self.action = False

        if self.avto_block:
            self.s_avto_block += 1
            # if self.uron == 0:
            #     print(self.s_avto_block)

        if self.s_avto_block >= self.timer_for_s_ab:
            self.pers.block.avto_block = False
            self.avto_block = False
            self.s_avto_block = 0


class Dvizh(Sposob):
    def __init__(self, pers, sprite_list, timer=True):
        super().__init__(pers, sprite_list)
        self.dvizh_sposob = True

        self.storona = 1

        self.s_dvizh = 0
        self.timer_for_s_dvizh = 60
        self.timer = timer
        self.s_dvizh_func = 0
        self.dvizh = False
        self.izmen_vel = True
        self.dvizh_force = (0, 0)
        self.dvizh_vel = (0, 0)
        self.pred_vel_x = 0
        self.pred_vel_y = 0

        self.fizika = None


class DvizhPers(Dvizh):
    def __init__(self, pers, sprite_list, vel: tuple, timer_for_s_dvizh=0, igrok=False):
        super().__init__(pers, sprite_list)
        self.igrok = igrok
        self.dvizh_vel = vel

        self.timer_for_s_dvizh = timer_for_s_dvizh
        self.stop_dvizh = False

    def update_storona(self):
        if self.pers.storona == 1:
            # print(-1, self.pers.storona)
            self.storona = -1
        elif self.pers.storona == 0:
            # print(1, self.pers.storona)
            self.storona = 1

    def dvizh_pers_func(self):
        if self.s_dvizh_func == 0:
            self.s_dvizh_func = 1
            self.dvizh = True
            self.pers.dvizh = True
            self.fizika.apply_force(self.pers, self.dvizh_force)
            if self.storona == 1:
                self.pers.new_force[0] += self.dvizh_force[0]
            elif self.storona == -1:
                self.pers.new_force[0] -= self.dvizh_force[0]
            self.pers.new_force[1] += self.dvizh_force[1]
            #print('1', self.pers.new_force, self.timer_for_s_dvizh)

    def update_dvizh_pers(self):
        if self.dvizh:
            if self.timer:
                self.s_dvizh += 1
            if self.izmen_vel:
                self.pers.pymunk.max_horizontal_velocity = self.dvizh_vel[0]
            self.pers.izmen_force = True
            if self.s_dvizh >= self.timer_for_s_dvizh:
                self.s_dvizh = 0
                self.dvizh = False
                if self.izmen_vel:
                    self.pers.pymunk.max_horizontal_velocity = self.pers.vel_x
                self.pers.izmen_force = False
                if self.storona == 1:
                    self.pers.new_force[0] -= self.dvizh_force[0]
                elif self.storona == -1:
                    self.pers.new_force[0] += self.dvizh_force[0]
                self.pers.new_force[1] -= self.dvizh_force[1]
                #print('2', self.pers.new_force, self.timer_for_s_dvizh)
                self.s_dvizh_func = 0
        if self.stop_dvizh and self.s_dvizh < self.timer_for_s_dvizh and self.dvizh:
            self.stop_dvizh = False
            self.dvizh = False
            self.s_dvizh = 0
            if self.izmen_vel:
                self.pers.pymunk.max_horizontal_velocity = self.pers.vel_x
            self.pers.izmen_force = False
            # if self.storona == 1:
            #     self.pers.new_force[0] -= self.dvizh_force[0]
            # elif self.storona == -1:
            #     self.pers.new_force[0] += self.dvizh_force[0]
            # self.pers.new_force[1] -= self.dvizh_force[1]
            #print('3', self.pers.new_force, self.timer_for_s_dvizh)
            self.s_dvizh_func = 0


class DvizhSprite(Dvizh):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.slovar_dvizh = {}

    def update_storona(self, sprite, a=0):
        if a == 1:
            if self.pers.storona == 0:
                self.storona = 1
            else:
                self.storona = -1
        elif a == 0:
            if sprite.center_x < self.pers.center_x:
                self.storona = -1
            elif sprite.center_x > self.pers.center_x:
                self.storona = 1

    def update_slovar_dvizh(self):
        if len(self.slovar_dvizh) < len(self.sprite_list):
            for sprite in self.sprite_list:
                self.slovar_dvizh.update({sprite: False})
        while len(self.slovar_dvizh) > len(self.sprite_list):
            for sprite_dvizh in self.slovar_dvizh:
                s = 0
                for sprite in self.sprite_list:
                    if sprite == sprite_dvizh:
                        s += 1
                if s == 0:
                    self.slovar_dvizh.pop(sprite_dvizh)
                    return

    def update_dvizh_sprite(self, timer=-1):
        for sprite in self.slovar_dvizh:
            if timer > -1:
                self.timer_for_s_dvizh = timer
            if self.slovar_dvizh[sprite]:
                sprite.slovar_dvizh[self][0] += 1
                # if self.sposobs == VOLNA:
                #     print(self.timer_for_s_dvizh, sprite.slovar_dvizh[self][0])
                if sprite.slovar_dvizh[self][0] >= self.timer_for_s_dvizh:
                    self.slovar_dvizh[sprite] = False
                    sprite.slovar_dvizh[self][0] = 0

                    self.update_storona(sprite)
                    #print(sprite.slovar_dvizh[self][1], sprite.uzhe_dvizh, self.s, self.sposobs)
                    if sprite.slovar_dvizh[self][1] or not sprite.uzhe_dvizh:
                        sprite.pymunk.max_horizontal_velocity = sprite.vel_x
                        sprite.slovar_dvizh[self][1] = False
                        sprite.uzhe_dvizh = False
                        sprite.dvizh = False

        if not arcade.check_for_collision_with_list(self, self.sprite_list):
            self.s_dvizh_func = 0

    def dvizh_sprite_func(self, sprite, a=0):
        if self.s_dvizh_func == 0:
            for i in self.slovar_dvizh:
                if i == sprite and not self.slovar_dvizh[sprite]:
                    self.s_dvizh_func += 1
                    self.slovar_dvizh[sprite] = True
                    if sprite.dvizh or sprite.uzhe_dvizh:
                        self.update_storona(sprite, a)
                        sprite.uzhe_dvizh = True
                        #print(sprite.new_force, self.dvizh_force, self.sposobs)
                        if sprite.new_force[0] < self.dvizh_force[0] or sprite.new_force[0] < self.dvizh_force[0]:
                            for dvizh in sprite.slovar_dvizh:
                                sprite.slovar_dvizh[dvizh][1] = False
                            sprite.slovar_dvizh.update({self: [0, True]})
                            self.fizika.apply_force(sprite, self.dvizh_force)
                            sprite.new_force = [self.dvizh_force[0] * self.storona, self.dvizh_force[1]]
                            sprite.pymunk.max_horizontal_velocity = self.dvizh_vel[0]
                        else:
                            sprite.slovar_dvizh.update({self: [0, False]})
                    else:
                        sprite.slovar_dvizh.update({self: [0, True]})
                        sprite.dvizh = True
                        self.update_storona(sprite, a)
                        self.pers.fizika.apply_force(sprite, self.dvizh_force)
                        sprite.new_force = [self.dvizh_force[0] * self.storona, self.dvizh_force[1]]
                        sprite.pymunk.max_horizontal_velocity = self.dvizh_vel[0]


class FizSposobFight(Fight, FizSposob, Block):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list)
        self.klass = FIZ_SPOSOB

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd

        self.udar_texture = None

        self.timer_for_s_block = 60
        self.s_block = self.timer_for_s_block

        self.minus_block_stamina = 0
        self.minus_for_block = -1

        self.force_for_block = -1
        self.return_force = 50000
        self.pred_return_force = self.return_force
        self.s_return_force = 0
        self.rf = False

        self.sposob_list = arcade.SpriteList()

    def otdacha(self):
        if not self.rf:
            self.s_return_force = 0
            for sprite in self.sprite_list:
                for sposob in sprite.sposob_list:
                    if sposob.sposob == VODA_UDARS:
                        for vu in sposob.vu_list:
                            if arcade.check_for_collision(vu, self) and (self.block or self.avto_block) and vu.action:
                                if self.return_force != sposob.force_for_block and sposob.force_for_block != -1:
                                    self.return_force = sposob.force_for_block
                                self.rf = True
                                if sposob.minus_for_block != -1:
                                    self.func_stamina(sposob.minus_for_block)
                                else:
                                    self.func_stamina(self.minus_block_stamina)
                                if not self.stamina:
                                    self.block = self.avto_block = False
                                if vu not in self.sposob_list:
                                    self.sposob_list.append(vu)
                    else:
                        if (sposob.podklass == (VODA or COLD_ORUZHIE) and arcade.check_for_collision(sposob, self) and
                                (self.block or self.avto_block) and sposob.action and not sposob.probit_block):
                            if self.return_force != sposob.force_for_block and sposob.force_for_block != -1:
                                self.return_force = sposob.force_for_block
                            self.rf = True
                            if sposob.minus_for_block != -1:
                                self.func_stamina(sposob.minus_for_block)
                            else:
                                self.func_stamina(self.minus_block_stamina)
                            if not self.stamina:
                                self.block = self.avto_block = False
                            if sposob not in self.sposob_list:
                                self.sposob_list.append(sposob)
        else:
            self.s_return_force += 1
        if self.rf and 0 < self.s_return_force <= 7:
            if self.pers.storona == 0:
                self.pers.fizika.apply_force(self.pers, (-self.return_force, 0))
            else:
                self.pers.fizika.apply_force(self.pers, (self.return_force, 0))
            self.pers.fizika.set_friction(self.pers, 0)

        for sposob in self.sposob_list:
            if sposob.action and (self.block or self.avto_block) and arcade.check_for_collision(sposob, self):
                self.s_return_force = 0
                if sposob.minus_for_block != -1:
                    self.func_stamina(sposob.minus_for_block)
                else:
                    self.func_stamina(self.minus_block_stamina)
            if not sposob.action and self.s_return_force >= 30:
                self.rf = False
                self.s_return_force = 0
                self.sposob_list.remove(sposob)
                self.return_force = self.pred_return_force

    def block_block(self):
        if self.block:
            self.s_block += 1
        else:
            self.s_block = 0
        if self.s_block >= self.timer_for_s_block and self.block:
            self.s_block = 0
            self.func_stamina(self.minus_block_stamina)


class StihiyaFight(Stihiya, Fight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.podklass = STIHIYA_FIGHT

        self.radius = None
        self.radius: hit_box_and_radius.Radius

    def update_radius_position(self):
        self.radius.position = self.position

    def update_mor(self, uron):
        if self.pers.mor:
            uron *= 2 / 3
            self.uron = uron


class ColdOruzhie(FizSposobFight):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.podklass = COLD_ORUZHIE

    def update_storona(self):
        if self.action:
            self.texture = self.udar_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points
            return
        if self.block or self.avto_block:
            self.texture = self.block_texture[self.pers.storona]
            self.hit_box._points = self.texture.hit_box_points

    def update_degree(self, sprite):
        for sposob in sprite.sposob_list:
            if sposob.podklass == MOLNIAY or sposob.klass == FIZ_SPOSOB:
                self.degree_block = 0
            elif sposob.podklass == OGON:
                self.degree_block = 0.5
            elif sposob.podklass == ZEMLYA:
                self.degree_block = 0.75
            elif sposob.podklass == VODA:
                self.degree_block = 0.8
            elif sposob.podklass == VETER:
                self.degree_block = 0.9


# Физические способности


class Rivoks(DvizhPers):
    def __init__(self, pers, sprite_list, timer_for_s_dvizh=0, vel=(0, 0), igrok=False):
        super().__init__(pers, sprite_list, vel, timer_for_s_dvizh, igrok)
        self.klass = RIVOKS

        self.radius_stop = hit_box_and_radius.KvadratRadius()

        self.levo = 0
        self.pravo = 0

    def timer_kd(self):
        if self.action:
            self.update_storona()
            self.pers.stan_for_sposob = True
            self.s_kd += 1
            if self.s_kd >= self.timer_for_s_kd:
                self.action = False
                self.pers.stan_for_sposob = False
                self.dvizh_pers_func()

    def updadte_stop(self):
        self.radius_stop.position = self.pers.position

        if not self.igrok:
            if not self.pers.s_kast_scena:
                if self.pers.radius_vid.check_collision(self.pers.igrok):
                    if self.pers.igrok.center_x > self.pers.radius_vid.center_x:
                        if self.levo <= abs(self.pers.igrok.left - self.pers.right) <= self.pravo:
                            if self.s_kd < self.timer_for_s_kd:
                                self.action = True
                        else:
                            if self.s_kd < self.timer_for_s_kd - self.timer_for_s_kd / 5:
                                self.action = False
                                self.s_kd = 0
                                self.pers.stan_for_sposob = False
                    elif self.pers.igrok.center_x < self.pers.radius_vid.center_x:
                        if self.levo <= abs(self.pers.igrok.right - self.pers.left) <= self.pravo:
                            if self.s_kd < self.timer_for_s_kd:
                                self.action = True
                        else:
                            if self.s_kd < self.timer_for_s_kd - 30:
                                self.action = False
                                self.s_kd = 0
                                self.pers.stan_for_sposob = False

                for drug in self.pers.v_drug_list:
                    if drug != self.pers and not drug.smert:
                        if (self.radius_stop.check_collision(drug.kvadrat_radius) and
                                abs(self.radius_stop.center_x - self.pers.igrok.center_x) >
                                abs(drug.center_x - self.pers.igrok.center_x)):
                            self.stop_dvizh = True
                            self.s_kd = 0

                if self.radius_stop.check_collision(self.pers.igrok) and self.dvizh:
                    self.stop_dvizh = True
                    self.s_kd = 0
        else:
            if self.radius_stop.check_collision(sprite_list=self.pers.sprite_list):
                self.stop_dvizh = True
                self.action = False
                self.s_kd = 0
                self.pers.stan_for_sposob = False


class Rivok(FizSposobFight, Rivoks):
    def __init__(self, pers, sprite_list, vel, timer_for_s=30, timer_for_s_kd=S_KD_RIVOK, timer_for_s_dvizh=60,
                 igrok=False):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.dvizh_vel = vel
        self.igrok = igrok
        self.sposob = RIVOK

        self.dvizh_force = (10000, 0)

        self.levo = 400
        self.pravo = 800

        self.timer_for_s = timer_for_s
        self.timer_for_s_kd = timer_for_s_kd
        self.timer_for_s_dvizh = timer_for_s_dvizh

        self.minus_stamina = 3

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if not self.pers.smert and not self.pers.oglush:

            self.radius_stop.position = self.pers.position

            self.timer_kd()

            if self.dvizh:
                if self.s_dvizh == 1:
                    self.func_stamina()
                    if not self.stamina:
                        self.s_kd = 0
                        self.pers.stan_for_sposob = False
                        self.stop_dvizh = True
                        self.s_dvizh += self.timer_for_s_dvizh
                        return
                    else:
                        self.pers.stamina -= self.minus_stamina
                if self.s_dvizh >= self.timer_for_s_dvizh:
                    self.s_kd = 0
            elif not self.dvizh and self.s_kd >= self.timer_for_s_kd:
                self.s_kd = 0

            self.updadte_stop()
        elif self.pers.smert or self.pers.oglush:
            if self.dvizh:
                self.stop_dvizh = True
            self.action = False
            self.s_kd = 0

        self.update_dvizh_pers()


class Udar(FizSposobFight):
    def __init__(self, pers, sprite_list, timer_for_s=45, timer_for_s_kd=105):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.sposob = UDAR

        self.s_kd = self.timer_for_s_kd + 5
        self.udar_texture = None
        self.scale = self.pers.scale + 0.05
        # self.block_texture = self.pers.block_texture

        self.probit_block = False
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if self.pers.sil:
            self.probit_block = True

        self.uron = self.pers.uron

        self.update_sposob()
        #self.update_scale()
        self.update_position()
        self.update_block()
        self.kd_timer_mana()

        if self.s == 1:
            self.func_stamina()
        if self.action and self.stamina:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    if not self.probit_block:
                        self.udar_or_block(sprite)
                    else:
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= self.uron

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.udar_texture = self.pers.udar_texture
        self.texture = self.udar_texture[self.pers.storona]


# Стихия молнии


class Molniya(StihiyaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.podklass = MOLNIAY

        self.timer_for_s = 3


class CepnayaMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = CEPNAYA_MOLNIYA

        self.uron = URON_CEP_MOLNIAY

        self.minus_mana = MINUS_MANA_CEP_MOLNIAY

        self.en_x = 0
        self.en_y = 0

        self.radius = hit_box_and_radius.Radius()

        self.timer_for_s_kd = S_KD_CEP_MOLNIAY
        self.s_kd = self.timer_for_s_kd

        self.timer_for_s_oglush = S_OGLUSH_CEP_MOLNIAY

        self.tp = False
        self.spisok = []

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor(self.uron)

        self.kd_timer_stamina()

        if self.action:
            spisok_rast = []
            spisok_xy = []
            spisok3 = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite=sprite) and sprite.hp > 0:
                    poz_x, poz_y = abs(sprite.center_x - self.pers.center_x), \
                        abs(sprite.center_y - self.pers.center_y)
                    pozi = (poz_x, poz_y)
                    spisok_rast.append(pozi)
                    x, y = sprite.center_x, sprite.center_y
                    xy = (x, y)
                    spisok_xy.append(xy)
            if len(spisok_rast) == 0:
                self.en_x, self.en_y = self.pers.position
                self.action = False
                self.s_kd = self.timer_for_s_kd + 1
            elif len(spisok_rast) > 0:
                if self.s == 1:
                    self.func_mana()
                    if self.mana:
                        self.tp = True
                    else:
                        self.s = 0
                        self.s_kd = self.timer_for_s_kd + 1
                else:
                    self.tp = False
                stx, sty = self.pers.position
                en = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[en]
                spisok3.append(spisok_xy[en])
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        self.udar(sprite)
                        self.oglush(sprite)

                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                arcade.draw_circle_filled(stx, sty, 50, MOL_BLUE)
                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                arcade.draw_circle_filled(stx, sty, 45, arcade.color.WHITE)
                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                radius = hit_box_and_radius.Radius()
                radius.position = enx, eny
                self.spisok.append([stx, sty, enx, eny])
                w = 1

                while w < 4:
                    if radius.check_collision(sprite_list=self.sprite_list):
                        if self.pers.position == (stx, sty):
                            pred_poz = 0, 0
                        else:
                            pred_poz = stx, sty
                        spisok_rast = []
                        spisok_xy = []
                        for sprite in self.sprite_list:
                            if radius.check_collision(sprite) and sprite.position != radius.position \
                                    and sprite.position != pred_poz and sprite.hp > 0:
                                poz_x, poz_y = abs(radius.center_x - sprite.center_x), abs(
                                    radius.center_y - sprite.center_y)
                                pozi = (poz_x, poz_y)
                                x, y = sprite.center_x, sprite.center_y
                                xy = (x, y)
                                e = 0
                                for i in spisok3:
                                    if xy[0] == i[0] and xy[1] == i[1]:
                                        e += 1
                                if e == 0:
                                    spisok_rast.append(pozi)
                                    spisok_xy.append(xy)
                        if len(spisok_rast) == 0:
                            if stx > enx:
                                self.en_x, self.en_y = enx - 250, eny + 150
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 250, eny + 150
                            break
                        elif w == 2 and len(spisok_rast) != 0:
                            en = spisok_rast.index(min(spisok_rast))
                            stx, sty = radius.position
                            enx, eny = spisok_xy[en]
                            for sprite in self.sprite_list:
                                if sprite.position == (enx, eny):
                                    self.udar(sprite)
                                    self.oglush(sprite)

                            arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                            arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                            arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                            arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                            arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                            arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                            if stx > enx:
                                self.en_x, self.en_y = enx - 250, eny + 150
                            elif stx < enx:
                                self.en_x, self.en_y = enx + 250, eny + 150
                            break
                        else:
                            if len(spisok_rast) != 0:
                                en = spisok_rast.index(min(spisok_rast))
                                stx, sty = radius.position
                                enx, eny = spisok_xy[en]
                                spisok3.append(spisok_xy[en])
                                for sprite in self.sprite_list:
                                    if sprite.position == (enx, eny):
                                        self.udar(sprite)
                                        self.oglush(sprite)

                                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 30)
                                arcade.draw_circle_filled(enx, eny, 30, MOL_BLUE)
                                arcade.draw_circle_filled(stx, sty, 30, MOL_BLUE)
                                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 20)
                                arcade.draw_circle_filled(stx, sty, 25, arcade.color.WHITE)
                                arcade.draw_circle_filled(enx, eny, 25, arcade.color.WHITE)
                                radius.position = enx, eny
                    w += 1

        self.update_slovar()

    def return_position(self):
        if self.tp:
            return self.en_x, self.en_y


class GnevTora(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = GNEV_TORA
        self.uron = URON_GNEV_TORA

        self.radius = hit_box_and_radius.Radius(0.5)

        self.timer_for_s_kd = S_KD_GENV_TORA
        self.s_kd = self.timer_for_s_kd

        self.timer_for_s_oglush = S_OGLUSH_GNEV_TORA

        self.minus_mana = MINUS_MANA_GNEV_TORA

    def update_animation(self, delta_time: float = 1 / 60):
        if self.action and self.mana and not self.kd:
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 250, MOL_BLUE)
            arcade.draw_circle_filled(self.pers.position[0], self.pers.position[1], 150, arcade.color.WHITE)

    def on_update(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor(self.uron)

        self.kd_timer_stamina()

        for sprite in self.sprite_list:
            if self.radius.check_collision(sprite) and self.action and self.mana:
                self.udar(sprite)
                self.oglush(sprite)

        if self.s == 1:
            self.func_mana()

        self.update_slovar()


class StreliPeruna(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = STRELI_PERUNA
        self.uron = URON_STRELI_PERUNA

        self.radius = hit_box_and_radius.Radius(2.5)

        self.timer_for_s_kd = S_KD_STRELI_PERUNA
        self.s_kd = self.timer_for_s_kd

        self.timer_for_s_oglush = S_OGLUSH_STRELI_PERUNA

        self.minus_mana = MINUS_MANA_STRLI_PERUNA

    def update_animation(self, delta_time: float = 1 / 60):
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor(self.uron)

        self.kd_timer_stamina()

        if self.action and self.radius.check_collision(sprite_list=self.sprite_list):
            spis_pos = []
            spis1 = []
            spis_rast = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite) and sprite.hp > 0:
                    spis_pos.append(sprite.position)
                    rx = abs(self.pers.center_x - sprite.center_x)
                    ry = abs(self.pers.center_y - sprite.center_y)
                    rast = math.hypot(rx, ry)
                    spis_rast.append((rx, ry))
                    spis1.append(rast)

            if len(spis_rast) <= 0:
                self.action = False
                self.s_kd = self.timer_for_s_kd

            for i in spis1:
                if len(spis1) > 5:
                    index = spis1.index(max(spis1))
                    spis_pos.pop(index)
                    spis1.remove(max(spis1))
                    spis_rast.pop(index)
                elif len(spis1) < 1:
                    return
                else:
                    break

            stx, sty = self.radius.position

            mnozh = len(spis1)

            while len(spis1) >= 1:
                enx, eny = min(spis_pos)
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny) and self.action and self.mana:
                        self.udar(sprite)
                        self.oglush(sprite)

                spis1.remove(spis1[spis_pos.index(min(spis_pos))])
                spis_pos.remove(min(spis_pos))

            if self.s == 1:
                self.timer_for_s_kd *= mnozh
                self.func_mana(self.minus_mana * mnozh)
        if not self.kd and not self.action:
            self.timer_for_s_kd = 30

        self.update_slovar()


class SharMolniay(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = SHAR_MOLNIYA

        self.uron = URON_SHAR_MOL
        self.uron1 = URON1_SHAR_MOL
        self.minus_mana = 1

        self.tex_shar = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.texture = self.tex_shar[1]
        self.scale = 0.01

        self.radius = hit_box_and_radius.Radius()
        self.radius1 = hit_box_and_radius.Radius()

        self.zaryad = False
        self.zaryad_b = False
        self.vzriv = False
        self.promah = False
        self.baf_uron = 1

        self.s_zaryad = 0
        self.timer_for_s_kd = S_KD_SHAR_MOL
        self.s_kd = self.timer_for_s_kd + 1
        self.s_do_promah = 0
        self.s_change_x = 0
        self.s = 0
        self.atak = False

        self.timer_for_s_oglush = S_OGLUSH_SHAR_MOL
        self.oglush1 = 5

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_mor(self.uron)
        uron = self.uron
        self.update_sposob()

        self.s_kd += 1
        self.update_radius_position()
        self.radius1.position = self.position
        if self.s_kd <= self.timer_for_s_kd:
            self.zaryad = False

        if self.change_x == 0:
            self.update_position()

        self.update_slovar()

        if self.zaryad:
            self.action = False
            self.zaryad_b = True
            self.s_zaryad += 1
            if self.s_zaryad < MAX_BAF_S_ZARYAD_SHAR_MOL:
                self.scale += 0.05 / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.baf_uron += BAF_URON_SHAR_MOL / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.minus_mana = 100 / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.timer_for_s_oglush += BAF_FOR_OGLUSH_SHAR_MOL / MAX_BAF_S_ZARYAD_SHAR_MOL
                self.func_mana(self.minus_mana)
                if not self.mana:
                    self.zaryad = False
                    self.s_zaryad = 0
                    self.vzriv = True
                    self.atak = True
                    self.timer_for_s_oglush = 6

        if self.s_zaryad > MAX_S_ZARYAD_SHAR_MOL:
            self.vzriv = True
            self.atak = True
            self.pers.hp -= uron * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
            self.timer_for_s_oglush *= VZRIV_BAF_OGLUSH_SHAR_MOL
            self.oglush(self.pers)
            self.radius1.scale = self.scale * 2
            for sprite in self.sprite_list:
                if self.radius1.check_collision(sprite) and sprite.hp > 0:
                    self.action = False
                    for i in self.slovar:
                        if sprite == i and not self.slovar[i]:
                            self.slovar[i] = True
                            sprite.hp -= uron * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
                            self.oglush(sprite)
            self.s_zaryad = 0
            self.zaryad = False
            self.s_kd = 0

        if (self.action and self.zaryad_b) or self.atak:
            self.zaryad = False
            self.s_do_promah += 1
            self.s_zaryad = 0
            if self.s_change_x == 0:
                self.s_kd = 0
                self.s_change_x = 1
                if self.pers.storona == 0:
                    self.change_x = SKOROST_SHAR_MOL
                else:
                    self.change_x = -SKOROST_SHAR_MOL

            if arcade.check_for_collision_with_list(self, self.sprite_list):
                self.atak = True
                self.radius1.scale = self.scale * 1.5
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite) and sprite.hp > 0:
                        self.action = False
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron)
                                self.oglush(sprite)

            if self.s_do_promah >= S_DO_PROMAH_SHAR_MOL:
                self.promah = True
                self.action = False
                self.atak = True
                self.s_do_promah = 0
                self.timer_for_s_oglush /= DEBAF_FOR_OGLUSH_SHAR_MOL
                for sprite in self.sprite_list:
                    if self.radius1.check_collision(sprite) and sprite.hp > 0:
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                sprite.hp -= uron * round(self.baf_uron) / PROMAH_DEBAF_URON_SHAR_MOL
                                self.oglush(sprite)

        elif not self.action and not self.atak:
            self.change_x = 0
            if not self.promah and self.vzriv:
                for i in self.slovar:
                    self.slovar[i] = False
            if not self.zaryad:
                self.baf_uron = 1
                self.zaryad_b = False
                self.scale = 0.01
                self.s_change_x = 0
                self.minus_mana = 1

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        uron1 = self.uron1
        if self.atak or self.zaryad or self.action:
            arcade.draw_circle_filled(self.center_x, self.center_y, 90, (44, 117, 255, 50), 5)
        if self.atak:
            self.timer_for_s_oglush /= self.oglush1
            self.s += 1
            if self.s > self.timer_for_s:
                self.atak = False
                self.promah = False
                self.vzriv = False
                self.s = 0
            spisok_rast = []
            spisok_xy = []
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite) and sprite.position != self.radius.position and sprite.hp > 0:
                    rast = (abs(self.radius.center_x - sprite.center_x),
                            abs(self.radius.center_y - sprite.center_y))
                    xy = sprite.position
                    spisok_rast.append(rast)
                    spisok_xy.append(xy)

            if len(spisok_rast) > 0:
                if self.vzriv:
                    self.timer_for_s_oglush *= VZRIV_BAF_OGLUSH_SHAR_MOL
                elif self.promah:
                    self.timer_for_s_oglush /= PROMAH_DEBAF_URON_SHAR_MOL

            if len(spisok_rast) > 5:
                while len(spisok_rast) > 5:
                    max_index = spisok_rast.index(max(spisok_rast))
                    spisok_rast.remove(spisok_rast[max_index])
                    spisok_xy.remove(spisok_xy[max_index])

            stx, sty = self.position
            while len(spisok_rast) >= 1:
                min_index = spisok_rast.index(min(spisok_rast))
                enx, eny = spisok_xy[min_index]
                arcade.draw_line(stx, sty, enx, eny, MOL_BLUE, 25)
                arcade.draw_line(stx, sty, enx, eny, arcade.color.WHITE, 15)
                for sprite in self.sprite_list:
                    if sprite.position == (enx, eny):
                        for i in self.slovar:
                            if sprite == i and not self.slovar[i]:
                                self.slovar[i] = True
                                if self.vzriv:
                                    sprite.hp -= uron1 * VZRIV_BAF_URON_SHAR_MOL * round(self.baf_uron)
                                    self.oglush(sprite)
                                elif self.promah:
                                    sprite.hp -= uron1 * round(self.baf_uron) / PROMAH_DEBAF_URON_SHAR_MOL
                                    self.oglush(sprite)
                                else:
                                    sprite.hp -= uron1 * round(self.baf_uron)
                                    self.oglush(sprite)
                spisok_rast.remove(spisok_rast[min_index])
                spisok_xy.remove(spisok_xy[min_index])

        if self.s == 1:
            if self.vzriv:
                self.func_mana(round(self.minus_mana * 1.2))
            else:
                self.func_mana(self.minus_mana)


class UdarZevsa(Molniya):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = UDAR_ZEVSA
        self.uron = URON_UDAR_ZEVSA

        self.timer_for_s_kd = S_KD_UDAR_ZEVSA
        self.s_kd = self.timer_for_s_kd + 5

        self.timer_for_s = S_UDAR_ZEVSA
        self.timer_for_s_oglush = S_OGLUSH_UDAR_ZEVSA

        self.radius = hit_box_and_radius.Radius(1.5)

        self.rast = 0
        self.slovar_rast = {}
        self.s1 = 0
        self.line_width = 15
        self.minus_mana = 2

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_position()
        self.update_radius_position()
        self.update_sposob()
        self.update_mor(self.uron)

        self.kd_timer_mana()

        if self.action:
            self.s1 = 1
            if len(self.slovar_rast) == 0:
                for sprite in self.sprite_list:
                    if self.radius.check_collision(sprite) and sprite.hp > 0:
                        rast_x = abs(sprite.center_x - self.pers.center_x)
                        rast_y = abs(sprite.center_y - self.pers.center_y)
                        rast = math.hypot(rast_x, rast_y)
                        self.slovar_rast.update({sprite: rast})

            if len(self.slovar_rast) == 0:
                self.action = False
                self.s_kd = self.timer_for_s_kd + 1
            else:
                if self.s % 30 == 0:
                    self.timer_for_s_kd += 30
                    self.uron *= BAF_URON_UDAR_ZEVSA
                    self.minus_mana *= 1.35
                    self.timer_for_s_oglush *= BAF_FOR_OGLUSH_UDAR_ZEVSA
                    self.func_mana(round(self.minus_mana))
                    self.line_width *= 1.1
                    for i in self.slovar:
                        self.slovar[i] = False

                self.rast = min(self.slovar_rast.values())
                for sprite in self.slovar_rast:
                    if self.slovar_rast[sprite] == self.rast:
                        if sprite.hp <= 0:
                            self.action = False
                            break
                        else:
                            self.udar(sprite)
                            self.oglush(sprite)
        else:
            if self.s1 == 1:
                self.s_kd = 0
                self.s1 -= 1
            if self.s_kd > self.timer_for_s_kd:
                self.timer_for_s_kd = S_KD_UDAR_ZEVSA
            self.rast = 0
            self.slovar_rast.clear()
            self.uron = URON_UDAR_ZEVSA
            self.line_width = 15
            self.minus_mana = 2
            self.timer_for_s_oglush = 12

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.action:
            for sprite in self.slovar_rast:
                if self.slovar_rast[sprite] == self.rast:
                    arcade.draw_line(self.pers.center_x, self.pers.center_y, sprite.center_x, sprite.center_y,
                                     MOL_BLUE, self.line_width)
                    break


# Стихия воды
V_LIST = []
'''list[str]'''


class Voda(StihiyaFight, DvizhSprite):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list)
        self.podklass = VODA

        self.degree_block = 0.2
        self.force_for_block = -1
        self.minus_for_block = -1
        self.probit_block = True

        self.min_v = 0
        self.minus_v = minus_v
        self.minus_max_v = 0
        self.v_max_minus = False
        self.s_v_max_minus = 0
        self.kritik = False

    def update_v(self):
        if self.s == 1:
            for pers in V_LIST:
                if pers.v >= self.minus_v and pers == self.pers:
                    pers.v -= self.minus_v
                else:
                    self.action = False
                    self.s = 0

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

    def func_for_init(self):
        if self.min_v > self.minus_v:
            self.minus_v = self.min_v
        self.scale = self.minus_v / 60

    def sbiv(self, sprite):
        if not sprite.smert:
            sprite.rotation = True
            # sprite.position_new = True
            # sprite.new_position = (sprite.center_x, 160)

    def update_sbiv(self):
        for sprite in self.sprite_list:
            if sprite.rotation and not sprite.oglush:
                sprite.rotation = False
                # sprite.position_new = False


class VodoHod(Voda):
    def __init__(self, pers, sprite_list, minus_v, igrok=False):
        super().__init__(pers, sprite_list, minus_v)
        self.tip = VODOHOD
        self.igrok = igrok
        self.max_ver_vel = 0
        # self.voda = voda
        #
        # self.mass = 0

        # self.dvizh_force = (0, 2700)
        # self.pers.vodohod = True
        # self.izmen_vel = False
        # self.dvizh_vel = (300, 2000)

    def hod(self, change_x, wall_list):
        if self.pers.oglush:
            self.action = False
        if self.action:
            self.pers.oglush_for_sposob = True
            if not arcade.check_for_collision_with_list(self, wall_list):
                self.change_y -= 1 / 2
            else:
                self.change_y = 1 / 2
            self.change_x = change_x
            self.fizika.set_position(self.pers, (self.center_x, self.top + 64))
        else:
            self.pers.oglush_for_sposob = False
            self.change_x = 0
            self.change_y = 0
        # if arcade.check_for_collision(self.voda, self.pers):
        #     self.action = True
        #     self.dvizh_pers_func()
        # else:
        #     self.action = False
        # self.update_passive_dvizh()


class Sputnik(Voda):
    def __init__(self, pers, sprite_list, vektor=1, szhatie_x=1, szhatie_y=1, minus_v=18):
        super().__init__(pers, sprite_list, minus_v)
        self.min_v = 18
        self.sposob = SPUTNIK
        self.uron = URON_SPUTNIK
        self.timer_for_s = S_SPUNNIK
        self.timer_for_s_kd = S_KD_SPUTNIK
        self.timer_for_s_oglush = 30
        self.s_kd = self.timer_for_s_kd + 1
        self.minus_mana = SPUTNIK_MINUS_MANA
        self.dvizh_force = (5000, 500)
        self.dvizh_vel = (100, 0)
        self.vektor = vektor
        self.szhatie_x = szhatie_x
        self.szhatie_y = szhatie_y

        self.fight = False
        self.rast = 0
        self.slovar_rast = {}

        self.radius = hit_box_and_radius.Radius(1.5)
        self.tex_sputnik = arcade.load_texture_pair('nuzhno/sputnik.png')
        self.texture = self.tex_sputnik[0]
        self.func_for_init()
        self.position = self.pers.center_x, self.pers.center_y - 64
        self.v_x = 0
        self.v_y = 0
        self.pred_x = self.pers.center_x
        self.pred_y = self.pers.center_y
        self.st = 0
        self.storona_x = 1
        self.storona_y = 1
        self.chetvert = 0
        self.max_change_x = SPUTNIK_CHANGE
        self.max_change_y = SPUTNIK_CHANGE
        self.min_change_x = 0
        self.min_change_y = 0
        self.polet = False
        self.not_draw = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_mor(self.uron)
        self.update_sposob()
        self.update_radius_position()
        self.update_v()

        self.st += 1
        if self.st >= 2:
            self.st = 0
            if self.pred_x != round(self.pers.center_x, 1):
                self.v_x = (round(self.pers.center_x, 1) - self.pred_x) / 2
            else:
                self.v_x = 0
            if self.pred_y != round(self.pers.center_y, 1):
                self.v_y = (round(self.pers.center_y, 1) - self.pred_y) / 2
            else:
                self.v_y = 0
            self.v_x = round(self.v_x, 5)
            self.v_y = round(self.v_y, 5)
            self.pred_x = round(self.pers.center_x, 1)
            self.pred_y = round(self.pers.center_y, 1)

        if self.polet:
            if self.s == 1:
                self.func_mana()
            if not self.mana:
                self.polet = False
                self.fight = False
                self.not_draw = True
                self.s = 0
            self.s += 1
            if self.s >= self.timer_for_s:
                self.s = 0
                self.polet = False
                self.action = False
                self.fight = False
                self.not_draw = True

        if self.action:
            if not self.radius.check_collision(sprite_list=self.sprite_list):
                self.action = False
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite) and sprite.hp > 0:
                    rast_x = abs(abs(self.center_x) - abs(sprite.center_x))
                    rast_y = abs(abs(self.center_y) - abs(sprite.center_y))
                    rast = math.hypot(rast_x, rast_y)
                    self.slovar_rast.update({sprite: rast})

            if len(self.slovar_rast) == 0:
                self.action = False
            else:
                self.not_draw = False

                pos_en = 0
                self.rast = min(self.slovar_rast.values())
                for sprite in self.slovar_rast:
                    if self.slovar_rast[sprite] == self.rast:
                        pos_en = sprite.position

                rast_x = abs(pos_en[0] - self.center_x)
                rast_y = abs(pos_en[1] - self.center_y)

                for sprite in self.sprite_list:
                    if sprite.center_x > self.pers.center_x:
                        self.storona_x = 1
                        if (1 * SPUTNIK_CHANGE >= self.change_x >= 0 and 1 * SPUTNIK_CHANGE >= self.change_y >= 0
                                and self.vektor == 1):
                            self.polet = True
                            self.storona_y = 1
                            self.fight = False
                            if round(rast_x, 1) == round(rast_y, 1):
                                self.change_y = SPUTNIK_CHANGE_UDAR
                                self.change_x = SPUTNIK_CHANGE_UDAR
                            else:
                                self.change_x = SPUTNIK_CHANGE_UDAR
                                self.change_y = rast_y / (rast_x / self.change_x)
                        elif (1 * SPUTNIK_CHANGE >= self.change_x >= 0 and (0 >= self.change_y >= -1 * SPUTNIK_CHANGE)
                                and self.vektor == -1):
                            self.polet = True
                            self.storona_y = -1
                            self.fight = False
                            if round(rast_x, 1) == round(rast_y, 1):
                                self.change_y = -SPUTNIK_CHANGE_UDAR
                                self.change_x = SPUTNIK_CHANGE_UDAR
                            else:
                                self.change_x = SPUTNIK_CHANGE_UDAR
                                self.change_y = -rast_y / (rast_x / self.change_x)
                    elif sprite.center_x < self.pers.center_x:
                        self.storona_x = -1
                        if (0 > self.change_x >= -1 * SPUTNIK_CHANGE and 0 >= self.change_y >= -1 * SPUTNIK_CHANGE
                                and self.vektor == 1):
                            self.polet = True
                            self.storona_y = -1
                            self.fight = False
                            if round(rast_x, 1) == round(rast_y, 1):
                                self.change_y = -SPUTNIK_CHANGE_UDAR
                                self.change_x = -SPUTNIK_CHANGE_UDAR
                            else:
                                self.change_x = -SPUTNIK_CHANGE_UDAR
                                self.change_y = rast_y / (rast_x / self.change_x)
                        elif (0 > self.change_x >= -1 * SPUTNIK_CHANGE and (1 * SPUTNIK_CHANGE >= self.change_y >= 0)
                                and self.vektor == -1):
                            self.polet = True
                            self.storona_y = 1
                            self.fight = False
                            if round(rast_x, 1) == round(rast_y, 1):
                                self.change_y = SPUTNIK_CHANGE_UDAR
                                self.change_x = -SPUTNIK_CHANGE_UDAR
                            else:
                                self.change_x = -SPUTNIK_CHANGE_UDAR
                                self.change_y = -rast_y / (rast_x / self.change_x)

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite) and sprite.hp > 0:
                        self.polet = False
                        self.action = False
                        self.udar(sprite)
                        self.oglush(sprite)
                        self.storona = self.storona_x
                        self.dvizh_sprite_func(sprite)
        else:
            self.slovar_rast = {}
            self.change_x = 0
            self.change_y = 0
            self.s = 0
            self.polet = False

        if self.fight:
            self.not_draw = False
            self.change_angle = 5
            angle_radians = math.radians(round(self.angle))
            self.change_x = (self.vektor * math.cos(angle_radians) * SPUTNIK_CHANGE) / self.szhatie_x + self.v_x# self.szhatie_x
            self.change_y = (math.sin(angle_radians) * SPUTNIK_CHANGE) / self.szhatie_y + self.v_y

            if 1 * SPUTNIK_CHANGE >= self.change_x > 0 and 1 * SPUTNIK_CHANGE >= self.change_y > 0:
                self.chetvert = 1
            elif 0 >= self.change_x > -1 * SPUTNIK_CHANGE and (1 * SPUTNIK_CHANGE > self.change_y >= 0):
                self.chetvert = 2
            elif 0 > self.change_x >= -1 * SPUTNIK_CHANGE and 0 > self.change_y >= -1 * SPUTNIK_CHANGE:
                self.chetvert = 3
            elif 1 * SPUTNIK_CHANGE > self.change_x > 0 and (0 > self.change_y > -1 * SPUTNIK_CHANGE):
                self.chetvert = 4

            self.max_change_x = SPUTNIK_CHANGE + self.v_x
            self.max_change_y = SPUTNIK_CHANGE + self.v_y
            self.min_change_x = 0 + self.v_x
            self.min_change_y = 0 + self.v_y

        if not self.action and not self.fight:
            self.not_draw = True
            self.position = self.pers.center_x, self.pers.center_y - 64
            self.change_x = 0
            self.change_y = 0
            self.angle = 0
            self.polet = False

        self.update_slovar_dvizh()
        self.update_dvizh_sprite()
        self.update_slovar()


class Sputniki(Voda):
    def __init__(self, pers, sprite_list, kol_vo=1, minus_v=18):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = SPUTNIKI
        self.voda = True

        self.kol_vo = kol_vo
        self.minus_max_v = self.minus_v * self.kol_vo
        self.v_max_minus = False

        self.sputnik_slovar = {}
        self.polet_list = arcade.SpriteList()
        self.fight = False
        self.fight_s = 0

        self.len = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_v()
        if self.fight:
            if not self.kritik:
                self.v_max_minus = True
            if self.kritik:
                self.kol_vo = 0
            else:
                self.kol_vo = 4
            if len(self.sputnik_slovar) < self.kol_vo:
                self.len = len(self.sputnik_slovar) + 1
                if len(self.sputnik_slovar) < self.kol_vo:
                    if len(self.sputnik_slovar) == 0:
                        sputnik = Sputnik(self.pers, self.sprite_list, minus_v=self.minus_v)
                        sputnik.pred_vel_x = self.pred_vel_x
                        self.sputnik_slovar.update({len(self.sputnik_slovar) + 1: sputnik})
                    else:
                        s = 0
                        while len(self.sputnik_slovar) < self.len:
                            a = 0
                            for sputnik_polet in self.sputnik_slovar:
                                if 0 < s < 5 and s != sputnik_polet:
                                    for sputnik in self.sputnik_slovar:
                                        if sputnik == s:
                                            a += 1
                                    if a == 0:
                                        sputnik = Sputnik(self.pers, self.sprite_list, minus_v=self.minus_v)
                                        sputnik.pred_vel_x = self.pred_vel_x
                                        self.sputnik_slovar.update({s: sputnik})
                                        break
                            s += 1

            q = 0
            for sputnik_polet1 in self.sputnik_slovar:
                sputnik = self.sputnik_slovar[sputnik_polet1]
                if sputnik.fight:
                    q += 1
            if q == 0:
                self.fight_s = 0

            if len(self.sputnik_slovar) == self.kol_vo:
                for sputnik_polet in self.sputnik_slovar:
                    if sputnik_polet == 1 and self.fight_s < 1:
                        self.sputnik_slovar[sputnik_polet].fight = True
                        self.fight_s += 1
                    if not self.sputnik_slovar[sputnik_polet].fight:
                        if self.fight_s == 1:
                            sputnik_fight = None
                            for sputnik_polet1 in self.sputnik_slovar:
                                if self.sputnik_slovar[sputnik_polet1].fight:
                                    sputnik_fight = sputnik_polet1
                            if sputnik_fight is not None and self.sputnik_slovar[sputnik_fight].__angle >= 90:
                                self.sputnik_slovar[sputnik_polet].fight = True
                                self.fight_s += 1
                        elif self.fight_s == 2:
                            sputnik_fight1 = None
                            sputnik_fight2 = None
                            s = 0
                            for sputnik_polet1 in self.sputnik_slovar:
                                if self.sputnik_slovar[sputnik_polet1].fight and s == 0:
                                    sputnik_fight1 = sputnik_polet1
                                    s += 1
                                elif self.sputnik_slovar[sputnik_polet1].fight and s == 1:
                                    sputnik_fight2 = sputnik_polet1

                            if sputnik_fight1 is not None and sputnik_fight2 is not None:
                                if (self.sputnik_slovar[sputnik_fight2].__angle >= 180
                                        and self.sputnik_slovar[sputnik_fight1].__angle >= 90):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 90
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 180):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 270
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 90):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 90
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 270):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                        elif self.fight_s == 3:
                            sputnik_fight1 = None
                            sputnik_fight2 = None
                            sputnik_fight3 = None
                            s = 0
                            for sputnik_polet1 in self.sputnik_slovar:
                                if self.sputnik_slovar[sputnik_polet1].fight and s == 0:
                                    sputnik_fight1 = sputnik_polet1
                                    s += 1
                                elif self.sputnik_slovar[sputnik_polet1].fight and s == 1:
                                    sputnik_fight2 = sputnik_polet1
                                    s += 1
                                elif self.sputnik_slovar[sputnik_polet1].fight and s == 2:
                                    sputnik_fight3 = sputnik_polet1

                            if sputnik_fight1 is not None and sputnik_fight2 is not None and sputnik_fight3 is not None:
                                if (self.sputnik_slovar[sputnik_fight2].__angle >= 180
                                        and self.sputnik_slovar[sputnik_fight1].__angle >= 90
                                        and self.sputnik_slovar[sputnik_fight3].__angle >= 270):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 90
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 180
                                      and self.sputnik_slovar[sputnik_fight3].__angle >= 270):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 270
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 90
                                      and self.sputnik_slovar[sputnik_fight3].__angle >= 180):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 90
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 270
                                      and self.sputnik_slovar[sputnik_fight3].__angle >= 180):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 180
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 270
                                      and self.sputnik_slovar[sputnik_fight3].__angle >= 90):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1
                                elif (self.sputnik_slovar[sputnik_fight2].__angle >= 270
                                      and self.sputnik_slovar[sputnik_fight1].__angle >= 180
                                      and self.sputnik_slovar[sputnik_fight3].__angle >= 90):
                                    self.sputnik_slovar[sputnik_polet].fight = True
                                    self.fight_s += 1

            for sputnik_polet in self.sputnik_slovar:
                sputnik = self.sputnik_slovar[sputnik_polet]
                sputnik.minus_v = self.minus_v
                sputnik.pred_vel_x = self.pred_vel_x
                sputnik.on_update()
                sputnik.update()
                if sputnik.fight:
                    for sprite in self.sprite_list:
                        if sprite.center_x > sputnik.center_x and sputnik.chetvert == 1 and self.action:
                            sputnik.action = True
                            self.action = False
                            self.fight_s -= 1
                            self.s += 1
                            break
                        elif sprite.center_x < sputnik.center_x and sputnik.chetvert == 3 and self.action:
                            sputnik.action = True
                            self.action = False
                            self.fight_s -= 1
                            self.s += 1
                            break

            for sputnik in self.sputnik_slovar:
                if self.sputnik_slovar[sputnik].action:
                    self.polet_list.append(self.sputnik_slovar[sputnik])
                    self.sputnik_slovar.pop(sputnik)
                    self.fight_s -= 1
                    break

            for sputnik in self.polet_list:
                sputnik.update()
                sputnik.on_update()

            for sputnik in self.polet_list:
                if not sputnik.polet and not sputnik.action and not sputnik.dvizh:
                    self.polet_list.remove(sputnik)
                    break
        else:
            self.v_max_minus = False

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        for sputnik in self.sputnik_slovar:
            if not self.sputnik_slovar[sputnik].not_draw:
                self.sputnik_slovar[sputnik].draw()

        for sputnik in self.polet_list:
            if not sputnik.not_draw:
                sputnik.draw()


class VodaUdar(Voda):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.min_v = 18
        self.sposob = VODA_UDAR
        self.uron = 50
        self.change = 15
        self.probit_block = False

        self.timer_for_s = 60
        self.timer_for_s_kd = 60
        self.timer_for_s_oglush = 5
        self.timer_for_s_dvizh = 5
        self.s_kd = self.timer_for_s_kd
        self.minus_mana = 2
        self.dvizh_force = (3000, 1000)
        self.dvizh_vel = (100, 0)

        self.rast = 0
        self.slovar_rast = {}

        self.radius = hit_box_and_radius.Radius(1.5)
        self.tex_sputnik = arcade.load_texture_pair('nuzhno/sputnik.png')
        self.texture = self.tex_sputnik[0]
        self.func_for_init()
        self.position = self.pers.center_x, self.pers.center_y - 64

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)
        self.update_v()
        self.update_radius_position()
        self.kd_timer_stamina()

        if not self.radius.check_collision(sprite_list=self.sprite_list):
            self.action = False
        else:
            s = 0
            for sprite in self.sprite_list:
                if sprite.hp <= 0:
                    s += 1

            if len(self.sprite_list) == s:
                self.action = False

        if self.action:
            for sprite in self.sprite_list:
                if self.radius.check_collision(sprite) and sprite.hp > 0:
                    rast_x = abs(self.center_x - sprite.center_x)
                    rast_y = abs(self.center_y - sprite.center_y)
                    rast = math.hypot(rast_x, rast_y)
                    self.slovar_rast.update({sprite: rast})

            if len(self.slovar_rast) > 0:
                self.rast = min(self.slovar_rast.values())
            else:
                self.action = False
            for sprite in self.slovar_rast:
                if self.slovar_rast[sprite] == self.rast and sprite.hp > 0:
                    rast_x = abs(sprite.center_x - self.center_x)
                    rast_y = abs(sprite.center_y - self.center_y)
                    self.update_storona(sprite)
                    self.change_x = self.change * self.storona
                    if self.center_y <= sprite.center_y:
                        self.change_y = rast_y / (rast_x / self.change_x) * self.storona
                        break
                    else:
                        self.change_y = rast_y / (rast_x / self.change_x)
                        if self.change_y > 0:
                            self.change_y *= -1

            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self) and sprite.hp > 0:
                    self.s += self.timer_for_s
                    if self.udar_or_block(sprite):
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite)
        else:
            self.change_x = 0
            self.change_y = 0
            self.slovar_rast.clear()
            self.update_position()

        self.update_slovar_dvizh()
        self.update_dvizh_sprite()
        self.update_slovar()


class VodaUdars(Voda):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = VODA_UDARS

        self.timer_for_s_kd = 15

        self.vu_list = arcade.SpriteList()
        for i in range(6):
            voda_udar = VodaUdar(self.pers, self.sprite_list, self.minus_v)
            self.vu_list.append(voda_udar)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_v()

        if not self.kritik:
            self.v_max_minus = True
        if self.kritik:
            self.kol_vo = 0
        else:
            self.kol_vo = 6

        for vu in self.vu_list:
            vu.fizika = self.fizika
            vu.on_update()
            vu.update()
            vu.pred_vel_x = self.pred_vel_x
            vu.sprite_list = self.sprite_list

        if self.timer_for_s_kd >= self.s_kd > 0:
            self.s_kd += 1
            self.action = False
        else:
            self.s_kd = 0

        if self.action:
            for vu in self.vu_list:
                if not vu.action and not vu.kd:
                    vu.action = True
                    self.action = False
                    self.s_kd += 1
                    break

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        for vu in self.vu_list:
            if vu.action:
                vu.draw()
                # vu.draw_hit_box()


class Volna(Voda):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.uron = 300
        self.minus_mana = 10
        self.sposob = VOLNA

        self.action_2 = True
        self.timer_for_s_2 = 15
        self.timer_for_s = 180 + self.timer_for_s_2
        self.timer_for_s_kd = 420
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = self.timer_for_s

        self.dvizh_force = (30000, 0)
        self.dvizh_vel = (900, 0)
        self.volna_tex = arcade.load_texture_pair('nuzhno/volna.png')
        self.texture = self.volna_tex[0]
        self.radius = hit_box_and_radius.Radius(2)
        self.s1 = 0
        self.min_v = 120
        self.func_for_init()

    # def pymunk_moved(self, physics_engine, dx, dy, d_angle):
    #     self.fizika = physics_engine

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_mor(self.uron)
        self.update_sposob()
        self.update_radius_position()
        self.kd_timer_mana()
        self.update_v()

        if self.s == 1:
            self.func_mana()

        if not self.action:
            self.update_position()
        else:
            if self.s_2 <= self.timer_for_s_2:
                self.pers.stan_for_sposob = True
                self.s_2 += 1
                self.action_2 = False
                self.update_position()
            else:
                self.pers.stan_for_sposob = False
                self.action_2 = True
            if self.s == self.timer_for_s_2 + 1:
                if self.pers.storona == 0:
                    self.change_x = 15
                else:
                    self.change_x = -15

            if self.action_2:
                for sprite in self.sprite_list:
                    if arcade.check_for_collision(sprite, self) and sprite.hp > 0:
                        self.udar(sprite)
                        self.timer_for_s_oglush = (self.timer_for_s - self.s) + 90
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite)

        self.update_slovar_dvizh()
        #for sprite in self.sprite_list:
        self.update_dvizh_sprite(self.timer_for_s - self.s)
        self.update_slovar()


class RechnoyDrakon(Voda):
    def __init__(self, pers, sprite_list, minus_v, rast, viev: arcade.View):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = RECHNOY_DRAKON

        self.uron = 500
        self.minus_mana = 10
        self.min_v = 120

        self.timer_for_s_zaderzh = 30
        self.s_zaderzh = 0
        self.timer_for_s = 180 + self.timer_for_s_zaderzh
        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = self.timer_for_s
        self.dvizh_force = (60000, 0)
        self.dvizh_vel = (600, 0)

        self.force_for_block = 1000000
        self.minus_for_block = 10
        self.probit_block = False

        self.radius = hit_box_and_radius.Radius()
        self.rechnoy_drakon_tex = arcade.load_texture_pair('nuzhno/rechnoy_drakon.png')
        self.texture = self.rechnoy_drakon_tex[1]
        self.func_for_init()

        self.normal_scale_xy = self.scale_xy
        self.max_widht = 1100
        self.vr_widht = 10000
        self.plus = True
        self.blizh_sprite = None

        self.stopp = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_slovar()
        self.update_v()
        self.update_mor(self.uron)
        self.update_radius_position()
        self.kd_timer_mana()

        if self.s == 1:
            self.func_mana()

        if self.action:
            self.pers.stan_for_sposob = True
            if self.s_zaderzh <= self.timer_for_s_zaderzh:
                self.s_zaderzh += 1
            else:
                rast_list = []
                for sprite in self.sprite_list:
                    if sprite.hp > 0:
                        rast_list.append(abs(sprite.center_x - self.pers.center_x))

                if len(rast_list) > 0:
                    min_rast = min(rast_list)
                    for sprite in self.sprite_list:
                        #print(rast_list)
                        if abs(sprite.center_x - self.pers.center_x) == min_rast:
                            self.vr_widht = min_rast
                            self.blizh_sprite = sprite

                    if arcade.check_for_collision(self.blizh_sprite, self):
                        self.plus = False
                    else:
                        self.plus = True

                if self.vr_widht < self.width and not self.plus:
                    self.width = self.vr_widht
                if self.width <= self.max_widht and self.plus:
                    self.scale_xy = (self.scale_xy[0] + 1.35, self.scale_xy[1])
                if self.pers.storona == 0:
                    self.left = self.pers.center_x
                else:
                    self.right = self.pers.center_x
                self.center_y = self.pers.center_y

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite):
                        if self.udar_or_block(sprite):
                            self.timer_for_s_oglush = (self.timer_for_s - self.s) + 90
                            self.oglush(sprite)
                            self.dvizh_sprite_func(sprite)
        else:
            self.pers.stan_for_sposob = False
            self.s_zaderzh = 0
            self.scale_xy = self.normal_scale_xy
            self.update_position()

        self.update_slovar_dvizh()
        self.update_dvizh_sprite(self.timer_for_s - self.s)


class UdarKita(Voda):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = UDAR_KITA

        self.uron = 2000
        self.minus_mana = 20

        self.timer_for_zaderzh = 60
        self.timer_for_s = 18 + self.timer_for_zaderzh
        self.timer_for_s_kd = 1200
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = 300
        self.timer_for_s_dvizh = 15
        self.dvizh_force = (0, -20000)
        self.dvizh_vel = (10, 0)

        self.min_v = 300

        self.radius = hit_box_and_radius.Radius(2)
        self.tex_udar_kita = arcade.load_texture_pair('nuzhno/UdarKita.png')
        self.texture = self.tex_udar_kita[0]

        self.func_for_init()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_v()
        self.update_mor(self.uron)
        self.update_radius_position()
        self.update_position()
        self.kd_timer_mana()

        if self.s == 1:
            self.func_mana()

        if self.action:
            self.bottom = self.pers.bottom
            if self.s <= self.timer_for_zaderzh:
                self.pers.stan_for_sposob = True
            else:
                self.pers.stan_for_sposob = False
                if self.s == self.timer_for_zaderzh + 1:
                    if self.pers.storona == 0:
                        self.change_angle = 5
                    else:
                        self.change_angle = -5
                if self.change_angle > 0:
                    self.left = self.pers.center_x - 32
                else:
                    self.right = self.pers.center_x + 32

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(sprite, self) and sprite.hp > 0:
                        self.udar(sprite)
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite)
        else:
            self.angle = 0
            self.change_angle = 0

        self.update_slovar_dvizh()
        self.update_dvizh_sprite()
        self.update_slovar()


class Tayfun(Voda):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = TAYFUN

        self.uron = 500
        self.minus_mana = 10
        self.min_v = 180

        self.timer_for_s = 45
        self.timer_for_s_kd = 300
        self.s_kd = self.timer_for_s_kd + 1
        self.timer_for_s_oglush = 180
        self.timer_for_s_dvizh = 60
        self.dvizh_force = (80000, 0)
        self.dvizh_vel = (800, 0)

        self.texture_tayfun = arcade.load_texture_pair('nuzhno/tayfun.png')
        self.texture = self.texture_tayfun[0]

        self.func_for_init()
        self.noramal_scale = self.scale

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_v()
        self.update_mor(self.uron)
        self.update_position()
        self.kd_timer_mana()

        if self.s == 1:
            self.func_mana()

        if self.action:
            self.scale += 0.5
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar(sprite)
                    self.dvizh_sprite_func(sprite)
                    self.oglush(sprite)
        else:
            self.scale = self.noramal_scale

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_dvizh_sprite()


class Hlist(Voda):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.sposob = HLIST

        self.uron = 125
        self.minus_mana = 3
        self.min_v = 30
        self.probit_block = False

        self.timer_for_s = 20
        self.timer_for_s_kd = 60
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_oglush = 60
        self.timer_for_s_dvizh = 60
        self.dvizh_force = (4000, 0)
        self.dvizh_vel = (100, 0)

        self.texture_hlist = arcade.load_texture_pair('nuzhno/hlist1.png')
        self.texture = self.texture_hlist[0]

        self.func_for_init()
        self.normal_scale_xy = self.scale_xy

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_v()
        self.update_mor(self.uron)
        self.kd_timer_mana()
        if self.pers.storona == 0:
            self.left, self.center_y = self.pers.position
        else:
            self.right, self.center_y = self.pers.position

        if self.s == 1:
            self.func_mana()

        if self.action:
            self.scale_xy = (self.scale_xy[0] + 1.75, self.scale_xy[1])
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and sprite.hp > 0:
                    self.s += self.timer_for_s
                    if self.udar_or_block(sprite):
                        self.oglush(sprite)
                        self.dvizh_sprite_func(sprite)
                        self.sbiv(sprite)
        else:
            self.scale_xy = self.normal_scale_xy

        self.update_slovar()
        self.update_slovar_dvizh()
        self.update_sbiv()
        self.update_dvizh_sprite()


class VodaShchit(Voda, Block):
    def __init__(self, pers, sprite_list, minus_v):
        super().__init__(pers, sprite_list, minus_v)
        self.position = 100, 200

        self.uron = 10
        self.minus_mana = 10
        self.min_v = 300

        self.timer_for_s_oglush = 20

        self.block_texture = arcade.load_texture_pair('nuzhno/VodaShchit.png')
        self.texture = self.block_texture[1]

        self.dvizh_force = (20000, 0)
        self.fors = self.dvizh_force
        self.dvizh_vel = (350, 0)
        #self.update_timer = False
        self.false = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.dvizh_vel = (self.pers.pymunk.max_horizontal_velocity, 0)
        if not self.pers.walk and not self.pers.beg:
            self.dvizh_force = (0, 0)
            self.timer_for_s_oglush = 60
        else:
            self.dvizh_force = self.fors
            self.timer_for_s_oglush = 20

        self.update_sposob()
        self.update_v()
        self.update_mor(self.uron)

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    # self.oglush(sprite)
                    self.dvizh_sprite_func(sprite)
                    self.false = True

        self.center_y = self.pers.center_y
        if self.pers.storona == 1:
            self.center_x = self.pers.center_x - 100
        else:
            self.center_x = self.pers.center_x + 100

        self.update_slovar_dvizh()
        self.update_dvizh_sprite()
        self.update_slovar()


class Techenie(VodoHod):
    def __init__(self, pers, sprite_list, minus_v, vel: tuple, igrok=False):
        super().__init__(pers, sprite_list, minus_v, igrok)
        self.minus_mana = 1 / 60
        self.sposob = TECHENIE
        self.uron = 5

        self.dvizh_vel = vel
        self.dvizh_force = (50000, -10000)
        self.timer_for_s_dvizh = 30
        self.s_kd = 2

        self.timer_for_s_oglush = 90

        self.minus_max_v = minus_v

        self.techenie_texture = arcade.load_texture_pair('nuzhno/techenie.png')
        self.texture = self.techenie_texture[0]
        self.angle = 90
        self.scale = 1.75
        self.hit_box._points = self.texture.hit_box_points

        #self.func_for_init()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        #print('_0_', self.pers.izmen_force, self.pers.new_force)
        self.update_mor(self.uron)
        self.update_sposob()
        self.update_v()

        if self.action and not self.kritik:
            self.pers.toggle = True
            self.s_kd = 0
            if self.s == 0:
                self.fizika.sprites[self.pers].body.body_type = self.fizika.KINEMATIC
            self.s += 1
            self.func_mana()

            self.v_max_minus = True

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and self.change_x != 0:
                    self.oglush(sprite)
                    self.dvizh_sprite_func(sprite, 1)
                    self.udar(sprite)
                    self.sbiv(sprite)
        else:
            self.s_kd += 1
            if self.s_kd == 1:
                self.fizika.remove_sprite(self.pers)
                self.fizika.add_sprite(self.pers, 1, 1,
                                       max_vertical_velocity=2000,
                                       max_horizontal_velocity=300,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9)
            self.pers.toggle = False
            self.update_position()
            self.v_max_minus = False
            self.s = 0

        self.update_sbiv()

        self.update_slovar_dvizh()
        self.update_dvizh_sprite()
        self.update_slovar()


# Стихия огня


class Ogon(StihiyaFight):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.podklass = OGON

        self.tik_uron = 0
        self.timer_for_s_tik = 0
        self.interval = 30
        self.v = 0

    def tik(self, sprite):
        s = 0
        for sposob in sprite.tik_slovar:
            if sposob == self.sposob:
                sprite.tik_slovar[sposob][0] = True
                s += 1

        if s == 0:
            sprite.tik_slovar.update({self.sposob: [True, 0]})

    def update_tik(self):
        for sprite in self.sprite_list:
            for sposob in sprite.tik_slovar:
                if sposob == self.sposob and sprite.tik_slovar[sposob][0]:
                    sprite.tik_slovar[sposob][1] += 1
                    if sprite.tik_slovar[sposob][1] % self.interval == 0:
                        sprite.hp -= self.tik_uron
                    if sprite.tik_slovar[sposob][1] >= self.timer_for_s_tik:
                        sprite.tik_slovar[sposob][0] = False
                        sprite.tik_slovar[sposob][1] = 0


class FireBall(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = FIRE_BALL

        self.uron = 100
        self.tik_uron = 10
        self.minus_mana = 5
        self.change = 15
        self.v = 3

        self.timer_for_s_zaryad = 30
        self.s_zaryad = 0
        self.timer_for_s = 90 + self.timer_for_s_zaryad
        self.timer_for_s_kd = 240
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 90

        self.tex = arcade.load_texture_pair('nuzhno/fire_ball.png')
        self.scale = 0.1
        self.texture = self.tex[0]
        self.storona = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)

        if self.pers.oglush and self.s_zaryad <= self.timer_for_s_zaryad:
            self.s_zaryad = 0
            self.s += self.timer_for_s * 2
            self.change_x = 0
            self.scale = 0.1

        self.kd_timer_mana()

        if self.action:
            if self.s == 1:
                self.func_mana()
            self.s_zaryad += 1
            if self.s_zaryad <= self.timer_for_s_zaryad:
                if self.pers.storona == 0:
                    self.storona = 1
                else:
                    self.storona = -1
                self.pers.stan_for_sposob = True
                self.update_position()
                self.scale += 0.03
            else:
                self.pers.stan_for_sposob = False
                self.change_x = self.change * self.storona

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite):
                        self.change_x = 0
                        self.s += self.timer_for_s
                        self.udar_or_block(sprite)
                        self.tik(sprite)
                        self.s_zaryad = 0
                        self.scale = 0.1
        else:
            self.change_x = 0
            self.s_zaryad = 0
            self.scale = 0.1
            self.update_position()

        self.update_tik()
        self.update_slovar()


class MiniFireBall(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = MINI_FIRE_BALL

        self.uron = 10
        self.tik_uron = 1
        self.change = 15
        self.minus_mana = 1
        self.v = 1

        self.timer_for_s_zaryad = 15
        self.s_zaryad = 0
        self.timer_for_s = 45 + self.timer_for_s_zaryad
        self.timer_for_s_kd = 30
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 60

        self.tex = arcade.load_texture_pair('nuzhno/mini_fire_ball.png')
        self.scale = 0.1
        self.storona = 1
        self.texture = self.tex[1]

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)
        if self.pers.oglush and self.s_zaryad <= self.timer_for_s_zaryad:
            self.s_zaryad = 0
            self.s += self.timer_for_s * 2
            self.change_x = 0
            self.scale = 0.1
        self.kd_timer_stamina()

        if self.s == 1:
            self.func_mana()

        if self.action:
            self.s_zaryad += 1
            if self.s_zaryad <= self.timer_for_s_zaryad:
                self.pers.stan_for_sposob = True
                if self.pers.storona == 1:
                    self.storona = -1
                else:
                    self.storona = 1
                self.update_position()
                self.scale += 0.06
            else:
                self.pers.stan_for_sposob = False
                self.change_x = self.change * self.storona

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite):
                        self.change_x = 0
                        self.s_zaryad = 0
                        self.scale = 0.1
                        self.s += self.timer_for_s
                        self.udar_or_block(sprite)
                        self.tik(sprite)
        else:
            self.update_position()
            self.change_x = 0
            self.scale = 0.1
            self.s_zaryad = 0

        self.update_tik()
        self.update_slovar()


class YazikiOgnya(Ogon):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.sposob = YAZIKI_OGNYA

        self.uron = 50
        self.tik_uron = 20
        self.minus_mana = 30

        self.timer_for_s = 180
        self.timer_for_s_kd = 420
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 120

        self.tex = arcade.load_texture_pair('nuzhno/fire_ball.png')
        self.texture = self.tex[1]
        self.normal_scale_xy = self.scale_xy
        self.max_widht = 530

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)
        self.kd_timer_mana()
        if self.pers.oglush:
            self.s += self.timer_for_s
            self.pers.stan_for_sposob = False
            self.scale_xy = self.normal_scale_xy
            self.update_position()

        if self.action:
            self.pers.stan_for_sposob = True
            if self.s == 1:
                self.func_mana()

            if self.width <= self.max_widht:
                self.scale_xy = (self.scale_xy[0] + 0.5, self.scale_xy[1])
            if self.pers.storona == 0:
                self.left = self.pers.center_x
            else:
                self.right = self.pers.center_x
            self.center_y = self.pers.center_y

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    if self.s % 30 == 0:
                        self.udar_or_block(sprite, False)
                        self.tik(sprite)
                        sprite.tik_slovar[self.sposob][1] = 0
        else:
            self.pers.stan_for_sposob = False
            self.scale_xy = self.normal_scale_xy
            self.update_position()

        self.update_tik()
        self.update_slovar()


class KulakOgnya(Ogon):
    def __init__(self, pers, sprite_list):
        self.sposob = KULAK_OGNYA

        super().__init__(pers, sprite_list)
        self.uron = 15
        self.tik_uron = 5
        self.minus_mana = 3
        self.change = 12

        self.s_kast = 0
        self.timer_for_s_kast = 15
        self.timer_for_s = 20 + self.timer_for_s_kast
        self.timer_for_s_kd = 60
        self.s_kd = self.timer_for_s_kd
        self.timer_for_s_tik = 60

        self.tex = arcade.load_texture_pair('nuzhno/fire_ball.png')
        self.scale_xy = (self.scale_xy[0] + 3, self.scale_xy[1])
        self.texture = self.tex[1]
        self.storona = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)
        self.kd_timer_mana()

        if self.action:
            if self.s == 1:
                self.func_mana()

            self.s_kast += 1
            if self.s_kast <= self.timer_for_s_kast:
                if self.pers.storona == 0:
                    self.storona = 1
                else:
                    self.storona = -1
                self.update_position()
            else:
                self.change_x = self.change * self.storona

                for sprite in self.sprite_list:
                    if arcade.check_for_collision(self, sprite):
                        self.udar(sprite)
                        self.tik(sprite)
                        self.change_x = 0
                        self.s += self.timer_for_s
        else:
            self.update_position()
            self.s_kast = 0
            self.change_x = 0

        self.update_tik()
        self.update_slovar()


# Стихия ветра


class Veter(StihiyaFight, DvizhSprite):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.podklass = VETER


class Poriv(Veter):
    def __init__(self, pers, sprite_list):
        super().__init__(pers, sprite_list)
        self.uron = 100
        self.minus_mana = 10
        self.change = 20

        self.timer_for_s = 90
        self.timer_for_s_kd = 240
        self.s_kd = self.timer_for_s_kd

        self.dvizh_force = (20000, 0)
        self.dvizh_vel = (300, 0)

        self.text = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.scale = 0.2
        self.texture = self.text[0]

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)
        self.kd_timer_mana()

        if self.s == 1:
            self.func_mana()

        if self.action:
            if self.s == 1:
                if self.pers.storona == 0:
                    self.change_x = self.change
                else:
                    self.change_x = -self.change

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar(sprite)
                    self.dvizh_sprite_func(sprite)
        else:
            self.update_position()
            self.change_x = 0

        self.update_slovar_dvizh()
        self.update_dvizh_sprite(self.timer_for_s - self.s)
        self.update_slovar()


class VeterOtalkivanie(arcade.Sprite):
    def __init__(self, igok, sprite_list):
        super().__init__()
        self.uron = 4

        self.igrok = igok
        self.sprite_list = sprite_list
        self.slovar = {}
        self.s3 = 0

        self.udar = False
        self.atak = False
        self.d = True
        self.s = 0
        self.s1 = 300

        self.force_x = 3000
        self.force_y = 5000

        #self.rad = hit_box_and_radius.Radius(0.5)
        self.tex = arcade.load_texture_pair('nuzhno/radius_porazheniya.png')
        self.scale = 0.5
        self.texture = self.tex[1]

        self.max = 5

    def on_update(self, delta_time: float = 1 / 60):
        if self.s3 == 0:
            for sprite in self.sprite_list:
                self.slovar.update({sprite: False})
            self.s3 += 1

        self.s1 += 1

        if self.s1 < 300 and not self.d:
            self.udar = False
        else:
            self.d = True

        if self.s1 >= 300 and self.s == 1:
            self.s1 = 0

        if self.udar:
            start = self.igrok.position
            if self.change_x == 0:
                self.position = start

            if self.igrok.storona == 0 and not self.atak:
                self.atak = True
                self.change_x = 10
            elif self.igrok.storona == 1 and not self.atak:
                self.atak = True
                self.change_x = -10
        else:
            self.d = False
            self.atak = False
            self.change_x = 0
            self.s = 0

        if self.s >= 120:
            self.udar = False
            self.s = 0
        if self.udar:
            self.s += 1

        for sprite in self.sprite_list:
            if arcade.check_for_collision(sprite, self) and self.udar:
                for i in self.slovar:
                    if i == sprite and not self.slovar[i]:
                        self.slovar[i] = True
                        sprite.hp -= self.uron

        if not self.udar:
            for i in self.slovar:
                self.slovar[i] = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture = self.tex[self.igrok.storona]

    def return_force(self, mass, xy: str):
        force_x = self.force_x
        force_y = self.force_y
        if xy == 'x':
            if mass < self.max:
                procent_max = self.max / 100
                procent_x = force_x / 100
                force_x -= procent_x * (mass / procent_max)
                if self.igrok.storona == 1:
                    return force_x
                else:
                    return -force_x
            else:
                return 0
        elif xy == 'y':
            if mass < self.max:
                procent_max = self.max / 100
                procent_y = force_y / 100
                force_y -= procent_y * (mass / procent_max)
                return force_y
            else:
                return 0
        elif xy == 'xy':
            if mass < self.max:
                procent_max = self.max / 100
                procent_x = force_x / 100
                procent_y = force_y / 100
                force_x -= procent_x * (mass / procent_max)
                force_y -= procent_y * (mass / procent_max)
                return (force_x, force_y)
            else:
                return 0


# Стихия земли


# Ближний бой


class MechOgon(ColdOruzhie, Ogon):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = MECH_OGON
        self.uron = 20
        self.tik_uron = 5
        self.minus_stamina = 5
        self.minus_block_stamina = 2
        self.minus_mana = 1

        self.timer_for_s_tik = 60

        self.udar_texture = arcade.load_texture_pair('nuzhno/mech_ogon.png')
        self.block_texture = arcade.load_texture_pair('nuzhno/mech_ogon_block.png')
        self.scale = 2
        self.texture = self.udar_texture[1]

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.update_mor(self.uron)
        self.kd_timer_stamina()
        self.update_position()
        self.update_block()
        self.block_block()
        self.otdacha()

        if self.s == 1:
            self.func_stamina()
            self.func_mana()

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.update_degree(sprite)
                    self.udar_or_block(sprite)
                    self.tik(sprite)

        self.update_tik()
        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()
        #self.draw_hit_box()


class ObichMech(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = OBICH_MECH
        self.uron = 50

        self.udar_texture = arcade.load_texture_pair('nuzhno/udar.png')
        self.block_texture = arcade.load_texture_pair('nuzhno/udar_block.png')
        self.texture = self.udar_texture[0]
        self.scale = 1.5

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60):
        self.update_sposob()
        self.update_block()
        self.block_block()
        self.kd_timer_stamina()
        self.update_position()
        self.otdacha()

        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            self.block = self.avto_block = False
            if self.pers.storona == 0:
                self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
            elif self.pers.storona == 1:
                self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_or_block(sprite)

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class DvuruchMech(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = DVURUCH_MECH

        self.uron = URON_DVURUCH_MECH

        self.udar_texture = arcade.load_texture_pair('nuzhno/udar.png')
        self.texture = self.udar_texture[0]
        self.scale = 1.5

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 2

        self.probit_block = False
        self.s_probit_block = 0
        self.kombo = False
        for oruzh in self.pers.oruzh_list:
            if oruzh.tip == RIVOK:
                self.kombo = True

    def on_update(self, delta_time: float = 1 / 60):
        self.update_sposob()
        self.otdacha()
        self.update_block()
        self.block_block()
        if self.probit_block:
            self.s_probit_block += 1
        if self.s_probit_block > 15:
            self.s_probit_block = 0
            self.probit_block = False

        self.kd_timer_stamina()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.kombo:
            for oruzh in self.pers.oruzh_list:
                if oruzh.tip == RIVOK and oruzh.action:
                    self.probit_block = True
                    self.s_probit_block = 0

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and not self.probit_block:
                    self.udar_or_block(sprite)
                elif arcade.check_for_collision(self, sprite) and self.probit_block:
                    self.udar(sprite)

        self.update_slovar()

        self.position = self.pers.position

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Shchit(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.sposob = SHCHIT
        self.uron = URON_SHCHIT

        self.scale = 0.5
        self.block_texture = arcade.load_texture_pair('nuzhno/shcit.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/shcit_udar.png')
        self.texture = self.block_texture[1]

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.otdacha()
        self.update_sposob()
        self.update_block()
        self.block_block()

        self.kd_timer_stamina()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        self.center_y = self.pers.center_y
        if not self.action:
            if self.pers.storona == 1:
                self.center_x = self.pers.center_x - 20
            else:
                self.center_x = self.pers.center_x + 20
        else:
            if self.pers.storona == 1:
                self.center_x = self.pers.center_x - 60
            else:
                self.center_x = self.pers.center_x + 60

        if self.action:
            self.s += 1
            self.block = self.avto_block = False
            for sprite in self.sprite_list:
                if arcade.check_for_collision(sprite, self):
                    self.udar_or_block(sprite)

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()
        

class Vila(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s=50, timer_for_s_kd=20):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = VILA
        self.uron = URON_VILA

        self.s_kd = self.timer_for_s_kd + 5

        self.udar_texture = arcade.load_texture_pair('nuzhno/vila.png')
        self.texture = self.udar_texture[0]

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.otdacha()
        self.update_block()
        self.block_block()

        self.kd_timer_mana()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            if self.pers.storona == 0:
                if self.s < self.timer_for_s // 2:
                    self.change_x = 3
                elif self.timer_for_s // 2 <= self.s < self.timer_for_s:
                    self.change_x = -3
            elif self.pers.storona == 1:
                if self.s < self.timer_for_s // 2:
                    self.change_x = -3
                elif self.timer_for_s // 2 <= self.s < self.timer_for_s:
                    self.change_x = 3

            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite) and self.s < 30:
                    self.udar_or_block(sprite)

        self.update_slovar()

        if not self.action:
            self.center_y = self.pers.center_y
            if self.pers.storona == 0:
                self.center_x = self.pers.center_x + 20
            elif self.pers.storona == 1:
                self.center_x = self.pers.center_x - 20

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class Topor(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = TOPOR
        self.uron = URON_TOPOR

        self.s_kd = self.timer_for_s_kd + 5

        self.udar_texture = arcade.load_texture_pair('nuzhno/topor0.png')
        self.texture = self.udar_texture[0]
        self.angle = 10

        self.minus_stamina = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_position()
        self.update_sposob()
        self.otdacha()
        self.update_block()
        self.block_block()

        self.kd_timer_mana()
        if self.s == 1:
            self.pers.stamina -= self.minus_stamina

        if self.action:
            if 10 <= self.s < 20:
                if self.pers.storona == 1:
                    self.change_angle = -12
                else:
                    self.change_angle = 12
            else:
                self.change_angle = 0
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_or_block(sprite)
        else:
            self.angle = 10

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()


class MechBrenda(ColdOruzhie):
    def __init__(self, pers, sprite_list, timer_for_s, timer_for_s_kd):
        super().__init__(pers, sprite_list, timer_for_s, timer_for_s_kd)
        self.tip = MECH_BRENDA
        self.uron = URON_MECH_BRENDA

        self.udar_texture = arcade.load_texture_pair('nuzhno/mech_Brenda0.png')
        self.texture = self.udar_texture[0]

        self.s_kd = self.timer_for_s_kd + 5
        self.minus_stamina = 2
        self.s1 = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.update_sposob()
        self.otdacha()
        self.update_block()
        self.block_block()

        self.kd_timer_mana()
        if self.s == 1 and self.action:
            self.pers.stamina -= self.minus_stamina * self.s1
            self.s1 += 1

        if self.s1 > 5:
            self.s1 = 1

        if self.action:
            for sprite in self.sprite_list:
                if arcade.check_for_collision(self, sprite):
                    self.udar_or_block(sprite)

        if self.pers.storona == 0:
            self.left, self.bottom = self.pers.center_x, self.pers.center_y - 40
        elif self.pers.storona == 1:
            self.right, self.bottom = self.pers.center_x, self.pers.center_y - 40

        self.update_slovar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.update_storona()
