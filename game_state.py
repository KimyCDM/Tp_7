from enum import Enum


class GameState(Enum):
   MAIN_MENU = 0
   OPTION = 1
   GAME_NOT_STARTED = 2
   GAME_STARTED = 3
   GAME_OVER = 4
   PAUSED = 5
   LEADER_BOARD = 6