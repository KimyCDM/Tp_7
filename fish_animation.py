from enum import Enum

import arcade

from PIL.ImageOps import mirror

"""
load sprite sheet
get texture grid
"""


class AnimationType(Enum):
    IDLE_LEFT = 0,
    IDLE_RIGHT = 1,
    SWIM_LEFT = 2,
    SWIM_RIGHT = 3


class PlayerAnimation(arcade.Sprite):
    PLAYER_SCALE = 0.20
    ANIMATION_SPEED = 8.0

    def __init__(self, animation_type):
        super().__init__()

        self.animation_type = animation_type

        if self.animation_type == AnimationType.IDLE_LEFT:
            self.sprite_sheet = arcade.load_spritesheet("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png")
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 20)
            self.textures = textures

        elif self.animation_type == AnimationType.IDLE_RIGHT:
            self.sprite_sheet = arcade.load_spritesheet("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png")
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 20)

            temp_texture = []
            for texture in textures:
                temp_texture.append(arcade.Texture(mirror(texture.image)))

            self.textures = temp_texture

        elif self.animation_type == AnimationType.SWIM_LEFT:
            self.sprite_sheet = arcade.load_spritesheet("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_swim.png")
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 12)
            self.textures = textures

        else:
            self.sprite_sheet = arcade.load_spritesheet("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_swim.png")
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 20)

            temp_texture = []
            for texture in textures:
                temp_texture.append(arcade.Texture(mirror(texture.image)))

            self.textures = temp_texture

        self.scale = self.PLAYER_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)

        self.animation_update_time = 1.0 / PlayerAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0

    def on_update(self, delta_time: float = 1 / 60):
        # Update the animation.
        self.time_since_last_swap += delta_time
        if self.time_since_last_swap > self.animation_update_time:
            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.current_texture = 0
                self.set_texture(self.current_texture)
            self.time_since_last_swap = 0.0


"""
        if self.animation_type == AnimationType.IDLE and  == "D":
            self.sprite_sheet = arcade.load_spritesheet("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png", flipped_horizontally=True)
            texture = self.sprite_sheet.get_texture_grid((498, 327), 4, 20)
"""