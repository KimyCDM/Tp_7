from enum import Enum

import arcade

from PIL.ImageOps import mirror


class AnimationType(Enum):
    IDLE_LEFT = 0,
    IDLE_RIGHT = 1,
    SWIM_LEFT = 2,
    SWIM_RIGHT = 3


class PlayerAnimation(arcade.Sprite):
    PLAYER_SCALE = 0.10
    ANIMATION_SPEED = 8.0

    def __init__(self, animation_type, player_color):
        super().__init__()

        if player_color == "Black":
            self.idle = "assets/2dfish/spritesheets/__cartoon_fish_06_black_idle.png"
            self.swim = "assets/2dfish/spritesheets/__cartoon_fish_06_black_swim.png"
        elif player_color == "Blue":
            self.idle = "assets/2dfish/spritesheets/__cartoon_fish_06_blue_idle.png"
            self.swim = "assets/2dfish/spritesheets/__cartoon_fish_06_blue_swim.png"
        elif player_color == "Green":
            self.idle = "assets/2dfish/spritesheets/__cartoon_fish_06_green_idle.png"
            self.swim = "assets/2dfish/spritesheets/__cartoon_fish_06_green_swim.png"
        elif player_color == "Purple":
            self.idle = "assets/2dfish/spritesheets/__cartoon_fish_06_purple_idle.png"
            self.swim = "assets/2dfish/spritesheets/__cartoon_fish_06_purple_swim.png"
        elif player_color == "Red":
            self.idle = "assets/2dfish/spritesheets/__cartoon_fish_06_red_idle.png"
            self.swim = "assets/2dfish/spritesheets/__cartoon_fish_06_red_swim.png"
        elif player_color == "Yellow":
            self.idle = "assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png"
            self.swim = "assets/2dfish/spritesheets/__cartoon_fish_06_yellow_swim.png"

        self.animation_type = animation_type

        if self.animation_type == AnimationType.IDLE_LEFT:
            self.sprite_sheet = arcade.load_spritesheet(self.idle)
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 20)
            self.textures = textures

        elif self.animation_type == AnimationType.IDLE_RIGHT:
            self.sprite_sheet = arcade.load_spritesheet(self.idle)
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 20)

            temp_texture = []
            for texture in textures:
                temp_texture.append(arcade.Texture(mirror(texture.image)))

            self.textures = temp_texture

        elif self.animation_type == AnimationType.SWIM_LEFT:
            self.sprite_sheet = arcade.load_spritesheet(self.swim)
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 12)
            self.textures = textures

        else:
            self.sprite_sheet = arcade.load_spritesheet(self.swim)
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 12)

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
