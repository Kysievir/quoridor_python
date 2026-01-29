from actions import Action, MovePawn, PlaceFence

from igraph import Graph

# TODO: Saving and initializing from a board position
class Board:
    def __init__(self, rows=9, cols=9):
        self.curr_player = 1
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
            self.p2_pawn = (x, y)
            
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
        x, y = self.p1_pawn if self.curr_player == 1 else self.p2_pawn

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                val_moves.add((nx, ny))
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
            self.move_pawn(action.x, action.y)

        # P1 wins if they reach the last row (index 8)
        # P2 wins if they reach the first row (index 0)
        if (self.p1_pawn[0] == self.rows - 1) or (self.p2_pawn[0] == 0):
            self.is_terminal = True
            return

        self.curr_player = 2 if self.curr_player == 1 else 1
