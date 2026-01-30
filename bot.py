from mcts import MCTS, StateInterface, ActionInterface
from board import Board, BoardState
from actions import Action, MovePawn, PlaceFence
from player import Player

class BotPlayer(Player):
    def __init__(self, player_no, name=None):
        super().__init__(player_no, name)
        self.is_bot = True

    def play(self, board: Board):
        board_state = BoardState(board)
        # TODO: Set an appriopriate iteration_limit.
        mcts = MCTS(time_limit=5)  # time_limit is in seconds
        action = mcts.search(initial_state=board_state)

        return action
    
