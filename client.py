import socket
import pickle
import threading
from board import Board


class QuoridorClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = Board()
        self.player_id = None
        self.mode = None
        self.connected = False

    def connect(self):
        try:
            self.socket.connect(('127.0.0.1', 5555))
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
