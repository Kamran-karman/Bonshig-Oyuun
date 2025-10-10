import os
import sys

import open_files

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import arcade
import hit_box_and_radius
import sposob_star
import sposobs
from sposobs import dvizh, fiz_sposob
from sposobs.stihiya import ogon, molniya, voda, veter
from sposobs.fiz_sposob import cold_oruzhie, rivoks
import arcade.gui
import random

KOOR_X = 100
KOOR_Y = 500
X_D_ZONE = 0.005
Y_D_ZONE = 0.1

# __Klassi__
DD = 0
MDD = 1
RDD = 2
TANK = 3
HILL = 4
SAPORT = 5

# ___Voyslav___
HP_VOYSLAV = 1200
MANA_VOYSLAV = 350
STAMINA_VOYSLAV = 250


# ___Balvanchik___
HP_BETA_BALVANCHIK = 1000
MANA_BETA_BALVANCHIK = 300
STAMINA_BETA_BALVANCHIK = 300
# ______________________


# ___Voin_Innocentii___
HP_V_I = 900
MANA_V_I = 100
STAMINA_V_I = 100
REAKCIYA_V_I = 65
# ______________________


# ___Gromila___
HP_GROMILA = 1500
STAMINA_GROMILA = 100
URON_GROMILA = 120
REAKCIYA_GROMILA = 10
# ______________________


# ___ZhitelInnocentii___
HP_ZHITEL_IN = 300
STAMINA_ZHITEL_IN = 30
REAKCIYA_ZHITEL_IN = 20
# ______________________


# ___Brend___
HP_BREND = 1200
STAMINA_BREND = 200
REAKCIYA_BREND = 70


def effect_update(effect: bool, s_effect: int, timer_for_s_effect: int):
    if effect:
        s_effect += 1
        if s_effect >= timer_for_s_effect:
            effect = False
            s_effect = 0
    return s_effect, effect


class InteractionSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.name = ''

        self.idle_texture = None


