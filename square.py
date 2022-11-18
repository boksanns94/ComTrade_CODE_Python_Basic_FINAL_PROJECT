"""
Definition of a single square field on the board.
"""


class Square:
    """
    General definition for a single square field.
    Contains information about the visual attributes of the square such as: position of the square on the field,
    dimensions of the square and color of the square. Also contains information about the piece on top of the
    square, a temporary piece cache as well as flags indicating move availability for pieces on the board.
    """
    def __init__(self, row, col, width, color, piece):
        """
        :param row: Integer
        :param col: Integer
        :param width: Integer
        :param color: Tuple
        :param piece: piece.Piece
        """
        self.row = row
        self.col = col
        self.width = width
        self.x = self.row * self.width
        self.y = self.col * self.width
        self.rect = (self.x, self.y, self.width, self.width)
        self.color = color

        self.piece = piece
        self.piece_cache = None

        self.selected_piece = False
        self.promotion_in_progress = False
        self.check_in_progress = False

        self.regular_move = False
        self.former_move = False
        self.eat_move = False
        self.special_move = False
        self.castle_move = False
        self.promotion_move = False
        self.enpassant_move = False
        self.double_move = False
