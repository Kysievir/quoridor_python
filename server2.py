from game import Game
from board import Board

import socket

"""
Features
1. TODO: Use the Game and Player class.
2. TODO: May send 'is_game_ready' to client in addition to 'board'.
3. TODO: Send only actions through network.
4. TODO: Have a time limit for each player and sync it with client every transaction.
"""

# This version will use the Game and Player class.
class Server:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.connections = []

        self.board = Board()
        self.game = None  # Created when there are enough players connected.
    
    def run(self):
        print("Server started. Waiting for players...")
