import random
import arcade
from PIL.ImageOps import mirror


fish_color_to_path = {
    0: "assets/2dfish/spritesheets/__cartoon_fish_06_black_swim.png",
    1: "assets/2dfish/spritesheets/__cartoon_fish_06_blue_swim.png",
    2: "assets/2dfish/spritesheets/__cartoon_fish_06_green_swim.png",
    3: "assets/2dfish/spritesheets/__cartoon_fish_06_red_swim.png",
    4: "assets/2dfish/spritesheets/__cartoon_fish_06_purple_swim.png",
    5: "assets/2dfish/spritesheets/__cartoon_fish_06_yellow_swim.png"
}


class FishyAnimation(arcade.Sprite):
    NPC_SCALE_LIST = [0.75, 0.90, 1.50, 1.75, 2.00]
    NPC_ANIMATION_SPEED = 8.0

    def __init__(self, player_scale):
        super().__init__()

        if player_scale > 0.55:
            self.npc_scale = random.choice(self.NPC_SCALE_LIST) * 0.55
        else:
            self.npc_scale = random.choice(self.NPC_SCALE_LIST) * player_scale
        self.fish_color = random.choice(list(fish_color_to_path.keys()))
        self.fish_direction = random.randint(1, 2)

        if self.fish_direction == 1:
            self.sprite_sheet = arcade.load_spritesheet(fish_color_to_path[self.fish_color])
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 12)
            self.textures = textures
            self.swim_speed = -1 - self.npc_scale*8

        if self.fish_direction == 2:
            self.sprite_sheet = arcade.load_spritesheet(fish_color_to_path[self.fish_color])
            textures = self.sprite_sheet.get_texture_grid((498, 327), 4, 12)

            temp_texture = []
            for texture in textures:
                temp_texture.append(arcade.Texture(mirror(texture.image)))

            self.textures = temp_texture
            self.swim_speed = 1 + self.npc_scale*8

        self.current_texture = 0
        self.set_texture(self.current_texture)

        self.scale = self.npc_scale
        self.animation_update_time = 1.0 / FishyAnimation.NPC_ANIMATION_SPEED
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
