import pygame
from board import Board
from actions import MovePawn, PlaceFence
from player import HumanPlayer, BotPlayer
from game import Game

from graphics import (
    WIDTH, HEIGHT, CELL_SIZE,
    draw_board, draw_player,
    draw_fence, draw_win
)

def choose_game_mode():
    print("Choose game mode:")
    print("1 - Human vs Human")
    print("2 - Human vs Bot")

    while True:
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            return "HUMAN_HUMAN"
        elif choice == "2":
            return "HUMAN_BOT"

def main():
    mode = choose_game_mode()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quoridor")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    if mode == "HUMAN_HUMAN":
        players = [HumanPlayer(1), HumanPlayer(2)]
    else:
        players = [HumanPlayer(1), BotPlayer(2)]

    game = Game(players)
    board = game.board

    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse = place fence
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col = mx // CELL_SIZE
                row = my // CELL_SIZE
                direction = "H" if event.button == 1 else "V"
                #game.handle_action(PlaceFence(row, col, direction))

        # Keyboard = move pawn
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.handle_action(MovePawn(-1, 0))
        elif keys[pygame.K_DOWN]:
            game.handle_action(MovePawn(1, 0))
        elif keys[pygame.K_LEFT]:
            game.handle_action(MovePawn(0, -1))
        elif keys[pygame.K_RIGHT]:
            game.handle_action(MovePawn(0, 1))
        '''
        # handle_action does not exist
            
        draw_board(screen)

        # Draw pawns
        r, c = board.p1_pawn
        draw_player(screen, r, c, players[0])

        r, c = board.p2_pawn
        draw_player(screen, r, c, players[1])

        # Draw fences
        '''
        for fence in board.fences:
            row, col, direction, player = fence
            draw_fence(screen, row, col, direction, player)
        '''

        #draw_ui(screen, players, font)

        # Win check (check_winner() doesn't exist)
        '''
        winner = board.check_winner()
        if winner:
            draw_win(screen, font, winner)
            pygame.display.flip()
            pygame.time.wait(3000)
            break
        '''

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()