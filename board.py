from actions import Action, MovePawn, PlaceFence
from mcts import StateInterface

from igraph import Graph

# TODO: Saving and initializing from a board position
class Board:
    def __init__(self, rows=9, cols=9):
        self.curr_player = 1
        self.is_terminal = False
        self.winner = None
        self.rows = rows
        self.cols = cols

        # TODO: Combine p1/p2 properties to one.
        self.p1_pawn = (1, (cols + 1) /  2)
        self.p2_pawn = (rows, (cols + 1) / 2)
        self.p1_fences = []
        self.p2_fences = []

        self.pawns = [(1, (cols + 1) /  2), (rows, (cols + 1) / 2)]
        self.fences = [[], []]

        self.fences_remaining = [10, 10]  # fences remaining for player 1, 2
        self.fences_flat = []
        self.valid_fence_placements = {
            (x, y, True) for x in range(1, cols) for y in range(1, rows)
        } | {
            (x, y, False) for x in range(1, cols) for y in range(1, rows)
        }

        # Initializing the board's graph representation (to disallow disconnecting fence placement)
        vertices = [(x, y) for x in range(1, cols + 1) for y in range(1, rows + 1)]
        vertex_id = {v: i for i, v in enumerate(vertices)}

        edges = [(vertex_id[(i, j)], vertex_id[(i + 1, j)]) 
                 for i in range(1, cols) for j in range(1, rows + 1)]
        
        edges += [(vertex_id[(i, j)], vertex_id[(i, j + 1)]) 
                 for i in range(1, cols + 1) for j in range(1, rows)]

        self.graph = Graph(edges=edges, directed=False)
        self.graph.vs["name"] = vertices

        # TODO: Should each player's number of remaining fences be tracked here?

    
    def move_pawn(self, x, y):
        """Cannot handle invalid moves, which should've been checked."""
        # TODO: Remove this
        if self.curr_player == 1:
            self.p1_pawn = (x, y)
        elif self.curr_player == 2:
            self.p2_pawn = (x, y)
        
        self.pawns[self.curr_player - 1] = (x, y)

    def place_fence(self, x, y, direction):
        """Cannot handle invalid placements, which should've been checked."""
        if self.curr_player == 1:
            self.fences[0].append((x, y, direction))
        elif self.curr_player == 2:
            self.fences[1].append((x, y, direction))
        
        self.fences_flat.append((x, y, direction))
        self.fences_remaining[self.curr_player - 1] -= 1

        blocked_placements = {(x, y, direction), (x, y, ~direction)}
        if direction:
            blocked_placements |= {(x - 1, y, direction), (x + 1, y, direction)}
        else:
            blocked_placements |= {(x, y - 1, direction), (x, y + 1, direction)}

        self.valid_fence_placements -= blocked_placements
        if direction:
            self.graph.delete_edges([
                (self.graph.vs.find(name=(x, y)),
                 self.graph.vs.find(name=(x, y + 1))),
                (self.graph.vs.find(name=(x + 1, y)),
                 self.graph.vs.find(name=(x + 1, y + 1)))
            ])
        
        self._discard_disconnecting_fences()

    def _discard_disconnecting_fences(self):

        for placement in self.valid_fence_placements:
            graph_copy = self.graph.copy()
            x, y, dir = placement
            if dir:
                graph_copy.delete_edges([
                    (graph_copy.vs.find(name=(x, y)),
                     graph_copy.vs.find(name=(x, y + 1))),
                    (graph_copy.vs.find(name=(x + 1, y)),
                     graph_copy.vs.find(name=(x + 1, y + 1)))
                ])
            else:
                graph_copy.delete_edges([
                    (graph_copy.vs.find(name=(x, y)),
                     graph_copy.vs.find(name=(x + 1, y))),
                    (graph_copy.vs.find(name=(x, y + 1)),
                     graph_copy.vs.find(name=(x + 1, y + 1)))
                ])
            
            final_y = 10 if self.curr_player == 1 else 0
            components = graph_copy.connected_components(mode="weak")
            membership = components.membership
            pawn_membership = membership[graph_copy.vs.find(name=self.pawns[self.curr_player - 1])]

            # Check that at least one final position is reachable, ie in the same connected component as the pawn.
            if not any((membership[graph_copy.vs.find(name=(x, final_y))] == pawn_membership
                        for x in range(1, 10))):
                self.valid_fence_placements.discard(placement)
            
        # # An alternative method with igraph all_minimal_st_separators
        # # It should be faster, but finding the corresponding fences gets too complicated.
        # seps = self.graph.all_minimal_st_separators()
        # two_vertex_seps = []
        # one_vertex_seps = []
        # for sep in seps:  # sep is a set of vertices
        #     if len(sep) == 2:
        #         two_vertex_seps.append(list(map(Board._vertex_id_to_name, sep)))
        #     elif len(sep) == 1:
        #         one_vertex_seps.append(Board._vertex_id_to_name(sep.pop()))
        
        # two_vertex_seps = [sep for sep in two_vertex_seps 
        #                    if Board._are_adjacent_cells(sep[0], sep[1])]
        # STILL NOT WORKING

    def get_valid_pawn_moves(self) -> set[tuple[int, int]]:
        val_moves = set()
        if self.curr_player == 1:
            x, y = self.pawns[0]
            x_opp, y_opp = self.pawns[1]
        elif self.curr_player == 2:
            x, y = self.pawns[0]
            x_opp, y_opp = self.pawns[1]

        # Potentially allowing move-up/down/left/right respectively
        if not (((x - 1, y, True) in self.fences_flat) 
                or ((x, y, True) in self.fences_flat)):
            val_moves.add((x, y + 1))
        
        if not (((x - 1, y - 1, True) in self.fences_flat) 
                or ((x, y - 1, True) in self.fences_flat)):
            val_moves.add((x, y - 1))

        if not (((x - 1, y, False) in self.fences_flat) 
                or ((x - 1, y - 1, False) in self.fences_flat)):
            val_moves.add((x - 1, y))
        
        if not (((x, y, False) in self.fences_flat) 
                or ((x, y - 1, False) in self.fences_flat)):
            val_moves.add((x + 1, y))
        
        if (x_opp, y_opp) in val_moves:
            val_moves.dicard((x_opp, y_opp))

            # Potentially allowing move-up/down/left/right from opponent respectively
            if not (((x_opp - 1, y_opp, True) in self.fences_flat) 
                    or ((x_opp, y_opp, True) in self.fences_flat)):
                val_moves.add((x_opp, y_opp + 1))
            
            if not (((x_opp - 1, y_opp - 1, True) in self.fences_flat) 
                    or ((x_opp, y_opp - 1, True) in self.fences_flat)):
                val_moves.add((x_opp, y_opp - 1))

            if not (((x_opp - 1, y_opp, False) in self.fences_flat) 
                    or ((x_opp - 1, y_opp - 1, False) in self.fences_flat)):
                val_moves.add((x_opp - 1, y_opp))
            
            if not (((x_opp, y_opp, False) in self.fences_flat) 
                    or ((x_opp, y_opp - 1, False) in self.fences_flat)):
                val_moves.add((x_opp + 1, y_opp))
        

        val_moves = {move for move in val_moves 
                     if (move[0] > 0 and move[0] <= self.cols)}
        
        return val_moves

    def get_valid_fence_placements(self) -> set[tuple[int, int, bool]]:
        if self.fences_remaining[self.curr_player - 1] > 0:
            return self.valid_fence_placements
        else:
            return set()

    def update(self, action: Action):
        if isinstance(action, MovePawn):
            x = action.x
            y = action.y
            if (x, y) not in self.get_valid_pawn_moves():
                raise ValueError("Invalid pawn move")
            
            self.move_pawn(x, y)

        elif isinstance(action, PlaceFence):
            x = action.x
            y = action.y
            direction = action.direction
            if (x, y, direction) not in self.get_valid_fence_placements():
                raise ValueError("Invalid fence placement")
            
            self.place_fence(action.x, action.y, action.direction)
        

        # P1 wins if they reach the last row (index 10 normally)
        # P2 wins if they reach the first row (index 0 normally)
        if (self.pawns[0][0] == self.rows + 1):
            self.winner = 1
            self.is_terminal = True
        elif self.pawns[1][0] == 0:
            self.winner = 2
            self.is_terminal = True
        else:
            self.curr_player = self.curr_player % 2 + 1

# Wrapper class for MCTS integration
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
        if self.is_terminal():
            return 1 if self.board.winner == 1 else -1
        else:
            return 0