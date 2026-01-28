import pygame

pygame.init()

CELL_SIZE = 60
BOARD_SIZE = 9
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()


def draw_board():
    screen.fill((240, 240, 240))
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)

def draw_players(screen, row, col, color):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)