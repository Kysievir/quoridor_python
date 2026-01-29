from board import Board
from actions import Action
import socket

# These classes are intended for the server only.

class Player:
    def __init__(self, player_no, name=None):
        self.name = name
        # Starting from 0, this determines the play order.
        self.player_no = player_no

    def play(self, board: Board) -> Action:
        pass


class HumanPlayer(Player):
    def __init__(self, conn: socket.socket, player_no, name=None):
        super().__init__(player_no, name)
        self.is_bot = False
        self.conn = conn
        self.conn.settimeout(None)  # TODO: Add a time limit.
    
    def play(self, board: Board) -> Action:
        pass


class BotPlayer(Player):
    def __init__(self, player_no, name=None):
        super().__init__(player_no, name)
        self.is_bot = True
