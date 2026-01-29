import sys
import pygame
from client import QuoridorClient
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

        if board.is_terminal:
            from graphics import draw_win
            draw_win(screen, font, board.winner)
            pygame.display.flip()
            continue


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSE CLICK DETECTED")

            if event.type == pygame.KEYDOWN and board.curr_player == client.player_id:
                r, c = board.pawns[client.player_id - 1]
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
                    
            if event.type == pygame.MOUSEBUTTONDOWN and board.curr_player == client.player_id:
                print("MY TURN, MOUSE CLICK")
                mx, my = event.pos

                cell_x = mx // CELL_SIZE
                cell_y = my // CELL_SIZE

                offset_x = mx % CELL_SIZE
                offset_y = my % CELL_SIZE

                SNAP_MARGIN = 10  # pixels near border

                direction = None
                row = col = None

                # Near horizontal border → horizontal fence
                if offset_y < SNAP_MARGIN:
                    direction = True   # horizontal
                    row = cell_y
                    col = cell_x

                # Near vertical border → vertical fence
                elif offset_x < SNAP_MARGIN:
                    direction = False  # vertical
                    row = cell_y
                    col = cell_x

                if direction is not None:
                    # board is 1-indexed
                    row += 1
                    col += 1

                    # Fence positions are only valid in 1..8
                    if 1 <= row <= 8 and 1 <= col <= 8:
                        client.send_action(PlaceFence(row, col, direction))



        draw_board(screen)

        # Draw player 1 fences
        for (x, y, direction) in board.fences[0]:
            draw_fence(screen, x, y, direction, owner=1)

        # Draw player 2 fences
        for (x, y, direction) in board.fences[1]:
            draw_fence(
                screen,
                x, y,
                direction,
                owner=2,
                is_bot=(client.mode == "HUMAN_BOT"))
        
        #draw_fence(screen, 3, 5, True, owner=1)


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

        p1_r, p1_c = board.pawns[0]
        draw_player(screen, p1_r, p1_c, HumanPlayer(1))

        p2_r, p2_c = board.pawns[1]
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
