import arcade
import main
import menu
from game_state import GameState


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        if self.game_view.lives != 0:
            arcade.draw_text("PAUSED", main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2 + 50,
                             arcade.color.BLACK, font_size=50, anchor_x="center")

            arcade.draw_text("Press Esc. to return",
                             main.SCREEN_WIDTH / 2,
                             main.SCREEN_HEIGHT / 2,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
            arcade.draw_text("Press Enter to go back to menu",
                             main.SCREEN_WIDTH / 2,
                             main.SCREEN_HEIGHT / 2 - 30,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
            arcade.draw_text(
                f"Time Played: {self.game_view.hour} h {self.game_view.minute} min {self.game_view.second} s",
                main.SCREEN_WIDTH / 2,
                main.SCREEN_HEIGHT / 2 - 60,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center")
            arcade.draw_text(f"Score: {int(float(self.game_view.score))}",
                             main.SCREEN_WIDTH / 2,
                             main.SCREEN_HEIGHT / 2 - 90,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
        elif self.game_view.lives == 0:
            self.game_view.game_state = GameState.GAME_OVER
            arcade.draw_text("Game Over!", main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2 + 50,
                             arcade.color.BLACK, font_size=50, anchor_x="center")
            arcade.draw_text("Press Enter to go back to menu",
                             main.SCREEN_WIDTH / 2,
                             main.SCREEN_HEIGHT / 2 - 30,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")
            arcade.draw_text(
                f"Time Played: {self.game_view.hour} h {self.game_view.minute} min {self.game_view.second} s",
                main.SCREEN_WIDTH / 2,
                main.SCREEN_HEIGHT / 2 - 60,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center")
            arcade.draw_text(f"Score: {int(float(self.game_view.score))}",
                             main.SCREEN_WIDTH / 2,
                             main.SCREEN_HEIGHT / 2 - 90,
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
                    score = int(float(reader.readline()))
                if score is None:
                    score = 0
            except FileNotFoundError:
                score = 0

            if self.game_view.score > score:
                with open('leaderboard.txt', 'w') as writer:
                    writer.write(str(self.game_view.score))

            menux = menu.MenuView()
            self.game_view.game_state = GameState.GAME_OVER
            self.window.show_view(menux)
