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


class LeaderboardView(arcade.View):
    def __init__(self):
        super().__init__()

        self.score = None
        self.score_text = None

        arcade.set_background_color(arcade.color.GRAY)

        self.ui = UIManager()

        self.anchor = self.ui.add(UIAnchorLayout())

        self.setup()

    def setup(self):
        try:
            with open('leaderboard.txt', 'r+') as reader:
                score = reader.readline()
                self.score = int(float(score))
            if self.score is None:
                self.score = 0
        except FileNotFoundError:
            self.score = 0

        self.score_text = arcade.Text(f"BEST SCORE:{self.score}", 450, 600, arcade.color.GOLD, 32)

        self.buttons()

    def buttons(self):
        button_back = self.anchor.add(
            UITextureButton(
                text="Back to Main Menu",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=0,
            align_y=0
        )

        @button_back.event("on_click")
        def on_click(_event):
            self.window.show_view(menu.MenuView())

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.score_text.draw()
        self.ui.draw()

    def on_update(self, delta_time):
        pass
