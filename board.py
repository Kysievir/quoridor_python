from actions import Action, MovePawn, PlaceFence


class Board:
    def __init__(self, rows=9, cols=9):
        self.curr_player = 1
        self.is_terminal = False
        self.rows = rows
        self.cols = cols
        self.p1_pawn = (0, 4)
        self.p2_pawn = (8, 4)
        self.fences = []

    def move_pawn(self, x, y):
        if self.curr_player == 1:
            self.p1_pawn = (x, y)
        elif self.curr_player == 2:
            self.p2_pawn = (x, y)

    def get_valid_pawn_moves(self) -> set[tuple[int, int]]:
        val_moves = set()
        x, y = self.p1_pawn if self.curr_player == 1 else self.p2_pawn

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                val_moves.add((nx, ny))
        return val_moves

    def update(self, action: Action):
        if isinstance(action, MovePawn):
            self.move_pawn(action.x, action.y)

        # P1 wins if they reach the last row (index 8)
        # P2 wins if they reach the first row (index 0)
        if (self.p1_pawn[0] == self.rows - 1) or (self.p2_pawn[0] == 0):
            self.is_terminal = True
            return

        self.curr_player = 2 if self.curr_player == 1 else 1
