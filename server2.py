from game import Game

# This version will use the Game and Player class.
class Server:
     def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.connections = []
        self.board = Board()