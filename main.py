"""
Tp7
Par Vincent et Yul :)
Jeu de Poisson
"""

import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
    UIView,
)
from game_state import GameState
from fish_animation import AnimationType, PlayerAnimation

SCREEN_WIDTH = 1164
SCREEN_HEIGHT = 764
SCREEN_TITLE = "Croisson"

BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")

"""
To do list
Invisible wall collison
Animation for swiming
Flip fish (working on)
"""


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
        def on_click(event):
            self.window.show_view(GameView())

        @button_leaderboard.event("on_click")
        def on_click(event):
            self.window.show_view(LeaderboardView())

        @button_option.event("on_click")
        def on_click(event):
            self.window.show_view(OptionView())

        @button_quit.event("on_click")
        def on_click(event):
            arcade.exit()

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)
        self.background_image_game = arcade.Sprite("assets/Background.png", 1)
        self.background_image_game.center_x = 1164 / 2
        self.background_image_game.center_y = 764 / 2
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_image_game)

        self.lives_text = None
        self.time_text = None

        self.second = None
        self.minute = None
        self.hour = None
        self.timer = None

        self.game_state = None

        self.live_sprite = None
        self.live_list = None
        self.lives = None

        self.start_game_text = None

        self.player_idle_left = None
        self.player_idle_right = None
        self.player_swim_left = None
        self.player_swim_right = None
        self.player = None
        self.player_list = None
        self.player_list = None
        self.player_color = None
        self.player_speed = None
        self.anim = None

        self.key_hold_x = None
        self.key_hold_y = None

        self.setup()

    def setup(self):
        self.game_state = GameState.GAME_NOT_STARTED

        self.lives_text = arcade.Text(f"Lives:", 20, 716, arcade.color.WHITE, 32)
        self.time_text = arcade.Text(f"Time Played: {self.hour} h {self.minute} min {self.second} s",
                                     600, 716, arcade.color.WHITE, 32)

        self.second = 0
        self.minute = 0
        self.hour = 0
        self.timer = 0

        self.live_sprite = arcade.Sprite("assets/MC_Heart.png", 0.25, 220, 730)
        self.live_list = arcade.SpriteList()
        self.live_list.append(self.live_sprite)
        self.lives = 3

        self.start_game_text = arcade.Text('Appuyez sur "Espace" pour commencer!', 50, 764 / 2, arcade.color.WHITE, 50)

        self.player_idle_left = PlayerAnimation(AnimationType.IDLE_LEFT)
        self.player_idle_right = PlayerAnimation(AnimationType.IDLE_RIGHT)
        self.player_swim_left = PlayerAnimation(AnimationType.SWIM_LEFT)
        self.player_swim_right = PlayerAnimation(AnimationType.SWIM_RIGHT)
        self.player_list = arcade.SpriteList()

        self.player = self.player_idle_left
        self.player_list.append(self.player)

        self.player.center_x = 300
        self.player.center_y = 300
        self.player_speed = 10

    def text(self):
        if self.game_state == GameState.GAME_NOT_STARTED:
            self.start_game_text.draw()

    def show_game_state(self, show):
        if show is True:
            print(self.game_state)

    def player_draw(self):

        self.player_list.draw()

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.text()

        arcade.draw_lrbt_rectangle_filled(0, 1664, 700, 764, (0, 128, 255))

        self.lives_text.draw()
        self.time_text.draw()

        for i in range(self.lives):
            self.live_sprite.center_x = 220 + (i - 1) * 60
            self.live_list.draw()

        self.player_draw()

    def in_game_timer(self):
        if self.game_state == GameState.GAME_STARTED:
            self.time_text.text = f"Time Played: {self.hour} h {self.minute} min {self.second} s"
            self.timer += 1
            if self.timer == 60:
                self.second += 1
                self.timer = 0
            if self.second == 60:
                self.minute += 1
                self.second = 0
            if self.minute == 60:
                self.hour += 1
                self.minute = 0

    def player_mouvement(self):
        if self.key_hold_x == "A" and self.game_state == GameState.GAME_STARTED and self.player.center_x != 0:
            self.player.center_x -= self.player_speed
        elif self.key_hold_x == "D" and self.game_state == GameState.GAME_STARTED and self.player.center_x != 1100:
            self.player.center_x += self.player_speed
        if self.key_hold_y == "W" and self.game_state == GameState.GAME_STARTED and self.player.center_y != 700:
            self.player.center_y += self.player_speed
        elif self.key_hold_y == "S" and self.game_state == GameState.GAME_STARTED and self.player.center_y != 0:
            self.player.center_y -= self.player_speed

    def player_change_anim(self, anim):
        self.player_list.pop()
        if anim == "swim":
            if self.anim == "idle left":
                anim = "swim left"
            elif self.anim == "idle right":
                anim = "swim right"
        elif anim == "idle":
            if self.anim == "swim left":
                anim = "idle left"
            elif self.anim == "swim right":
                anim = "idle right"

        self.anim = anim

        if self.anim == "idle left":
            self.player_idle_left.center_x = self.player.center_x
            self.player_idle_left.center_y = self.player.center_y
            self.player = self.player_idle_left
        elif self.anim == "idle right":
            self.player_idle_right.center_x = self.player.center_x
            self.player_idle_right.center_y = self.player.center_y
            self.player = self.player_idle_right
        elif self.anim == "swim left":
            self.player_swim_left.center_x = self.player.center_x
            self.player_swim_left.center_y = self.player.center_y
            self.player = self.player_swim_left
        elif self.anim == "swim right":
            self.player_swim_right.center_x = self.player.center_x
            self.player_swim_right.center_y = self.player.center_y
            self.player = self.player_swim_right
        self.player_list.append(self.player)

    def on_update(self, delta_time):
        self.player.on_update(delta_time)

        self.show_game_state(False)
        self.in_game_timer()
        self.player_mouvement()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE and self.game_state == GameState.GAME_NOT_STARTED:
            self.game_state = GameState.GAME_STARTED
        if key == arcade.key.A and self.game_state == GameState.GAME_STARTED:
            self.key_hold_x = "A"
            self.player_change_anim("swim left")
        elif key == arcade.key.D and self.game_state == GameState.GAME_STARTED:
            self.key_hold_x = "D"
            self.player_change_anim("swim right")
        if key == arcade.key.W and self.game_state == GameState.GAME_STARTED:
            self.key_hold_y = "W"
            self.player_change_anim("swim")
        elif key == arcade.key.S and self.game_state == GameState.GAME_STARTED:
            self.key_hold_y = "S"
            self.player_change_anim("swim")

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.A and self.key_hold_x == "A":
            self.key_hold_x = None
            self.player_change_anim("idle left")
        elif key == arcade.key.D and self.key_hold_x == "D":
            self.key_hold_x = None
            self.player_change_anim("idle right")
        if key == arcade.key.W and self.key_hold_y == "W" or key == arcade.key.S and self.key_hold_y == "S":
            self.key_hold_y = None
            self.player_change_anim("idle")

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


class LeaderboardView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


class OptionView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    game = GameView()
    menu = MenuView()
    leaderbord = LeaderboardView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
