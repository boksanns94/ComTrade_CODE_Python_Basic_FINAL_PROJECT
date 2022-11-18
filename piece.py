"""
Definitions of chess piece types.
"""


class Piece:
    """
    General definition for all piece types.
    Contains information about team, piece type and piece image.
    """
    def __init__(self, team, type_, image):
        """
        :param team: String
        :param type_: String
        :param image: pygame.Surface
        """
        self.team = team
        self.piece = type_
        self.image = image


Queen = Piece
Bishop = Piece
Knight = Piece


class Pawn(Piece):
    """
    Specific definition of the Pawn piece.
    Adds attribute for tracking if the piece executed a double move.
    """
    def __init__(self, team, type_, image):
        super().__init__(team, type_, image)
        self.double_move = False


class Rook(Piece):
    """
    Specific definition of the Rook piece.
    Adds attribute for tracking if the piece has moved.
    """
    def __init__(self, team, type_, image):
        super().__init__(team, type_, image)
        self.moved = False


King = Rook