class AnimatedSprite(InteractionSprite):
    def __init__(self):
        super().__init__()
        self.s_walk_texture = 0
        self.walk_textures = []

        self.jump_texture = None
        self.fall_texture = None

        self.tipo_return = False

        self.storona = 0

    def update_storona(self, speed_x, x_d_zone):
        if speed_x < -x_d_zone and self.storona == 0:
            self.storona = 1
        elif speed_x > x_d_zone and self.storona == 1:
            self.storona = 0

    def idle_animation(self, speed_x):
        if abs(speed_x) < X_D_ZONE:
            self.s_walk_texture = 0
            self.__update_texture_and_hitbox(self.idle_texture[self.storona])
            self.tipo_return = True

    def jump_animation(self, speed_y, y_d_zone, jump):
        if jump:
            if speed_y > y_d_zone:
                self.s_walk_texture = 0
                self.texture = self.jump_texture[self.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.tipo_return = True
            elif speed_y < -y_d_zone:
                self.s_walk_texture = 0
                self.__update_texture_and_hitbox(self.fall_texture[self.storona])
                self.tipo_return = True

    def __update_texture_and_hitbox(self, texture):
        self.texture = texture
        self.hit_box._points = self.texture.hit_box_points


class AnimatedSpriteDxy(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.is_on_ground = True
        self.x_odometr = 0

    def update_isonground_and_xodometr(self, dx, physics_engine):
        self.is_on_ground = physics_engine.is_on_ground(self)
        self.x_odometr += dx


class Pers(arcade.Sprite):
    def __init__(self, sprite_list):
        super().__init__()
        self.sprite_list = sprite_list

        self.max_hp = 0
        self.hp = 0
        self.hp_print = 0
        self.max_mana = 0
        self.mana = 0
        self.mana_print = 0
        self.max_stamina = 0
        self.stamina = 0
        self.stamina_print = 0
        self.dx = 0
        self.dy = 0
        self.smert = False
        self.minus_hp = False
        self.prised = False
        self.beg = False
        self.toggle = False
        self.kast_scena = False
        self.fight = False
        self.speak = False
        self.sulky = False
        self.ulibka = False

        self.ugl = 0

        self.five_sposobs = arcade.SpriteList()
        self.block_list = arcade.SpriteList()
        self.sposob_list = arcade.SpriteList()
        self.voda_list = arcade.SpriteList()
        self.radius_list = arcade.SpriteList()

        self.mor = False
        self.s_mor = 0
        self.timer_for_s_mor = 600
        self.slabweak = False
        self.s_slabweak = 0
        self.timer_for_s_slabweak = 600
        self.timer_for_s = 60
        self.s = 0

        self.oglush = False
        self.s_oglush = 0
        self.timer_for_s_oglush = 0

        self.stan = False

        self.stan_for_sposob = False
        self.s_stan_f_sp = 0
        self.timer_for_s_stan_f_sp = 0

        self.oglush_for_sposob = False

        self.dvizh = False
        self.uzhe_dvizh = False
        self.slovar_dvizh = {}

        self.tik_slovar = {}

        self.reakciya = 0
        self.block = sposobs.Block(self, self.sprite_list)
        self.block_vel = 0
        self.obich_vel = 0
        self.sil = False
        self.pariv = False
        self.new_force = [0, 0]

        self.storona = 1
        self.vel_x = 0
        self.vel_y = 0

        self.s_walk_texture = 0
        self.walk_textures = []

        self.s_block_texture = 0
        self.block_textures = []

        self.dialog_textures = []

        self.idle_texture = None
        self.jump_texture = None
        self.fall_texture = None
        self.udar_texture = None
        self.block_texture = None
        self.smert_texture = None
        self.sbiv_texture = None

        self.uron = 0
        self.udar = fiz_sposob.Udar(self, self.sprite_list, self.uron)
        self.sposob_list.append(self.udar)

        self.is_on_ground = True
        self.x_odometr = 0

        self.kvadrat_radius = hit_box_and_radius.KvadratRadius(self.scale)
        self.radius_list.append(self.kvadrat_radius)

        self.pers = ''
        self.tipo_return = False

        self.fizika = None

        self.rotation = False
        self.rotation_new = 0

        self.iskl_list = []

        self.spec_func = None

    def _update_harakteristiki(self, vivod=False):
        self.s += 1
        if self.s >= self.timer_for_s:
            self.s = 0
            if self.mor:
                self.mana += 0.5
                self.hp -= 0.5
            else:
                self.mana += 1
            if self.slabweak:
                self.stamina += 0.2
                self.mana -= 2
            else:
                self.stamina += 1
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp >= self.hp_print:
            self.minus_hp = False
        if self.hp <= 0:
            self.smert = True
            for sposob in self.sposob_list:
                sposob.action = False
        elif self.hp < self.hp_print:
            self.hp_print = self.hp
            if vivod:
                print(f'{self.pers} hp:', self.hp_print)
            self.minus_hp = True
        elif self.hp > self.hp_print:
            self.hp_print = self.hp
            if self.hp <= 0:
                self.smert = True

        if self.mor:
            self.s_mor += 1
            if self.s_mor >= self.timer_for_s_mor:
                self.mor = False
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.mana < self.mana_print:
            self.mana_print = self.mana
            if vivod:
                print(f'{self.pers} mana:', round(self.mana_print), self.mor)
        elif self.mana > self.mana_print:
            self.mana_print = self.mana
        if self.mana < 0:
            self.s_mor = 0
            self.mor = True

        if self.slabweak:
            self.s_slabweak += 1
            if self.s_slabweak >= self.timer_for_s_slabweak:
                self.slabweak = False
        if self.stamina >= self.max_stamina:
            self.stamina = self.max_stamina
        if self.stamina < self.stamina_print:
            self.stamina_print = self.stamina
            if vivod:
                print(f'{self.pers} stamina:', round(self.stamina_print), self.slabweak)
        elif self.stamina > self.stamina_print:
            self.stamina_print = self.stamina
        if self.stamina < 0:
            self.slabweak = True
            self.s_slabweak = 0

    def harakteristiki(self):
        self.hp = self.hp_print = self.max_hp
        self.mana = self.mana_print = self.max_mana
        self.stamina = self.stamina_print = self.max_stamina

    def update_lists(self):
        for s in self.sposob_list:
            if s.klass == sposobs.STIHIYA:
                if s.voda:
                    self.voda_list.append(s)
            if s.block_sposob:
                self.block_list.append(s)

    def update_storona(self, dx, physics_engine):
        if not self.smert and not self.oglush and not self.oglush_for_sposob:
            rf = False
            for block in self.block_list:
                if block.tip == sposobs.COLD_ORUZHIE:
                    if block.rf:
                        rf = True

            if not rf and not self.fight:
                if dx < -X_D_ZONE and self.storona == 0:
                    self.storona = 1
                elif dx > X_D_ZONE and self.storona == 1:
                    self.storona = 0

                for sprite in self.sprite_list:
                    if sprite.hp > 0:
                        if self.kvadrat_radius.check_collision(sprite):
                            if self.center_x > sprite.center_x:
                                self.storona = 1
                            elif self.center_x < sprite.center_x:
                                self.storona = 0
                        for _sposob in self.sposob_list:
                            for block in sprite.block_list:
                                if ((self.kvadrat_radius.check_collision(sprite) or
                                     (self.kvadrat_radius.check_collision(block) and sprite.block.block))
                                        and (abs(dx) < X_D_ZONE or _sposob.action)):
                                    if self.center_x > sprite.center_x:
                                        self.storona = 1
                                    elif self.center_x < sprite.center_x:
                                        self.storona = 0

            self.is_on_ground = physics_engine.is_on_ground(self)
            self.x_odometr += dx

    def update_block(self):
        self.block.update_block()
        for sposob_ in self.sposob_list:
            if sposob_.block_sposob and sposob_.sposob != sposobs.UDAR:
                if sposob_.main_block:
                    self.udar.main_block = False
        if self.oglush:
            self.block.block = self.block.avto_block = False
        if not self.block.block and not self.block.avto_block:
            self.block_vel = self.pymunk.max_horizontal_velocity / 2
            if not self.dvizh and self.obich_vel > 0 and not self.beg:
                self.pymunk.max_horizontal_velocity = self.obich_vel
        if (self.block.block or self.block.avto_block) and not self.dvizh:
            if self.pymunk.max_horizontal_velocity != self.block_vel:
                self.obich_vel = self.pymunk.max_horizontal_velocity
            self.pymunk.max_horizontal_velocity = self.block_vel

    def block_animation(self):
        if not self.smert and not self.oglush and not self.oglush_for_sposob:
            if len(self.block_list) == 0 and (self.udar.block or self.udar.avto_block):
                self.texture = self.block_texture[self.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.tipo_return = True
            elif len(self.block_list) > 0 and (self.block.block or self.block.avto_block):
                for block in self.block_list:
                    if block.main_block:
                        block.update_animation()
                # if self.s_block_texture < 3:
                #     self.texture = self.block_textures[self.s_block_texture][self.storona]
                #     self.hit_box._points = self.texture.hit_box_points
                #     self.s_block_texture += 1
                #     self.tipo_return = True
                # else:
                #     self.texture = self.block_texture[self.storona]
                #     self.hit_box._points = self.texture.hit_box_points
                #     self.tipo_return = True
            else:
                self.s_block_texture = 0

    def udar_func(self):
        if not self.smert and not self.oglush and not self.oglush_for_sposob and self.udar.action:
            self.texture = self.udar_texture[self.storona]
            self.hit_box._points = self.texture.hit_box_points
            self.tipo_return = True

    def avto_block_func(self, sprite):
        if (self.slabweak or ((sprite.storona == self.storona == 0 and sprite.center_x < self.center_x) or
            (sprite.storona == self.storona == 1 and sprite.center_x > self.center_x))
                or self.oglush):
            return False

        r = 10
        if self.block.block or self.block.avto_block:
            return True
        if self.pers == 'Oyuun':
            return False

        if self.reakciya > sprite.reakciya:
            if sprite.reakciya * r <= self.reakciya:
                self.block.avto_block = True
                return True
            else:
                shanc = 0
                while r >= 0.1:
                    if (round(sprite.reakciya * (r - 0.1), 1) < round(sprite.reakciya * r, 1)
                            <= self.reakciya):
                        break
                    r -= 0.1
                    shanc += 1

                rand = random.randint(1, 100)
                while shanc > 0:
                    if rand == shanc:
                        self.block.avto_block = True
                        return True
                    shanc -= 1

                return False
        elif self.reakciya < sprite.reakciya:
            if sprite.reakciya >= self.reakciya * r:
                return False
            else:
                shanc = 100
                while r >= 0.1:
                    if round(self.reakciya * (r - 0.1), 1) < round(self.reakciya * r, 1) <= sprite.reakciya:
                        break
                    r -= 0.1
                    shanc -= 1

                rand = random.randint(1, 100)
                while shanc > 0:
                    if rand == shanc:
                        self.block.avto_block = True
                        return True
                    shanc -= 1

                return False
        else:
            if random.randint(0, 1) == 1:
                self.block.avto_block = True
                return True
            else:
                return False

    def idle_animation(self, dx):
        if not self.smert and not self.oglush and not self.oglush_for_sposob:
            if abs(dx) < X_D_ZONE:
                self.s_walk_texture = 0
                self.texture = self.idle_texture[self.storona]
                self.hit_box._points = self.texture.hit_box_points
                self.tipo_return = True

    def jump_animation(self, dy):
        if not self.smert and not self.oglush and not self.oglush_for_sposob:
            if not self.is_on_ground:
                if dy > Y_D_ZONE:
                    self.s_walk_texture = 0
                    self.texture = self.jump_texture[self.storona]
                    self.hit_box._points = self.texture.hit_box_points
                    self.tipo_return = True
                elif dy < -Y_D_ZONE:
                    self.s_walk_texture = 0
                    self.texture = self.fall_texture[self.storona]
                    self.hit_box._points = self.texture.hit_box_points
                    self.tipo_return = True

    def walk_animation(self):
        if not self.smert and not self.oglush and not self.oglush_for_sposob:
            if abs(self.x_odometr) > 15:
                self.x_odometr = 0
                self.s_walk_texture += 1
                if self.s_walk_texture > 7:
                    self.s_walk_texture = 0
                self.texture = self.walk_textures[self.s_walk_texture][self.storona]
                self.hit_box._points = self.texture.hit_box_points

    def rotation_animation(self):
        if self.rotation:
            self.texture = self.sbiv_texture[self.storona]
            self.hit_box._points = self.texture.hit_box_points
            self.center_y = 160
            self.tipo_return = True

    def update_radius_list(self):
        for radius in self.radius_list:
            radius.position = self.position
        self.kvadrat_radius.scale = self.scale

    def slabweak_func(self, force, friction):
        if self.slabweak and not self.dvizh:
            return (0, 0), 1
        else:
            return force, friction

    def smert_func(self):
        self.center_y = 128
        if random.randint(0, 1) == 0:
            self.angle = 90 * -1
        else:
            self.angle = 90 * 1

    def oglush_force(self, force, friction, a):
        if self.oglush:
            if self.s_oglush >= self.timer_for_s_oglush or self.dvizh:
                return force, friction
            return (0, 0), friction * a
        return force, friction

    def action(self, sposob_1, toggle=False):
        for sposob_0 in self.sposob_list:
            if sposob_0.action and sposob_0.sposob != sposob_1 and not sposob_0.action_2:
                break
        for sposob_2 in self.sposob_list:
            if sposob_2.sposob == sposob_1:
                if toggle:
                    sposob_2.action = not sposob_2.action
                else:
                    sposob_2.action = True

    def update_sposob_list(self):
        for sposob_ in self.sposob_list:
            sposob_.sprite_list = self.sprite_list
            sposob_.on_update()
            sposob_.update()

    def draw_sposob_list(self):
        for s in self.sposob_list:
            s.update_animation()
            if s.action:
                if len(self.iskl_list) > 0:
                    for iskl in self.iskl_list:
                        if s.sposob == iskl:
                            break
                        else:
                            s.draw()
                else:
                    s.draw()


class Rock(Pers):
    def __init__(self, sprite_list):
        super().__init__(sprite_list)
        self.pers = 'Rock'

        self.max_hp = 6100
        self.hp = 6100
        self.idle_texture = arcade.load_texture('nuzhno/Rock/rock.png')
        self.hit_box._points = self.texture.hit_box_points
        self.scale = 2
        self.tresk = False
        self.tresk_texture_list = []
        self.s_tresk = 0
        self.rotation = False
        for i in range(10):
            texture = arcade.load_texture(f'nuzhno/Rock/rock{i}.png')
            self.tresk_texture_list.append(texture)
        self.angle = 0

    def tresk_animation(self):
        if self.max_hp - 825 < self.hp <= self.max_hp - 450 and self.s_tresk == 0:
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 625 and self.s_tresk == 0:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 2125 and self.s_tresk == 1:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 2425 and self.s_tresk == 2:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 2925 and self.s_tresk == 3:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 3250 and self.s_tresk == 4:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 3500 and self.s_tresk == 5:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 4000 and self.s_tresk == 6:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 4500 and self.s_tresk == 7:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]
        elif self.hp <= self.max_hp - 4900 and self.s_tresk == 8:
            self.s_tresk += 1
            self.idle_texture = self.tresk_texture_list[self.s_tresk]

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self._update_harakteristiki()
        if self.s_tresk < 1:
            self.rotation = False
        else:
            self.rotation = True
        self.tresk_animation()
        # if self.rotation:
        #     self.angle = 90
        #     #self.center_y = 160
        # else:
        #     self.angle = 0
        self.texture = self.idle_texture
        self.hit_box._points = self.texture.hit_box_points


class Gonec(Pers):
    def __init__(self, sprite_list):
        super().__init__(sprite_list)

        self.hp = 1

        main_patch = 'nuzhno/male_person/malePerson_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')

        for i in range(8):
            texture = arcade.load_texture_pair(f'{main_patch}walk{i}.png')
            self.walk_textures.append(texture)
        self.texture = self.idle_texture[1]

        sposobs.update_texture_list(3, f'{main_patch}dialog', '.png', self.dialog_textures)

        self.s1 = 0
        self.anim = 0

    def animation_1(self):
        if self.anim:
            self.s1 += 1
            if self.s1 >= 60:
                self.s1 = 0
                self.anim = False

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.tipo_return = False

        if self.change_x > 0:
            self.storona = 0
        elif self.change_x < 0:
            self.storona = 1

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture[self.storona]

        if self.change_y > 0:
            self.texture = self.jump_texture[self.storona]
        elif self.change_y < 0:
            self.texture = self.fall_texture[self.storona]

        if abs(self.change_x) > 0 and self.change_y == 0:
            self.s_walk_texture += 0.25
            if self.s_walk_texture > 7:
                self.s_walk_texture = 0
            self.texture = self.walk_textures[int(self.s_walk_texture)][self.storona]


class Sinhelm(Pers):
    def __init__(self, sprite_list):
        super().__init__(sprite_list)
        self.pers = 'Sinhelm'
        self.hp = 1
        self.olen_beg = False
        self.landing = False
        self.s_landing = 0
        self.timer_for_s_landing = 30
        self.podgotovka = False
        self.s_podgotovka = 0
        self.timer_for_s_podgotovka = 120
        self.izmen_storona = True
        self.storona = 1
        self.anim = True

        main_patch = 'nuzhno/Sinhelm/sinhelm_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.ukaz_texture = arcade.load_texture_pair(f'{main_patch}ukaz.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}fall.png')
        self.landing_texture = arcade.load_texture_pair(f'{main_patch}landing.png')
        self.podgotovka_texture = arcade.load_texture_pair(f'{main_patch}podgotovka.png')

        for i in range(8):
            texture = arcade.load_texture_pair(f'{main_patch}walk{i}.png')
            self.walk_textures.append(texture)
        self.texture = self.idle_texture[0]

        sposobs.update_texture_list(3, f'{main_patch}dialog', '.png', self.dialog_textures)

        self.ukaz = False
        self.s_ukaz = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        #print(self.anim)
        self.tipo_return = False
        if self.izmen_storona:
            if dx < -X_D_ZONE and self.storona == 0:
                self.storona = 1
            elif dx > X_D_ZONE and self.storona == 1:
                self.storona = 0
        self.is_on_ground = physics_engine.is_on_ground(self)
        self.x_odometr += dx

        if self.landing:
            if self.s_landing <= self.timer_for_s_landing:
                self.texture = self.landing_texture[self.storona]
                self.s_landing += 1
            else:
                self.landing = False
                self.s_landing = 0
            return

        if self.podgotovka:
            if self.s_podgotovka <= self.timer_for_s_podgotovka:
                self.s_podgotovka += 1
                self.texture = self.podgotovka_texture[self.storona]
            else:
                self.podgotovka = False
                self.s_podgotovka = 0
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        if self.ukaz:
            self.s_ukaz += 1
            if self.s_ukaz >= 15:
                self.ukaz = False
                self.s_ukaz = 0
            self.texture = self.ukaz_texture[0]
            return

        if self.anim:
            self.texture = self.idle_texture[self.storona]


