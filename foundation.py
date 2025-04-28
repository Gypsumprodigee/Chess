import pygame
import sys
import copy

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 700  # Extra space at bottom for text
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
BLACK = (0, 0, 0)

# Set up display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")

# Board setup
board_cordinates = [[' ' for _ in range(8)] for _ in range(8)]
current_turn = "white"
selected_square = None
game_over = False
winner = None

# Initialize the chess board
white_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] + ['P'] * 8
black_pieces = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'] + ['p'] * 8

# Load images
def load_piece_image(name):
    img = pygame.image.load(f'chess_pieces/{name}.png')
    return pygame.transform.scale(img, (64, 64))

piece_images = {
    'K': load_piece_image('white-king'),
    'Q': load_piece_image('white-queen'),
    'R': load_piece_image('white-rook'),
    'B': load_piece_image('white-bishop'),
    'N': load_piece_image('white-knight'),
    'P': load_piece_image('white-pawn'),
    'k': load_piece_image('black-king'),
    'q': load_piece_image('black-queen'),
    'r': load_piece_image('black-rook'),
    'b': load_piece_image('black-bishop'),
    'n': load_piece_image('black-knight'),
    'p': load_piece_image('black-pawn')
}

# Board initialization
for i in range(8):
    board_cordinates[0][i] = black_pieces[i]
    board_cordinates[1][i] = black_pieces[i + 8]
    board_cordinates[6][i] = white_pieces[i + 8]
    board_cordinates[7][i] = white_pieces[i]

# Special states
castling_rights = {'white': {'K': True, 'Q': True}, 'black': {'K': True, 'Q': True}}
en_passant_target = None

# Drawing
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != ' ':
                img = piece_images.get(piece)
                if img:
                    x = col * SQUARE_SIZE + (SQUARE_SIZE - 64) // 2
                    y = row * SQUARE_SIZE + (SQUARE_SIZE - 64) // 2
                    WIN.blit(img, (x, y))

def draw_text(text, y, size=30, color=BLACK):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    WIN.blit(text_surface, text_rect)

# Move checking
def is_path_clear(fr, fc, tr, tc, board):
    dr = tr - fr
    dc = tc - fc
    step_r = (dr > 0) - (dr < 0)
    step_c = (dc > 0) - (dc < 0)
    r, c = fr + step_r, fc + step_c
    while (r, c) != (tr, tc):
        if board[r][c] != ' ':
            return False
        r += step_r
        c += step_c
    return True

def is_valid_move(piece, fr, fc, tr, tc, board):
    if piece == ' ':
        return False

    target = board[tr][tc]
    if (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
        return False

    dr, dc = tr - fr, tc - fc
    direction = 1 if piece.islower() else -1
    piece = piece.lower()

    if piece == 'p':  # Pawn
        if dc == 0 and target == ' ':
            if dr == direction:
                return True
            if (fr == 1 and direction == 1) or (fr == 6 and direction == -1):
                if dr == 2 * direction and board[fr + direction][fc] == ' ':
                    return True
        if abs(dc) == 1 and dr == direction and (target != ' ' or (en_passant_target == (tr, tc))):
            return True
        return False
    elif piece == 'r':
        return (dr == 0 or dc == 0) and is_path_clear(fr, fc, tr, tc, board)
    elif piece == 'b':
        return abs(dr) == abs(dc) and is_path_clear(fr, fc, tr, tc, board)
    elif piece == 'q':
        return (abs(dr) == abs(dc) or dr == 0 or dc == 0) and is_path_clear(fr, fc, tr, tc, board)
    elif piece == 'n':
        return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]
    elif piece == 'k':
        if max(abs(dr), abs(dc)) == 1:
            return True
        if fr == tr and abs(dc) == 2:
            if dc == 2 and castling_rights[current_turn]['K']:
                return is_path_clear(fr, fc, tr, tc - 1, board) and board[fr][7].lower() == 'r'
            if dc == -2 and castling_rights[current_turn]['Q']:
                return is_path_clear(fr, fc, tr, tc + 1, board) and board[fr][0].lower() == 'r'
        return False
    return False

def is_in_check(board, color):
    king = 'K' if color == 'white' else 'k'
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                king_pos = (r, c)
                break
    if not king_pos:
        return True
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if (color == 'white' and piece.islower()) or (color == 'black' and piece.isupper()):
                if is_valid_move(piece, r, c, king_pos[0], king_pos[1], board):
                    return True
    return False

