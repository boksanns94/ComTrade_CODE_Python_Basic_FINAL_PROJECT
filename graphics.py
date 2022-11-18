"""
Definitions of all functions that will be handling the gui.
Loading of necessary images used in the gui.
"""


import pygame
import piece
import board as brd
import globals as glb


eat_img = pygame.image.load("images/eat.png")
spec_img = pygame.image.load("images/spec.png")
move_img = pygame.image.load("images/move.png")
w_checkmate_img = pygame.image.load("images/w_checkmate.png")
b_checkmate_img = pygame.image.load("images/b_checkmate.png")
stalemate_img = pygame.image.load("images/stalemate.png")


def get_clicked_square():
    """
    Returns the row and column of a clicked square.
    :return: Tuple
    """
    mouse_position = pygame.mouse.get_pos()
    i = mouse_position[0] // glb.SQUAREWIDTH
    j = mouse_position[1] // glb.SQUAREWIDTH
    if i == 8:
        i = 7
    if j == 8:
        j = 7
    return i, j


def fill_color(win, square, color=None):
    """
    Fills the background of a single square.
    :param win: pygame.Surface
    :param square: square.Square
    :param color: Tuple
    :return: None
    """
    if not color:
        color = square.color
    pygame.draw.rect(win, color, square.rect)


def fill_image(win, square, image=None):
    """
    Places an image inside of a single square.
    :param win: pygame.Surface
    :param square: square.Square
    :param image: pygame.Surface
    :return: None
    """
    if not image:
        if square.piece:
            win.blit(square.piece.image, (square.x, square.y))
    else:
        win.blit(image, (square.x, square.y))


def draw_square(win, square):
    """
    Fills the background and places an image of a single square.
    :param win: pygame.Surface
    :param square: square.Square
    :return: None
    """
    color = None
    image = None

    if square.selected_piece or square.former_move:
        color = glb.SELECTED
    fill_color(win, square, color)

    if square.regular_move:
        image = move_img
    if square.special_move:
        image = spec_img
    if square.eat_move:
        image = eat_img
    fill_image(win, square, image)

    if square.piece:
        fill_image(win, square)


def draw_lines(win):
    """
    Draws all vertical and horizontal lines between squares.
    :param win: pygame.Surface
    :return: None
    """
    for i in range(9):
        pygame.draw.line(win, glb.BLACK, (0, i * glb.SQUAREWIDTH), (glb.BOARDWIDTH, i * glb.SQUAREWIDTH))
        for j in range(9):
            pygame.draw.line(win, glb.BLACK, (j * glb.SQUAREWIDTH, 0), (j * glb.SQUAREWIDTH, glb.BOARDWIDTH))


def draw_chessboard(win, chessboard):
    """
    Draws the entire state of the chessboard.
    :param win: pygame.Surface
    :param chessboard: Dict
    :return: None
    """
    for row in range(8):
        for col in range(8):
            draw_square(win, chessboard[(row, col)])
    draw_lines(win)
    pygame.display.update()


def set_promotion_display(chessboard, clicked_square):
    """
    Draws the piece choice gui when a promotion move occurs.
    :param chessboard: Dict
    :param clicked_square: Tuple
    :return: None
    """
    if chessboard[clicked_square].col == 0:
        direction = 1
    elif chessboard[clicked_square].col == 7:
        direction = -1

    offset = [(clicked_square[0], (clicked_square[1] + i * direction)) for i in range(4)]
    pieces = [chessboard[clicked_square].piece.team + "_" + p for p in ["queen", "bishop", "knight", "rook"]]
    promotion_choices = zip(offset, pieces)

    for promotion_choice in promotion_choices:
        chessboard[promotion_choice[0]].piece_cache = chessboard[promotion_choice[0]].piece
        chessboard[promotion_choice[0]].piece = eval(brd.basic_pieces[promotion_choice[1]])
        chessboard[promotion_choice[0]].promotion_in_progress = True
        chessboard[promotion_choice[0]].former_move = True


def reset_promotion_display(chessboard, promotion_field):
    """
    Removes the piece choice gui after the choice is made and reverts the previous state of the chessboard.
    :param chessboard: Dict
    :param promotion_field: Tuple
    :return: None
    """
    if chessboard[promotion_field].col == 0:
        direction = 1
    elif chessboard[promotion_field].col == 7:
        direction = -1

    offset = [(promotion_field[0], (promotion_field[1] + i * direction)) for i in range(4)]
    for offset_val in offset:
        chessboard[offset_val].piece = chessboard[offset_val].piece_cache
        chessboard[offset_val].piece_cache = None
        chessboard[offset_val].promotion_in_progress = False
        if offset_val[1] in [2, 3, 4, 5]:
            chessboard[offset_val].former_move = False


def draw_end_prompt(win, end_result):
    """
    Draws the end message after the game ends.
    :param win: pygame.Surface
    :param end_result: String
    :return: None
    """
    x = 2 * glb.SQUAREWIDTH
    y = 3 * glb.SQUAREWIDTH
    width = 4 * glb.SQUAREWIDTH + 1
    height = 2 * glb.SQUAREWIDTH + 1
    rect_outline = (x, y, width, height)
    rect_fill = (x+1, y+1, width-2, height-2)
    pygame.draw.rect(win, (255, 0, 0), rect_outline, 1)

    if end_result == "b":
        win.blit(w_checkmate_img, (x + 1, y + 1))
    if end_result == "w":
        win.blit(b_checkmate_img, (x + 1, y + 1))
    if end_result == "stalemate":
        win.blit(stalemate_img, (x + 1, y + 1))

    pygame.display.update()