class AdnotBratislav(Pers):
    def __init__(self, sprite_list):
        super().__init__(sprite_list)
        self.pers = 'Bratislav'

        self.hp = 1

        main_patch = 'nuzhno/male_person/malePerson_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')

        sposobs.update_texture_list(3, f'{main_patch}dialog', '.png', self.dialog_textures)

        for i in range(8):
            texture = arcade.load_texture_pair(f'{main_patch}walk{i}.png')
            self.walk_textures.append(texture)
        self.texture = self.idle_texture[0]

        self.anim_2_list = []
        self.s_anim_2_list = 0
        texture = arcade.load_texture_pair(f'{main_patch}walk3.png')
        self.anim_2_list.append(texture)
        texture = arcade.load_texture_pair(f'{main_patch}anim_2.png')
        self.anim_2_list.append(texture)

        self.anim_1 = False
        self.anim_2 = False
        self.rock = False
        self.s_anim_2 = 0

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.tipo_return = False

        if self.anim_1:
            self.texture = self.jump_texture[self.storona]
            return

        if self.anim_2:
            self.s_anim_2 += 1
            if self.s_anim_2 >= 120 and self.s_anim_2_list == 0:
                self.s_anim_2_list += 1
                self.rock = True
            self.texture = self.anim_2_list[self.s_anim_2_list][self.storona]
            if self.s_anim_2 == 210:
                self.anim_2 = False
                self.s_anim_2 = 0
                self.s_anim_2_list = 0
            return

        if self.change_x > 0:
            self.storona = 0
        elif self.change_x < 0:
            self.storona = 1

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture[self.storona]

        if self.change_y > 0:
            self.texture = self.jump_texture[self.storona]
        elif self.change_y < 0:
            self.texture = self.fall_texture[self.storona]

        if abs(self.change_x) > 0 and self.change_y == 0:
            self.s_walk_texture += 0.25
            if self.s_walk_texture > 7:
                self.s_walk_texture = 0
            self.texture = self.walk_textures[int(self.s_walk_texture)][self.storona]


