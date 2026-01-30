import socket
import pickle
import threading
import time
from board import Board
from actions import MovePawn, PlaceFence


class QuoridorServer:
    def __init__(self, host='0.0.0.0', port=5556):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.connections = []
        self.board = Board()
        self.mode = "HUMAN_HUMAN"

    def handle_client(self, conn, player_id):
        conn.sendall(pickle.dumps({"player_id": player_id, "mode": self.mode}))
        while True:
            try:
                data = conn.recv(8192)
                if not data:
                    break
                action = pickle.loads(data)
                if self.board.curr_player == player_id and not self.board.is_terminal:
                    if self.board.update(action):
                        self.broadcast(self.board)
            except:
                break
        conn.close()

    def broadcast(self, data):
        serialized = pickle.dumps(data)
        for conn in self.connections:
            try:
                conn.sendall(serialized)
            except:
                continue

    def run(self):
        print("Server waiting for 2 players...")
        while len(self.connections) < 2:
            conn, addr = self.server.accept()
            p_id = len(self.connections) + 1
            self.connections.append(conn)
            threading.Thread(target=self.handle_client,
                             args=(conn, p_id), daemon=True).start()

        time.sleep(1)
        self.broadcast(self.board)
        while True:
            time.sleep(1)
