from board import Board
from player import Player
from actions import PlaceFence

class Game:
    def __init__(self, players: list[Player], rows=9, cols=9):
        self.players = players
        self.num_players = 2  # This is fixed for now.
        self.board = Board(rows, cols)
    
    def run(self) -> int:
        curr_player_no = 1
        while not self.board.is_terminal:
            player = self.players[curr_player_no - 1]
            action = player.play(self.board)
            self.board.update(action)

            curr_player_no = curr_player_no % 2 + 1
        
        return self.board.winner