class Voyslav(Pers):
    def __init__(self, sprite_list, fizika):
        super().__init__(sprite_list)
        self.pers = 'igrok'

        self.max_hp = HP_VOYSLAV
        self.max_mana = MANA_VOYSLAV
        self.max_stamina = STAMINA_VOYSLAV
        self.reakciya = 990
        self.harakteristiki()

        self.scale = 1

        main_patch = "nuzhno/male_adventurer/maleAdventurer"
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[0]

        self.fizika = fizika

        self.shchit = cold_oruzhie.Shchit(self, self.sprite_list, 15, 5)
        self.sposob_list.append(self.shchit)
        self.block_list.append(self.shchit)
        self.oruzh_list.append(self.shchit)

        self.molniya = molniya.CepnayaMolniay(self, self.sprite_list)
        self.sposob_list.append(self.molniya)
        self.gnev_Tora = molniya.GnevTora(self, self.sprite_list)
        self.sposob_list.append(self.gnev_Tora)
        self.streliPeruna = molniya.StreliPeruna(self, self.sprite_list)
        self.sposob_list.append(self.streliPeruna)
        self.shar_mol = molniya.SharMolniay(self, self.sprite_list)
        self.sposob_list.append(self.shar_mol)
        self.udar_Zevsa = molniya.UdarZevsa(self, self.sprite_list)
        self.sposob_list.append(self.udar_Zevsa)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False
        self.update_storona(dx, physics_engine)

        self.block_animation()
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()
        if self.tipo_return:
            return

    def on_update(self, delta_time: float = 1 / 60):
        self.mana += 1 / 60
        self._update_harakteristiki()

        self.update_sposob_list()
        self.update_radius_list()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

        self.shchit.fizika = self.fizika
        self.shchit.on_update()

        self.gnev_Tora.on_update()
        self.shar_mol.on_update()
        self.shar_mol.update()
        self.udar_Zevsa.on_update()

    def update_animation(self, delta_time: float = 1 / 60):
        if self.block.block or self.block.avto_block or self.shchit.action:
            self.shchit.draw()

        self.shchit.update_animation()

        if (self.shar_mol.udar and self.shar_mol.zaryad_b) or self.shar_mol.zaryad:
            self.shar_mol.draw()
        self.shar_mol.update_animation()
        self.molniya.update_animation()
        self.gnev_Tora.update_animation()
        self.streliPeruna.update_animation()
        self.udar_Zevsa.update_animation()


