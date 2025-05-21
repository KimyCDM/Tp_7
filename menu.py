import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
)


import leaderboard
import option
import game

BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.GRAY)

        self.ui = UIManager()

        self.anchor = self.ui.add(UIAnchorLayout())

        self.buttons()

    def buttons(self):
        button_new = self.anchor.add(
            UITextureButton(
                text="Play",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-75,
        )

        button_leaderboard = self.anchor.add(
            UITextureButton(
                text="Leaderboard",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-150,
        )

        button_option = self.anchor.add(
            UITextureButton(
                text="Option",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-225,
        )

        button_quit = self.anchor.add(
            UITextureButton(
                text="Quit game",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-300,
        )

        @button_new.event("on_click")
        def on_click(_event):
            self.window.show_view(game.GameView())

        @button_leaderboard.event("on_click")
        def on_click(_event):
            self.window.show_view(leaderboard.LeaderboardView())

        @button_option.event("on_click")
        def on_click(_event):
            self.window.show_view(option.OptionView())

        @button_quit.event("on_click")
        def on_click(_event):
            arcade.exit()

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
