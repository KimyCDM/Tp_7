"""
Tp7
Par Vincent et Yul :)
Jeu de Poisson
To do list
fish rng/size
EASTEREGG
"""

import random
import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
)
from game_state import GameState
from fish_animation import AnimationType, PlayerAnimation
from fish_npc import FishyAnimation

SCREEN_WIDTH = 1164
SCREEN_HEIGHT = 764
SCREEN_TITLE = "Croisson"

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

        self.background_image_game = arcade.Sprite("assets/Background.png", 1)
        self.background_image_game.center_x = 1164 / 2
        self.background_image_game.center_y = 764 / 2
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_image_game)

        self.lives_text = None
        self.time_text = None
        self.score_text = None

        self.second = None
        self.minute = None
        self.hour = None
        self.timer = None

        self.game_state = None
        self.score = None

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
        self.player_speed = None
        self.anim = None

        self.key_hold_x = None
        self.key_hold_y = None

        self.fish_spawn_speed = None
        self.fish_spawn_time = None
        self.fish_list = None
        self.fish = None

        self.protection_timer = None
        self.protection = None

        self.fish_color = None

        self.setup()

    def setup(self):
        self.game_state = GameState.GAME_NOT_STARTED

        self.lives_text = arcade.Text(f"Lives:", 20, 716, arcade.color.WHITE, 32)
        self.time_text = arcade.Text(f"Time Played: {self.hour} h {self.minute} min {self.second} s",
                                     600, 716, arcade.color.WHITE, 32)
        self.score_text = arcade.Text(f"Score:{self.score}", 400, 716, arcade.color.WHITE, 32)

        self.second = 0
        self.minute = 0
        self.hour = 0
        self.timer = 0
        self.score = 0

        self.live_sprite = arcade.Sprite("assets/MC_Heart.png", 0.25, 220, 730)
        self.live_list = arcade.SpriteList()
        self.live_list.append(self.live_sprite)
        self.lives = 3

        self.start_game_text = arcade.Text('Appuyez sur "Espace" pour commencer!', 50, 764 / 2, arcade.color.WHITE, 50)

        try:
            with open('player_options.txt', 'r+') as reader:
                # Further file processing goes here
                self.fish_color = reader.readline()
            if self.fish_color is None:
                self.fish_color = "Black"
        except FileNotFoundError:
            self.fish_color = "Black"

        self.player_idle_left = PlayerAnimation(AnimationType.IDLE_LEFT, self.fish_color)
        self.player_idle_right = PlayerAnimation(AnimationType.IDLE_RIGHT, self.fish_color)
        self.player_swim_left = PlayerAnimation(AnimationType.SWIM_LEFT, self.fish_color)
        self.player_swim_right = PlayerAnimation(AnimationType.SWIM_RIGHT, self.fish_color)
        self.player_list = arcade.SpriteList()

        self.player = self.player_idle_left
        self.player_list.append(self.player)

        self.player.center_x = 300
        self.player.center_y = 300
        self.player_speed = 4 + PlayerAnimation.PLAYER_SCALE

        self.fish_spawn_time = random.randint(180, 300)
        self.fish_spawn_speed = 0
        self.fish_list = arcade.SpriteList()

        self.protection = False
        self.protection_timer = 0

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
        self.score_text.draw()

        for i in range(self.lives):
            self.live_sprite.center_x = 220 + (i - 1) * 60
            self.live_list.draw()

        self.player_draw()

        self.fish_list.draw()

    def in_game_timer(self):
        if self.game_state == GameState.GAME_STARTED:
            self.time_text.text = f"Time Played: {self.hour} h {self.minute} min {self.second} s"
            self.timer += 1
            if self.timer == 60:
                self.second += 1
                self.score += 1
                self.timer = 0
                if self.protection is True:
                    self.protection_timer += 1
                    if self.protection_timer > 3:
                        self.protection = False
                        self.protection_timer = 0
            if self.second == 60:
                self.minute += 1
                self.second = 0
            if self.minute == 60:
                self.hour += 1
                self.minute = 0

    def player_mouvement(self):
        if (self.key_hold_x == "A" and self.game_state == GameState.GAME_STARTED and
                self.player.center_x > 0 + PlayerAnimation.PLAYER_SCALE*25):
            self.player.center_x -= self.player_speed
        elif (self.key_hold_x == "D" and self.game_state == GameState.GAME_STARTED and
              self.player.center_x < 1100 - PlayerAnimation.PLAYER_SCALE*25):
            self.player.center_x += self.player_speed
        if (self.key_hold_y == "W" and self.game_state == GameState.GAME_STARTED and
                self.player.center_y < 680 - PlayerAnimation.PLAYER_SCALE*25):
            self.player.center_y += self.player_speed
        elif (self.key_hold_y == "S" and self.game_state == GameState.GAME_STARTED and
              self.player.center_y > 0 + PlayerAnimation.PLAYER_SCALE*25):
            self.player.center_y -= self.player_speed

    def player_change_anim(self, anim):
        scale = self.player.scale
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
        self.player.scale = scale

    def fish_spawn(self):
        self.fish_spawn_speed += 1
        if self.fish_spawn_speed >= self.fish_spawn_time:
            self.fish_spawn_speed = 0
            self.fish_spawn_time = random.randint(60, 180)
            fish = FishyAnimation(PlayerAnimation.PLAYER_SCALE)
            self.fish_list.append(fish)
            fish.center_y = random.randint(0, 650)
            if fish.fish_direction == 1:
                fish.center_x = 1164
            else:
                fish.center_x = 0

    def eating(self):
        fish_hit_list = arcade.check_for_collision_with_list(self.player, self.fish_list)
        for fish in fish_hit_list:
            if PlayerAnimation.PLAYER_SCALE >= fish.npc_scale:
                fish.remove_from_sprite_lists()
                PlayerAnimation.PLAYER_SCALE += fish.npc_scale/5
                self.player.scale = PlayerAnimation.PLAYER_SCALE
                self.score += fish.npc_scale*10
            elif PlayerAnimation.PLAYER_SCALE <= fish.npc_scale and self.protection is False:
                self.lives -= 1
                self.protection = True

    def gameover(self):
        if self.lives == 0:
            self.game_state = GameState.GAME_OVER
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_update(self, delta_time):
        self.player.on_update(delta_time)
        self.show_game_state(False)
        self.in_game_timer()
        self.player_mouvement()
        self.eating()
        self.player_speed = 4 + PlayerAnimation.PLAYER_SCALE
        self.score_text = arcade.Text(f"Score:{int(float(self.score))}", 380, 716, arcade.color.WHITE, 32)
        self.gameover()

        if self.game_state == GameState.GAME_STARTED:
            self.fish_spawn()

        for fish in self.fish_list:
            fish.on_update(delta_time)
            fish.center_x += fish.swim_speed

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
        if key == arcade.key.ESCAPE and self.game_state == GameState.GAME_STARTED:
            self.game_state = GameState.PAUSED
            pause = PauseView(self)
            self.window.show_view(pause)
        if key == arcade.key.ENTER and self.game_state == GameState.GAME_OVER:  # reset game
            menu = MenuView()
            self.window.show_view(menu)

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
                # Further file processing goes here
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
        def on_click(event):
            self.window.show_view(MenuView())

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
        """
        button_fool_mode = self.anchor.add(
            UITextureButton(
                text=f"Fool Mode: {self.fool_mode}",
                texture=BUTTON_NORMAL,
                texture_hovered=BUTTON_HOVER,
                texture_pressed=BUTTON_PRESS,
            ),
            align_x=-450,
            align_y=-150,
        )
        """

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
        def on_click(event):
            fish_color_list = ["Black", "Blue", "Green", "Purple", "Red", "Yellow"]
            self.player_color = random.choice(fish_color_list)
            button_fish_color.text = f"Fish Color: {self.player_color}"

        """
        @button_fool_mode.event("on_click")
        def on_click(event):
            if not self.fool_mode:
                self.fool_mode = True
            elif self.fool_mode:
                self.fool_mode = False
            button_fool_mode.text = f"Fool Mode: {self.fool_mode}"
        """

        @button_return.event("on_click")
        def on_click(event):
            with open('player_options.txt', 'w') as writer:
                # Further file processing goes here
                writer.write(self.player_color)
            self.window.show_view(MenuView())

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        if self.game_view.lives != 0:
            arcade.draw_text("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                             arcade.color.BLACK, font_size=50, anchor_x="center")

            # Show return or reset
            arcade.draw_text("Press Esc. to return",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
            arcade.draw_text("Press Enter to reset",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 30,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
            arcade.draw_text(
                f"Time Played: {self.game_view.hour} h {self.game_view.minute} min {self.game_view.second} s",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 60,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center")
            arcade.draw_text(f"Score: {int(float(self.game_view.score))}",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 90,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
        elif self.game_view.lives == 0:
            self.game_view.game_state = GameState.GAME_OVER
            arcade.draw_text("Game Over!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                             arcade.color.BLACK, font_size=50, anchor_x="center")
            arcade.draw_text("Press Enter to return",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 30,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
            arcade.draw_text(
                f"Time Played: {self.game_view.hour} h {self.game_view.minute} min {self.game_view.second} s",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 60,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center")
            arcade.draw_text(f"Score: {int(float(self.game_view.score))}",
                             SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2 - 90,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            self.window.show_view(self.game_view)
            self.game_view.game_state = GameState.GAME_STARTED
        elif key == arcade.key.ENTER:  # reset game
            try:
                with open('leaderboard.txt', 'r+') as reader:
                    # Further file processing goes here
                    score = int(float(reader.readline()))
                if score is None:
                    score = 0
            except FileNotFoundError:
                score = 0

            if self.game_view.score > score:
                with open('leaderboard.txt', 'w') as writer:
                    # Further file processing goes here
                    writer.write(str(self.game_view.score))

            menu = MenuView()
            self.game_view.game_state = GameState.GAME_OVER
            self.window.show_view(menu)


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
