import arcade
from interaction_sprites.battles.mobs import Mob

VRAG_VEL_X = 300

class Vrag(Mob):
    def __init__(self, igrok, name, walls_list):
        super().__init__(name, arcade.SpriteList(), walls_list)
        self.igrok = igrok
        self.sprite_list.append(self.igrok)

        self.ataka = False

        self.not_ii = False

        self.povedenie = 0

        self.__s_ii = 0
        self.__vpered = True

    def ii(self):
        self.update_radius_list()
        self._update_hp()
        self.__s_ii += 1
        if self.__s_ii > 6 and not self.stan_for_sposob and not self.kast_scena and not self.oglush:
            self.__s_ii = 0
            if not self.not_ii:
                if self.center_y > self.igrok.center_y:
                    self.center_y += 1
                    if arcade.check_for_collision(self.igrok, self):
                        if self.igrok.center_x >= self.center_x:
                            self.force_x = -10000
                        else:
                            self.force_x = 10000
                        self.center_y -= 1
                        return
                    self.center_y -= 1
                if self.radius_vid.check_collision(self.igrok) and not self.oglush:
                    if self.igrok.center_x < self.radius_vid.center_x:
                        if (abs(self.igrok.right - self.left) <= self.d_zone
                                or (abs(self.igrok.block.right - self.left) <= self.d_zone and self.igrok.block.block)
                                or not self.__vpered):
                            self.force_x, self.force_y = 0., 0.
                            self.go = False
                            self.storona = 1
                        else:
                            self.friction = 0.7
                            self.force_x = -15000
                            self.go = True

                        self.can_jump()
                    elif self.igrok.center_x > self.radius_vid.center_x:
                        if (abs(self.right - self.igrok.left) <= self.d_zone
                                or (abs(self.igrok.block.left - self.right) <= self.d_zone and self.igrok.block.block)
                                or not self.__vpered):
                            self.force_x, self.force_y = 0., 0.
                            self.go = False
                            self.storona = 0
                        else:
                            self.friction = 0.7
                            self.force_x = 15000
                            self.go = True

                        self.can_jump()
                    else:
                        self.force_x = 0

                    # for drug in self.drug_list:
                    #     if (drug.center_x > self.center_x and abs(self.right - drug.left) <= self.d_zone and not drug.go
                    #             and self.igrok.center_x > self.center_x):
                    #         self.go = False
                    #         self.force_x = 0.
                    #         break
                    #     elif (drug.center_x < self.center_x and abs(self.left - drug.right) <= self.d_zone and not drug.go
                    #           and self.igrok.center_x < self.center_x):
                    #         self.go = False
                    #         self.force_x = 0.
                    #         break
                else:
                    self.go = False
                    self.force_x, self.force_y = 0., 0.
                    self.friction = 1

                self.walk = self.go

                self.move()
        if not self.dvizh and self.oglush:
            self.friction = 0
            self.force_x = 0

    def can_jump(self):
        if self.kvadrat_radius.check_collision(sprite_list=self.walls_list):
            for wall in self.walls_list:
                if (self.kvadrat_radius.check_collision(wall) and wall.center_y > self.bottom and
                        ((self.storona == 0 and wall.center_x > self.center_x) or (self.storona == 1 and wall.center_x < self.center_x))):
                    self.__vpered = False
                    if self.fizika.is_on_ground:
                        self.force_y = 50000
                    break
                else:
                    self.force_y = 0
                    if self.fizika.is_on_ground:
                        self.__vpered = True
        else:
            self.__vpered = True
            self.force_y = 0

    def move(self):
        self.fizika.fizika.apply_force(self, (self.force_x, self.force_y))
        self.fizika.fizika.set_friction(self, self.friction)

    @property
    def operation(self):
        return self.__s_ii


    def apply_force_x(self, force_x):
        if self.igrok.center_x < self.radius_vid.center_x:
            self.force_x = -force_x
            if self.force_x >= 0:
                self.storona = 1
        elif self.igrok.center_x > self.radius_vid.center_x:
            self.force_x = force_x
            if self.force_x <= 0:
                self.storona = 0

    def return_force(self, xy: str):
        if not self.fizika.is_on_ground:
            self.force_y = 0
        if xy == 'x':
            return self.force_x
        if xy == 'y':
            return self.force_y
