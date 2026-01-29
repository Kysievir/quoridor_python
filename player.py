from board import Board
from actions import Action


class Player:
    def __init__(self, player_no, name=None):
        self.name = name
        # Starting from 0, this determines the play order.
        self.player_no = player_no
        self.fences_remaining = 10

    def play(self, board: Board) -> Action:
        pass


class HumanPlayer(Player):
    def __init__(self, player_no, name=None):
        super().__init__(player_no, name)
        self.is_bot = False


class BotPlayer(Player):
    def __init__(self, player_no, name=None):
        super().__init__(player_no, name)
        self.is_bot = True