class Oyuun(Pers):
    def __init__(self, sprite_list):
        super().__init__(sprite_list)
        self.pers = 'Oyuun'

        self.max_hp = 2500
        self.max_mana = 600
        self.max_stamina = 240
        self.reakciya = 75
        self.uron = 15
        self.harakteristiki()
        self.vel_x = 300

        main_patch = 'nuzhno/Oyuun/maleAdventurer'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.block_texture = arcade.load_texture_pair('nuzhno/Oyuun/maleAdventurer_jump.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/Oyuun/master/udar0.png')
        for i in range(8):
            tex = arcade.load_texture_pair(f'{main_patch}_walk{i}.png')
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[0]

        sposobs.update_texture_list(3, f'{main_patch}_dialog', '.png', self.dialog_textures)

        self.udar.master = True
        udar_main_patch = 'nuzhno/Oyuun/master/udar'
        sposobs.update_texture_list(2, udar_main_patch, '.png', self.udar.idle_udar_texture_list)
        sposobs.update_texture_list(2, udar_main_patch + '_W', '.png', self.udar.jump_udar_texture_list)
        sposobs.update_texture_list(2, udar_main_patch + '_WAD', '.png',
                                    self.udar.jump_dvizh_udar_texture_list)
        sposobs.update_texture_list(2, udar_main_patch + '_move', '.png', self.udar.move_udar_texture_list)

        self.razminka = False
        self.razminka_textures_list = []
        self.s_razminka_texture = 0
        for i in range(12):
            texture = arcade.load_texture(f'nuzhno/Oyuun/Razminka/razminka{i}.png')
            self.razminka_textures_list.append(texture)

        self.concentration = False
        self.concentration_textures_list = []
        self.s_concentration_texture = 0
        for i in range(15):
            texture = arcade.load_texture(f'nuzhno/Oyuun/Concentration/concentration{i}.png')
            self.concentration_textures_list.append(texture)

        self.wasu = False
        self.s_wasu = 0

        self.read = False
        self.gotov = False

        self.hit_box_2 = hit_box_and_radius.HitBox(self.idle_texture, self)

        self.v_max = 3000
        self.v = self.v_max
        self.v_plus = 1 / 3
        self.kritik = False
        voda.V_LIST.append(self)

        self.rech_drakon = voda.RechnoyDrakon(self, self.sprite_list, 12)
        self.sposob_list.append(self.rech_drakon)
        self.five_sposobs.append(self.rech_drakon)
        # self.iskl_list.append(self.rech_drakon.sposobs)
        self.hlist = voda.Hlist(self, self.sprite_list, 20)
        self.sposob_list.append(self.hlist)
        self.five_sposobs.append(self.hlist)
        self.volna = voda.Volna(self, self.sprite_list, 200)
        self.sposob_list.append(self.volna)
        self.five_sposobs.append(self.volna)
        self.udar_kita = voda.UdarKita(self, self.sprite_list, 1500)
        self.sposob_list.append(self.udar_kita)
        self.five_sposobs.append(self.udar_kita)
        self.tayfun = voda.Tayfun(self, self.sprite_list, 300, True)
        self.sposob_list.append(self.tayfun)
        self.five_sposobs.append(self.tayfun)
        self.techenie = voda.Reka(self, self.sprite_list, 150, 900, True)
        self.sposob_list.append(self.techenie)
        self.voda_udars = voda.VodaFightUdars(self, self.sprite_list, 10)
        self.sposob_list.append(self.voda_udars)
        self.iskl_list.append(self.voda_udars.sposob)
        self.voda_shchit = voda.VodaShchit(self, self.sprite_list, 100)
        #self.voda_shchit.main_block = True
        self.iskl_list.append(self.voda_shchit.sposob)
        self.sposob_list.append(self.voda_shchit)
        idle_kombo_texture_list = []
        idle_kombo_texture_list = sposobs.update_texture_list(8,
                                                             'nuzhno/Oyuun/karakatica/kombo',
                                                             '.png', idle_kombo_texture_list)
        idle_udar_texture_list = []
        idle_udar_texture_list = sposobs.update_texture_list(4,
                                                            'nuzhno/Oyuun/karakatica/udar',
                                                            '.png', idle_udar_texture_list)
        obich_texture = arcade.load_texture_pair('nuzhno/Oyuun/karakatica/obich.png')
        block_texture = arcade.load_texture_pair('nuzhno/Oyuun/karakatica/block.png')
        self.karakatica = voda.Karakatica(self, self.sprite_list, 600, idle_udar_texture_list,
                                          idle_kombo_texture_list, obich_texture, block_texture)
        self.sposob_list.append(self.karakatica)
        self.iskl_list.append(sposobs.KARAKATICA)
        self.udar.timer_for_s_kd = 15
        self.udar.timer_for_s = 15
        self.udar.minus_stamina = 2

        self.chest = False

        self.update_lists()

    def udar_animation(self, dx, dy):
        self.udar.update_udar(dx, dy, Y_D_ZONE, X_D_ZONE)
        self.udar.position = self.position

        if self.udar.action:
            self.tipo_return = True
        else:
            if 0 < random.randint(1, 5) < 4:
                index = 0
            else:
                index = 1

            if self.udar.jump and not self.udar.move:
                self.udar_texture = self.udar.jump_udar_texture_list[index]
            elif self.udar.move and not self.udar.jump:
                self.udar_texture = self.udar.move_udar_texture_list[index]
            elif self.udar.move and self.udar.jump:
                self.udar_texture = self.udar.jump_dvizh_udar_texture_list[index]
            else:
                self.udar_texture = self.udar.idle_udar_texture_list[index]

    def razminka_animation(self):
        self.s_razminka_texture += 0.08
        if self.s_razminka_texture > 12:
            self.s_razminka_texture = 0
            self.razminka = False
            return
        self.texture = self.razminka_textures_list[int(self.s_razminka_texture)]

    def concentration_animation(self):
        self.s_concentration_texture += 0.05
        if self.s_concentration_texture > 15:
            self.s_concentration_texture = 0
            self.concentration = False
            self.action(sposobs.VODA_UDARS)
            return
        self.texture = self.concentration_textures_list[int(self.s_concentration_texture)]

    def write_and_stand_up_animation(self):
        self.s_wasu += 1
        if self.s_wasu >= 340:
            self.wasu = False
            self.s_wasu = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.dx = dx
        self.dy = dy
        self.tipo_return = False
        self.update_storona(dx, physics_engine)
        for v in self.voda_list:
            v.fizika = physics_engine
            for sprite in self.sprite_list:
                v.pred_vel_x = sprite.vel_x

        if self.chest:
            self.texture = self.jump_texture[self.storona]
            return

        if self.gotov:
            self.texture = self.walk_textures[2][self.storona]
            return

        if self.read:
            self.texture = self.fall_texture[self.storona]
            return

        self.udar_animation(dx, dy)
        self.udar_func()
        if self.tipo_return:
            return
        if not self.fight:
            self.hit_box_2.position = self.position
        else:
            if not self.karakatica.kombo:
                self.hit_box_2.center_y = self.center_y - 43
                if self.storona == 0:
                    self.hit_box_2.center_x = self.center_x - 38
                else:
                    self.hit_box_2.center_x = self.center_x + 38
            else:
                self.hit_box_2.center_x = self.center_x
                self.hit_box_2.center_y = self.center_y - 42
        self.hit_box_2.update_animation()

        self.block_animation()
        if self.tipo_return:
            return

        if self.fight:
            self.hit_box._points = self.texture.hit_box_points
            return
        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.mana += 4 / 60
        self._update_harakteristiki()
        self.update_block()

        self.update_sposob_list()
        self.update_radius_list()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.draw_sposob_list()
        self.voda_udars.draw()


