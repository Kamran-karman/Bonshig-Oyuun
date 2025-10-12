import random

import hit_box_and_radius
import sposobs
from interaction_sprites import battles
from interaction_sprites.battles import effect_update, X_D_ZONE
from animations.pers_animations import spec_battle_animations
import arcade
from sposobs.fiz_sposob import cold_oruzhie
from sposobs.fiz_sposob import baf_ogon_cold
from sposobs import dal_oruzh
from sposobs.stihiya import ogon
from interaction_sprites.battles.mobs import vrags


class __Gorozhanen(vrags.Vrag):
    def __init__(self, igrok, name, walls_list: arcade.SpriteList):
        super().__init__(igrok, name, walls_list)
        self.max_hp = 1000
        self.max_mana = 25
        self.max_stamina = 100
        self.harakteristiki()

        self.scale = 1.5
        self.kvadrat_radius.update()

        self.reakciya = 10
        self.vel_x = self.walk_vel_x = vrags.VRAG_VEL_X
        self.beg_vel_x = self.vel_x * 1.7

        self.block.timer_for_s_ab = 30

        self.animations = spec_battle_animations.GorozhanenAnimations(self)

        self.udar.scale = self.scale + 0.05
        self.uron = 7
        self.udar.main_block = False
        self.udar.timer_for_s_kd = 30
        self.sposob_list.append(self.udar)

        self._stop_update_storona = False

        self.kulak_ognya = ogon.KulakOgnya(self, self.sprite_list)
        self.kulak_ognya.s_kd = self.kulak_ognya.timer_for_s_kd = 300
        self.sposob_list.append(self.kulak_ognya)

        self.radius_ataki = hit_box_and_radius.Radius(self, 0.25)
        self.radius_list.append(self.radius_ataki)

        self.s_action = 0
        self.timer_for_s_action = 0

        self.d_zone = 40

        self._name_drug_list = arcade.SpriteList()

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if not self._stop_update_storona:
            self._battle_update_storona(dx, X_D_ZONE)
        self.fizika.update(physics_engine, dx, dy)

        self.animations.tipo_return = False

        self.animations.smert_animation()
        if self.animations.tipo_return:
            return

        self.animations.sbiv_animation()
        if self.animations.tipo_return:
            return

        if not self.oglush:
            self.animations.vstat_animation()
            if self.animations.tipo_return:
                return

            self.animations.udaren_animation()
            if self.animations.tipo_return:
                return

            self.animations.block_animation()
            if self.animations.tipo_return:
                return

            self.animations.udar_animations()
            if self.animations.tipo_return:
                return

            self.animations.plus_animations(dx, dy, self.fizika.is_on_ground, battles.X_D_ZONE, battles.Y_D_ZONE,
                                            self.fizika.x_odometr, 1)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self._update_harakteristiki()
        self.update_sposob_list(self.fizika.fizika)
        self._update_beg()
        self.update_popad()
        self.ii()

        self.s_oglush, self.oglush = effect_update(self.oglush, self.s_oglush, self.timer_for_s_oglush)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.draw_sposob_list()

    def _move_not_ii(self):
        if self.not_ii:
            self.can_jump()
            self.move()

    def append_drug(self, drug):
        super().append_drug(drug)
        if drug != self and self.name == drug.name:
            self._name_drug_list.append(drug)


class G1(__Gorozhanen):
    '''
    Бежит
    '''

    def __init__(self, igrok, walls_list):
        super().__init__(igrok, "G1", walls_list)
        self.max_hp += 150
        self.harakteristiki()

        self.oruhz = cold_oruzhie.Molotok(self, self.sprite_list)
        self.oruhz.main_block = True
        self.block = self.oruhz
        self.sposob_list.append(self.oruhz)

        self.timer_for_s_action = 180
        self.radius_action.scale = 1

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            match self.povedenie:
                case 0:
                    if self.radius_action.check_collision(self.igrok) and self.s_action == 0:
                        self.povedenie = 1

                    if self.s_action != 0:
                        self.s_action -= 1
                case 1:
                    self.beg = True
                    self.walk = False
                    self.s_action += 1
                    if self.s_action >= self.timer_for_s_action or self.popad:
                        self.beg = False
                        self.walk = True
                        self.povedenie = 0
                    if self.radius_ataki.check_collision(self.igrok):
                        self.beg = False
                        self.walk = True
                        self.s_action = 0
                        self.povedenie = 2
                        if not self.kulak_ognya.kd:
                            self.kulak_ognya.action = True
                case 2:
                    if self.radius_ataki.check_collision(self.igrok):
                        if not self.oruhz.kd and not (self.block.block or self.block.avto_block) and not self.kulak_ognya.action:
                            self.oruhz.action = True
                    else:
                        self.povedenie = 0
        elif self.oglush:
            self.s_action = self.povedenie = 0
            self.oruhz.s += self.oruhz.timer_for_s
            self.beg = False
            self.walk = True


class G2(__Gorozhanen):
    '''
    Танк
    '''

    def __init__(self, igrok, walls_list):
        super().__init__(igrok, "G2", walls_list)
        self.max_hp += 300
        self.max_mana += 5
        self.harakteristiki()

        self.oruhz = cold_oruzhie.Molotok(self, self.sprite_list)
        self.oruhz.main_block = True
        self.block = self.oruhz
        self.sposob_list.append(self.oruhz)

        self.radius_action.scale = 1.7
        self.timer_for_s_action = 180

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            match self.povedenie:
                case 0:
                    if self.s_action == 0:
                        if self.radius_action.check_collision(self.igrok):
                            self.povedenie = 1
                            self.s_action = 0
                            self.block.block = True
                    else:
                        self.s_action -= 1
                case 1:
                    self.s_action += 1
                    if self.s_action >= self.timer_for_s_action:
                        self.block.block = False
                        self.povedenie = 0
                    if self.radius_ataki.check_collision(self.igrok):
                        self.block.block = False
                        self.s_action = 0
                        self.povedenie = 2
                case 2:
                    if self.radius_ataki.check_collision(self.igrok):
                        if self.kulak_ognya.kd:
                            if not self.oruhz.kd and not (self.block.block or self.block.avto_block) and not self.kulak_ognya.action:
                                self.oruhz.action = True
                        elif not self.kulak_ognya.kd and not (self.block.block or self.block.avto_block) and not self.oruhz.action:
                            self.kulak_ognya.action = True
                    else:
                        self.povedenie = 0
        elif self.oglush:
            self.s_action = self.povedenie = 0
            self.oruhz.s += self.oruhz.timer_for_s
            self.block.block = False


class G3(__Gorozhanen):
    '''
    Отступает
    '''

    def __init__(self, igrok, walls_list):
        super().__init__(igrok, "G3", walls_list)
        self.oruhz = cold_oruzhie.Molotok(self, self.sprite_list)
        self.oruhz.main_block = True
        self.block = self.oruhz
        self.sposob_list.append(self.oruhz)

        self.timer_for_s_action = 45
        self.radius_action.scale = 1
        self.nazad = False

        self.raduis_stop = hit_box_and_radius.Radius(self, 1.6)
        self.radius_list.append(self.raduis_stop)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.povedenie != 0:
            self._stop_update_storona = False
        super().pymunk_moved(physics_engine, dx, dy, d_angle)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            def check_drug(drug, func, s_list: list, x: int = 30):
                if ((self.igrok.center_x > drug.center_x > self.center_x + x
                     or self.center_x - x > drug.center_x > self.igrok.center_x) and drug.name != self.name):
                    func()
                    s_list[0] += 1
                if drug.name == self.name:
                    s_list[1] += 1

            match self.povedenie:
                case 0:
                    self.not_ii = True
                    self._stop_update_storona = True

                    def func():
                        self.not_ii = False
                        self.povedenie = 1

                    if self.radius_ataki.check_collision(self.igrok):
                        x = 30
                    else:
                        x = 150

                    d = 0
                    spis = [0, 0]
                    for drug in self.drug_list:
                        check_drug(drug, func, spis, x)

                        if ((self.igrok.center_x > drug.center_x > self.center_x
                             or self.center_x > drug.center_x > self.igrok.center_x) and drug.name != self.name):
                            d += 1

                    if spis[1] == len(self.drug_list):
                        self.povedenie = 3
                        self.not_ii = True
                        return

                    if spis[0] > 0:
                        return
                    else:
                        if self.radius_action.check_collision(self.igrok) and d == 0:
                            self.kulak_ognya.action = True
                            self.povedenie = 2
                        else:
                            self.friction = 0.7
                            if self.igrok.center_x > self.center_x:
                                self.storona = 0
                            else:
                                self.storona = 1
                            if self.s_action < self.timer_for_s_action and not self.nazad:
                                self.s_action += 1
                                self.force_x = 10000
                                if self.s_action == self.timer_for_s_action:
                                    self.nazad = True
                            elif self.s_action > 0 and self.nazad:
                                self.s_action -= 1
                                self.force_x = -10000
                                if self.s_action == 0:
                                    self.nazad = False

                            # self.can_jump()
                            #
                            # self.move()
                case 1:
                    a = 0
                    for drug in self.drug_list:
                        if ((self.igrok.center_x > self.center_x > drug.center_x + 30
                             or drug.center_x - 30 > self.center_x > self.igrok.center_x) and drug.name != self.name):
                            self.not_ii = True
                            self.povedenie = 0
                            return
                        if drug.name == self.name:
                            a += 1

                    if a == len(self.drug_list):
                        self.povedenie = 3
                        self.not_ii = True
                    else:
                        if self.radius_ataki.check_collision(self.igrok):
                            if not self.oruhz.kd and not (self.block.block or self.block.avto_block):
                                self.oruhz.action = True
                case 2:
                    def func():
                        self.not_ii = True
                        self.povedenie = 0

                    spis = [0, 0]
                    for drug in self.drug_list:
                        check_drug(drug, func, spis)

                    if spis[1] == len(self.drug_list):
                        self.povedenie = 3
                        self.not_ii = True
                        return

                    if spis[0] > 0:
                        self.beg = False
                        self.walk = True
                        return
                    else:
                        if self.raduis_stop.check_collision(self.igrok):
                            self.friction = 0.7
                            self.beg = True
                            self.walk = False
                            if self.igrok.center_x > self.center_x:
                                self.force_x = -10000
                            else:
                                self.force_x = 10000
                            # self.can_jump()
                            # self.move()
                        else:
                            self.povedenie = 0
                            self.beg = False
                            self.walk = True
                case 3:
                    a = 0
                    for drug in self.drug_list:
                        if drug.name == self.name:
                            a += 1

                    if a == len(self.drug_list):
                        self.friction = 0.7
                        self.beg = True
                        self.walk = False
                        if self.igrok.center_x > self.center_x:
                            self.force_x = -10000
                        else:
                            self.force_x = 10000

                        # self.can_jump()

                        for wall in self.walls_list:
                            if (self.kvadrat_radius.check_collision(wall) and wall.center_y > self.center_y and
                                    ((wall.center_x > self.center_x > self.igrok.center_x) or
                                     (wall.center_x < self.center_x < self.igrok.center_x)) and self.fizika.dx < X_D_ZONE):
                                self.povedenie = 4
                                self.kulak_ognya.timer_for_s_kd = 120
                                self.not_ii = False
                                return
                    else:
                        self.friction = 0
                        self.force_x = 0
                        self.beg = False
                        self.walk = True
                        self.povedenie = 0

                    # self.move()
                case 4:
                    if not self.radius_ataki.check_collision(self.igrok) and self.radius_action.check_collision(self.igrok):
                        self.beg = True
                        self.walk = False
                    elif self.radius_ataki.check_collision(self.igrok):
                        self.walk = True
                        self.beg = False
                        if self.kulak_ognya.kd:
                            if not self.oruhz.kd and not (
                                    self.block.block or self.block.avto_block) and not self.kulak_ognya.action:
                                self.oruhz.action = True
                        elif not self.kulak_ognya.kd and not (
                                self.block.block or self.block.avto_block) and not self.oruhz.action:
                            self.kulak_ognya.action = True
                    elif not self.radius_action.check_collision(self.igrok):
                        self.beg = False
                        self.walk = True


        elif self.oglush:
            self.s_action = self.povedenie = 0
            self.nazad = False
            self.oruhz.s += self.oruhz.timer_for_s
            self.block.block = False
            self.beg = False
            self.walk = True

        self._move_not_ii()


