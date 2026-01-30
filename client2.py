import pygame
import socket
import threading
import pickle
from board import Board
from actions import MovePawn, PlaceFence
from graphics import (
    WIDTH, HEIGHT, CELL_SIZE, RED, BLUE, BLACK, WHITE,
    draw_empty_board, draw_player, draw_fence, convert_coord, draw_win
)


class Client:
    def __init__(self, host='127.0.0.1', port=5556):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host, self.port = host, port
        self.board = Board()
        self.player_id, self.mode = None, None
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            threading.Thread(target=self._listen, daemon=True).start()
            return True
        except:
            return False

    def _listen(self):
        while True:
            try:
                data = self.socket.recv(8192)
                if not data:
                    break
                obj = pickle.loads(data)
                if isinstance(obj, Board):
                    self.board = obj
                elif isinstance(obj, dict):
                    self.player_id = obj.get("player_id")
                    self.mode = obj.get("mode")
            except:
                break

    def send_action(self, action):
        try:
            self.socket.send(pickle.dumps(action))
        except:
            pass

    def run(self):
        if not self.connect():
            return

        running = True
        while running:
            self.clock.tick(60)
            board = self.board
            draw_empty_board(self.screen)

            # 1. DRAW PLACED FENCES AND PAWNS
            for i, p_fences in enumerate(board.fences):
                for f in p_fences:
                    draw_fence(self.screen, f[0], f[1], f[2], owner=i+1)
            for i, (px, py) in enumerate(board.pawns):
                draw_player(self.screen, px, py, i+1, False)

            # 2. PREVIEW LOGIC (The "Hover" effect)
            if not board.is_terminal and board.curr_player == self.player_id:
                mx, my = pygame.mouse.get_pos()
                # Determine board coordinates from mouse
                bx, by = mx // CELL_SIZE + 1, 9 - (my // CELL_SIZE)

                # Snap Margin to check if mouse is near an intersection
                SNAP = 15
                preview_dir = None
                if mx % CELL_SIZE < SNAP:
                    preview_dir = False  # Vertical Hover
                elif my % CELL_SIZE < SNAP:
                    preview_dir = True  # Horizontal Hover

                # If near intersection and valid, draw preview
                if preview_dir is not None and (bx if preview_dir else bx-1, by, preview_dir) in board.valid_fence_placements:
                    from graphics import draw_fence_preview
                    # Adjust coordinates for the preview draw function
                    draw_fence_preview(
                        self.screen, bx if preview_dir else bx-1, by, preview_dir)

            # 3. WIN SCREEN
            if board.is_terminal:
                draw_win(self.screen, self.font, board.winner)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                continue

            # 4. TURN INFO AND EVENT HANDLING
            turn_msg = f"Player {board.curr_player}'s Turn" + \
                (" (YOU)" if board.curr_player == self.player_id else "")
            self.screen.blit(self.font.render(
                turn_msg, True, BLACK), (20, HEIGHT - 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if board.curr_player != self.player_id:
                    continue

                # Movement (Keyboard)
                if event.type == pygame.KEYDOWN:
                    x, y = board.pawns[self.player_id - 1]
                    moves = {pygame.K_UP: (x, y+1), pygame.K_DOWN: (x, y-1),
                             pygame.K_LEFT: (x-1, y), pygame.K_RIGHT: (x+1, y)}
                    if event.key in moves:
                        self.send_action(MovePawn(*moves[event.key]))

                # Build Fence (Click)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    bx, by = mx // CELL_SIZE + 1, 9 - (my // CELL_SIZE)
                    if mx % CELL_SIZE < SNAP:
                        self.send_action(PlaceFence(bx-1, by, False))
                    elif my % CELL_SIZE < SNAP:
                        self.send_action(PlaceFence(bx, by, True))

        pygame.quit()
