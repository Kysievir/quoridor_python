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

def draw_board(screen):
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

def draw_player(screen, row, col, player):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2

    if player.is_bot:
        color = YELLOW
    else:
        color = RED if player.player_no == 1 else BLUE

    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)

def draw_fence(screen, row, col, direction, player):
    color = RED if player.player_no == 1 else BLUE

    if direction == "H":
        rect = pygame.Rect(
            col * CELL_SIZE,
            row * CELL_SIZE - 5,
            CELL_SIZE * 2,
            10
        )
    else:  # "V"
        rect = pygame.Rect(
            col * CELL_SIZE - 5,
            row * CELL_SIZE,
            10,
            CELL_SIZE * 2
        )

    pygame.draw.rect(screen, color, rect)

#
'''
def draw_ui(screen, players, font):
    y = GRID_SIZE * CELL_SIZE + 10
    for p in players:
        text = f"Player {p.player_no} fences: {p.fences_remaining}"
        color = RED if p.player_no == 1 else BLUE
        label = font.render(text, True, color)
        screen.blit(label, (20 + (p.player_no - 1) * 250, y))
'''

def draw_win(screen, font, winner_id):
    screen.fill(WHITE)
    text = font.render(f"Player {winner_id} wins!", True, BLACK)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)