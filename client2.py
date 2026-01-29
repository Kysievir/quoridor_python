from board import Board

import socket

# Maybe a Home page to select mode instead of doing it in the terminal.
class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = Board()
        self.player_id = None
        self.mode = None
        self.connected = False