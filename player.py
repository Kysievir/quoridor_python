from board import Board
from actions import Action

class Player:
    def __init__(self, player_no, name=None):
        self.name = name
        self.player_no = player_no  # Starting from 0, this determines the play order.
        self.fences_remaining = 10
    
    def play(self, board: Board) -> Action:
        pass

class HumanPlayer(Player):
    pass

class BotPlayer(Player):
    pass