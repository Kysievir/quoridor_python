from actions import Action, MovePawn, PlaceFence

# TODO: Saving and initializing from a board position
class Board:
    def __init__(self, rows=9, cols=9):
        self.curr_player = 0
        self.is_terminal = False
        self.rows = rows
        self.cols = cols
        self.p1_pawn = (1, 5)
        self.p2_pawn = (9, 5)
        self.p1_fences = []
        self.p2_fences = []
        self.fences = []

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

    def get_valid_pawn_moves(self) -> set[tuple[int, int]]:
        val_moves = set()
        if self.curr_player == 1:
            x, y = self.p1_pawn

            # 1. Move-up
            if not (((x - 1, y, True) in self.fences) or ((x, y, True) in self.fences)):
                val_moves.add((x, y + 1))
            
            # 2. Move-down
            if not (((x - 1, y - 1) in self.fences) or ((x, y - 1) in self.fences)):
                val_moves.add((x, y - 1))
            
            # TODO: Move-left, move-right
            # TODO: Consider blockage by player and jumping moves.

        return val_moves
    
    def get_valid_fence_placements(self) -> set[tuple[int, int, bool]]:
        val_placements = set()
        # TODO: Get non-blocking fence placements.
        # TODO: Ensure the board is not totally divided.
        
        return val_placements

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