class BetaMaster(Pers):
    def __init__(self, sprite_list, fizika):
        super().__init__(sprite_list)
        self.max_hp = 6000
        self.max_mana = 500
        self.max_stamina = 500
        self.harakteristiki()
        voda.V_LIST.append(self)
        self.kritik = False

        self.reakciya = 10000

        self.scale = 1

        main_patch = "nuzhno/male_adventurer/maleAdventurer"

        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[0]

        self.fizika = fizika

        self.shchit = cold_oruzhie.Shchit(self, self.sprite_list, 10, 10)
        self.sposob_list.append(self.shchit)

        # self.oruzh_list.append(self.shchit)

        self.mech = cold_oruzhie.ObichMech(self, self.sprite_list, 10, 5)
        self.sposob_list.append(self.mech)
        # self.oruzh_list.append(self.mech)

        self.molniya = molniya.CepnayaMolniay(self, self.sprite_list)
        self.sposob_list.append(self.molniya)
        self.gnev_Tora = molniya.GnevTora(self, self.sprite_list)
        self.sposob_list.append(self.gnev_Tora)
        self.streliPeruna = molniya.StreliPeruna(self, self.sprite_list)
        self.sposob_list.append(self.streliPeruna)
        self.v_max = 6000
        self.v = self.v_max
        self.v_plus = 2
        self.sputniki = sposob_star.Sputniki(self, self.sprite_list, 4, 36)
        self.sposob_list.append(self.sputniki)
        self.volna = voda.Volna(self, self.sprite_list)
        self.sposob_list.append(self.volna)
        self.techenie = voda.Techenie(self, self.sprite_list, 600, True)
        self.sposob_list.append(self.techenie)
        self.rechnoy_drakon = voda.RechnoyDrakon(self, self.sprite_list)
        self.sposob_list.append(self.rechnoy_drakon)
        self.udar_kita = voda.UdarKita(self, self.sprite_list)
        self.sposob_list.append(self.udar_kita)
        self.tayfun = voda.Tayfun(self, self.sprite_list, True)
        self.sposob_list.append(self.tayfun)
        self.test = veter.Poriv(self, self.sprite_list)
        self.sposob_list.append(self.test)

        self.update_lists()

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False
        self.fight = False
        self.update_storona(dx, physics_engine)
        for v in self.voda_list:
            v.fizika = physics_engine
            for sprite in self.sprite_list:
                v.pred_vel_x = sprite.vel_x


        self.block_animation()
        self.udar_func()
        if self.tipo_return:
            return

        if self.fight:
            self.hit_box._points = self.texture.hit_box_points
            return
        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()
        # if self.tipo_return:
        #     return

    def on_update(self, delta_time: float = 1 / 60):
        self.mana += 1
        self.max_mana += 1 / 60
        self.stamina += 1
        self.max_stamina += 1 / 60
        self.hp += 10
        self.max_hp += 1
        self._update_harakteristiki()
        # self.techenie.update()

        for v in self.voda_list:
            for sprite in self.sprite_list:
                self.test.pred_vel_x = sprite.vel_x
                v.pred_vel_x = sprite.vel_x

#        self.update_sposob_list()
        self.block.update_block()
        self.test.update()
        self.update_radius_list()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

        self.shchit.fizika = self.fizika

    def update_animation(self, delta_time: float = 1 / 60):
        if self.block.block or self.block.avto_block:
            self.shchit.draw()
        if self.shchit.action:
            self.shchit.draw()

        if self.mech.action:
            self.mech.draw()

        for sposob_ in self.sposob_list:
            sposob_.update_animation()

        # a = abs(self.bottom - self.top) / 2
        # arcade.draw(self.techenie.left - 100, self.techenie.top, self.techenie.right + 100,
        #                  self.techenie.top, arcade.csscolor.WHITE, 5)
        # arcade.draw(self.techenie.left - 100, self.techenie.center_y - 115 * 1.75 / 2, self.techenie.right + 100,
        #                  self.techenie.center_y - 115 * 1.75 / 2, arcade.csscolor.BLACK, 5)

        # self.sputnik.update_animation()
        self.sputniki.draw()
        self.draw_sposob_list()
        self.test.draw()


class Vrag(Pers):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(sprite_list)
        self.klass = 0

        self.force_x = 0
        self.force_y = 0

        self.radius_vid = hit_box_and_radius.Radius(5)
        self.radius_list.append(self.radius_vid)
        self.radius_ataki = hit_box_and_radius.Radius(0.25)
        self.radius_list.append(self.radius_ataki)
        self.radius_ataki2 = hit_box_and_radius.Radius()
        self.radius_list.append(self.radius_ataki2)

        self.igrok = igrok
        self.sprite_list.append(self.igrok)
        self.v_drug_list = v_drug_list

        self.walls_list = walls_list

        self.go = True
        self.d_zone = 50

        self.kast_scena = kast_scena
        self.tip = tip

        self.udar.sprite_list = self.sprite_list

        self.s = 0
        self.s1 = 0
        self.atak = False

    def ii(self, dx, physics_engine):
        self.update_radius_list()
        self.update_storona(dx, physics_engine)
        if not self.smert:
            if (self.radius_vid.check_collision(self.igrok) and not self.kast_scena and not self.oglush
                    and not self.stan and not self.stan_for_sposob):
                if self.igrok.center_x < self.radius_vid.center_x:
                    if abs(self.igrok.right - self.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                        self.storona = 1
                    else:
                        self.force_x = -15000
                        self.go = True

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < X_D_ZONE):
                            for wall in self.walls_list:
                                if self.kvadrat_radius.check_collision(wall):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0
                elif self.igrok.center_x > self.radius_vid.center_x:
                    if abs(self.right - self.igrok.left) <= self.d_zone:
                        self.force_x, self.force_y = 0., 0.
                        self.go = False
                        self.storona = 0
                    else:
                        self.force_x = 15000
                        self.go = True

                        if (self.kvadrat_radius.check_collision(sprite_list=self.sprite_list) and
                                self.is_on_ground and abs(dx) < X_D_ZONE):
                            for wall in self.walls_list:
                                if self.kvadrat_radius.check_collision(wall):
                                    self.force_y = 50000
                                    break
                                else:
                                    self.force_y = 0

                for drug in self.v_drug_list:
                    if (drug.center_x > self.center_x and abs(self.right - drug.left) <= self.d_zone and not drug.go
                            and self.igrok.center_x > self.center_x):
                        self.go = False
                        self.force_x = 0.
                        break
                    elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= self.d_zone and not drug.go
                          and self.igrok.center_x < self.center_x):
                        self.go = False
                        self.force_x = 0.
                        break
            else:
                self.go = False
                self.force_x, self.force_y = 0., 0.

    def update_udar(self):
        if not self.smert and not self.kast_scena and not self.oglush:
            if len(self.oruzh_list) == 0:
                if self.radius_ataki.check_collision(self.igrok):
                    self.udar.action = True
                else:
                    self.udar.action = False
            elif len(self.oruzh_list) > 0:
                for oruzh in self.oruzh_list:
                    if self.radius_ataki.check_collision(self.igrok) and oruzh.sposob == self.tip:
                        oruzh.action = True
                    else:
                        oruzh.action = False
                    oruzh.on_update()
                    oruzh.update()

    def sposob_action(self):
        self.s += 1
        if self.radius_ataki2.check_collision(self.igrok):
            self.atak = True
            for _sposob in self.sposob_list:
                if _sposob.action:
                    self.s1 += 1
                    break
                elif not _sposob.action:
                    self.s1 = 0
        else:
            self.atak = False

        if self.s >= 3600:
            self.s = 0

    def return_force(self, xy: str):
        if not self.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y

    def oruzh_update_animation(self):
        if len(self.oruzh_list) > 0:
            for oruzh in self.oruzh_list:
                if oruzh.sposob == self.tip:
                    if oruzh.action:
                        oruzh.draw()
                    oruzh.update_animation()
        else:
            if self.udar.action:
                self.udar.draw()
                self.udar.update_animation()