class __Opolchenec(__Gorozhanen):
    def __init__(self, igrok, name, walls_list: arcade.SpriteList):
        super().__init__(igrok, name, walls_list)
        self.min_hp = 0
        self.min_mana = 0

        self.max_hp = 2300
        self.max_mana = 50
        self.max_stamina = 200
        self.harakteristiki()

        self.reakciya = 14

        self.animations = spec_battle_animations.OpolchenecAnimations(self)

        self.beg_vel_x = self.vel_x * 1.9

        self.uron = 10

        self.kulak_ognya.timer_for_s_kd = ogon.KulakOgnya(self, self.sprite_list).timer_for_s_kd
        self.__kul_og_kd = self.kulak_ognya.timer_for_s_kd

        self.mini_fire_ball = ogon.MiniFireBall(self, self.sprite_list)
        self.sposob_list.append(self.mini_fire_ball)

    @property
    def kul_og_kd(self):
        return self.__kul_og_kd

    def harakteristiki(self):
        super().harakteristiki()
        self.min_hp = self.max_hp * 0.3
        self.min_mana = self.max_mana * 0.25


class OpMdd1(__Opolchenec):
    def __init__(self, igrok, walls_list: arcade.SpriteList):
        super().__init__(igrok, "OpMdd1", walls_list)
        self.oruzh = baf_ogon_cold.OgonMolotok(self, self.sprite_list)
        self.oruzh.main_block = True
        self.oruzh.baf = True
        self.block = self.oruzh
        self.sposob_list.append(self.oruzh)

        self.__radius_beg = hit_box_and_radius.Radius(self)
        self.radius_list.append(self.__radius_beg)
        self.__radius_fireball = hit_box_and_radius.Radius(self)
        self.radius_action.scale = 2

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            if self.hp <= self.min_hp and self.povedenie < 4:
                self.walk = False
                self.beg = True
                self.block.block = False
                self.povedenie = 4
                if self.mana > self.min_mana:
                    self.kulak_ognya.timer_for_s_kd //= 2
            if self.mana <= self.min_mana and self.kul_og_kd >= self.kulak_ognya.timer_for_s_kd:
                self.kulak_ognya.timer_for_s_kd = self.kul_og_kd * 5
                self.oruzh.timer_for_s_kd //= 2
                self.oruzh.baf = False
            elif self.mana > self.min_mana and self.kulak_ognya.timer_for_s_kd == self.kul_og_kd * 5:
                self.kulak_ognya.timer_for_s_kd = self.kul_og_kd
                self.oruzh.timer_for_s_kd *= 2

            match self.povedenie:
                case 0:
                    if self.radius_action.check_collision(self.igrok):
                        if not self.radius_ataki.check_collision(sprite_list=self.drug_list):
                            self.block.block = True
                            self.povedenie = 1
                        else:
                            if not self.mini_fire_ball.kd:
                                self.mini_fire_ball.action = True
                            self.beg = True
                            self.walk = False
                            self.povedenie = 2
                case 1:
                    self.block.block = True
                    if (self.radius_ataki.check_collision(sprite_list=self.drug_list) or (
                        not self.radius_ataki.check_collision(sprite_list=self.drug_list) and
                        self.__radius_beg.check_collision(self.igrok)
                    )) and not self.popad:
                        if not self.mini_fire_ball.kd:
                            self.mini_fire_ball.action = True
                        self.povedenie = 2
                        self.block.block = False
                        self.beg = True
                        self.walk = False
                    else:
                        if not self.radius_action.check_collision(self.igrok):
                            self.povedenie = 0
                            self.block.block = False
                case 2:
                    if not self.radius_action.check_collision(self.igrok):
                        self.povedenie = 0
                        self.beg = False
                        self.walk = True
                    else:
                        if self.popad:
                            self.povedenie = 1
                            self.block.block = True
                            self.walk = True
                            self.beg = False
                        else:
                            if self.radius_ataki.check_collision(self.igrok):
                                self.oruzh.action = True
                                self.povedenie = 3
                            elif (self.__radius_beg.check_collision(self.igrok) and not self.kulak_ognya.action
                                  and not self.kulak_ognya.kd):
                                self.kulak_ognya.action = True
                case 3:
                    if not self.radius_ataki.check_collision(self.igrok):
                        self.mini_fire_ball.action = True
                        self.povedenie = 2
                    else:
                        if (not self.kulak_ognya.action and not self.kulak_ognya.kd and not self.oruzh.action
                                and not (self.block.block or self.block.avto_block)):
                            self.kulak_ognya.action = True
                        elif (not self.kulak_ognya.action and not self.oruzh.kd and not self.oruzh.action
                              and not (self.block.block or self.block.avto_block)):
                            self.oruzh.action = True
                case 4:
                    if self.radius_ataki.check_collision(self.igrok):
                        if (not self.kulak_ognya.action and not self.kulak_ognya.kd and not self.oruzh.action
                                and not (self.block.block or self.block.avto_block)):
                            self.kulak_ognya.action = True
                        elif (not self.kulak_ognya.action and not self.oruzh.kd and not self.oruzh.action
                              and not (self.block.block or self.block.avto_block)):
                            self.oruzh.action = True
        elif self.oglush and self.povedenie != 4:
            self.povedenie = 1
            self.walk = True
            self.beg = False
            self.block.block = False


class OpMdd2(__Opolchenec):
    def __init__(self, igrok, walls_list: arcade.SpriteList):
        super().__init__(igrok, "OpMdd2", walls_list)
        self.max_hp += 300
        self.harakteristiki()

        self.oruzh = cold_oruzhie.Molotok(self, self.sprite_list)
        self.oruzh.main_block = True
        self.oruzh.baf = True
        self.block = self.oruzh
        self.sposob_list.append(self.oruzh)

        self.radius_action.scale = 1.5

        self.s_block = 0
        self.timer_for_s_block = 15

        self.s_kombo = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            for drug in self.drug_list:
                if ((drug.center_x > self.center_x and self.storona == 0
                    or drug.center_x < self.center_x and self.storona == 1) and drug.name != self.name
                        and not self.radius_ataki.check_collision(self.igrok)):
                    if drug.beg and (self.storona == 0 and drug.fizika.dx <= 0
                                     or self.storona == 1 and drug.fizika.dx >= 0):
                        self.povedenie = 4
                        self.beg = True
                        self.walk = self.block.block = False
                        self.mini_fire_ball.action = True

            if self.povedenie != 4:
                if self.hp < self.min_hp and self.povedenie != 5:
                    self.povedenie = 5
                    self.block.block = self.walk = True
                    self.beg = False
                    self.s_kombo = 0

            if (self.mana <= self.min_mana and (self.kulak_ognya.timer_for_s_kd == self.kul_og_kd
                    or self.kulak_ognya.timer_for_s_kd == 10)):
                if self.kulak_ognya.timer_for_s_kd == 10:
                    self.s_kombo = 4
                self.kulak_ognya.timer_for_s_kd = self.kul_og_kd * 5
                self.mini_fire_ball.timer_for_s_kd *= 5
            elif self.mana > self.min_mana and self.kulak_ognya.timer_for_s_kd == self.kul_og_kd * 5:
                self.kulak_ognya.timer_for_s_kd = self.kul_og_kd
                self.mini_fire_ball.timer_for_s_kd //= 5
                self.oruzh.baf = False

            match self.povedenie:
                case 0:
                    if self.radius_action.check_collision(self.igrok) or self.popad:
                        self.povedenie = 1
                        self.block.block = True
                    else:
                        for drug in self.drug_list:
                            if (drug.center_x > self.center_x and self.storona == 0
                                    or drug.center_x < self.center_x and self.storona == 1) and drug.beg:
                                self.mini_fire_ball.action = True
                                self.povedenie = 2
                                self.beg = True
                                self.walk = False
                                break
                case 1:
                    if not self.radius_action.check_collision(self.igrok):
                        self.s_block += 1
                        if self.popad:
                            self.s_block = 0
                        if self.s_block >= self.timer_for_s_block:
                            self.s_block = self.povedenie = 0
                            self.block.block = False
                    else:
                        self.s_block = 0
                        if self.radius_ataki.check_collision(self.igrok):
                            self.block.block = False
                            self.kulak_ognya.action = True
                            self.kulak_ognya.timer_for_s_kd = 10
                            self.povedenie = 3
                        else:
                            for drug in self.drug_list:
                                if (drug.center_x > self.center_x and self.storona == 0
                                        or drug.center_x < self.center_x and self.storona == 1) and drug.beg:
                                    self.mini_fire_ball.action = True
                                    self.povedenie = 2
                                    self.beg = True
                                    self.walk = self.block.block = False
                                    break
                case 2:
                    if self.radius_ataki.check_collision(self.igrok):
                        self.kulak_ognya.action = self.walk = True
                        self.kulak_ognya.timer_for_s_kd = 10
                        self.beg = False
                        self.povedenie = 3
                    else:
                        s = 0
                        for drug in self.drug_list:
                            if (drug.center_x > self.center_x and self.storona == 0
                                    or drug.center_x < self.center_x and self.storona == 1) and drug.beg:
                                s += 1
                        if s == 0 or self.popad:
                            self.povedenie = 1
                            self.block.block = self.walk = True
                            self.beg = False
                case 3:
                    if self.radius_ataki.check_collision(self.igrok):
                        if self.s_kombo < 4:
                            if not self.kulak_ognya.action and not self.kulak_ognya.kd:
                                self.kulak_ognya.action = True
                                self.s_kombo += 1
                                if self.s_kombo == 4:
                                    self.kulak_ognya.timer_for_s_kd = self.kul_og_kd
                        else:
                            if (not self.kulak_ognya.action and not self.kulak_ognya.kd and not self.oruzh.action
                                    and not (self.block.block or self.block.avto_block)):
                                self.kulak_ognya.action = True
                            elif (not self.kulak_ognya.action and not self.oruzh.kd and not self.oruzh.action
                                  and not (self.block.block or self.block.avto_block)):
                                self.oruzh.action = True
                    else:
                        self.mini_fire_ball.action = True
                        self.povedenie = self.s_kombo = 0
                case 4:
                    s = 0
                    for drug in self.drug_list:
                        if ((drug.center_x > self.center_x and self.storona == 0
                             or drug.center_x < self.center_x and self.storona == 1) and drug.name != self.name
                                and not self.radius_ataki.check_collision(self.igrok)):
                            if drug.beg and (self.storona == 0 and drug.fizika.dx <= 0
                                             or self.storona == 1 and drug.fizika.dx >= 0):
                                s += 1

                    if s == 0:
                        self.povedenie = 1
                        self.block.block = self.walk = True
                        self.beg = False
                case 5:
                    if self.popad:
                        self.s_block = 0
                    if self.s_block < self.timer_for_s_block:
                        self.s_block += 1
                    else:
                        if self.radius_ataki.check_collision(self.igrok):
                            match self.s_kombo:
                                case 0:
                                    if not self.kulak_ognya.kd:
                                        self.block.block = False
                                        self.kulak_ognya.action = True
                                    self.s_kombo += 1
                                case 1:
                                    if not self.kulak_ognya.action:
                                        self.block.block = True
                                        self.s_block = 0
                                        self.s_kombo += 1
                                case 2:
                                    self.block.block = False
                                    self.oruzh.action = True
                                    self.s_kombo += 1
                                case 3:
                                    if not self.oruzh.action:
                                        self.block.block = True
                                        self.s_block = self.s_kombo = 0
                        else:
                            self.s_kombo = 0
                            if self.radius_action.check_collision(self.igrok):
                                self.block.block = self.walk = True
                                self.beg = False
                            else:
                                self.beg = True
                                self.block.block = self.walk = False
        elif self.oglush:
            if self.povedenie != 4:
                self.povedenie = 1
            self.block.block = False
            self.walk = True
            self.beg = False
            if self.s_oglush + 1 >= self.timer_for_s_oglush:
                self.block.block = True

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self._battle_update_storona(dx, X_D_ZONE)
        super().pymunk_moved(physics_engine, dx, dy, d_angle)


