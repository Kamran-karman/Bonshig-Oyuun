from arcade import Texture
import instruments

class Animations:
    def __init__(self, sprite):
        self.sprite = sprite
        self.main_patch = ''
        self.slovar_animation: dict[str, list[int, int, int, instruments.TextureList]] = {}
        '''0 - счётчик

           1 - предел

           2 - кадр

           3 - список текстур'''

    def _update_texture_and_hitbox(self, texture: Texture):
        self.sprite.texture = texture
        self.sprite.hit_box._points = self.sprite.texture.hit_box_points


