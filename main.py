"""
Tp7
Par Vincent et Yul :)
Jeu de Poisson
"""

import arcade
from game_state import GameState
import menu

SCREEN_WIDTH = 1164
SCREEN_HEIGHT = 764
SCREEN_TITLE = "Croisson"

BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menux = menu.MenuView()
    window.show_view(menux)
    arcade.run()


if __name__ == "__main__":
    main()