class __OpRdd(__Opolchenec):
    def __init__(self, igrok, name, walls_list):
        super().__init__(igrok, name, walls_list)
        self.radius_ataki.scale = 1.3
        self.radius_action.scale = 0.9
        self._radius_stop = hit_box_and_radius.Radius(self, 1.5)
        self.radius_list.append(self._radius_stop)
        self._radius_blizko = hit_box_and_radius.Radius(self, 0.3)
        self.radius_list.append(self._radius_blizko)

        self.ognen_snaryad = ogon.OgnenSnaryad(self, self.sprite_list)
        self.sposob_list.append(self.ognen_snaryad)
        self.fireball = ogon.FireBall(self, self.sprite_list)
        self.sposob_list.append(self.fireball)
        self.kulak_ognya.timer_for_s_kd = 60


class OpRdd1(__OpRdd):
    def __init__(self, igrok, walls_list: arcade.SpriteList):
        super().__init__(igrok, "OpRdd1", walls_list)
        self.max_mana += 20
        self.max_hp -= 300
        self.harakteristiki()

        self.__odni = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            if not self.__odni:
                if self.hp <= self.min_hp:
                    if self.povedenie == 0:
                        self.povedenie = 6
                    if self.radius_ataki.scale < 1.6:
                        self.not_ii = True
                        self.povedenie = 6
                        self.radius_ataki.scale += 0.3
                        self.radius_action.scale += 0.3
                        self._radius_stop.scale += 0.3
                        if self.mana > self.min_mana:
                            for sposob in self.sposob_list:
                                if sposob.klass == sposobs.STIHIYA:
                                    sposob.timer_for_s_kd //= 3

                for drug in self.drug_list:
                    if drug.name != self.name:
                        break
                else:
                    print("_5____--")
                    self.povedenie = 5
                    self._radius_stop.scale = self.radius_ataki.scale
                    self.__odni = True

            if self.mana <= self.min_mana and self.kulak_ognya.timer_for_s_kd < self.kul_og_kd * 2:
                self.kulak_ognya.timer_for_s_kd = self.kul_og_kd * 2
                if self.hp <= self.min_hp:
                    a = 6
                else:
                    a = 2
                for sposob in self.sposob_list:
                    if sposob.klass == sposobs.STIHIYA:
                        sposob.timer_for_s_kd *= a

            match self.povedenie:
                case 0:
                    if self.radius_ataki.check_collision(self.igrok):
                        def atak():
                            if self.igrok.center_x > self.center_x:
                                self.storona = 0
                            else:
                                self.storona = 1
                            self.povedenie = 1
                            self.not_ii = self.fireball.action = True
                            self.friction = 1
                            self.force_x = 0

                        if self.radius_ataki.check_collision(sprite_list=self.drug_list):
                            for drug in self.drug_list:
                                if (self.igrok.center_x > self.center_x > drug.center_x or
                                        self.igrok.center_x < self.center_x < drug.center_x) and drug.name != self.name:
                                    self.povedenie = 2
                                    self.not_ii = True
                                    self._stop_update_storona = True
                                    break
                            else:
                                atak()
                        else:
                            atak()
                case 1:
                    if self.igrok.center_x > self.center_x:
                        self.storona = 0
                    else:
                        self.storona = 1
                    if self.radius_action.check_collision(self.igrok):
                        if not self.mini_fire_ball.kast:
                            self.mini_fire_ball.action = True
                            if self.mini_fire_ball.kd:
                                self.povedenie = 3
                                self.beg = self._stop_update_storona = True
                                self.walk = False
                    else:
                        if self.radius_ataki.check_collision(self.igrok):
                            if not self.block.block and not self.block.avto_block:
                                if (not self.fireball.action and not self.fireball.kd and not self.mini_fire_ball.kast
                                        and not self.ognen_snaryad.kast):
                                    self.fireball.action = True
                                elif (not self.fireball.kast and not self.mini_fire_ball.kd and not self.mini_fire_ball.action
                                        and not self.ognen_snaryad.kast):
                                    self.mini_fire_ball.action = True
                                elif (not self.fireball.kast and not self.ognen_snaryad.kd and not self.mini_fire_ball.kast
                                        and not self.ognen_snaryad.action):
                                    self.ognen_snaryad.action = True
                        else:
                            self.not_ii = False
                            self.povedenie = 0
                case 2:
                    def nazad(storona):
                        self.friction = 0.7
                        self.force_x = 10000 if storona == 1 else -10000
                        self.storona = storona

                    for drug in self.drug_list:
                        if drug.name != self.name:
                            if self.igrok.center_x > self.center_x > drug.center_x:
                                nazad(0)
                            elif self.igrok.center_x < self.center_x < drug.center_x:
                                nazad(1)
                            elif (self.igrok.center_x > drug.center_x - 100 > self.center_x or
                                  self.igrok.center_x < drug.center_x + 100 < self.center_x):
                                if self.radius_ataki.check_collision(self.igrok):
                                    if self.igrok.center_x > self.center_x:
                                        self.storona = 0
                                    else:
                                        self.storona = 1
                                    self.povedenie = 1
                                    self.fireball.action = True
                                    self._stop_update_storona = False
                                    self.force_x = 0
                                    self.friction = 1
                                else:
                                    self.povedenie = 0
                                    self.not_ii = self._stop_update_storona = False
                case 3:
                    if self._radius_stop.check_collision(self.igrok):
                        self.friction = 0.7
                        if self.igrok.center_x > self.center_x:
                            self.force_x = -10000
                            self.storona = 1
                        else:
                            self.force_x = 10000
                            self.storona = 0

                        if self.kvadrat_radius.check_collision(sprite_list=self.walls_list):
                            for wall in self.walls_list:
                                if ((self.igrok.center_x > self.center_x > wall.center_x
                                     or self.igrok.center_x < self.center_x < wall.center_x) and wall.center_y > self.top
                                        and self.kvadrat_radius.check_collision(wall)):
                                    self.povedenie = 4
                                    self.friction = 1
                                    self.force_x = 0
                                    self.walk = True
                                    self.beg = self._stop_update_storona = False
                    else:
                        if self.igrok.center_x > self.center_x:
                            self.storona = 0
                        else:
                            self.storona = 1
                        self.povedenie = 0
                        self.not_ii = self._stop_update_storona = self.beg = False
                        self.walk = True
                case 4:
                    if self._radius_stop.check_collision(self.igrok) and not self.block.block and not self.block.avto_block:
                        if (not self.fireball.action and not self.fireball.kd and not self.mini_fire_ball.kast
                                and not self.ognen_snaryad.kast and not self.kulak_ognya.kast):
                            self.fireball.action = True
                        elif (not self.fireball.kast and not self.mini_fire_ball.kd and not self.mini_fire_ball.action
                                  and not self.ognen_snaryad.kast and not self.kulak_ognya.kast):
                            self.mini_fire_ball.action = True
                        elif (not self.fireball.kast and not self.ognen_snaryad.kd and not self.mini_fire_ball.kast
                                  and not self.ognen_snaryad.action and not self.kulak_ognya.kast):
                            self.ognen_snaryad.action = True
                        elif (self._radius_blizko.check_collision(self.igrok) and not self.fireball.kast
                                and not self.kulak_ognya.kd and not self.mini_fire_ball.kast and not self.ognen_snaryad.action
                                    and not self.kulak_ognya.action):
                            self.kulak_ognya.action = True
                    else:
                        self.not_ii = False
                        if not self.__odni:
                            self.povedenie = 0
                        else:
                            self.povedenie = 5
                case 5:
                    if self.radius_ataki.check_collision(self.igrok):
                        self.not_ii = self.walk = True
                        self.beg = False
                        self.fireball.action = True
                        self.povedenie = 4
                        self.friction = 1
                        self.force_x = 0
                    else:
                        self.not_ii = False
                        self._stop_update_storona = False
                case 6:
                    def nazad(storona):
                        self.friction = 0.7
                        self.force_x = 10000 if storona == 0 else -10000
                        self.storona = storona

                    def drug_check():
                        for drug in self.drug_list:
                            if drug.name != self.name:
                                if (self.igrok.center_x > drug.center_x > self.center_x + 500 or
                                        self.igrok.center_x < drug.center_x < self.center_x - 500):
                                    return False
                        return True

                    if self.kvadrat_radius.check_collision(sprite_list=self.walls_list):
                        for wall in self.walls_list:
                            if ((self.igrok.center_x > self.center_x > wall.center_x
                                    or self.igrok.center_x < self.center_x < wall.center_x) and wall.center_y > self.top
                                    and self.kvadrat_radius.check_collision(wall)):
                                self.povedenie = 5
                                self._radius_stop.scale = self.radius_ataki.scale
                                self.__odni = True
                                return

                    if self.radius_ataki.check_collision(self.igrok):
                        self.not_ii = True
                        if self.radius_action.check_collision(self.igrok) or drug_check():
                            self._stop_update_storona = self.beg = self.not_ii = True
                            self.walk = False
                            self.povedenie = 3

                        self.friction = 1
                        self.apply_force_x(0)
                        if not self.block.block and not self.block.avto_block:
                            if (not self.fireball.action and not self.fireball.kd
                                    and not self.mini_fire_ball.kast and not self.ognen_snaryad.kast):
                                self.fireball.action = True
                            elif (not self.fireball.kast and not self.mini_fire_ball.kd
                                  and not self.mini_fire_ball.action and not self.ognen_snaryad.kast):
                                self.mini_fire_ball.action = True
                            elif (not self.fireball.kast and not self.ognen_snaryad.kd
                                  and not self.mini_fire_ball.kast and not self.ognen_snaryad.action):
                                self.ognen_snaryad.action = True
                    else:
                        self.not_ii = False
                        self.friction = 0.7
                        self.apply_force_x(10000)

        elif self.oglush:
            self.walk = True
            self.not_ii = self.beg = self.block.block = False
            if not self.__odni:
                self.povedenie = 0
            else:
                self.povedenie = 5

        self._move_not_ii()