def is_legal_move(board, piece, fr, fc, tr, tc, color):
    temp_board = copy.deepcopy(board)
    temp_board[tr][tc] = temp_board[fr][fc]
    temp_board[fr][fc] = ' '
    return not is_in_check(temp_board, color)

def promote_pawn(board, r, c):
    if r == 0 or r == 7:
        board[r][c] = 'Q' if board[r][c].isupper() else 'q'

def perform_castling(board, fr, fc, tr, tc):
    if abs(fc - tc) == 2:
        if tc == 6:
            board[fr][5] = board[fr][7]
            board[fr][7] = ' '
        elif tc == 2:
            board[fr][3] = board[fr][0]
            board[fr][0] = ' '

def has_legal_moves(board, color):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if (color == 'white' and piece.isupper()) or (color == 'black' and piece.islower()):
                for tr in range(8):
                    for tc in range(8):
                        if is_valid_move(piece, r, c, tr, tc, board):
                            if is_legal_move(board, piece, r, c, tr, tc, color):
                                return True
    return False

def main():
    global selected_square, current_turn, en_passant_target, game_over, winner
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        draw_board()
        draw_pieces(board_cordinates)

        if not game_over:
            draw_text(f"{current_turn.capitalize()}'s Turn", 660, size=30, color=(0, 0, 255))
            if is_in_check(board_cordinates, current_turn):
                draw_text("Check!", 690, size=25, color=(255, 0, 0))
        else:
            if winner == 'draw':
                draw_text("Stalemate - Draw!", 660, size=40, color=(0, 0, 255))
            else:
                draw_text(f"{winner.capitalize()} Wins!", 660, size=40, color=(255, 0, 0))
            draw_text("Press R to Restart", 690, size=30, color=(0, 0, 255))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    restart()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                if y > 640:
                    continue
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                if selected_square is None:
                    piece = board_cordinates[row][col]
                    if piece != ' ' and ((current_turn == 'white' and piece.isupper()) or (current_turn == 'black' and piece.islower())):
                        selected_square = (row, col)
                else:
                    from_row, from_col = selected_square
                    to_row, to_col = row, col
                    piece = board_cordinates[from_row][from_col]

                    if is_valid_move(piece, from_row, from_col, to_row, to_col, board_cordinates):
                        if is_legal_move(board_cordinates, piece, from_row, from_col, to_row, to_col, current_turn):
                            moving_piece = board_cordinates[from_row][from_col]

                            # Handle en passant
                            if moving_piece.lower() == 'p' and (to_row, to_col) == en_passant_target:
                                board_cordinates[from_row][to_col] = ' '

                            # Move
                            board_cordinates[to_row][to_col] = moving_piece
                            board_cordinates[from_row][from_col] = ' '

                            # Castling
                            if moving_piece.lower() == 'k':
                                perform_castling(board_cordinates, from_row, from_col, to_row, to_col)
                                castling_rights[current_turn]['K'] = False
                                castling_rights[current_turn]['Q'] = False

                            # Update castling rights if rook moves
                            if moving_piece.lower() == 'r':
                                if from_col == 0:
                                    castling_rights[current_turn]['Q'] = False
                                if from_col == 7:
                                    castling_rights[current_turn]['K'] = False

                            # Pawn promotion
                            promote_pawn(board_cordinates, to_row, to_col)

                            # Update en passant
                            if moving_piece.lower() == 'p' and abs(to_row - from_row) == 2:
                                en_passant_target = ((from_row + to_row) // 2, from_col)
                            else:
                                en_passant_target = None

                            # Switch turn
                            current_turn = 'black' if current_turn == 'white' else 'white'

                            # Check for end
                            if not has_legal_moves(board_cordinates, current_turn):
                                if is_in_check(board_cordinates, current_turn):
                                    game_over = True
                                    winner = 'white' if current_turn == 'black' else 'black'
                                else:
                                    game_over = True
                                    winner = 'draw'

                    selected_square = None

    pygame.quit()
    sys.exit()

def restart():
    global board_cordinates, current_turn, selected_square, castling_rights, en_passant_target, game_over, winner
    board_cordinates = [[' ' for _ in range(8)] for _ in range(8)]
    current_turn = "white"
    selected_square = None
    castling_rights = {'white': {'K': True, 'Q': True}, 'black': {'K': True, 'Q': True}}
    en_passant_target = None
    game_over = False
    winner = None

    # Initialize again
    for i in range(8):
        board_cordinates[0][i] = black_pieces[i]
        board_cordinates[1][i] = black_pieces[i + 8]
        board_cordinates[6][i] = white_pieces[i + 8]
        board_cordinates[7][i] = white_pieces[i]

if __name__ == "__main__":
    main()
