import socket
import pickle
import threading
import time
import random
from board import Board
from actions import MovePawn


class QuoridorServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.connections = []
        self.board = Board()

        print("Choose game mode:")
        print("1 - Human vs Bot")
        print("2 - Human vs Human")
        choice = input("Enter 1 or 2: ")
        self.mode = "HUMAN_BOT" if choice == "1" else "HUMAN_HUMAN"

    def handle_bot_turn(self):
        if self.board.is_terminal or self.board.curr_player != 2:
            return

        time.sleep(0.5)
        valid_moves = list(self.board.get_valid_pawn_moves())
        if valid_moves:
            move = min(valid_moves, key=lambda m: m[0])
            self.board.update(MovePawn(move[0], move[1]))
            self.broadcast(self.board)

    def handle_client(self, conn, player_id):
        conn.sendall(pickle.dumps({"player_id": player_id, "mode": self.mode}))

        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                action = pickle.loads(data)
                if isinstance(action, MovePawn) and self.board.curr_player == player_id:
                    self.board.update(action)
                    self.broadcast(self.board)

                    if self.mode == "HUMAN_BOT":
                        self.handle_bot_turn()
            except:
                break

        if conn in self.connections:
            self.connections.remove(conn)
        conn.close()

    def broadcast(self, data):
        serialized_data = pickle.dumps(data)
        for conn in self.connections:
            try:
                conn.sendall(serialized_data)
            except:
                continue

    def run(self):
        print(f"Server started ({self.mode}). Waiting for players...")
        needed = 1 if self.mode == "HUMAN_BOT" else 2

        while len(self.connections) < needed:
            conn, addr = self.server.accept()
            p_id = len(self.connections) + 1
            self.connections.append(conn)
            print(f"Player {p_id} connected from {addr}")
            threading.Thread(target=self.handle_client,
                             args=(conn, p_id), daemon=True).start()

        # Sync initial board to all clients
        time.sleep(0.5)
        self.broadcast(self.board)

        while True:
            time.sleep(1)
