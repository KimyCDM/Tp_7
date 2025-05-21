import random
import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
)

import menu

BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")


class OptionView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_color = "Yellow"
        self.fool_mode = False

        arcade.set_background_color(arcade.color.GRAY)

        self.ui = UIManager()

        self.anchor = self.ui.add(UIAnchorLayout())

        self.buttons()

    def buttons(self):
        button_fish_color = self.anchor.add(
            UITextureButton(
                text=f"Fish Color: {self.player_color}",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-75,
        )

        button_return = self.anchor.add(
            UITextureButton(
                text=f"Back to Main Menu",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-150,
        )

        @button_fish_color.event("on_click")
        def on_click(_event):
            fish_color_list = ["Black", "Blue", "Green", "Purple", "Red", "Yellow"]
            self.player_color = random.choice(fish_color_list)
            button_fish_color.text = f"Fish Color: {self.player_color}"

        @button_return.event("on_click")
        def on_click(_event):
            with open('player_options.txt', 'w') as writer:
                writer.write(self.player_color)
            self.window.show_view(menu.MenuView())

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
