from actions import Action, MovePawn, PlaceFence

from igraph import Graph

# TODO: Saving and initializing from a board position


class Board:
    def __init__(self, rows=9, cols=9):
        self.curr_player = 0
        self.is_terminal = False
        self.rows = rows
        self.cols = cols
        self.p1_pawn = (0, 4)
        self.p2_pawn = (8, 4)
        self.p1_fences = []
        self.p2_fences = []
        self.fences = []
        self.valid_fence_placements = {
            (x, y, True) for x in range(1, cols) for y in range(1, rows)
        } | {
            (x, y, False) for x in range(1, cols) for y in range(1, rows)
        }

        # Initializing the board's graph representation (to disallow disconnecting fence placement)
        vertices = [(x, y) for x in range(1, cols + 1)
                    for y in range(1, rows + 1)]
        vertex_id = {v: i for i, v in enumerate(vertices)}
        edges = []  # TODO
        self.graph = Graph(edges=edges, directed=False)

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
            blocked_placements |= {
                (x - 1, y, direction), (x + 1, y, direction)}
        else:
            blocked_placements |= {
                (x, y - 1, direction), (x, y + 1, direction)}

        self.valid_fence_placements -= blocked_placements

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
        # TODO: Get non-blocking fence placements.

        # TODO: Ensure the board is not totally divided.

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