class OpRdd2(__OpRdd):
    def __init__(self, pers, walls_list):
        super().__init__(pers, "OpRdd2", walls_list)
        self.max_mana += 15
        self.max_hp -= 100
        self.harakteristiki()

        self.oruzh = cold_oruzhie.Molotok(self, self.sprite_list)
        self.oruzh.main_block = True
        self.oruzh.baf = True
        self.block = self.oruzh
        self.sposob_list.append(self.oruzh)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.operation == 0:
            def ataka():
                def dal_ataki():
                    if (not self.fireball.action and not self.fireball.kd and not self.mini_fire_ball.kast
                            and not self.ognen_snaryad.kast):
                        self.fireball.action = True
                    elif (not self.fireball.kast and not self.mini_fire_ball.kd and not self.mini_fire_ball.action
                              and not self.ognen_snaryad.kast):
                        self.mini_fire_ball.action = True
                    elif (not self.fireball.kast and not self.ognen_snaryad.kd and not self.mini_fire_ball.kast
                              and not self.ognen_snaryad.action):
                        self.ognen_snaryad.action = True

                if not self.block.block and not self.block.avto_block:
                    if not self._radius_blizko.check_collision(self.igrok):
                        dal_ataki()
                    else:
                        if not self.fireball.kast and not self.mini_fire_ball.kast and not self.ognen_snaryad.kast:
                            if not self.oruzh.action and not self.oruzh.kd and not self.kulak_ognya.kast:
                                self.oruzh.action = True
                            elif not self.oruzh.action and not self.kulak_ognya.kd and not self.kulak_ognya.action:
                                self.kulak_ognya.action = True
                            elif not self.oruzh.action or not self.kulak_ognya.kast:
                                dal_ataki()

            if self.povedenie != 3:
                for drug in self.drug_list:
                    if drug.name != self.name and drug.beg and drug.storona != self.storona and abs(self.center_x - drug.center_x) < 100:
                        self.beg = self.not_ii = True
                        self.walk = False
                        self.povedenie = 3

            if self.hp <= self.min_hp and self.povedenie != 5:
                if self.povedenie != 3:
                    self.povedenie = 4
                    self.beg = False
                    self.walk = True
                    self.not_ii = False
                if self.kulak_ognya.timer_for_s_kd == self.kul_og_kd // 2 and self.mana > self.min_mana:
                    for sposob in self.sposob_list:
                        if sposob.klass == sposobs.STIHIYA:
                            sposob.timer_for_s_kd //= 3

            if self.mana <= self.min_mana:
                if self.povedenie != 3:
                    self.povedenie = 5

                if self.kulak_ognya.timer_for_s_kd < self.kul_og_kd:
                    self.oruzh.baf = False
                    for sposob in self.sposob_list:
                        if sposob.klass == sposobs.STIHIYA:
                            if self.hp <= self.min_hp:
                                sposob.timer_for_s_kd *= 6
                            else:
                                sposob.timer_for_s_kd *= 2

            match self.povedenie:
                case 0:
                    if self.radius_ataki.check_collision(self.igrok):
                        self.povedenie = 1
                        self.beg = False
                        self.not_ii = self.fireball.action = self.walk = True
                        self.friction = 1
                        self.force_x = 0
                    else:
                        for drug in self.drug_list:
                            if ((self.igrok.center_x > drug.center_x > self.center_x or
                                    self.igrok.center_x < drug.center_x < self.center_x)
                                    and (abs(self.center_x - drug.center_x) < 200 or drug.beg)):
                                self.beg = True
                                self.walk = False
                            else:
                                self.beg = False
                                self.walk = True
                case 1:
                    if self.radius_action.check_collision(self.igrok):
                        self._stop_update_storona = True
                        self.povedenie = 2
                    else:
                        if self.radius_ataki.check_collision(self.igrok):
                            ataka()
                        else:
                            self.not_ii = False
                            self.povedenie = 0
                case 2:
                    if self._radius_stop.check_collision(self.igrok):
                        self.walk = True
                        self.friction = 0.7
                        if self.igrok.center_x < self.center_x:
                            self.force_x = 10000
                            self.storona = 1
                        elif self.igrok.center_x > self.center_x:
                            self.storona = 0
                            self.force_x = -10000

                        ataka()
                        for drug in self.drug_list:
                            if drug.name != self.name and (self.igrok.center_x > drug.center_x > self.center_x + 100 or
                                    self.igrok.center_x < drug.center_x < self.center_x - 100):
                                self.povedenie = 0
                                self.not_ii = self._stop_update_storona = False
                                break
                    else:
                        self.povedenie = 0
                        self.not_ii = self._stop_update_storona = False
                case 3:
                    for drug in self.drug_list:
                        if drug.name != self.name:
                            if drug.beg and drug.storona != self.storona and abs(self.center_x - drug.center_x) < 100:
                                self.friction = 0.7
                                if drug.storona == 0:
                                    self.force_x = 10000
                                else:
                                    self.force_x = -10000
                            else:
                                self.walk = True
                                self.beg = self.not_ii = False
                                self.povedenie = 0
                case 4:
                    if self.radius_ataki.check_collision(self.igrok):
                        self.not_ii = True
                        ataka()
                    else:
                        self.not_ii = False
                case 5:
                    if self._radius_blizko.check_collision(self.igrok):
                        if not self.block.block and not self.block.avto_block:
                            if not self.oruzh.action and not self.oruzh.kd and not self.kulak_ognya.kast:
                                self.oruzh.action = True
                            elif not self.oruzh.action and not self.kulak_ognya.kd and not self.kulak_ognya.action:
                                self.kulak_ognya.action = True
            # print(self.povedenie)

        elif self.oglush:
            self.povedenie = 0
            self.walk = True
            self.not_ii = False
            self.beg = self.block.block = False

        self._move_not_ii()


class __Polic(__Opolchenec):
    def __init__(self, igrok, name, walls_list: arcade.SpriteList):
        super().__init__(igrok, name, walls_list)
        self.max_hp = 3500
        self.max_mana = 150
        self.harakteristiki()

        self.reakciya = 28

        self.animations = spec_battle_animations.PolicAnimations(self)

        self.beg_vel_x = self.vel_x * 2.7

        self.uron = 12

        self.fireball = ogon.FireBall(self, self.sprite_list)
        self.sposob_list.append(self.fireball)
        self.ognen_snaryad = ogon.OgnenSnaryad(self, self.sprite_list)
        self.sposob_list.append(self.ognen_snaryad)
        self.mech_ogon = cold_oruzhie.MechOgon(self, self.sprite_list, 25, 30)
        self.mech_ogon.main_block = True
        self.block = self.mech_ogon
        self.sposob_list.append(self.mech_ogon)
        self.polet = ogon.Polet(self, self.sprite_list)
        self.sposob_list.append(self.polet)
        self.pistolet = dal_oruzh.Pistolet(self, self.sprite_list)
        self.sposob_list.append(self.pistolet)

        self.radius_action.scale = 1.6

        self.s_polet = 0
        self.polet_storona = 0
        self.p = 0

        self._stop_update_beg = False

        self.otstup = False
        self.s_otstup = 0
        self.timer_for_s_otstup = 50
        self.otstup_rasst = 500

        self.s_kombo = 0
        self.mech_s_popal = 0
        self.kombo_mech = 2
        self.kombo_mech2 = 4

        self.s_nazad = 0

        self.s_block = 0
        self.timer_for_s_block = 5

        self._pov_min_hp = False

        self.state = 0

    def check_sposob_action(self):
        for sposob in self.sposob_list:
            if sposob.action:
                if sposob.tip == sposobs.STIHIYA_KAST:
                    if sposob.kast:
                        return False
                else:
                    return False
        else:
            return True

    def otstuplenie(self):
        self.not_ii = self._stop_update_storona = True
        def konec():
            self.force_x = 0
            self.pymunk.max_horizontal_velocity = self.walk_vel_x
            if abs(self.fizika.dx) < X_D_ZONE:
                self.otstup = False
                self.block.block = False
                self.not_ii = False
                self.s_otstup = 0

        self.s_otstup += 1
        if self.s_otstup >= self.timer_for_s_otstup:
            konec()
            return
        elif abs(self.center_x - self.igrok.center_x) < self.otstup_rasst:
            self.pymunk.max_horizontal_velocity = 200
            if not self.oglush:
                self.block.block = True
            self.apply_force_x(-3000)
        elif abs(self.center_x - self.igrok.center_x) >= self.otstup_rasst:
            konec()

    def _update_beg(self):
        if not self._stop_update_beg:
            super()._update_beg()

    @property
    def _rasst(self):
        return abs(self.center_x - self.igrok.center_x) if not self.igrok.block.block \
                else abs(self.center_x - self.igrok.block.center_x)

    def _min_mana_sposob(self, sposob_1, sposob_2):
        if self.mana <= self.min_mana:
            return sposob_1
        else:
            return sposob_2


