import arcade

import hit_box_and_radius
import sposobs
from sposobs import fiz_sposob
from sposobs.fiz_sposob import cold_oruzhie
from sposobs.stihiya import ogon_baf

class OgonMolotok(ogon_baf.BafColdOr, cold_oruzhie.Molotok):
    def __init__(self, pers):
        super().__init__(pers, arcade.load_texture_pair("resources/Sposob_animations/molotok_ogon_baf.png"))
        self.klass = sposobs.FIZ_SPOSOB
        self.podklass = sposobs.FIZ_SPOSOB_FIGHT
        self.tip = sposobs.COLD_ORUZHIE
        self.sposob = sposobs.OGON_MOLOTOK

        self.tik_uron = 5
        self.timer_for_s = 30

        self.minus_mana = 1

    def on_update(self, delta_time: float = 1 / 60, physics_engine: arcade.PymunkPhysicsEngine = None) -> None:
        self.update_mor()
        super().on_update(delta_time, physics_engine)
        self.update_tik()

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        super().update_animation(delta_time)
        self.baf_animations()

