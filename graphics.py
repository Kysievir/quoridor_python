from player import BotPlayer
from board import Board

import pygame

GRID_SIZE = 9
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 80  # extra space for UI

WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (50, 80, 220)
YELLOW = (220, 200, 50)
GRAY = (180, 180, 180)


def draw_empty_board(screen):
    screen.fill(WHITE)

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(
            screen, BLACK,
            (0, i * CELL_SIZE),
            (GRID_SIZE * CELL_SIZE, i * CELL_SIZE)
        )
        pygame.draw.line(
            screen, BLACK,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        )


def draw_player(screen, row, col, player_no: int, is_bot: bool):
    x = (col - 1) * CELL_SIZE + CELL_SIZE // 2
    y = (row - 1) * CELL_SIZE + CELL_SIZE // 2

    if is_bot:
        color = YELLOW
    else:
        color = RED if player_no == 1 else BLUE

    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)


def draw_fence(screen, row, col, direction, owner, is_bot=False):
    if owner == 1:
        color = RED
    elif owner == 2 and is_bot:
        color = YELLOW
    else:
        color = BLUE

    # Convert board coords (1–8) → pixel coords
    px = (col - 1) * CELL_SIZE
    py = (row - 1) * CELL_SIZE

    if direction:  # horizontal
        rect = pygame.Rect(
            px,
            py + CELL_SIZE - 5,
            CELL_SIZE * 2,
            10
        )
    else:  # vertical
        rect = pygame.Rect(
            px + CELL_SIZE - 5,
            py,
            10,
            CELL_SIZE * 2
        )

    pygame.draw.rect(screen, color, rect)


def draw_win(screen, font, winner_id):
    screen.fill(WHITE)
    text = font.render(f"Player {winner_id} wins!", True, BLACK)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

def draw_board(board: Board):
    pass