class PMdd(__Polic):
    def __init__(self, igrok, walls_list):
        super().__init__(igrok, "PMdd", walls_list)
        self.max_hp += 200
        self.harakteristiki()

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.popad and not self.oglush:
            # self.not_ii = self._stop_update_storona = True
            self.povedenie = 3
            self.mech_s_popal = self.s_kombo = self.mech_ogon.s_popal = self.s_mimo = self.force_x = 0
            self.mech_ogon.timer_for_s_kd = 50
            self.otstup = self.mech_ogon.ogon_state = self.beg = self.popad = False
            self.friction = 1

        if self.operation == 0 or self.povedenie == 6:
            rasst = abs(self.center_x - self.igrok.center_x)
            rasst_block = abs(self.center_x - self.igrok.block.center_x)

            if self.mana <= self.min_mana and self.kul_og_kd == self.kulak_ognya.timer_for_s_kd:
                for sposob in self.sposob_list:
                    if sposob.klass == sposobs.STIHIYA:
                        sposob.timer_for_s_kd *= 2

            if self.povedenie != 6:

                if len(self.drug_list) != 0 and not self.oglush_for_sposob:
                    dl = 0
                    dr = 0
                    sp = 0
                    s = 0
                    for drug in self.drug_list:
                        if drug.povedenie == 5:
                            sp += 1
                        if (abs(drug.center_x - self.igrok.center_x) > rasst or drug.povedenie == 5) and drug.name == self.name:
                            s += 1

                        if drug.center_x < self.igrok.center_x:
                            dl += 1
                        elif drug.center_x > self.igrok.center_x:
                            dr += 1

                    if self.hp > self.min_hp and self.mana > self.min_mana:
                        # minimum = round(len(self.drug_list) )* 0.4 if len(self.drug_list) * 0.4 > 0.5 else 1
                        if sp == 0 and self.povedenie != 5 and (rasst <= 300 or rasst_block <= 300 and self.igrok.block.block):
                            if ((dr < self.perem and self.center_x < self.igrok.center_x)
                                    or (dl < self.perem and self.center_x > self.igrok.center_x)):
                                self.povedenie = 5
                                self.mech_s_popal = self.s_kombo = self.mech_ogon.s_popal = self.s_mimo = self.force_x = 0
                                self.mech_ogon.timer_for_s_kd = 50
                                self.mech_ogon.ogon_state = self.beg = self.popad = False
                                if self.center_x > self.igrok.center_x:
                                    self.polet_storona = 1
                                else:
                                    self.polet_storona = 0
                                self.otstup = self._stop_update_beg = True
                                self.otstup_rasst = 200

                    if not self.fireball.kd and not self.fireball.action and self.povedenie < 4 and s == 0 and len(self.drug_list) > 6:
                        self.povedenie = 4
                        self.mech_s_popal = self.s_kombo = self.mech_ogon.s_popal = self.s_mimo = self.force_x = 0
                        self.mech_ogon.timer_for_s_kd = 50
                        self.not_ii = self._stop_update_storona = True
                        if self.hp < self.min_hp:
                            self.otstup = True
                            self.otstup_rasst = 1000
                            # self.beg, self.walk = self.beg, self.walk
                        # for drug in self.drug_list:
                        #     drug: Balvanchik
                        #     drug.fire_ball.s += drug.fire_ball.timer_for_s

                if (not self.igrok.block.block and self.igrok.top >= self.pistolet.center_y >= self.igrok.bottom
                        and (not self.pistolet.action and not self.pistolet.kd and self.pistolet.perezaryadka
                             or not self.pistolet.perezaryadka and self.pistolet.kd) and self.povedenie < 3
                        and 1000 > rasst > 700 and self.igrok.fizika.dx < X_D_ZONE):
                    self.not_ii = True
                    if not self.pistolet.kd:
                        self.pistolet.action = True
                    self.friction = 1
                    self.apply_force_x(0)
                    self.move()
                    self.povedenie = 6
                    # print(1000)

            if self.povedenie != 7:
                for drug in self.drug_list:
                    if drug.povedenie == 7 and drug.name == self.name:
                        self.povedenie = 7
                        self.beg = True
                        self.walk = False
                        self.not_ii = self._stop_update_storona = False

            if self.hp > self.min_hp:
                match self.povedenie:
                    case 0:
                        sposob_action = self._min_mana_sposob(self.mini_fire_ball, self.fireball)

                        if rasst > 800:
                            if not self.igrok.block.block and not sposob_action.action and not sposob_action.kd:
                                sposob_action.action = True
                                s = 0
                                for drug in self.drug_list:
                                    if self.center_x + 400 >= drug.center_x >= self.center_x - 400:
                                        s += 1

                                if s > 2:
                                    self.povedenie = 7
                                    self.beg = True
                                    self.walk = False
                        else:
                            if (self.radius_ataki.check_collision(self.igrok) or self.radius_ataki.check_collision(self.igrok.block)
                                    and self.igrok.block.block):
                                if not self.mech_ogon.kd and self.check_sposob_action():
                                    if self.mana > self.min_mana:
                                        self.mech_ogon.ogon_state = True
                                    self.mech_s_popal += 1
                                    self.mech_ogon.action = True
                            if self.mech_ogon.s_popal == 2:
                                self.povedenie = 1
                                self.mech_ogon.ukol = True
                            elif self.mech_s_popal == 4:
                                self.mech_s_popal = self.s_kombo = 0
                                self.mech_ogon.timer_for_s_kd = 50
                                self.povedenie = 2
                                self.otstup = True
                    case 1:
                        if (self.radius_ataki.check_collision(self.igrok) or self.radius_ataki.check_collision(self.igrok.block)
                                and self.igrok.block.block):
                            if not self.mech_ogon.kd and self.check_sposob_action() and ((self.mech_s_popal < self.kombo_mech
                                  and self.s_kombo == 0) or (self.mech_s_popal < self.kombo_mech2 and self.s_kombo == 1)):
                                self.mech_s_popal += 1
                                self.mech_ogon.action = True
                            elif (not self.ognen_snaryad.kd and self.check_sposob_action() and self.s_kombo == 0
                                  and self.mech_s_popal == self.kombo_mech):
                                self.ognen_snaryad.action = True
                                if self.mana > self.min_mana:
                                    self.mech_ogon.ogon_state = True
                                self.s_kombo += 1
                                self.mech_ogon.ukol = True
                            elif (not self.kulak_ognya.kd and self.check_sposob_action()
                                  and self.s_kombo == 1 and self.mech_s_popal == self.kombo_mech2):
                                self.s_kombo = self.mech_s_popal = 0
                                self.action(self.kulak_ognya.sposob)
                                self.mech_ogon.timer_for_s_kd = 25

                        if self.mech_ogon.s_popal == 0:
                            self.povedenie = 0
                            self.mech_s_popal = self.s_kombo = self.force_x = 0
                            self.mech_ogon.ogon_state = False
                            self.mech_ogon.timer_for_s_kd = 50
                    case 2:
                        if self.otstup:
                            self.otstuplenie()
                        else:
                            self.force_x = 0
                            if self.s_kombo == 0 and not self.ognen_snaryad.kd and not self.ognen_snaryad.action:
                                self.ognen_snaryad.action = True
                                self.s_kombo += 1
                                if self.mana > self.min_mana:
                                    self.mech_ogon.ogon_state = True
                            elif self.s_kombo == 1:
                                if self.ognen_snaryad.kast:
                                    self.force_x = 0
                                else:
                                    if ((not self.radius_ataki.check_collision(self.igrok.block) and self.igrok.block.block) or
                                            not self.radius_ataki.check_collision(self.igrok)):
                                        self.apply_force_x(10000)
                                        self.beg = True
                                        self.walk = False
                                        self.mech_ogon.action = True
                                        self.mech_ogon.ukol = True
                                        self.mech_ogon.s = 2
                                    else:
                                        self.beg = False
                                        self.walk = True
                                        self.s_kombo = 0
                                        self.povedenie = 0
                                        self.mech_ogon.ogon_state = False
                    case 3:
                        if self.oglush:
                            self.block.block = False
                            self.s_kombo = 0
                        else:
                            sposob_action = self._min_mana_sposob(self.kulak_ognya, self.ognen_snaryad)

                            self.storona = 0 if self.igrok.center_x > self.center_x else 1

                            if not self.block.block and self.s_kombo == 0:
                                self.s_kombo = 1
                                self.block.block = True
                            if self.popad and self.block.block:
                                self.s_block = 0

                            if self.block.block:
                                self.s_block += 1
                                if self.s_block >= self.timer_for_s_block:
                                    self.s_block = 0
                                    self.block.block = False
                            if ((not self.block.block or (self.radius_ataki.check_collision(self.igrok) or
                                                          (self.radius_ataki.check_collision(self.igrok.block)
                                  and self.igrok.block.block))) and not sposob_action.kd and self.check_sposob_action()):
                                self.block.block = False
                                sposob_action.action = True
                                self.apply_force_x(100)
                                self.s_kombo = 2

                            if self.s_kombo == 2 and not sposob_action.kast:
                                self.not_ii = False
                                self.povedenie = 0
                                self.s_kombo = 0
                                self.friction = 0.7
                    case 4:
                        if rasst < 800:
                            self.beg = True
                            self.walk = False
                            self.apply_force_x(-10000)
                        else:
                            sposob_action = self._min_mana_sposob(self.mini_fire_ball, self.fireball)

                            self.force_x = 0
                            self.beg = False
                            self.walk = True
                            if self.igrok.center_x < self.center_x:
                                self.storona = 1
                            else:
                                self.storona = 0
                            if abs(self.fizika.dx) <= X_D_ZONE and not sposob_action.kd and not sposob_action.action:
                                self.action(sposob_action.sposob)
                            if not sposob_action.kast:
                                if self.mana > self.min_mana:
                                    if not self.mini_fire_ball.kd and not self.mini_fire_ball.action:
                                        self.mini_fire_ball.action = True
                                    if not self.mini_fire_ball.kast and self.mini_fire_ball.action:
                                        self.povedenie = 0
                                        self.not_ii = self._stop_update_storona = False
                                else:
                                    self.povedenie = 0
                                    self.not_ii = self._stop_update_storona = False
                    case 5:
                        if self.otstup:
                            self.otstuplenie()
                        else:
                            self.not_ii = True
                            if self.polet_storona == 0:
                                if self.center_x > self.igrok.center_x:
                                    self.storona = 1
                                    if rasst > 300:
                                        self.p = 1

                                if self.center_x < self.igrok.center_x and self.p == 0:
                                    self.force_x = 10000
                                elif self.center_x > self.igrok.center_x and self.p == 1:
                                    if self.polet.action:
                                        self.force_x = -3000
                                    else:
                                        self.force_x = 0
                            elif self.polet_storona == 1:
                                if self.center_x < self.igrok.center_x:
                                    self.storona = 0
                                    if rasst > 300:
                                        self.p = 1

                                if self.center_x > self.igrok.center_x and self.p == 0:
                                    self.force_x = -10000
                                elif self.center_x < self.igrok.center_x and self.p == 1:
                                    if self.polet.action:
                                        self.force_x = 3000
                                    else:
                                        self.force_x = 0

                            if not self.polet.action and not self.polet.kd and self.s_polet == 0:
                                self.s_polet = 1
                                self.action(self.polet.sposob)

                            if self.s_polet == 1 and self.fizika.is_on_ground and not self.polet.action:
                                self.s_polet = self.povedenie = 0
                                self.force_x = 0
                                self.otstup_rasst = 500
                                self.p = 0
                                self.not_ii = self._stop_update_beg = False
                    case 6:
                        if self.pistolet.action and not self.pistolet.perezaryadka and not self.pistolet.kd:
                            self.not_ii = False
                            self.friction = 0.7
                            self.povedenie = 0
                            # print(self.pistolet.action, self.pistolet.perezaryadka)
                            # print("-"*10)
                            # print(self.pistolet.kd, self.pistolet.perezaryadka)
                        elif not self.pistolet.kd and not self.pistolet.action and self.pistolet.perezaryadka:
                            self.not_ii = False
                            self.friction = 0.7
                            self.povedenie = 0
                        if not self.pistolet.perezaryadka and self.pistolet.kd:
                            # print("-_- :] ")
                            self.pistolet.perezaryadka_func()
                    case 7:
                        sposob_action = self._min_mana_sposob(self.kulak_ognya, self.ognen_snaryad)
                        if rasst < 400 and not sposob_action.action and not sposob_action.kd:
                            sposob_action.action = True
                        if self.radius_ataki.check_collision(self.igrok) or (self.radius_ataki.check_collision(self.igrok.block)
                                                                             and self.igrok.block.block):
                            self.kulak_ognya.action = True
                            self.beg, self.walk = self.walk, self.beg
                            self.povedenie = 1
            else:
                # print(1, self.povedenie, self.mana)
                self.timer_for_s_block *= 2
                if 0 < self.povedenie < 3:
                    if not self.radius_action.check_collision(self.igrok):
                        self.povedenie = 0
                        self.otstup = self.not_ii = self._stop_update_storona = False
                        self.otstup_rasst = 500
                elif self.povedenie == 3:
                    self.otstup_rasst = 850
                elif self.povedenie == 7:
                    self.povedenie = 5
                match self.povedenie:
                    case 0:
                        sposob_action = self._min_mana_sposob(self.ognen_snaryad, self.mini_fire_ball)

                        if self.radius_action.check_collision(self.igrok):
                            if not self.block.block and not sposob_action.kd and self.check_sposob_action():
                                sposob_action.action = True
                            if not sposob_action.kast:
                                self.block.block = True

                            if rasst < 300:
                                if not self.kulak_ognya.kd and not self.kulak_ognya.action and self.check_sposob_action():
                                    self.kulak_ognya.action = True
                                if not self.kulak_ognya.kast and self.kulak_ognya.action:
                                    self.otstup = True
                                    self.povedenie = 1
                    case 1:
                        if self.otstup:
                            self.otstuplenie()
                        else:
                            sposob_action = self._min_mana_sposob(self.ognen_snaryad, self.mini_fire_ball)
                            sposob_action2 = self._min_mana_sposob(self.kulak_ognya, self.ognen_snaryad)

                            if self.radius_action.check_collision(self.igrok):
                                if ((self.s_kombo == 0 or self.s_kombo == 2) and not sposob_action.kd
                                        and self.check_sposob_action()):
                                    sposob_action.action = True
                                    self.s_kombo += 1
                                elif not sposob_action.kast:
                                    if self.s_kombo == 1 or self.s_kombo == 3:
                                        self.block.block = True
                                        self.pymunk.max_horizontal_velocity = 200
                                        if rasst < 300 or (rasst_block < 300 and self.igrok.block.block):
                                            if not sposob_action2.kd and not sposob_action2.action:
                                                self.action(sposob_action2.sposob)
                                                self.s_kombo += 1
                                                if self.s_kombo == 4:
                                                    if self.mana > self.min_mana:
                                                        self.mech_ogon.ogon_state = True
                                                    self.block.block = False
                                                    self.pymunk.max_horizontal_velocity = self.walk_vel_x
                                            if not sposob_action2.kast and self.s_kombo == 2:
                                                self.otstup = True
                                    if self.s_kombo > 3 and (self.radius_ataki.check_collision(self.igrok) or
                                         self.radius_ataki.check_collision(self.igrok.block) and self.igrok.block.block) \
                                            and not self.mech_ogon.kd and not self.mech_ogon.action:
                                        self.mech_s_popal += 1
                                        self.action(self.mech_ogon.sposob)

                                    if self.mech_s_popal >= 2:
                                        self.mech_s_popal = self.mech_ogon.s_popal = self.s_kombo = 0
                                        self.mech_ogon.ogon_state = False
                                        self.otstup = True
                                        if self.mech_ogon.s_popal == 0:
                                            self.otstup_rasst = 700
                                            self.povedenie = 2
                                            self.not_ii = self._stop_update_storona = True

                            else:
                                self.not_ii = self.mech_ogon.ogon_state = False
                                self.povedenie = self.mech_s_popal = self.mech_ogon.s_popal = self.s_kombo = 0
                    case 2:
                        if self.otstup:
                            self.otstuplenie()
                            self.not_ii = self._stop_update_storona = True
                        else:
                            if 1000 > rasst > self.otstup_rasst:
                                self.apply_force_x(-7500)
                                if self.mana > self.min_mana:
                                    if (not self.mini_fire_ball.kd and self.check_sposob_action()
                                            and not self.mini_fire_ball.action):
                                        self.mini_fire_ball.action = True
                                    elif (not self.ognen_snaryad.kd and self.check_sposob_action()
                                          and not self.ognen_snaryad.action):
                                        self.ognen_snaryad.action = True
                                    elif (not self.kulak_ognya.kd and self.check_sposob_action()
                                          and not self.kulak_ognya.action):
                                        self.kulak_ognya.action = True
                                else:
                                    if (not self.ognen_snaryad.kd and self.check_sposob_action()
                                            and not self.ognen_snaryad.action):
                                        self.ognen_snaryad.action = True
                            else:
                                self.otstup_rasst = 500
                                self.povedenie = 1
                                self.otstup = True
                    case 3:
                        if self.oglush:
                            self.block.block = False
                            self.s_kombo = 0
                            self.otstup = True
                        else:
                            if self.otstup:
                                self.otstuplenie()
                            else:
                                sposob_action = self._min_mana_sposob(self.ognen_snaryad, self.mini_fire_ball)
                                sposob_action2 = self._min_mana_sposob(self.mini_fire_ball, self.fireball)
                                self.storona = 0 if self.igrok.center_x > self.center_x else 1
                                if self.s_kombo == 0 and not sposob_action.kd and self.check_sposob_action():
                                    sposob_action.action = True
                                    self.s_kombo += 1
                                elif self.s_kombo == 1:
                                    self.s_nazad += 1
                                    if not self.ognen_snaryad.kd and self.check_sposob_action():
                                        self.ognen_snaryad.action = True

                                    if self.s_nazad >= 15:
                                        self.s_nazad = 0
                                        self.s_kombo += 1
                                elif self.s_kombo == 2 and not sposob_action2.kd and self.check_sposob_action():
                                    sposob_action2.action = True
                                    self.s_kombo += 1


                                if self.s_kombo == 3 and not sposob_action2.kast:
                                    self.not_ii = self._stop_update_storona = False
                                    self.povedenie = 0
                                    self.s_kombo = 0
                                    self.otstup_rasst = 500
                    case 4:
                        if self.otstup:
                            self.otstuplenie()
                        else:
                            self.friction = 1
                            self.force_x = 0
                            sposob_action = self._min_mana_sposob(self.mini_fire_ball, self.fireball)
                            if abs(self.fizika.dx) <= X_D_ZONE and not sposob_action.kd and not sposob_action.action:
                                self.action(sposob_action.sposob)
                            if not sposob_action.kast:
                                self.povedenie = 0
                                self.not_ii = self._stop_update_storona = False
                                self.friction = 0.7
                                self.otstup_rasst = 500
                    case 5:
                        sposob_action = self._min_mana_sposob(self.kulak_ognya, self.ognen_snaryad)

                        if rasst < 400 and not sposob_action.action and not sposob_action.kd:
                            sposob_action.action = True
                        if self.radius_ataki.check_collision(self.igrok) or (self.radius_ataki.check_collision(self.igrok.block)
                                                                             and self.igrok.block.block):
                            self.kulak_ognya.action = True
                            self.beg, self.walk = self.walk, self.beg
                            self.povedenie = 1
                    case 6:
                        if self.pistolet.action and not self.pistolet.perezaryadka and not self.pistolet.kd:
                            self.not_ii = False
                            self.friction = 0.7
                            self.povedenie = 0
                            # print(self.pistolet.action, self.pistolet.perezaryadka)
                            # print("-"*10)
                            # print(self.pistolet.kd, self.pistolet.perezaryadka)
                        elif not self.pistolet.kd and not self.pistolet.action and self.pistolet.perezaryadka:
                            self.not_ii = False
                            self.friction = 0.7
                            self.povedenie = 0
                        if not self.pistolet.perezaryadka and self.pistolet.kd:
                            # print("-_- :] ")
                            self.pistolet.perezaryadka_func()

        elif self.oglush:
            self.povedenie = 3
            self.mech_ogon.ogon_state = self.beg = self.otstup = self.block.block = False
            self.walk = True
            self.mech_s_popal = self.s_kombo = self.mech_ogon.s_popal = self.force_x = 0
            self.mech_ogon.timer_for_s_kd = 30
            self.otstup_rasst = 500

        self._move_not_ii()

    def append_drug(self, drug):
        super().append_drug(drug)
        self.perem = round(len(self.drug_list) * 0.4) if len(self.drug_list) * 0.4 >= 0.5 else 1