class BetaBalvanchik(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.pers = 'betabalvanchik'

        self.radius_ataki_1 = hit_box_and_radius.Radius()

        self.max_hp = HP_BETA_BALVANCHIK + 10000
        self.max_mana = MANA_BETA_BALVANCHIK
        self.max_stamina = STAMINA_BETA_BALVANCHIK
        self.reakciya = 50
        self.harakteristiki()

        self.scale = 1.2

        main_patch = "nuzhno/male_adventurer/maleAdventurer"
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.smert_texture = arcade.load_texture_pair('nuzhno/smert.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')
        self.block_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[0]

        self.mech = cold_oruzhie.ObichMech(self, self.sprite_list, 30, 600)
        self.sposob_list.append(self.mech)
        self.oruzh_list.append(self.mech)
        self.fire_ball = ogon.FireBall(self, self.sprite_list)
        self.fire_ball.s_kd = 0
        self.fire_ball.timer_for_s_kd = 240
        self.timer_for_s_stan_f_sp = self.fire_ball.timer_for_s_kast
        self.sposob_list.append(self.fire_ball)
        self.yaziki_ognya = ogon.YazikiOgnya(self, sprite_list)
        self.yaziki_ognya.s_kd = 0
        self.sposob_list.append(self.yaziki_ognya)
        self.kulak_ognya = ogon.KulakOgnya(self, self.sprite_list)
        self.sposob_list.append(self.kulak_ognya)

        self.s = 0
        self.s1 = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii(dx, physics_engine)

        self.block_animation()
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()

    def on_update(self, delta_time: float = 1 / 60):
        self.s += 1
        self._update_harakteristiki()
        self.radius_ataki_1.position = self.position
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)
        self.update_udar()
        if self.radius_ataki_1.check_collision(self.igrok):
            for _sposob in self.sposob_list:
                if _sposob.sposob != sposobs.OBICH_MECH:
                    if _sposob.action:
                        self.s1 += 1
                        break
                    elif not _sposob.action:
                        self.s1 = 0
            if self.s1 == 0:
                if self.s % 210 == 0 and not self.sposob_list[1].action:
                    self.sposob_list[1].action = True
                elif self.s % 330 == 0 and not self.sposob_list[2].action:
                    self.sposob_list[2].action = True
                elif self.s % 90 == 0 and not self.sposob_list[3].action:
                    self.sposob_list[3].action = True

        self.s_stan_f_sp, self.stan_for_sposob = effect_update(self.stan_for_sposob, self.s_stan_f_sp,
                                                               self.timer_for_s_stan_f_sp)

        for _sposob in self.sposob_list:
            _sposob.on_update()
            _sposob.update()

        if self.s >= 3600:
            self.s = 0

    def update_animation(self, delta_time: float = 1 / 60):
        #self.mech.draw()
        if self.mech.action or self.mech.block or self.mech.avto_block:
            self.mech.draw()

        self.oruzh_update_animation()
        if self.fire_ball.action:
            self.fire_ball.draw()
        if self.yaziki_ognya.action:
            self.yaziki_ognya.draw()
        if self.kulak_ognya.action:
            self.kulak_ognya.draw()


class VoinOgon(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip: int = 0, kast_scena: bool = False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.pers = 'voin_ogon'
        self.klass = MDD

        self.max_hp = 10000
        self.max_mana = 90
        self.max_stamina = 60
        self.reakciya = 50
        self.harakteristiki()

        self.radius_ataki2.scale = 0.35
        self.radius_block = hit_box_and_radius.Radius()
        self.radius_list.append(self.radius_block)

        main_patch = "nuzhno/male_adventurer/maleAdventurer"
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.smert_texture = arcade.load_texture_pair('nuzhno/smert.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')
        self.sbiv_texture = arcade.load_texture_pair(f'{main_patch}_sbiv.png')
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[0]

        self.kulak_ognya = ogon.KulakOgnya(self, self.sprite_list)
        self.sposob_list.append(self.kulak_ognya)
        self.mech_ogon = cold_oruzhie.MechOgon(self, self.sprite_list, 60, 90)
        self.mech_ogon.main_block = True
        self.sposob_list.append(self.mech_ogon)
        self.oruzh_list.append(self.mech_ogon)

        self.update_lists()

    def ii_mdd(self, dx, physics_engine):
        self.ii(dx, physics_engine)
        if not self.smert and not self.kast_scena and not self.oglush and self.stamina > self.max_stamina / 2:
            if self.radius_block.check_collision(self.igrok):
                if self.igrok.center_x >= self.center_x and self.storona == 0 and self.igrok.storona == 1:
                    self.block.block = True
                elif self.igrok.center_x < self.center_x and self.storona == 1 and self.igrok.storona == 0:
                    self.block.block = True
                else:
                    self.block.block = False
            else:
                for sposob_ in self.igrok.sposob_list:
                    if sposob_.action and arcade.check_for_collision_with_list(sposob_, self.block_list):
                        self.block.block = True
                        break
                    else:
                        self.block.block = False
        else:
            self.block.block = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii_mdd(dx, physics_engine)

        self.rotation_animation()
        if self.tipo_return:
            return

        self.block_animation()
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()
        self.draw_sposob_list()
        if self.mech_ogon.block or self.mech_ogon.avto_block:
            self.mech_ogon.draw()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.update_udar()
        self.sposob_action()
        self.update_block()
        if self.s1 == 0 and self.atak:
            if self.s % 40 == 0 and not self.kulak_ognya.action:
                self.kulak_ognya.action = True

        self.s_stan_f_sp, self.stan_for_sposob = effect_update(self.stan_for_sposob, self.s_stan_f_sp,
                                                               self.timer_for_s_stan_f_sp)

        self.update_sposob_list()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)


