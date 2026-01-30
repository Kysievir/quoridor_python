from board import Board
from actions import MovePawn, PlaceFence
from graphics import (
    WIDTH, HEIGHT, CELL_SIZE, RED, BLUE, BLACK,
    draw_empty_board, draw_player, draw_fence, convert_coord
)

import pygame
import socket
import threading
import pickle

# Maybe a Home page to select mode instead of doing it in the terminal.
class Client:
    def __init__(self, host='127.0.0.1', port=5556):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.board = Board()
        self.player_id = None
        self.mode = None
        self.connected = False

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quoridor Multiplayer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            threading.Thread(target=self._listen, daemon=True).start()
            return True
        except:
            return False
    
    def _listen(self):
        while True:
            try:
                data = self.socket.recv(4096)
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
            self.connected = False

    def run(self):
        if not self.connect():
            print("Server not found! Run 'python main.py server' first.")
            return

        running = True
        while running:
            self.clock.tick(60)
            board = self.board  # _listen should update the board here if server sends any update.

            draw_empty_board(self.screen)

            # Draw player 1 fences
            for (x, y, direction) in board.fences[0]:
                draw_fence(self.screen, x, y, direction, owner=1)

            # Draw player 2 fences
            for (x, y, direction) in board.fences[1]:
                draw_fence(
                    self.screen,
                    x, y,
                    direction,
                    owner=2,
                    is_bot=(self.mode == "HUMAN_BOT"))
            
            #draw_fence(screen, 3, 5, True, owner=1)


            # Turn Indicator
            turn_color = RED if board.curr_player == 1 else BLUE
            turn_text = f"Player {board.curr_player}'s Turn"
            if board.curr_player == self.player_id:
                turn_text += " (YOU)"

            text_surf = self.font.render(turn_text, True, turn_color)
            self.screen.blit(text_surf, (20, HEIGHT - 60))

            # ID Indicator
            id_text = self.font.render(
                f"You are Player {self.player_id}", True, BLACK)
            self.screen.blit(id_text, (20, HEIGHT - 30))

            p1_x, p1_y = board.pawns[0]
            draw_player(self.screen, p1_x, p1_y, 1, False)

            p2_x, p2_y = board.pawns[1]
            is_bot = (self.mode == "HUMAN_BOT")
            draw_player(self.screen, p2_x, p2_y, 2, is_bot)

            pygame.display.flip()

            if board.is_terminal:
                from graphics import draw_win
                draw_win(self.screen, self.font, board.winner)
                pygame.display.flip()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("MOUSE CLICK DETECTED")

                if event.type == pygame.KEYDOWN and board.curr_player == self.player_id:
                    x, y = board.pawns[self.player_id - 1]
                    move = None
                    if event.key == pygame.K_UP:
                        move = (x, y + 1) 
                    elif event.key == pygame.K_DOWN:
                        move = (x, y - 1)
                    elif event.key == pygame.K_LEFT:
                        move = (x - 1, y)
                    elif event.key == pygame.K_RIGHT:
                        move = (x + 1, y)

                    if move and move in board.get_valid_pawn_moves():
                        self.send_action(MovePawn(move[0], move[1]))
                        
                elif event.type == pygame.MOUSEBUTTONDOWN and board.curr_player == self.player_id:
                    print("MY TURN, MOUSE CLICK")
                    mx, my = event.pos

                    cell_x = mx // CELL_SIZE
                    cell_y = my // CELL_SIZE

                    cell_x, cell_y = convert_coord(cell_x, cell_y)

                    offset_x = mx % CELL_SIZE
                    offset_y = my % CELL_SIZE

                    SNAP_MARGIN = 10  # pixels near border

                    direction = None
                    y = x = None

                    # Near horizontal border → horizontal fence
                    if offset_y < SNAP_MARGIN:
                        direction = True   # horizontal
                        y = cell_y
                        x = cell_x

                    # Near vertical border → vertical fence
                    elif offset_x < SNAP_MARGIN:
                        direction = False  # vertical
                        y = cell_y
                        x = cell_x

                    # if direction is not None:
                    #     # board is 1-indexed
                    #     row += 1
                    #     col += 1

                    # Fence positions are only valid in 1..8 TODO: Use get_valid instead.
                    if direction is not None:
                        if 1 <= x <= 8 and 1 <= y <= 8:
                            self.send_action(PlaceFence(x, y, direction))
                            print(f"Placing fence {(x, y, direction)}")

        pygame.quit()