class PRdd(__Polic):
    def __init__(self, igrok, walls_list):
        super().__init__(igrok, "PRdd", walls_list)
        self.max_mana += 50
        self.harakteristiki()
        # self.hp = self.min_hp

        self.otstup_rasst = 750

        self.yaziki_ognya = ogon.YazikiOgnya(self, self.sprite_list)
        self.sposob_list.append(self.yaziki_ognya)
        self.shchit = cold_oruzhie.Shchit(self, self.sprite_list, 20, 20)
        self.shchit.main_block = True
        self.block = self.shchit
        self.sposob_list.append(self.shchit)

        self.radius_ataki.scale = 0.2

        self.__s8 = 0
        self.__sposob_list8 = []  # arcade.SpriteList()
        self.__sposob_list8.append(self.mech_ogon)
        self.__sposob_list8.append(self.kulak_ognya)
        self.__sposob_list8.append(self.ognen_snaryad)
        self.__sposob_list8.append(self.mini_fire_ball)

        self.__pov_min_mana = False

        self.__action_pist = 0

        self.__pov_list = [3, 5, 6, 7, 8]

        self.__s_min_10 = False
        self.__sposob10 = None

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)

        if self.oglush:
            self.povedenie = self.__pov_list[0]
            self.apply_force_x(-10000)

        if self.operation == 0 or self.pistolet.action and not self.pistolet.pricel:

            if (self.povedenie != self.__pov_list[3] and self.state == 0 or self.povedenie != self.__pov_list[4]
                    and self.povedenie != self.__pov_list[3] and self.state == 1):
                if self.povedenie != self.__pov_list[1] and self.povedenie != self.__pov_list[2]:
                    if self.mana > self.min_mana:
                        for f_sposob in self.igrok.five_sposobs:
                            if f_sposob.center_x > self.center_x:
                                storona = 0
                            else:
                                storona = 1
                            if (storona == 0 or storona == 1) and f_sposob.action and not self.__check_pered(900):
                                if abs(f_sposob.change_x) >= 10 and ((storona == 0 and abs(f_sposob.left - self.center_x) <= 900)
                                                                     or (storona == 1 and abs(f_sposob.right - self.center_x) <= 900)):
                                    self.povedenie = self.__pov_list[0]
                                    self._stop_update_storona = self.polet.action = self._stop_update_beg = self.not_ii = True
                                    self.apply_force_x(0)
                                    self.block.block = False
                                    self._pov_min_hp = self.__pov_min_mana = False
                                elif abs(f_sposob.change_x) < 10 and ((storona == 0 and abs(f_sposob.left - self.center_x) <= 400)
                                                                     or (storona == 1 and abs(f_sposob.right - self.center_x) <= 400)):
                                    self.povedenie = self.__pov_list[0]
                                    self._stop_update_storona = self.polet.action = self._stop_update_beg = self.not_ii = True
                                    self.apply_force_x(-30000)
                                    self.block.block = False
                                    self._pov_min_hp = self.__pov_min_mana = False

                    if (self.povedenie != self.__pov_list[0] and self.povedenie != self.__pov_list[1]
                            and self.povedenie != self.__pov_list[2]
                         and not self.radius_ataki.check_collision(self.igrok) and not self.igrok.block.block
                            and abs(self.igrok.fizika.dx) < X_D_ZONE and not self.pistolet.action
                          and 1000 > self._rasst > 700):
                        if (self.__check_pered(300) and self.__check_drug_poved(self.__pov_list[1])
                                and self.__check_drug_poved(self.__pov_list[2])):
                            self.povedenie = self.__pov_list[1]
                            self.not_ii = self._stop_update_storona = True
                            self.friction = 0.7
                            self._pov_min_hp = self.__pov_min_mana = False

                    for wall in self.walls_list:
                        if self.kvadrat_radius.check_collision(wall) and wall.center_y > self.top:
                            print(self.povedenie, self.state, "________============")
                            self.povedenie = self.__pov_list[3]
                            self.not_ii = self._stop_update_storona = True
                            self.apply_force_x(0)
                            self.friction = 1
                            if self.state == 1:
                                self.__sposob10 = self._min_mana_sposob(self.yaziki_ognya, self.fireball)
                                self.__sposob10.action = True
                            break
            elif ((self.povedenie == self.__pov_list[3] or self.povedenie == self.__pov_list[4])
                  and not self.radius_action.check_collision(self.igrok) and self.state != 1):
                self._pov_min_hp = self.__pov_min_mana = False
                self.povedenie = 0
                self.not_ii = self._stop_update_storona = False
                self.friction = 0.7

            if self.mana <= self.min_mana and self.kul_og_kd == self.kulak_ognya.timer_for_s_kd:
                for sposob in self.sposob_list:
                    if sposob.klass == sposobs.STIHIYA:
                        sposob.timer_for_s_kd *= 2

            if self.hp <= self.min_hp:
                if self.state != 1:
                    self.state = 1
                    self.__pov_list[0] = 4
                    self.__pov_list[1] = 7
                    self.__pov_list[2] = 8
                    self.__pov_list[3] = 9
                    self.__pov_list[4] = 10

                match self.povedenie:
                    case 0:
                        if self.radius_action.check_collision(self.igrok):
                            if self.__check_pered():
                                self.povedenie = 1
                                self.__s8 = 2
                                self.block.block = True
                                self.pymunk.max_horizontal_velocity = self.vel_x * 0.5
                                self._stop_update_beg = True
                            else:
                                self.povedenie = 3
                                self.not_ii = self._stop_update_storona = self.otstup = True
                                self.ognen_snaryad.action = True
                    case 1:
                        if self.radius_action.check_collision(self.igrok):
                            if self.block.block:
                                self.s_block += 1
                                if self.s_block > self.timer_for_s_block and self.__check_sposob_list8(1, 3):
                                    self.s_block = 0
                                    self.block.block = False
                                    self.not_ii = True
                                    self.friction = 1
                                    self.apply_force_x(0)
                            else:
                                if self._rasst > 220:
                                    self.__sposob_list8[self.__s8].action = True
                                    self.__s8 += 1
                                    if self.__s8 > 3:
                                        self.__s8 = 2
                                else:
                                    self.__sposob_list8[self.__s8].action = True
                                    self.__s8 += 1
                                    if self.__s8 > 3:
                                        self.__s8 = 1
                                self.block.block = True
                                self.povedenie = 2
                                self.friction = 0.7
                                self.pymunk.max_horizontal_velocity = self.vel_x
                                self._stop_update_storona = True
                        else:
                            self.povedenie = 0
                            self.pymunk.max_horizontal_velocity = self.vel_x
                            self.not_ii = False
                    case 2:
                        if self.s_block < self.timer_for_s_block:
                            self.s_block += 1
                            self.apply_force_x(-7000)
                        else:
                            self.s_block = 0
                            self.apply_force_x(0)
                            self._stop_update_storona = False
                            if self.__check_pered():
                                self.povedenie = 1
                            else:
                                self.povedenie = 0
                                self.not_ii = self.block.block = False
                    case 3:
                        if self.otstup:
                            if not self.ognen_snaryad.kast:
                                self.otstuplenie()
                        else:
                            if not self.__check_pered(700):
                                s = 0
                                for drug in self.drug_list:
                                    if self.name != drug.name:
                                        s += 1

                                if s == 0 and self.__check_drug_poved(5):
                                    self.povedenie = 5
                                    self.not_ii = self._stop_update_storona = False
                                    self.block.block = True
                                    self.pymunk.max_horizontal_velocity = 200
                                    self._stop_update_beg = True
                                    return
                            sposob_action = self._min_mana_sposob(self.mini_fire_ball, self.ognen_snaryad)
                            if not sposob_action.kast:
                                self.povedenie = 0
                                self.not_ii = self._stop_update_storona = self.block.block = False
                            sposob_action.action = True
                    case 4:
                        self.__pov_polet()
                    case 5:
                        if not self.__check_pered(700):
                            if (self._rasst <= 220 and not self.radius_ataki.check_collision(self.igrok)
                                    and not self.kulak_ognya.kd and not self.kulak_ognya.action):
                                self.kulak_ognya.action = True
                            elif self.radius_ataki.check_collision(self.igrok):
                                if self.mech_ogon.s_popal >= 2 == self.s_kombo:
                                    self.s_kombo += 1
                                    self.mech_s_popal = 0
                                elif self.s_kombo == 2 != self.mech_ogon.s_popal:
                                    self.s_kombo = 0
                                if self.__check_sposob_list8(0, 3) and self.s_kombo < 2 or self.s_kombo > 2:
                                    self.mech_s_popal += 1
                                    match self.s_kombo:
                                        case 0:
                                            self.s_kombo += 1
                                            self.mech_ogon.ukol = self.mech_ogon.action = True
                                        case 1:
                                            self.s_kombo += 1
                                            self.mech_ogon.ukol = False
                                            self.mech_ogon.action = True
                                        case 3:
                                            self.ognen_snaryad.action = True
                                            self.mech_ogon.ogon_state = True if self.mana > self.min_mana else False
                                            self.s_kombo += 1
                                        case 4:
                                            self.mech_ogon.action = True
                                            self.s_kombo += 1
                                        case 5:
                                            self.mech_ogon.action = self.mech_ogon.ukol = True
                                            self.s_kombo += 1
                                        case 6:
                                            self.mech_ogon.ukol = False
                                            self.mech_ogon.action = True
                                            self.s_kombo += 1
                                        case 7:
                                            self.s_kombo = 0
                                            self.mech_ogon.action = True

                                if self.mech_s_popal > 6 and self.s_kombo < 2:
                                    self.otstup = True
                                    self.s_kombo = 0
                                    self.povedenie = 6
                                    for drug in self.drug_list:
                                        if drug.name == self.name:
                                            drug.povedenie = 6
                                            drug.not_ii = drug._stop_update_storona = True
                                    self._stop_update_beg = False
                                    self.pymunk.max_horizontal_velocity = self.vel_x
                            else:
                                self.block.block = True
                        else:
                            self.povedenie = 0
                            self.block.block = self._stop_update_beg = False
                            self.pymunk.max_horizontal_velocity = self.vel_x
                    case 6:
                        if self.otstup:
                            self.otstuplenie()
                        else:
                            for drug in self.drug_list:
                                if drug.name == self.name and drug.otstup:
                                    self.apply_force_x(-10000)
                                    break
                            else:
                                self.povedenie = 0
                                self.not_ii = self._stop_update_storona = False
                    case 7:
                        if not self.__check_drug(300):
                            self.apply_force_x(-10000)
                        else:
                            self.apply_force_x(0)
                            self.friction = 1
                            if self.pistolet.perezaryadka:
                                self.pistolet.action = True
                                self.__action_pist = 0
                            else:
                                self.pistolet.perezaryadka_func()
                                self.__action_pist = 1
                            self.povedenie = 8
                    case 8:
                        if (self.__action_pist == 0 and not self.pistolet.perezaryadka or self.__action_pist == 1
                                and not self.pistolet.kd):
                            self.povedenie = 0
                            self._stop_update_storona = False
                    case 9:
                        if not self.__sposob10.action:
                            self.not_ii = self._stop_update_storona = False
                            self.block.block = True
                            self.friction = 0.7
                            self.apply_force_x(10000)
                            self.povedenie = 10
                            self.__s8 = 1
                            self.mech_ogon.ogon_state = True if self.mana > self.min_mana else False
                    case 10:
                        if self._rasst >= 250:
                            self.block.block = True
                        else:
                            self.block.block = False
                            if self.__check_sposob_list8(1, 3):
                                if not self.__sposob_list8[self.__s8].kast and not self.__s_min_10:
                                    self.__sposob_list8[self.__s8].action = True
                                    self.__s8 = self.__s8 + 1 if self.__s8 < 3 else 1
                                    self.__s_min_10 = True
                            else:
                                self.__s_min_10 = False

                            if not self.__sposob_list8[0].action and not self.__sposob_list8[0].kd and self.__s_min_10:
                                if random.randint(0, 2) == 0:
                                    self.mech_ogon.ukol = True
                                else:
                                    self.mech_ogon.ukol = False
                                self.__sposob_list8[0].action = True
                                self.__s_min_10 = False
            else:
                match self.povedenie:
                    case 0:
                        if self.radius_action.check_collision(self.igrok):
                            if self.__check_pered():
                                self.povedenie = 1
                                self.friction = 1
                                self.apply_force_x(0)
                                self.not_ii = True
                            else:
                                self.povedenie = 2
                                self.not_ii = self._stop_update_storona = True
                    case 1:
                        if self.radius_action.check_collision(self.igrok):
                            if not self.__check_pered():
                                if self.radius_ataki.check_collision(self.igrok):
                                    self.povedenie = 3
                                    self._stop_update_storona = self.polet.action = self._stop_update_beg = True
                                    self.apply_force_x(-30000)
                                    self.friction = 0.7
                                    return
                                else:
                                    self.povedenie = 2
                                    self.not_ii = self._stop_update_storona = True
                                    self.friction = 0.7
                                    return
                            else:
                                for drug in self.drug_list:
                                    if drug.name == self.name and abs(self.center_x - drug.center_x) < 30:
                                        self.povedenie = 4
                                        self._stop_update_storona = True
                                        self.friction = 0.7
                                        return
                            self.friction = 1
                            if self.igrok.center_x > self.center_x:
                                self.storona = 0
                            else:
                                self.storona = 1
                            for sposob in self.sposob_list:
                                if (sposob.klass == sposobs.STIHIYA and not sposob.kd and not sposob.action
                                        and self.check_sposob_action() and not sposob.dvizh_sposob):
                                    if sposob.sposob == sposobs.KULAK_OGNYA:
                                        if self._rasst <= 220:
                                            sposob.action = True
                                    elif sposob.sposob == sposobs.YAZIKI_OGNYA:
                                        if self.mana > self.min_mana:
                                            sposob.action = True
                                    else:
                                        sposob.action = True

                        else:
                            self.povedenie = 0
                            self.not_ii = False
                            self.friction = 0.7
                    case 2:
                        self.apply_force_x(-10000)
                        if self.igrok.center_x > self.center_x:
                            self.storona = 0
                        else:
                            self.storona = 1
                        if self.radius_action.check_collision(self.igrok):
                            if not self.__check_pered():
                                self.block.block = True
                                if self.radius_ataki.check_collision(self.igrok):
                                    self.povedenie = 3
                                    self._stop_update_storona = self.polet.action = self._stop_update_beg = True
                                    self.apply_force_x(-30000)
                                    self.block.block = False
                            else:
                                self.block.block = False
                            if self._rasst > 220:
                                if not self.ognen_snaryad.kd and not self.ognen_snaryad.action and not self.mini_fire_ball.kast:
                                    self.ognen_snaryad.action = True
                                elif not self.mini_fire_ball.kd and not self.mini_fire_ball.action and not self.ognen_snaryad.kast:
                                    self.mini_fire_ball.action = True
                            else:
                                if (not self.ognen_snaryad.kd and not self.ognen_snaryad.action
                                        and not self.mini_fire_ball.kast and not self.kulak_ognya.kast):
                                    self.ognen_snaryad.action = True
                                elif (not self.mini_fire_ball.kd and not self.mini_fire_ball.action
                                      and not self.ognen_snaryad.kast and not self.kulak_ognya.kast):
                                    self.mini_fire_ball.action = True
                                elif (not self.kulak_ognya.kd and not self.kulak_ognya.action
                                      and not self.ognen_snaryad.kast and not self.mini_fire_ball.kast):
                                    self.kulak_ognya.action = True
                        else:
                            self.povedenie = 0
                            self.not_ii = self._stop_update_storona = False
                    case 3:
                        self.__pov_polet()
                    case 4:
                        for drug in self.drug_list:
                            if drug.name == self.name and abs(self.center_x - drug.center_x) < 30:
                                force_x = 10000 if not self.radius_ataki.check_collision(self.igrok) else -10000
                                self.apply_force_x(force_x)
                                break
                        else:
                            self.apply_force_x(0)
                            self.friction = 1
                            self.povedenie = 1
                            self._stop_update_storona = False
                    case 5:
                        if not self.__check_drug(300):
                            self.apply_force_x(-10000)
                        else:
                            self.apply_force_x(0)
                            self.friction = 1
                            if self.pistolet.perezaryadka:
                                self.pistolet.action = True
                                self.__action_pist = 0
                            else:
                                self.pistolet.perezaryadka_func()
                                self.__action_pist = 1
                            self.povedenie = 6
                    case 6:
                        if (self.__action_pist == 0 and not self.pistolet.perezaryadka or self.__action_pist == 1
                                and not self.pistolet.kd):
                            self.povedenie = 1
                            self._stop_update_storona = False
                    case 7:
                        if self._rasst > 250:
                            for sposob in self.sposob_list:
                                if (sposob.klass == sposobs.STIHIYA and not sposob.kd and not sposob.action
                                        and self.check_sposob_action() and not sposob.dvizh_sposob
                                        and sposob.sposob != sposobs.KULAK_OGNYA):
                                    if sposob.sposob == sposobs.YAZIKI_OGNYA:
                                        if self.mana > self.min_mana:
                                            sposob.action = True
                                    else:
                                        sposob.action = True
                        else:
                            self.not_ii = self._stop_update_storona = False
                            self.block.block = True
                            self.friction = 0.7
                            self.povedenie = 8
                            self.__s8 = 2
                            self.s_block += self.timer_for_s_block
                            self.mech_ogon.ogon_state = True if self.mana > self.min_mana else False
                    case 8:
                        if self._rasst <= 250:
                            if self.block.block:
                                self.s_block += 1
                            else:
                                s = 0
                                for sposob8 in self.__sposob_list8:
                                    if not sposob8.kast:
                                        s += 1

                                if s == len(self.__sposob_list8):
                                    self.block.block = True

                            if self.s_block > self.timer_for_s_block and self.__check_sposob_list8(0, 3):
                                if self.__s8 == 0:
                                    if not self.__sposob_list8[self.__s8].action:
                                        self.s_block = 0
                                        self.block.block = False
                                        self.__s8 = self.__s8 + 1 if self.__s8 < 3 else 0
                                else:
                                    if not self.__sposob_list8[self.__s8].kast:
                                        self.s_block = 0
                                        self.block.block = False
                                        self.__s8 = self.__s8 + 1 if self.__s8 < 3 else 0
                                self.__sposob_list8[self.__s8].action = True
                        else:
                            self.povedenie = 7
                            self.s_block = self.__s8 = 0
                            self.block.block = False
                            self.not_ii = self._stop_update_storona = True
                            self.friction = 1
                            self.mech_ogon.ogon_state = False

            print(self.povedenie, self.mana, self.hp)
            # print(self.povedenie, self.storona)

        self._move_not_ii()

    def __check_sposob_list8(self, p, v):
        s = 0
        sk = 0
        for i in range(p, v + 1):
            sk += 1
            if not self.__sposob_list8[i].kd:
                if self.__sposob_list8[i].tip == sposobs.STIHIYA_KAST:
                    if not self.__sposob_list8[i].kast:
                        s += 1
                else:
                    s += 1

        if s == sk:
            return True
        else:
            return False

    def __pov_polet(self):
        if self.igrok.center_x > self.center_x:
            self.storona = 0
        else:
            self.storona = 1
        if not self.polet.action and self.igrok.fizika.is_on_ground:
            self.polet.action = False
            self.povedenie = 0
            self.not_ii = self._stop_update_storona = False

    def __check_pered(self, x = 100):
        for drug in self.drug_list:
            if ((self.igrok.center_x > drug.center_x > self.center_x + x
                 or self.igrok.center_x < drug.center_x < self.center_x - x)
                    and not self.radius_ataki.check_collision(self.igrok)):
                #print(self.igrok.center_x, drug.center_x, self.center_x - x)
                return True
        return False

    def __check_drug(self, x):
        for drug in self.drug_list:
            if abs(drug.center_x - self.center_x) >= x:
                return True
        return False

    def __check_drug_poved(self, povedenie):
        for ndrug in self._name_drug_list:
            if ndrug.povedenie == povedenie and ndrug.state == self.state:
                return False
        return True

