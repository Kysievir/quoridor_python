from mcts import MCTS, StateInterface, ActionInterface
from board import Board
from actions import Action, MovePawn, PlaceFence

class BoardWrapper(StateInterface):
    def __init__(self, board: Board):
        self.board = board
    
    def get_current_player(self) -> int:
        return 1 if self.board.curr_player == 1 else -1
    
    def get_possible_actions(self) -> list[Action]:
        actions = []
        actions += [MovePawn(x, y) 
                    for x, y in self.board.get_valid_pawn_moves()]
        actions += [PlaceFence(x, y, dir) 
                    for x, y, dir in self.board.get_valid_fence_placements()]
        return actions

    def take_action(self, action: Action):
        self.board.update(action)

    def is_terminal(self):
        return self.board.is_terminal

    def get_reward(self):
        # only needed for terminal states
        raise NotImplementedError()
    
