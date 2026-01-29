import sys
import pygame
from client import QuoridorClient
from server import QuoridorServer
from actions import MovePawn
from player import HumanPlayer, BotPlayer
from graphics import (
    WIDTH, HEIGHT, CELL_SIZE, RED, BLUE, BLACK,
    draw_board, draw_player
)


def run_server():
    server = QuoridorServer()
    server.run()


def run_client():
    client = QuoridorClient()
    if not client.connect():
        print("Server not found! Run 'python main.py server' first.")
        return

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quoridor Multiplayer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        clock.tick(60)
        board = client.board

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and board.curr_player == client.player_id:
                r, c = board.p1_pawn if client.player_id == 1 else board.p2_pawn
                move = None
                if event.key == pygame.K_UP:
                    move = (r - 1, c)
                elif event.key == pygame.K_DOWN:
                    move = (r + 1, c)
                elif event.key == pygame.K_LEFT:
                    move = (r, c - 1)
                elif event.key == pygame.K_RIGHT:
                    move = (r, c + 1)

                if move and move in board.get_valid_pawn_moves():
                    client.send_action(MovePawn(move[0], move[1]))

        draw_board(screen)

        # Turn Indicator
        turn_color = RED if board.curr_player == 1 else BLUE
        turn_text = f"Player {board.curr_player}'s Turn"
        if board.curr_player == client.player_id:
            turn_text += " (YOU)"

        text_surf = font.render(turn_text, True, turn_color)
        screen.blit(text_surf, (20, HEIGHT - 60))

        # ID Indicator
        id_text = font.render(
            f"You are Player {client.player_id}", True, BLACK)
        screen.blit(id_text, (20, HEIGHT - 30))

        p1_r, p1_c = board.p1_pawn
        draw_player(screen, p1_r, p1_c, HumanPlayer(1))

        p2_r, p2_c = board.p2_pawn
        is_bot = (client.mode == "HUMAN_BOT")
        draw_player(screen, p2_r, p2_c, BotPlayer(2)
                    if is_bot else HumanPlayer(2))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [server|client]")
    elif sys.argv[1].lower() == "server":
        run_server()
    elif sys.argv[1].lower() == "client":
        run_client()
