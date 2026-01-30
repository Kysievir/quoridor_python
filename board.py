from actions import Action, MovePawn, PlaceFence
from igraph import Graph


class Board:
    def __init__(self, rows=9, cols=9, data: dict = None):
        if data is not None:
            self._from_dict(data)
            return

        self.curr_player = 1
        self.is_terminal = False
        self.winner = None
        self.rows = rows
        self.cols = cols

        # P1 starts at bottom (5,1), P2 at top (5,9)
        self.pawns = [((cols + 1) // 2, 1), ((cols + 1) // 2, rows)]
        self.fences = [[], []]
        self.fences_remaining = [10, 10]
        self.fences_flat = []

        self.valid_fence_placements = {
            (x, y, True) for x in range(1, cols) for y in range(1, rows)
        } | {
            (x, y, False) for x in range(1, cols) for y in range(1, rows)
        }

        # Graph setup: Nodes are cells (1,1) through (9,9)
        vertices = [(x, y) for x in range(1, cols + 1)
                    for y in range(1, rows + 1)]
        vertex_id = {v: i for i, v in enumerate(vertices)}
        edges = [(vertex_id[(i, j)], vertex_id[(i + 1, j)])
                 for i in range(1, cols) for j in range(1, rows + 1)]
        edges += [(vertex_id[(i, j)], vertex_id[(i, j + 1)])
                  for i in range(1, cols + 1) for j in range(1, rows)]

        self.graph = Graph(edges=edges, directed=False)
        self.graph.vs["name"] = vertices

    def place_fence(self, x, y, direction):
        if self.curr_player == 1:
            self.fences[0].append((x, y, direction))
        else:
            self.fences[1].append((x, y, direction))

        self.fences_flat.append((x, y, direction))
        self.fences_remaining[self.curr_player - 1] -= 1

        blocked = {(x, y, direction), (x, y, not direction)}
        if direction:  # Horizontal
            blocked |= {(x - 1, y, direction), (x + 1, y, direction)}
            v_pairs = [((x, y), (x, y + 1)), ((x + 1, y), (x + 1, y + 1))]
        else:  # Vertical
            blocked |= {(x, y - 1, direction), (x, y + 1, direction)}
            v_pairs = [((x, y), (x + 1, y)), ((x, y + 1), (x + 1, y + 1))]

        self.valid_fence_placements -= blocked

        for v1, v2 in v_pairs:
            idx1 = self.graph.vs.find(name=v1).index
            idx2 = self.graph.vs.find(name=v2).index
            try:
                eid = self.graph.get_eid(idx1, idx2)
                self.graph.delete_edges(eid)
            except:
                pass

    def get_valid_pawn_moves(self) -> set[tuple[int, int]]:
        x, y = self.pawns[self.curr_player - 1]
        v_idx = self.graph.vs.find(name=(x, y)).index
        neighbors = self.graph.neighbors(v_idx)
        return {self.graph.vs[n]["name"] for n in neighbors}

    def update(self, action: Action) -> bool:
        success = False
        if isinstance(action, MovePawn):
            if (action.x, action.y) in self.get_valid_pawn_moves():
                self.pawns[self.curr_player - 1] = (action.x, action.y)
                success = True
        elif isinstance(action, PlaceFence):
            if (action.x, action.y, action.direction) in self.valid_fence_placements:
                self.place_fence(action.x, action.y, action.direction)
                success = True

        if success:
            if self.pawns[0][1] == self.rows:
                self.winner, self.is_terminal = 1, True
            elif self.pawns[1][1] == 1:
                self.winner, self.is_terminal = 2, True
            else:
                self.curr_player = self.curr_player % 2 + 1
            return True
        return False
