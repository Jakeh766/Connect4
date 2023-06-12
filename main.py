import numpy as np
import pygame

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = ROW_COUNT * SQUARESIZE + 100
SIZE = (WIDTH,HEIGHT)
RADIUS = int(SQUARESIZE/2-5)

board = np.zeros((ROW_COUNT,COLUMN_COUNT))

def draw_board():
    ...

def is_col_valid(col):
    return board[ROW_COUNT-1][col] == 0

def next_open_row(col):
    for row in range (ROW_COUNT):
        if board [row][col] == 0:
            return row

def print_board():
    print(np.flip(board, 0))

def drop_piece(row,col,piece):
    board[row][col] = piece

def winning_move(piece):
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True

    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column + 1] == piece and board[row][column + 2] == piece and \
                    board[row][column + 3] == piece:
                return True




pygame.init()

screen = pygame.display.set_mode(SIZE)
game_in_progress = True

turn = 0

while game_in_progress:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            game_in_progress = False

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,RED,(posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,WIDTH, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_col_valid(col):
                    row = next_open_row(col)
                    drop_piece(row,col,1)

                    if winning_move(1)





pygame.quit()
