import sys
import pygame
from client import QuoridorClient
from client2 import Client
from server import QuoridorServer
from actions import MovePawn, PlaceFence
from player import HumanPlayer, BotPlayer
from graphics import (
    WIDTH, HEIGHT, CELL_SIZE, RED, BLUE, BLACK,
    draw_board, draw_player, draw_fence
)


def run_server():
    server = QuoridorServer()
    server.run()


def run_client():
    client = Client()
    client.run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|client]")
    elif sys.argv[1].lower() == "server":
        run_server()
    elif sys.argv[1].lower() == "client":
        run_client()
