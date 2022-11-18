"""
Dictionary containing all piece type and team combinations.
Dictionary containing the default starting placements of all pieces on the board.
"""


basic_pieces = {
    "w_king": 'piece.King("w", "king", pygame.image.load("images/w_king.png"))',
    "b_king": 'piece.King("b", "king", pygame.image.load("images/b_king.png"))',
    "w_queen": 'piece.Queen("w", "queen", pygame.image.load("images/w_queen.png"))',
    "b_queen": 'piece.Queen("b", "queen", pygame.image.load("images/b_queen.png"))',
    "w_bishop": 'piece.Bishop("w", "bishop", pygame.image.load("images/w_bishop.png"))',
    "b_bishop": 'piece.Bishop("b", "bishop", pygame.image.load("images/b_bishop.png"))',
    "w_knight": 'piece.Knight("w", "knight", pygame.image.load("images/w_knight.png"))',
    "b_knight": 'piece.Knight("b", "knight", pygame.image.load("images/b_knight.png"))',
    "w_rook": 'piece.Rook("w", "rook", pygame.image.load("images/w_rook.png"))',
    "b_rook": 'piece.Rook("b", "rook", pygame.image.load("images/b_rook.png"))',
    "w_pawn": 'piece.Pawn("w", "pawn", pygame.image.load("images/w_pawn.png"))',
    "b_pawn": 'piece.Pawn("b", "pawn", pygame.image.load("images/b_pawn.png"))'
}


default_starting_placement = {
    (0, 0): "b_rook", (1, 0): "b_knight", (2, 0): "b_bishop", (3, 0): "b_queen",
    (4, 0): "b_king", (5, 0): "b_bishop", (6, 0): "b_knight", (7, 0): "b_rook",

    (0, 1): "b_pawn", (1, 1): "b_pawn", (2, 1): "b_pawn", (3, 1): "b_pawn",
    (4, 1): "b_pawn", (5, 1): "b_pawn", (6, 1): "b_pawn", (7, 1): "b_pawn",

    (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
    (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,

    (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
    (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,

    (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
    (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,

    (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
    (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

    (0, 6): "w_pawn", (1, 6): "w_pawn", (2, 6): "w_pawn", (3, 6): "w_pawn",
    (4, 6): "w_pawn", (5, 6): "w_pawn", (6, 6): "w_pawn", (7, 6): "w_pawn",

    (0, 7): "w_rook", (1, 7): "w_knight", (2, 7): "w_bishop", (3, 7): "w_queen",
    (4, 7): "w_king", (5, 7): "w_bishop", (6, 7): "w_knight", (7, 7): "w_rook"
}
