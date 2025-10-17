import random

import arcade
import arcade.gui

import instruments
from my_gui import circles, ui
from interaction_sprites.battles import igrok
from interaction_sprites.battles.mobs.vrags import aarons
from my_gui import line
import sposobs
import pymunk
import my_gui.ui

W = 1600
H = 900

GRAVITY = (0, -1250)
DAMPING = 0.9
IGROK_MOVE_GROUND = 6000
MASS_IGROK = 1
IG_MAX_VERTICAL_SPEED = 10000
IG_MAX_HORIZANTAL_SPEED = 300
IG_OBICH_HORIZANTAL_SPEED = 350
VRAG_OBICH_HORIZANTAL_SPEED = 300
IGROK_JUMP_FORCE = 40000
WALL_FRICTION = 0.9


class BetaViev(arcade.View):
    def __init__(self):
        super().__init__()
        self.igrok = None
        arcade.set_background_color((200, 100, 100, 1))
        self.igrok: igrok.BetaOyuun
        #self.igrok = None

        self.vibor_sposob = None

        self.vrag_list = None
        self.zhivie_vrag_list = None

        self.walls_list = arcade.SpriteList()
        self.platforms_list = None
        self.sprite_list = None

        self.smert_list1 = None
        self.smert_list2 = None

        self.fizika = arcade.PymunkPhysicsEngine()

        self.kamera = None

        self.levo = False
        self.pravo = False

        self.x = 0
        self.y = 0

        self.line_hp = None
        self.line_mana = None
        self.line_stamina = None
        self.line_v = None
        self.circles = circles.Circles(72)

        self.s = 0
        self.s1 = 0
        self.s_zoom = 0
        self.s_zoom1 = 0
        self.zoom = False
        self.zoom1 = False

        self.kast_scena = False

        def ffc():
            return 1, 1, 1

        class Ispar(arcade.Sprite):
            def __init__(self):
                super().__init__()
                self.texture = arcade.load_texture('nuzhno/ispar.png')
        self.ispar = Ispar()

        self.s_voln = 0

        self.line_x = 0
        self.I = True

    def setup(self):
        self.kamera = arcade.Camera()
        self.kamera.zoom = 1.2

        self.smert_list1 = arcade.SpriteList()
        self.smert_list2 = arcade.SpriteList()

        self.sprite_list = arcade.SpriteList()

        self.zhivie_vrag_list = arcade.SpriteList()
        self.vrag_list = arcade.SpriteList()

        # for x in range(-10000, 10000, 128):
        #     wall = arcade.Sprite('nuzhno/grassmid.png')
        #     wall.position = x, 64
        #     self.walls_list.append(wall)

        plast = arcade.Sprite("resources/plast.png")
        plast.position = 0, 64
        self.walls_list.append(plast)

        stena = arcade.Sprite("resources/stena.png")
        stena.position = 3200, 128 + stena.height / 2
        self.walls_list.append(stena)
        dom = arcade.Sprite('resources/dom.png', center_x=-3500, center_y=650)
        dom.position = -4000, 128 + dom.height / 2
        self.walls_list.append(dom)
        krilco = arcade.Sprite('resources/krilco.png', center_x=dom.center_x - dom.width / 2 - 207, center_y=650)
        krilco.position = dom.center_x - dom.width / 2 - 207, 128 + krilco.height / 2
        krilco.hit_box._points = (
            (-krilco.width/2, -krilco.height/2), (krilco.width/2, -krilco.height/2),
            (krilco.width/2, 518 - krilco.height/2), (-krilco.width/2, 408 - krilco.height/2)
        )
        self.walls_list.append(krilco)


        # wall = arcade.Sprite('nuzhno/grassmid.png')
        # wall.position = 600, 192
        # self.walls_list.append(wall)
        #
        # for y in range(192, 481, 128):
        #     wall = arcade.Sprite('nuzhno/grassmid.png')
        #     wall.position = 2500, y
        #     self.walls_list.append(wall)
        #
        # for y in range(192, 1000, 128):
        #     wall = arcade.Sprite('nuzhno/grassmid.png')
        #     wall.position = 4600, y
        #     self.walls_list.append(wall)

        #
        # for x in range(0, 100, 128):
        #     wall = arcade.Sprite('nuzhno/grassmid.png')
        #     wall.position = x, 70
        #     self.walls_list.append(wall)

        # self.vrag_list.append(self.rock)

        # self.igrok = pers.BetaMaster(self.vrag_list, self.fizika)
        self.igrok = igrok.BetaOyuun(self.vrag_list, self.walls_list)
        self.igrok.position = 1500, 328

        # self.igrok.hp = 10
        # self.igrok.mana = 10
        # self.igrok.stamina = 10

        self.line_hp = line.Line(self.igrok.max_hp, 20, 280, 850, self.kamera)
        # colors_mana = {0: (138, 43, 255, 255), 1: (0, 0, 255, 255), 2: (0, 0, 150, 255), 3: (0, 0, 100, 255),
        #                4: (0, 0, 50, 255)}
        # self.line_mana = line.Line(self.igrok.max_mana, 20, 170, 810, self.kamera, 15,
        #                            colors=colors_mana)
        # colors_stamina = {0: (255, 255, 255, 255), 1: (230, 230, 230, 255), 2: (200, 200, 200, 255),
        #                   3: (150, 150, 150, 255), 4: (100, 100, 100, 255)}
        # self.line_stamina = line.Line(self.igrok.max_stamina, 20, 170, 790, self.kamera, 15,
        #                               colors_stamina)
        colors_v = {0: (0, 200, 255, 255), 1: (0, 200, 255, 255), 2: (0, 200, 255, 255), 3: (0, 200, 255, 255),
                    4: (0, 200, 255, 255)}
        self.line_v = line.Line(self.igrok.v_max, 20, 170, 690, self.kamera, 40, colors_v)

        circles_texture = instruments.TextureList()
        circles_texture.load_textures(5, 'resources/sposob', instruments.PNG, False)
        self.circles.create_circles(self.igrok.five_sposobs, 634,
                                    -20,
                                    260, circles_texture)
        # x - 0.2625 (504)
        # y - 1/12 (90)
        # rasst - 0.09375 (180)

        # 0.27
        # 0.73

        texture_list = instruments.TextureList()
        texture_list.load_textures(5, "resources/sposob", ".png", False)
        self.vibor_sposob = my_gui.ui.ViborSosob(self.igrok, 2, 5, texture_list, self.circles)
        self.vibor_sposob.enable()

        # for x in range(900, 1700, 200):
        #     bb = vrags.G1(self.igrok, self.walls_list)
        #     bb.position = x, 192
        #     self.vrag_list.append(bb)
        #
        # for x in range(400, 1150, 250):
        #     bb = vrags.G2(self.igrok, self.walls_list)
        #     bb.position = x, 192
        #     self.vrag_list.append(bb)
        #
        # for x in range(1400, 2300, 300):
        #     bb = vrags.G3(self.igrok, self.walls_list)
        #     bb.position = x, 192
        #     self.vrag_list.append(bb)
        #
        # op = vrags.OpRdd1(self.igrok, self.walls_list)
        # op.position = 1800, 192
        # self.vrag_list.append(op)

        # for vrag in self.vrag_list:
        #     self.zhivie_vrag_list.append(vrag)
        #     for drug in self.vrag_list:
        #         if vrag != drug:
        #             vrag.append_drug(drug)

        # self.igrok.sprite_list = self.vrag_list

        self.fizika = arcade.PymunkPhysicsEngine(GRAVITY, DAMPING)

        def begin_handler(sprite_a, sprite_b, arbiter, space, data):
            physics_object_a = self.fizika.sprites[sprite_a]
            physics_object_b = self.fizika.sprites[sprite_b]
            if physics_object_a.shape.collision_type == physics_object_b.shape.collision_type == 0:
                return False
            else:
                return True

        def begin_handler1(sprite_a, sprite_b, arbiter, space, data):
            physics_object_a = self.fizika.sprites[sprite_a]
            physics_object_b = self.fizika.sprites[sprite_b]
            if physics_object_a.shape.collision_type == physics_object_b.shape.collision_type == 1:
                return False
            else:
                return True

        def begin_handler2(sprite_a, sprite_b, arbiter, space, data):
            physics_object_a = self.fizika.sprites[sprite_a]
            physics_object_b = self.fizika.sprites[sprite_b]
            if physics_object_a.shape.collision_type == 2 and physics_object_b.shape.collision_type == 1:
                return False
            else:
                return True

        self.fizika.add_collision_handler("vrag", "vrag", begin_handler)
        self.fizika.add_collision_handler("vod_marionetka", "vod_marionetka", begin_handler1)
        self.fizika.add_collision_handler("igrok", "vod_marionetka", begin_handler2)

        self.fizika.add_sprite(self.igrok, MASS_IGROK, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                               max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED,
                               moment_of_inertia=self.fizika.MOMENT_INF, damping=0.9, collision_type="igrok")
        for vrag in self.vrag_list:
            self.fizika.add_sprite(vrag, 1, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=VRAG_OBICH_HORIZANTAL_SPEED,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9,
                                   collision_type="vrag")
            self.fizika.resync_sprites()
        self.fizika.add_sprite_list(self.walls_list, friction=WALL_FRICTION,
                                    body_type=self.fizika.STATIC, collision_type="wall")

        # self.wave(2, aarons.PRdd, 1700, 1900, 192)
        # self.wave(1, aarons.PMdd, 750, 1000, 192)
        # self.wave(2, aarons.OpMdd2, 400, 600, 192)
        # self.wave(2, aarons.OpMdd1, 500, 920, 192)
        # self.wave(2, aarons.OpRdd1, 1200, 1400, 192)
        # self.wave(1, aarons.OpRdd2, 450, 540, 192)
        # self.wave(2, aarons.G2, 1100, 1400, 192)
        # self.wave(2, aarons.G1, 650, 1250, 192)
        # self.wave(1, aarons.G3, 700, 1300, 192)

        for vrag in self.vrag_list:
            for drug in self.vrag_list:
                vrag.append_drug(drug)

    def wave(self, kol_vo, personazh, start, end, const, xy=True):
        vrag_list = arcade.SpriteList()

        prom = abs(start - end) // kol_vo
        for i in range(start, end, prom):
            if xy:
                vrag = personazh(self.igrok, self.walls_list)
                vrag.position = i, const
                vrag_list.append(vrag)
            else:
                vrag = personazh(self.igrok, self.walls_list)
                vrag.position = const, i
                vrag_list.append(vrag)

        for vrag in vrag_list:
            self.vrag_list.append(vrag)
            self.zhivie_vrag_list.append(vrag)
            self.fizika.add_sprite(vrag, 1 + random.randint(1, 5) / 50 , 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=300,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9,
                                   collision_type="vrag")
            self.fizika.step()
            # for drug in self.vrag_list:
            #     if vrag != drug:
            #         vrag.append_drug(drug)


        self.igrok.sprite_list = self.vrag_list
        #self.igrok.fizika = self.fizika

    def draw_ispar(self):
        sprite_list = arcade.SpriteList()
        sprite_list.append(self.igrok)
        for vrag in self.vrag_list:
            sprite_list.append(vrag)
        voda_list = arcade.SpriteList()
        ogon_list = arcade.SpriteList()

        position = 0

        for sprite in sprite_list:
            for sposob_ in sprite.sposob_list:
                if sposob_.podklass == sposobs.VODA:
                    voda_list.append(sposob_)
                elif sposob_.podklass == sposobs.OGON:
                    ogon_list.append(sposob_)

        for voda in voda_list:
            for ogon in ogon_list:
                if voda.action and ogon.action:
                    if arcade.check_for_collision(voda, ogon):
                        if ogon.scale <= voda.scale:
                            if voda.center_x >= ogon.center_x:
                                position = voda.left, ogon.center_y
                            else:
                                position = voda.right, ogon.center_y
                        else:
                            if voda.center_x >= ogon.center_x:
                                position = ogon.right, voda.center_y
                            else:
                                position = ogon.left, voda.center_y
        if position != 0:
            self.ispar.position = position
            self.ispar.update_animation()

    def on_draw(self):
        self.clear()

        self.smert_list1.draw()
        self.igrok.draw()
        self.igrok.update_animation()
        for vrag in self.zhivie_vrag_list:
            vrag.draw()
            vrag.update_animation()
        #self.igrok.draw_hit_box()
        self.smert_list2.draw()

        self.walls_list.draw()
        # self.box_fight.draw()

        # self.draw_ispar()

        self.line_hp.draw()
        # self.line_mana.draw()
        # self.line_stamina.draw()
        self.line_v.draw()
        #self.igrok.draw_hit_box(arcade.color.DARK_BLUE)

        self.circles.draw(self.x, self.y)

        arcade.draw_circle_filled(self.x + self.window.width, self.y + self.window.height, 10, arcade.color.WHITE)
        arcade.draw_circle_filled(self.x + 0, self.y + self.window.height, 10, arcade.color.WHITE)
        arcade.draw_circle_filled(self.x + 0, self.y + 0, 10, arcade.color.WHITE)
        arcade.draw_circle_filled(self.x + self.window.width, self.y + 0, 10, arcade.color.WHITE)

        arcade.draw_circle_filled(self.x + self.window.width, self.y + self.window.height
                                  + (self.kamera.zoom ** 2 * self.window.height - self.window.height) * 0.73, 10, arcade.color.GRAY)
        kry_x = (self.window.width * 1.44 - self.window.width) * 0.27
        arcade.draw_circle_filled(self.x - kry_x, self.y + self.window.height, 10, arcade.color.GRAY)
        arcade.draw_circle_filled(self.x + 0, self.y - 61.236, 10, arcade.color.GRAY)
        arcade.draw_circle_filled(self.x + self.window.width, self.y - 61.236, 10, arcade.color.GRAY)

        # 73 yf 27

        # nearest_wall_list = instruments.nearest(self.igrok.techenie.point, self.walls_list, 7)
        # s = 0
        # colors = [
        #     arcade.color.WHITE, arcade.color.BLACK, arcade.color.GRAY, arcade.color.RED, arcade.color.YELLOW,
        #     arcade.color.ORANGE, arcade.color.GREEN, arcade.color.BLUE
        # ]
        # for nearest_wall in nearest_wall_list:
        #     arcade.draw_line(self.igrok.techenie.point[0], self.igrok.techenie.point[1], nearest_wall.center_x,
        #                      nearest_wall.center_y, colors[s], 3)
        #     s += 1

        # arcade.draw_line(self.igrok.center_x - 500, self.igrok.center_y, self.igrok.center_x + 500, self.igrok.center_y,
        #                  (255, 0, 0, 255), 3)

        if self.vibor_sposob.active:
            self.vibor_sposob.draw()
            self.vibor_sposob.enable()
        else:
            self.vibor_sposob.disable()
        self.kamera.use()

    def move_sprite(self, sprite, minus_stamina, force, friction):
        # force, friction = sprite.oglush_force(force, friction, 2)
        # force, friction = sprite.slabweak_func(force, friction)
        # if sprite.dvizh:
        #     force = (tuple(sprite.new_force))
        self.fizika.apply_force(sprite, force)
        self.fizika.set_friction(sprite, friction)
        #sprite.stamina -= minus_stamina

    def izmen_poly(self, sprite):
        physics_object = self.fizika.sprites[sprite]
        poly = sprite.hit_box.points
        scaled_poly = [[x * sprite.scale for x in z] for z in poly]
        shape = pymunk.Poly(physics_object.body, scaled_poly, radius=0)
        shape.friction = physics_object.shape.friction
        shape.elasticity = physics_object.shape.elasticity
        shape.collision_type = physics_object.shape.collision_type
        new_physics_object = arcade.PymunkPhysicsObject(physics_object.body, shape)
        self.fizika.sprites[sprite] = new_physics_object
        self.fizika.space.remove(physics_object.shape)
        self.fizika.space.add(shape)

    def on_update(self, delta_time: float):
        if self.zoom:
            self.s_zoom += 1
            if self.s_zoom > 180:
                self.s_zoom = 0
                self.zoom = False
            if self.zoom:
                if self.s_zoom <= 180:
                    self.kamera.zoom -= 1 / 600
        if self.zoom1:
            self.s_zoom1 += 1
            if self.s_zoom1 > 180:
                self.s_zoom1 = 0
                self.zoom1 = False
            if self.zoom1:
                if self.s_zoom1 <= 180:
                    self.kamera.zoom += 1 / 600
        # for sprite in self.fizika.sprites:
        #     if sprite in self.fizika.non_static_sprite_list:
        #         self.update_poly(sprite)

        self.vibor_sposob.trigger_render()
        self.vibor_sposob.on_update(delta_time)

        self.circles.update()

        self.center_kamera_za_igrok()
        self.x, self.y = self.kamera.position
        self.line_hp.update(self.igrok.hp, self.x, self.y)
        # self.line_mana.update(self.igrok.mana, self.x, self.y)
        # self.line_stamina.update(self.igrok.stamina, self.x, self.y)
        self.line_v.update(self.igrok.v, self.x, self.y)
        # if self.s_voln == 0:
        #     self.s_voln += 1
        #     self.volna(3, pers.BetaBalvanchik, 1000, 1300, 200, sposobs.OBICH_MECH, 10000)

        for vrag in self.zhivie_vrag_list:
            if vrag.smert:
                if random.randint(0, 1) == 1:
                    self.smert_list1.append(vrag)
                else:
                    self.smert_list2.append(vrag)
                self.zhivie_vrag_list.remove(vrag)
                self.fizika.remove_sprite(vrag)
                vrag.animations.smert_animation()
                for vrag1 in self.vrag_list:
                    vrag1.update_drug_list()
            else:
                vrag.on_update()

                if vrag.sbiv:
                    self.izmen_poly(vrag)

                # if y > 0:
                #     self.s += 1
                # if self.s > 2 and not vrag.fizika.is_on_ground:
                #     y = 0
                #
                # force = (x, y)
                # friction = 0.7
                # # if vrag.dvizh:
                # #     force = vrag.new_force  # (vrag.new_force[0], vrag)
                # #     print(force)
                # #     self.move_sprite(vrag, 0.2 / 60, force, friction)
                # if not vrag.dvizh:
                #     vrag.vel_x = vrag.pymunk.max_horizontal_velocity
                #     if abs(x) > 0:
                #         self.move_sprite(vrag, 0.2 / 60, force, friction)
                #     elif y > 0:
                #         self.move_sprite(vrag, 0.2 / 60, force, friction)
                #     else:
                #         self.fizika.set_friction(vrag, 1)
                #
                # if y == 0 and self.s >= 2:
                #     self.s = 0

        friction = 0.6
        #self.move_sprite(self.igrok, 0.2 / 60, (0, 1500), 0.5)
        if not self.igrok.stan_for_sposob:
            if self.pravo and not self.levo:
                #self.fizika.set_position(self.igrok, (self.igrok.center_x + 100, self.igrok.center_y))
                self.igrok.storona = 0
                if not self.igrok.toggle:
                    self.move_sprite(self.igrok, 0.2 / 60, (IGROK_MOVE_GROUND, 0), friction)
                else:
                    self.igrok.techenie.hod(15, self.walls_list)
            elif not self.pravo and self.levo:
                #self.fizika.set_position(self.igrok, (self.igrok.center_x - 100, self.igrok.center_y))
                self.igrok.storona = 1
                if not self.igrok.toggle:
                    self.move_sprite(self.igrok, 0.2 / 60, (-IGROK_MOVE_GROUND, 0), friction)
                else:
                    self.igrok.techenie.hod(-15, self.walls_list)
            else:
                #self.igrok.storona = 0
                # print("____________")
                self.igrok.techenie.hod(0, self.walls_list)
                # self.fizika.set_friction(self.igrok, 1)

        self.igrok.on_update()

        # if self.igrok.molniya.tp and self.s1 == 0:
        #     self.s1 += 1
        #     poz = self.igrok.molniya.return_position()
        #     self.fizika.set_position(self.igrok, poz)

        # if len(self.zhivie_vrag_list) <= 0 and self.s_voln == 0:
        #     self.s_voln += 1
        #     self.volna(10, pers.BetaBalvanchik, 201, -1000, -500, 200, True, 500)

        self.igrok: igrok.BetaOyuun
        if self.igrok.voda_shchit in self.fizika.sprites and not self.igrok.voda_shchit.block:
            self.fizika.remove_sprite(self.igrok.voda_shchit)
        self.fizika.step()

    def on_key_press(self, symbol: int, modifiers: int):
        self.vibor_sposob.on_key_press(symbol, modifiers)

        if symbol == arcade.key.R and self.igrok.pistolet.kd:
            self.igrok.pistolet.perezaryadka = True

        if symbol == arcade.key.I:
            self.I = not self.I
            self.line_x = int(self.line_x)

        if symbol == arcade.key.SPACE:
            self.igrok.action(sposobs.VODA_UDARS)
            self.igrok.action(sposobs.UDAR)

        if not self.vibor_sposob.active:
            if symbol == arcade.key.Y:
                # self.igrok.test.fight = True
                # self.fizika.sprites[self.igrok].body.body_type = self.fizika.KINEMATIC
                for x in range(490, 1000, 100):
                    vrag = aarons.Balvanchik(self.igrok, "Balvan", self.walls_list)
                    vrag.position = x, 300
                    self.vrag_list.append(vrag)
                    self.zhivie_vrag_list.append(vrag)
                    self.fizika.add_sprite(vrag, 1, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
                                   max_horizontal_velocity=VRAG_OBICH_HORIZANTAL_SPEED,
                                   moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9,
                                   collision_type="vrag")

                for vrag in self.vrag_list:
                    for drug in self.vrag_list:
                        if vrag != drug:
                            vrag.append_drug(drug)

            # if symbol == arcade.key.S:
            #     self.igrok.scale -= 0.5
            #     physics_object = self.fizika.sprites[self.igrok]
            #     poly = self.igrok.hit_box.points
            #     scaled_poly = [[x * self.igrok.scale for x in z] for z in poly]
            #     shape = pymunk.Poly(physics_object.body, scaled_poly, radius=0)
            #     shape.friction = physics_object.shape.friction
            #     shape.elasticity = physics_object.shape.elasticity
            #     shape.collision_type = physics_object.shape.collision_type
            #     new_physics_object = arcade.PymunkPhysicsObject(physics_object.body, shape)
            #     self.fizika.sprites[self.igrok] = new_physics_object
            #     self.fizika.space.remove(physics_object.shape)
            #     self.fizika.space.add(shape)
            #
            # if symbol == arcade.key.X:
            #     self.igrok.scale += 0.5
            #     physics_object = self.fizika.sprites[self.igrok]
            #     poly = self.igrok.hit_box.points
            #     scaled_poly = [[x * self.igrok.scale for x in z] for z in poly]
            #     shape = pymunk.Poly(physics_object.body, scaled_poly, radius=0)
            #     shape.friction = physics_object.shape.friction
            #     shape.elasticity = physics_object.shape.elasticity
            #     shape.collision_type = physics_object.shape.collision_type
            #     new_physics_object = arcade.PymunkPhysicsObject(physics_object.body, shape)
            #     self.fizika.sprites[self.igrok] = new_physics_object
            #     self.fizika.space.remove(physics_object.shape)
            #     self.fizika.space.add(shape)

            if symbol == arcade.key.RSHIFT:
                self.igrok.techenie.action = not self.igrok.techenie.action

            if symbol == arcade.key.E:
                self.igrok.kritik = not self.igrok.kritik

            if symbol == arcade.key.LSHIFT:
                self.igrok.beg = True
                self.igrok.pymunk.max_horizontal_velocity = IG_MAX_HORIZANTAL_SPEED * 4
                self.igrok.walk = False

            if symbol == arcade.key.LCTRL:
                self.zoom1 = True
                self.zoom = False

            if symbol == arcade.key.Z:
                self.zoom = True
                self.zoom1 = False

            if symbol == arcade.key.Q:
                if self.kamera.zoom != 2:
                    self.kamera.zoom = 2
                else:
                    self.kamera.zoom = 1.1

            if symbol == arcade.key.NUM_0:
                self.igrok.action(self.igrok.five_sposobs[4].sposob)

            if symbol == arcade.key.NUM_1:
                self.igrok.action(self.igrok.five_sposobs[0].sposob)

            if symbol == arcade.key.NUM_2:
                self.igrok.action(self.igrok.five_sposobs[3].sposob)

            if symbol == arcade.key.NUM_3:
                self.igrok.action(self.igrok.five_sposobs[2].sposob)

            if symbol == arcade.key.RETURN:
                self.igrok.action(self.igrok.five_sposobs[1].sposob)

            if symbol == arcade.key.NUM_DECIMAL:
                self.igrok.block.block = True

            if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
                if not self.I:
                    self.line_x += 1
                # self.igrok.storona = 1
                # self.igrok.animations.storona = 0
                self.pravo = True
                self.igrok.walk = True
            elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
                if not self.I:
                    self.line_x -= 1
                # self.igrok.storona = -1
                # self.igrok.animations.storona = 1
                self.levo = True
                self.igrok.walk = True

            if symbol == arcade.key.W or symbol == arcade.key.UP:
                if self.igrok.fizika.is_on_ground and not self.igrok.toggle:
                    # self.move_sprite(self.igrok, 2, (0, IGROK_JUMP_FORCE), 0.5)
                    if not self.igrok.dvizh:
                        force = (0, IGROK_JUMP_FORCE)
                    else:
                        force = (0, IGROK_JUMP_FORCE + self.igrok.new_force[1])
                    self.fizika.apply_force(self.igrok, force)
                # if self.igrok.toggle:
                #     self.igrok.techenie.vverh_func(self.walls_list, 15)

            if symbol == arcade.key.DOWN:
                self.fizika.set_position(self.igrok, (self.igrok.center_x, self.igrok.center_y - 50))

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.T:
            new_body = self.fizika.sprites[self.igrok].body
            new_body.body_type = self.fizika.DYNAMIC
            self.fizika.sprites[self.igrok].body = new_body
            self.fizika.set_position(self.igrok, (0, 300))


            # self.fizika.remove_sprite(self.igrok)
            # self.fizika.add_sprite(self.igrok, MASS_IGROK, 1, max_vertical_velocity=IG_MAX_VERTICAL_SPEED,
            #                        max_horizontal_velocity=IG_MAX_HORIZANTAL_SPEED,
            #                        moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF, damping=0.9,
            #                        collision_type='player')

        if _symbol == arcade.key.LSHIFT:
            self.igrok.beg = False
            self.igrok.walk = True
            self.igrok.pymunk.max_horizontal_velocity = IG_MAX_HORIZANTAL_SPEED

        if _symbol == arcade.key.NUM_DECIMAL:
            self.igrok.block.block = False

        if _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.pravo = False
            self.igrok.walk = False
        elif _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.levo = False
            self.igrok.walk = False

    def center_kamera_za_igrok(self):
        ekran_center_x = self.igrok.center_x - W / 2
        ekran_center_y = self.igrok.center_y - H / 5
        # if ekran_center_y < 300:
        # ekran_center_y = 64

        self.kamera.move_to((ekran_center_x, ekran_center_y))
        self.x = self.kamera.position[0]
        self.y = self.kamera.position[1]


win = arcade.Window(W, H, fullscreen=True)
viev1 = BetaViev()
viev1.setup()
win.show_view(viev1)

arcade.run()

