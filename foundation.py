import pygame
import sys
# Chess board representation (2D array or 8x8 grid)
board_cordinates = [[' ' for _ in range(8)] for _ in range(8)]

# Initialize the chess board with pieces
white_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',  # major pieces
                'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']  # pawns

black_pieces = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',  # major pieces
                'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']  # pawns
black_queen = pygame.image.load('chess_pieces/black-queen.png')
black_queen = pygame.transform.scale(black_queen, (64, 64))
black_king = pygame.image.load('chess_pieces/black-king.png')
black_king = pygame.transform.scale(black_king, (64, 64))
black_rook = pygame.image.load('chess_pieces/black-rook.png')  
black_rook = pygame.transform.scale(black_rook, (64, 64)) 
black_knight = pygame.image.load('chess_pieces/black-knight.png')
black_knight = pygame.transform.scale(black_knight, (64, 64))
black_bishop = pygame.image.load('chess_pieces/black-bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (64, 64))
black_pawn = pygame.image.load('chess_pieces/black-pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (64, 64))
white_queen = pygame.image.load('chess_pieces/white-queen.png')
white_queen = pygame.transform.scale(white_queen, (64, 64))
white_king = pygame.image.load('chess_pieces/white-king.png')
white_king = pygame.transform.scale(white_king, (64, 64))
white_rook = pygame.image.load('chess_pieces/white-rook.png')
white_rook = pygame.transform.scale(white_rook, (64, 64))
white_knight = pygame.image.load('chess_pieces/white-knight.png')
white_knight = pygame.transform.scale(white_knight, (64, 64))
white_bishop = pygame.image.load('chess_pieces/white-bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (64, 64))
white_pawn = pygame.image.load('chess_pieces/white-pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (64, 64))
piece_images = {
    'K': white_king,
    'Q': white_queen,
    'R': white_rook,
    'B': white_bishop,
    'N': white_knight,
    'P': white_pawn,
    'k': black_king,
    'q': black_queen,
    'r': black_rook,
    'b': black_bishop,
    'n': black_knight,
    'p': black_pawn
}
selected_square = None  # Variable to track the selected square
# Place black pieces (rows 0 & 1)
for i in range(8):
    board_cordinates[0][i] = black_pieces[i]      # row 0: back rank
    board_cordinates[1][i] = black_pieces[i + 8]  # row 1: pawns

# Place white pieces (rows 6 & 7)
for i in range(8):
    board_cordinates[6][i] = white_pieces[i + 8]  # row 6: pawns
    board_cordinates[7][i] = white_pieces[i]      # row 7: back rank

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
BLACK = (0, 0, 0)

# Set up display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")

# Load font for piece rendering
FONT = pygame.font.SysFont("arial", 36)

# Draw board squares
def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces
def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != ' ':
                piece_image = piece_images.get(piece)
                if piece_image:
                    x = col * SQUARE_SIZE + (SQUARE_SIZE - 64) // 2
                    y = row * SQUARE_SIZE + (SQUARE_SIZE - 64) // 2

                    win.blit(piece_image, (x, y))
# Main game loop
def main():
    global selected_square
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        draw_board(WIN)
        draw_pieces(WIN, board_cordinates)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                if selected_square is None:
                    # First click: select the piece
                    if board_cordinates[row][col] != ' ':
                        selected_square = (row, col)
                else:
                    # Second click: move the piece
                    from_row, from_col = selected_square
                    to_row, to_col = row, col

                    # Basic move (no rules, no turn control)
                    board_cordinates[to_row][to_col] = board_cordinates[from_row][from_col]
                    board_cordinates[from_row][from_col] = ' '

                    selected_square = None
    pygame.quit()
    sys.exit()


main()