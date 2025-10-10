import animations
import sposobs

import instruments

ACTION = "action"
DEACTION = "deaction"


class SposobAnimation(animations.Animations):
    def __init__(self, sprite: sposobs.Sposob):
        super().__init__(sprite)
        self.main_patch = "resources/Sposob_animations/"

        self.slovar_animation.update({ACTION: [0, 0, 0, instruments.TextureList()],
                                      DEACTION: [0, 0, 0, instruments.TextureList()]})
        self.s = 0

    def action_animation(self):
        if self.sprite.action:
            self.slovar_animation[DEACTION][0] = 0
            self.slovar_animation[ACTION][0] += self.slovar_animation[ACTION][2]
            if self.slovar_animation[ACTION][0] > self.slovar_animation[ACTION][1]:
                self.slovar_animation[ACTION][0] = 0
                self.s += 1
            self._update_texture_and_hitbox(self.slovar_animation[ACTION][3][int(self.slovar_animation[ACTION][0])]
                                            [self.sprite.storona])
        else:
            self.slovar_animation[ACTION][0] = 0
            self.s = 0

    def deaction_animations(self):
        self.sprite: sposobs.Sposob
        if not self.sprite.action and self.sprite.kd and self.slovar_animation[DEACTION][0] < self.slovar_animation[DEACTION][1]:
            self.slovar_animation[DEACTION][0] += self.slovar_animation[DEACTION][2]
            self._update_texture_and_hitbox(self.slovar_animation[DEACTION][3][int(self.slovar_animation[DEACTION][0])]
                                            [self.sprite.storona])