class MagOgon(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip: int = 0, kast_scena: bool = False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.pers = 'mag_ogon'
        self.klass = RDD

        self.d_zone1 = 200

        self.max_hp = 500
        self.max_mana = 180
        self.max_stamina = 60
        self.harakteristiki()

        self.radius_ataki_1 = hit_box_and_radius.Radius(1.5)

        main_patch = 'nuzhno/female_person/femalePerson'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.udar_texture = arcade.load_texture_pair(f'{main_patch}_udar.png')
        self.smert_texture = arcade.load_texture_pair(f'{main_patch}_smert.png')
        self.block_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.sbiv_texture = arcade.load_texture_pair(f'{main_patch}_sbiv.png')
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[0]

        self.yaziki_ognya = ogon.YazikiOgnya(self, self.sprite_list)
        self.sposob_list.append(self.yaziki_ognya)
        self.fire_ball = ogon.FireBall(self, self.sprite_list)
        self.sposob_list.append(self.fire_ball)
        self.mini_fire_ball = ogon.MiniFireBall(self, self.sprite_list)
        self.sposob_list.append(self.mini_fire_ball)
        for s in self.sposob_list:
            s.s_kd = 0
        self.update_lists()

    def ii_rdd(self, dx, physics_engine):
        if not self.smert:
            self.ii(dx, physics_engine)
            if (self.radius_vid.check_collision(self.igrok) and not self.kast_scena and not self.oglush
                    and not self.stan and not self.stan_for_sposob):
                if self.igrok.center_x < self.radius_vid.center_x and abs(self.igrok.right - self.left) <= self.d_zone1:
                    self.force_x = 0.
                    self.go = False
                elif (self.igrok.center_x > self.radius_vid.center_x
                      and abs(self.right - self.igrok.left) <= self.d_zone1):
                    self.force_x = 0.
                    self.go = False

                for drug in self.v_drug_list:
                    if (drug.center_x > self.center_x and abs(self.right - drug.left) <= self.d_zone1 and not drug.go
                            and self.igrok.center_x > self.center_x) and drug.klass == MDD:
                        self.go = False
                        self.force_x = 0.
                        break
                    elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= self.d_zone1 and not drug.go
                          and self.igrok.center_x < self.center_x) and drug.klass == MDD:
                        self.go = False
                        self.force_x = 0.
                        break

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii_rdd(dx, physics_engine)

        if self.rotation:
            self.texture = self.sbiv_texture[self.storona]
            self.hit_box._points = self.texture.hit_box_points
            self.center_y = 160
            return

        self.block_animation()
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.yaziki_ognya.draw_hit_box(arcade.color.WHITE) # Доделать механику языка
        self.draw_sposob_list()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)
        self.s_stan_f_sp, self.stan_for_sposob = effect_update(self.stan_for_sposob, self.s_stan_f_sp,
                                                               self.timer_for_s_stan_f_sp)
        self.update_udar()
        self.sposob_action()
        if self.s1 == 0 and self.atak:
            for s in self.sposob_list:
                if not s.kd and not s.action and s.sposob != sposobs.UDAR:
                    self.action(s.sposob)

        self.update_sposob_list()


class VoinInnocentii(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)

        self.max_hp = HP_V_I
        self.max_mana = MANA_V_I
        self.max_stamina = STAMINA_V_I
        self.reakciya = REAKCIYA_V_I
        self.harakteristiki()

        self.rivok_distanc = 800

        self.scale = 1.1

        main_patch = 'nuzhno/male_person/malePerson'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)

        self.texture = self.idle_texture[self.storona]

        self.rivok = rivoks.Rivok(self, sprite_list, (9000, 0), 30, 60)

        self.pers = 'voin_innocentii'

        self.dvuruch_mech = cold_oruzhie.DvuruchMech(self, self.sprite_list, 15, 60)
        self.sposob_list.append(self.dvuruch_mech)
        self.oruzh_list.append(self.dvuruch_mech)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii(dx, physics_engine)

        self.block_animation()
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()
        if self.tipo_return:
            return

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.rivok.pred_vel_x = self.vel_x
        self._update_harakteristiki()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)
        self.s_stan_f_sp, self.stan_for_sposob = effect_update(self.stan_for_sposob, self.s_stan_f_sp,
                                                               self.timer_for_s_stan_f_sp)
        self.rivok.on_update()
        self.update_udar()


class Gromila(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=0, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.max_hp = HP_GROMILA
        self.max_stamina = STAMINA_GROMILA
        self.uron = URON_GROMILA
        self.harakteristiki()

        self.sil = True

        self.reakciya = REAKCIYA_GROMILA

        self.scale = 2

        main_patch = 'nuzhno/male_person/malePerson'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}_idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}_jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}_fall.png')
        self.udar_texture = arcade.load_texture_pair(f'nuzhno/gronila_udar.png')

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)

        self.texture = self.idle_texture[self.storona]

        self.pers = 'gromila'
        self.udar.minus_stamina = 5

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii(dx, physics_engine)

        self.block_animation()
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()
        if self.tipo_return:
            return

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)
        # self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()


class ZhitelInnocentii(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=(0,0), kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.max_hp = HP_ZHITEL_IN
        self.max_stamina = STAMINA_ZHITEL_IN
        self.reakciya = REAKCIYA_ZHITEL_IN
        self.harakteristiki()

        self.scale = 0.9

        main_patch = 'nuzhno/female_person/femalePerson_'
        self.idle_texture = arcade.load_texture_pair(f'{main_patch}idle.png')
        self.jump_texture = arcade.load_texture_pair(f'{main_patch}jump.png')
        self.fall_texture = arcade.load_texture_pair(f'{main_patch}fall.png')
        self.udar_texture = arcade.load_texture_pair(f'{main_patch}climb0.png')
        self.texture = self.idle_texture[1]
        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}walk{i}.png")
            self.walk_textures.append(tex)

        self.pers = 'zhitel_innocentii'

        self.vila = cold_oruzhie.Vila(self, self.sprite_list)
        self.sposob_list.append(self.vila)
        self.oruzh_list.append(self.vila)
        self.topor = cold_oruzhie.Topor(self, self.sprite_list, 30, 20)
        self.sposob_list.append(self.topor)
        self.oruzh_list.append(self.topor)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii(dx, physics_engine)

        self.block_animation()
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()
        if self.tipo_return:
            return

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)
        # self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()


class Brend(Vrag):
    def __init__(self, igrok, sprite_list, v_drug_list, walls_list, tip=1206, kast_scena=False):
        super().__init__(igrok, sprite_list, v_drug_list, walls_list, tip, kast_scena)
        self.max_hp = HP_BREND
        self.max_stamina = STAMINA_BREND
        self.reakciya = REAKCIYA_BREND
        self.harakteristiki()

        main_patch = 'nuzhno/male_adventurer/maleAdventurer'
        self.idle_texture = arcade.load_texture_pair(f"{main_patch}_idle.png")
        self.jump_texture = arcade.load_texture_pair(f"{main_patch}_jump.png")
        self.fall_texture = arcade.load_texture_pair(f"{main_patch}_fall.png")
        self.udar_texture = arcade.load_texture_pair('nuzhno/udar2.png')
        self.scale = 1.05

        for i in range(8):
            tex = arcade.load_texture_pair(f"{main_patch}_walk{i}.png")
            self.walk_textures.append(tex)
        self.texture = self.idle_texture[self.storona]

        self.mech_Brenda = cold_oruzhie.MechBrenda(self, self.sprite_list, 10, 10)
        self.sposob_list.append(self.mech_Brenda)
        self.oruzh_list.append(self.mech_Brenda)

        self.pers = 'Brend'

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.tipo_return = False

        self.ii(dx, physics_engine)

        self.block_animation()
        if self.tipo_return:
            return
        self.udar_func()
        if self.tipo_return:
            return

        self.jump_animation(dy)
        if self.tipo_return:
            return
        self.idle_animation(dx)
        if self.tipo_return:
            return
        self.walk_animation()
        if self.tipo_return:
            return

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)
        #self.oglush_update()
        self.update_udar()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.oruzh_update_animation()
