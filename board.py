from actions import Action, MovePawn, PlaceFence

from igraph import Graph

# TODO: Saving and initializing from a board position
class Board:
    def __init__(self, rows=9, cols=9):
        self.curr_player = 0
        self.is_terminal = False
        self.rows = rows
        self.cols = cols
        self.p1_pawn = (1, (cols + 1) /  2)
        self.p2_pawn = (rows, (cols + 1) / 2)
        self.p1_fences = []
        self.p2_fences = []
        self.fences = []
        self.valid_fence_placements = {
            (x, y, True) for x in range(1, cols) for y in range(1, rows)
        } | {
            (x, y, False) for x in range(1, cols) for y in range(1, rows)
        }

        # Initializing the board's graph representation (to disallow disconnecting fence placement)
        vertices = [(x, y) for x in range(1, cols + 1) for y in range(1, rows + 1)]
        vertex_id = {v: i for i, v in enumerate(vertices)}

        edges = [(vertex_id((i, j)), vertex_id((i + 1, j))) 
                 for i in range(1, cols) for j in range(1, rows + 1)]
        
        edges += [(vertex_id((i, j)), vertex_id((i, j + 1))) 
                 for i in range(1, cols + 1) for j in range(1, rows)]

        self.graph = Graph(edges=edges, directed=False)
        self.graph.vs["name"] = vertices

        # TODO: Should each player's number of remaining fences be tracked here?

    
    def move_pawn(self, x, y):
        if self.curr_player == 1:
            self.p1_pawn = (x, y)
        elif self.curr_player == 2:
            self.p2_pawn == (x, y)
    
    def place_fence(self, x, y, direction):
        if self.curr_player == 1:
            self.p1_fences.append((x, y, direction))
        elif self.curr_player == 2:
            self.p2_fences.append((x, y, direction))
        
        self.fences.append((x, y, direction))

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

    def get_valid_pawn_moves(self) -> set[tuple[int, int]]:
        val_moves = set()
        if self.curr_player == 1:
            x, y = self.p1_pawn
            x_opp, y_opp = self.p2_pawn
        elif self.curr_player == 2:
            x, y = self.p2_pawn
            x_opp, y_opp = self.p1_pawn

        # Potentially allowing move-up/down/left/right respectively
        if not (((x - 1, y, True) in self.fences) 
                or ((x, y, True) in self.fences)):
            val_moves.add((x, y + 1))
        
        if not (((x - 1, y - 1) in self.fences) 
                or ((x, y - 1) in self.fences)):
            val_moves.add((x, y - 1))

        if not (((x - 1, y) in self.fences) 
                or ((x - 1, y - 1) in self.fences)):
            val_moves.add((x - 1, y))
        
        if not (((x, y) in self.fences) 
                or ((x, y - 1) in self.fences)):
            val_moves.add((x + 1, y))
        
        if (x_opp, y_opp) in val_moves:
            val_moves.dicard((x_opp, y_opp))

            # Potentially allowing move-up/down/left/right from opponent respectively
            if not (((x_opp - 1, y_opp, True) in self.fences) 
                    or ((x_opp, y_opp, True) in self.fences)):
                val_moves.add((x_opp, y_opp + 1))
            
            if not (((x_opp - 1, y_opp - 1) in self.fences) 
                    or ((x_opp, y_opp - 1) in self.fences)):
                val_moves.add((x_opp, y_opp - 1))

            if not (((x_opp - 1, y_opp) in self.fences) 
                    or ((x_opp - 1, y_opp - 1) in self.fences)):
                val_moves.add((x_opp - 1, y_opp))
            
            if not (((x_opp, y_opp) in self.fences) 
                    or ((x_opp, y_opp - 1) in self.fences)):
                val_moves.add((x_opp + 1, y_opp))
        

        val_moves = {move for move in val_moves 
                     if (move[0] > 0 and move[0] <= self.cols)}

        return val_moves
    
    def get_valid_fence_placements(self) -> set[tuple[int, int, bool]]:

        # TODO: Ensure the board is not totally divided.
        # Use igraph all_minimal_st_separators to check each separator of size <= 2
        
        seps = self.graph.all_minimal_st_separators()
        two_vertex_seps = []
        one_vertex_seps = []
        for sep in seps:  # sep is a set of vertices
            if len(sep) == 2:
                two_vertex_seps.append(list(map(Board._vertex_id_to_name, sep)))
            elif len(sep) == 1:
                one_vertex_seps.append(Board._vertex_id_to_name(sep.pop()))
        
        two_vertex_seps = [sep for sep in two_vertex_seps 
                           if Board._are_adjacent_cells(sep[0], sep[1])]
        
        # Almost done. This is getting complicated. Maybe check one by one instead.
        

    @staticmethod 
    def _are_adjacent_cells(coord_1, coord_2) -> bool:
        pass

    @staticmethod
    def _vertex_id_to_name(vertex_id: int) -> tuple[int, int]:
        pass

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
        
        # Check if the game has ended.
        if (self.p1_pawn[1] == 10) or (self.p2_pawn[1] == 0):
            self.is_terminal = True
            return
        
        self.curr_player = self.curr_player % 2 + 1