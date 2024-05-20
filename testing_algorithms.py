import numpy as np
import pygame
import random
import sys

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

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def draw_board(board):
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(column*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(column*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

        for column in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if board[row][column] == 1:
                    pygame.draw.circle(screen, RED, (
                    int(column * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[row][column] == 2:
                    pygame.draw.circle(screen, YELLOW, (
                    int(column * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

def is_col_valid(board,col):
    return board[ROW_COUNT-1][col] == 0

def next_open_row(board,col):
    for row in range (ROW_COUNT):
        if board [row][col] == 0:
            return row

def drop_piece(board,row,col,piece):
    board[row][col] = piece

def winning_move(board,piece):
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True

    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] == piece and \
                    board[row+3][column] == piece:
                return True

    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row+1][column + 1] == piece and board[row+2][column + 2] == piece and \
                    board[row+3][column + 3] == piece:
                return True

    for column in range(COLUMN_COUNT - 3):
        for row in range(3,ROW_COUNT):
            if board[row][column] == piece and board[row-1][column + 1] == piece and board[row-2][column + 2] == piece and \
                    board[row-3][column + 3] == piece:
                return True

def get_valid_locations(board):
    valid_locations =[]
    for col in range(COLUMN_COUNT):
        if is_col_valid(board,col):
            valid_locations.append(col)

    return valid_locations
def generate_random_move():
    return random.choice(valid_locations)


def connect_block(board, piece):
    score = 0
    for col in valid_locations:
        temp_board = board.copy()
        drop_piece(temp_board, next_open_row(board, col), col, piece)
        if winning_move(temp_board, piece):
            return col
        temp_board1= board.copy()
        if piece == 1:
            drop_piece(temp_board1, next_open_row(board,col),col,2)
            if winning_move(temp_board1, 2):
                return col
        else:
            drop_piece(temp_board1, next_open_row(board, col), col, 1)
            if winning_move(temp_board1, 1):
                return col



    return random.choice(valid_locations)



def connect_block_score(board, piece):
    current_score = score_position(board,piece)
    best_score = 0
    best_col = 0
    for col in valid_locations:
        temp_board = board.copy()
        drop_piece(temp_board, next_open_row(board, col), col, piece)
        if winning_move(temp_board, piece):
            return col
        temp_board1 = board.copy()
        if piece == 1:
            drop_piece(temp_board1, next_open_row(board, col), col, 2)
            if winning_move(temp_board1, 2):
                return col
        else:
            drop_piece(temp_board1, next_open_row(board, col), col, 1)
            if winning_move(temp_board1, 1):
                return col
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col


    if best_score <= current_score:
        return random.choice(valid_locations)


    return best_col

def score_position(board, piece):
    score = 0
    center_col = [board[row][COLUMN_COUNT//2] for row in range (len(board))]
    score += center_col.count(piece) * 3

    for row in range(ROW_COUNT):
        row_pieces = [int(i) for i in list(board[row,:])]
        for column in range(COLUMN_COUNT-3):
            score += eval_window(row_pieces[column:column+4],piece)

    for row in range(ROW_COUNT-3):
        for column in range(COLUMN_COUNT-3):
            score += eval_window([board[row+1][column+1] for i in range(4)],piece)

    for row in range(ROW_COUNT-3):
        for column in range(3,COLUMN_COUNT+1):
            score += eval_window([board[row+1][column-1] for i in range(4)],piece)

    for column in range(COLUMN_COUNT):
        col_pieces = [int(i) for i in list(board[:,column])]
        for row in range(ROW_COUNT-3):
            score += eval_window(col_pieces[row:row+4],piece)



    return score


def minimax(board,piece,depth,alpha,beta,maximizing_player):
    valid_locations = get_valid_locations(board)
    if piece == 1:
        opp_piece = 2
    else:
        opp_piece = 1
    if winning_move(board,piece):
        return (None,10000)
    elif winning_move(board,opp_piece):
        return (None,-10000)
    elif len(valid_locations) == 0:
        return (None,0)

    if depth == 0:
        return (None, score_position(board,piece))

    if maximizing_player:
        value = -1000000
        column = valid_locations[0]
        for column in valid_locations:
            row = next_open_row(board,column)
            board_copy=board.copy()
            drop_piece(board_copy,row,column,piece)
            new_score = minimax(board_copy,piece,depth-1,alpha,beta,False)[1]
            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

    else:
        value = 1000000
        column = valid_locations[0]
        for column in valid_locations:
            row = next_open_row(board,column)
            board_copy = board.copy()
            drop_piece(board_copy, row, column, piece)
            new_score = minimax(board_copy, piece, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col

            beta = max(alpha, value)
            if alpha >= beta:
                break



def eval_window(window,piece):
    score = 0
    if window.count(piece) == 4:
        score += 1000

    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 45

    elif window.count(piece) == 2 and window.count(0) == 2:
        score+= 20

    if piece == 1:
        opponent_piece = 2
    else:
        opponent_piece = 1
    if window.count(opponent_piece) ==3 and window.count(0) == 1:
        score -= 35

    return score






def reset_board():
    global board
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))

pygame.init()

myfont = pygame.font.SysFont('arial',75)
screen = pygame.display.set_mode(SIZE)
game_in_progress = True
board = create_board()
# turn = 0
# draw_board()
# pygame.display.update()
player1_wins = 0
player2_wins = 0
player1_starting_wins = 0
player2_starting_wins = 0
tied_games = 0
for i in range(10000):

    if i <= 4999:
        turn = 0
    else:
        turn = 1

    first_turn = True
    while game_in_progress:
    # for event in pygame.event.get():
    #     if event.type == pygame.quit:
    #         game_in_progress = False
    #         sys.exit()
    #
    #     if event.type == pygame.MOUSEMOTION:
    #         pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
    #         posx = event.pos[0]
    #         if turn == 0:
    #             pygame.draw.circle(screen,RED,(posx, int(SQUARESIZE/2)), RADIUS)
    #         else:
    #             pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
    #     pygame.display.update()
    #
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         pygame.draw.rect(screen,BLACK,(0,0,WIDTH, SQUARESIZE))
            if turn == 0:
                valid_locations = get_valid_locations(board)
                if not valid_locations:
                    tied_games += 1
                    game_in_progress = False
                else:
                    # if first_turn:
                    #     col = COLUMN_COUNT//2
                    #     first_turn = False
                    # else:
                        col = connect_block_score(board,1)

                if is_col_valid(board,col):
                    # pygame.time.wait(500)
                    row = next_open_row(board,col)
                    drop_piece(board,row,col,1)

                    if winning_move(board,1):
                        # label = myfont.render("Player 1 wins!",1, RED)
                        # screen.blit(label, (40,10))
                        game_in_progress = False
                        player1_wins += 1
                        if i <= 4999:
                            player1_starting_wins += 1

                    # draw_board()
                    turn = 1

            elif turn == 1:
                # posx = event.pos[0]
                # col = int(posx // SQUARESIZE)
                valid_locations = get_valid_locations(board)
                if not valid_locations:
                    tied_games += 1
                    game_in_progress = False
                else:
                    col = connect_block(board,2)

                if is_col_valid(board,col):
                    # pygame.time.wait(500)
                    row = next_open_row(board,col)
                    drop_piece(board,row, col, 2)

                    if winning_move(board,2):
                        # label = myfont.render("Player 2 wins!", 1, YELLOW)
                        # screen.blit(label, (40, 10))
                        game_in_progress = False
                        player2_wins += 1
                        if i >= 5000:
                            player2_starting_wins += 1

                    turn = 0

                    # draw_board()

    game_in_progress = True
    reset_board()
    i += 1
pygame.quit()

print("Player1 won ",player1_wins," games")
print("Player2 won ",player2_wins," games")
print("There were ",tied_games," tied games")
print("Player1 won","{:.2%}".format(player1_starting_wins/5000),"of the games they started (",player1_starting_wins,"out of 5000)")
print("Player2 won","{:.2%}".format(player2_starting_wins/5000),"of the games they started (",player2_starting_wins,"out of 5000)")