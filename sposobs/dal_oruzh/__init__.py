import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import sposobs
import hit_box_and_radius
import arcade
import math



class DalOruzh(sposobs.Fight):
    def __init__(self, pers):
        super().__init__(pers)
        self.klass = sposobs.DAL_ORUZH

        self.speed = 0
        self.patrons = 0

        self.patrons_texture = None

        self.vidno = False
        self.pricel = False
        self.perezaryadka = True

        self.timer_for_s_pricel = 0

        self.radius = hit_box_and_radius.Radius(self)

    def ataka(self):
        for sprite in self.pers.sprite_list:
            if (sprite.center_x > self.center_x or sprite.center_x < self.center_x) and self.radius.check_collision(sprite):
                self.vidno = True
                break

    def perezaryadka_func(self):
        if self.kd:
            self.perezaryadka = True


class Ognestrel(DalOruzh):
    def __init__(self, pers):
        super().__init__(pers)
        self.tip = sposobs.OGNESTREL

        self.radius.scale = 10

    def on_update(self, delta_time: float = 1 / 60) -> None:
        # print(self.pers.name, self.action)
        self.position = self.pers.position
        if self.patrons > 0 and not self.pers.oglush:
            self.update_sposob()
            if self.perezaryadka or self.action:
                self.kd_timer_stamina()
                # if self.perezaryadka and not self.action:
                #     print(self.s_kd, self.kd, self.s, self.action)
            self.ataka()

            if self.kd and self.perezaryadka:
                self.pers.oglush_for_sposob = True
            else:
                self.pers.oglush_for_sposob = False

            if self.vidno and self.action or self.s >= self.timer_for_s_pricel:
                #print(1)
                if self.s < self.timer_for_s_pricel:
                    self.pricel = True
                    self.pers.oglush_for_sposob = True
                else:
                    print("Выстрел")
                    self.pers.oglush_for_sposob = False
                    if self.s == self.timer_for_s_pricel:
                        self.patrons -= 1
                        self.perezaryadka = False
                    self.pricel = False
                    for sprite in self.pers.sprite_list:
                        if arcade.check_for_collision(sprite, self) and not sprite.block.block:
                            self.udar(sprite)
                            self.s += self.timer_for_s
                            break

            self.update_slovar()
        else:
            self.action = False
            if self.s > 0:
                self.s += self.timer_for_s


class Pistolet(Ognestrel):
    def __init__(self, pers):
        super().__init__(pers)
        self.sposob = sposobs.PISTOLET

        self.uron = 1500

        self.patrons = 4

        self.timer_for_s_pricel = 120
        self.timer_for_s = self.timer_for_s_pricel + 1
        self.timer_for_s_kd = 360

        self.texture = arcade.load_texture("resources/Sposob_animations/pulya.png")


