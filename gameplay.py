"""
Definitions of all functions that will be handling gameplay.
"""

import pygame
import graphics as gui
import piece
import square as sq
import board as brd
import globals as glb


def populate_chessboard(chessboard):
    """
    Populates the dictionary with starting piece positions.
    :param chessboard: Dict
    :return: None
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                color = glb.DARKFIELD
            else:
                color = glb.WHITEFIELD

            placed_piece = brd.default_starting_placement[(row, col)]
            if placed_piece is not None:
                generated_piece = eval(brd.basic_pieces[placed_piece])
            else:
                generated_piece = None
            chessboard[(row, col)] = sq.Square(row, col, glb.SQUAREWIDTH, color, generated_piece)

            if (
                chessboard[(row, col)].piece is not None and
                chessboard[(row, col)].piece.type_ in ["rook", "king"]
            ):
                if chessboard[(row, col)].piece.team == "w" and col != 7:
                    chessboard[(row, col)].piece.moved = True
                if chessboard[(row, col)].piece.team == "b" and col != 0:
                    chessboard[(row, col)].piece.moved = True


def switch_active_team(team):
    """
    Changes which team is currently playing.
    :param team: String
    :return: String
    """
    if team == "w":
        return "b"
    if team == "b":
        return "w"


def clear_selection_highlight(chessboard):
    """
    Clears all move highlights from the field, except highlights for former moves.
    :param chessboard: Dict
    :return: None
    """
    for square in chessboard:
        chessboard[square].selected_piece = False
        chessboard[square].regular_move = False
        chessboard[square].eat_move = False
        chessboard[square].special_move = False
        chessboard[square].castle_move = False
        chessboard[square].enpassant_move = False
        chessboard[square].promotion_move = False
        chessboard[square].double_move = False


def clear_cached_move(chessboard):
    """
    Resets cached moves that were used for checking if a check has occured.
    :param chessboard: Dict
    :return: None
    """
    for square in chessboard:
        if chessboard[square].check_in_progress:
            chessboard[square].piece = chessboard[square].piece_cache
            chessboard[square].piece_cache = None
            chessboard[square].check_in_progress = False


def is_any_piece_selected(chessboard):
    """
    Checks if any piece on the board is selected.
    :param chessboard: Dict
    :return: Bool
    """
    for square in chessboard:
        if chessboard[square].selected_piece:
            return True
    return False


def is_same_team(chessboard, square1, square2):
    """
    Tests if two pieces are on the same team.
    :param chessboard: Dict
    :param square1: Tuple
    :param square2: Tuple
    :return: Bool
    """
    return chessboard[square1].piece.team == chessboard[square2].piece.team


def is_square_within_board(square):
    """
    Tests if square is within chessboard limits.
    :param square: Tuple
    :return: Bool
    """
    return 0 <= square[0] < 8 and 0 <= square[1] < 8


def is_direction_finished(chessboard, source, destination):
    """
    Checks if highlighting should be stopped in a direction for rook, bishop or queen piece.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :return: Bool
    """
    if not is_square_within_board(destination):
        return True
    elif chessboard[destination].piece is not None:
        if(
                chessboard[destination].eat_move or
                is_same_team(chessboard, source, destination)
        ):
            return True
    else:
        return False


def generate_moves_king(moves, king):
    """
    Generates all potential moves the king can perform from the current square.
    :param moves: List
    :param king: Tuple
    :return: None
    """
    offset = range(-1, 2)
    moves.extend(
        [
            (king[0] + offset_col, king[1] + offset_row)
            for offset_col in offset
            for offset_row in offset
            if offset_col != 0 or offset_row != 0
        ]
    )


def generate_moves_rook(moves, rook):
    """
    Generates all potential moves the rook can perform from the current square.
    :param moves: List
    :param rook: Tuple
    :return: None
    """
    offset = range(1, 8)
    moves.extend(
        [
            [(rook[0] + offset_val, rook[1]) for offset_val in offset],
            [(rook[0] - offset_val, rook[1]) for offset_val in offset],
            [(rook[0], rook[1] + offset_val) for offset_val in offset],
            [(rook[0], rook[1] - offset_val) for offset_val in offset]
        ]
    )


def generate_moves_bishop(moves, bishop):
    """
    Generates all potential moves the bishop can perform from the current square.
    :param moves: List
    :param bishop: Tuple
    :return: None
    """
    offset = range(1, 8)
    moves.extend(
        [
            [(bishop[0] + offset_val, bishop[1] - offset_val) for offset_val in offset],
            [(bishop[0] - offset_val, bishop[1] - offset_val) for offset_val in offset],
            [(bishop[0] - offset_val, bishop[1] + offset_val) for offset_val in offset],
            [(bishop[0] + offset_val, bishop[1] + offset_val) for offset_val in offset]
        ]
    )


def generate_moves_queen(moves, queen):
    """
    Generates all potential moves the queen can perform from the current square.
    :param moves: List
    :param queen: Tuple
    :return: None
    """
    generate_moves_bishop(moves, queen)
    generate_moves_rook(moves, queen)


def generate_moves_knight(moves, knight):
    """
    Generates all potential moves the knight can perform from the current square.
    :param moves: List
    :param knight: Tuple
    :return: None
    """
    offset = [-1, 1, -2, 2]
    moves.extend(
        [
            (knight[0] + offset_col, knight[1] + offset_row)
            for offset_col in offset
            for offset_row in offset
            if offset_col + offset_row != 0 and offset_col != offset_row
        ]
    )


def generate_moves_pawn(chessboard, pawn, enpassant=None, eat=None, double=None, single=None):
    """
    Generates all potential moves the pawn can perform from the current square.
    :param chessboard: Dict
    :param pawn: Tuple
    :param enpassant: List
    :param eat: List
    :param double: Bool
    :param single: Bool
    :return: Tuple
    """
    if chessboard[pawn].piece.team == "w":
        direction = -1
    else:
        direction = 1

    if single is not None:
        return pawn[0], pawn[1] + direction

    if double is not None:
        return pawn[0], pawn[1] + (2 * direction)

    if eat is not None:
        eat.extend(
            [
                (pawn[0] - 1, pawn[1] + direction),
                (pawn[0] + 1, pawn[1] + direction)
            ]
        )

    if enpassant is not None:
        eat_moves = [
            (pawn[0] - 1, pawn[1] + direction),
            (pawn[0] + 1, pawn[1] + direction)
        ]
        enpassant.extend(
            [
                (eat_moves[0], (eat_moves[0][0], eat_moves[0][1] - direction)),
                (eat_moves[1], (eat_moves[1][0], eat_moves[1][1] - direction))
            ]
        )


def highlight_move(chessboard, source, destination, team):
    """
    Highlights a single regular or eat move.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param team: String
    :return: None
    """
    if is_square_within_board(destination):
        if chessboard[destination].piece is not None:
            if (
                    chessboard[destination].piece.team != team and
                    chessboard[destination].piece.type_ != "king"
            ):
                if not is_check_caused(chessboard, source, destination, team):
                    chessboard[destination].eat_move = True
        else:
            if not is_check_caused(chessboard, source, destination, team):
                chessboard[destination].regular_move = True


def highlight_castling(chessboard, source, team):
    """
    Highlights pieces that are eligible for castling.
    :param chessboard: Dict
    :param source: Tuple
    :param team: String
    :return: None
    """
    if (
            chessboard[source].piece.type_ == "king" and
            not chessboard[source].piece.moved
    ):
        rooks = [(0, source[1]), (7, source[1])]
        for rook in rooks:
            if (
                    chessboard[rook].piece is not None and
                    chessboard[rook].piece.type_ == "rook" and
                    is_same_team(chessboard, source, rook) and
                    not chessboard[rook].piece.moved
            ):
                if rook[0] == 0:
                    fields_in_between = [(row, source[1]) for row in range(1, 4)]
                if rook[0] == 7:
                    fields_in_between = [(row, source[1]) for row in range(5, 7)]
                all_fields_free = True

                for field in fields_in_between:
                    if chessboard[field].piece is not None:
                        all_fields_free = False

                if (
                        all_fields_free and
                        not is_check_caused(chessboard, source, rook, team)
                ):
                    chessboard[rook].special_move = True
                    chessboard[rook].castle_move = True

    if (
            chessboard[source].piece.type_ == "rook" and
            not chessboard[source].piece.moved
    ):
        king = (4, source[1])
        if (
                chessboard[king].piece is not None and
                chessboard[king].piece.type_ == "king" and
                is_same_team(chessboard, source, king) and
                not chessboard[king].piece.moved
        ):
            if source[0] == 0:
                fields_in_between = [(row, source[1]) for row in range(1, 4)]
            if source[0] == 7:
                fields_in_between = [(row, source[1]) for row in range(5, 7)]
            all_fields_free = True

            for field in fields_in_between:
                if chessboard[field].piece is not None:
                    all_fields_free = False

            if (
                    all_fields_free and
                    not is_check_caused(chessboard, source, king, team)
            ):
                chessboard[king].special_move = True
                chessboard[king].castle_move = True


def highlight_moves_king(chessboard, king, team):
    """
    Highlight moves of the king piece.
    :param chessboard: Dict
    :param king: Tuple
    :param team: String
    :return: None
    """
    moves = []
    generate_moves_king(moves, king)
    for move in moves:
        highlight_move(chessboard, king, move, team)
    highlight_castling(chessboard, king, team)


def highlight_moves_rook(chessboard, rook, team):
    """
    Highlight moves of the rook piece.
    :param chessboard: Dict
    :param rook: Tuple
    :param team: String
    :return: None
    """
    move_directions = []
    generate_moves_rook(move_directions, rook)
    for direction in move_directions:
        for move in direction:
            highlight_move(chessboard, rook, move, team)
            if is_direction_finished(chessboard, rook, move):
                break
    highlight_castling(chessboard, rook, team)


def highlight_moves_bishop(chessboard, bishop, team):
    """
    Highlight moves of the bishop piece.
    :param chessboard: Dict
    :param bishop: Tuple
    :param team: String
    :return: None
    """
    move_directions = []
    generate_moves_bishop(move_directions, bishop)
    for direction in move_directions:
        for move in direction:
            highlight_move(chessboard, bishop, move, team)
            if is_direction_finished(chessboard, bishop, move):
                break


def highlight_moves_queen(chessboard, queen, team):
    """
    Highlight moves of the queen piece.
    :param chessboard: Dict
    :param queen: Tuple
    :param team: String
    :return: None
    """
    highlight_moves_rook(chessboard, queen, team)
    highlight_moves_bishop(chessboard, queen, team)


def highlight_moves_knight(chessboard, knight, team):
    """
    Highlight moves of the knight piece.
    :param chessboard: Dict
    :param knight: Tuple
    :param team: String
    :return: None
    """
    moves = []
    generate_moves_knight(moves, knight)
    for move in moves:
        highlight_move(chessboard, knight, move, team)


def highlight_moves_pawn(chessboard, pawn, team):
    """
    Highlight moves of the pawn piece.
    :param chessboard: Dict
    :param pawn: Tuple
    :param team: String
    :return: None
    """
    single_move = generate_moves_pawn(chessboard, pawn, single=True)
    if (
            is_square_within_board(single_move) and
            chessboard[single_move].piece is None
    ):
        if single_move[1] in [0, 7]:
            if not is_check_caused(chessboard, pawn, single_move, team):
                chessboard[single_move].special_move = True
                chessboard[single_move].promotion_move = True
        else:
            if not is_check_caused(chessboard, pawn, single_move, team):
                chessboard[single_move].regular_move = True

    double_move = generate_moves_pawn(chessboard, pawn, double=True)
    if (
            is_square_within_board(double_move) and
            chessboard[single_move].piece is None and
            chessboard[double_move].piece is None and
            pawn[1] in [1, 6]
    ):
        if not is_check_caused(chessboard, pawn, double_move, team):
            chessboard[double_move].special_move = True
            chessboard[double_move].double_move = True

    eat_moves = []
    generate_moves_pawn(chessboard, pawn, eat=eat_moves)
    for move in eat_moves:
        if (
                is_square_within_board(move) and
                chessboard[move].piece is not None and
                not is_same_team(chessboard, pawn, move) and
                chessboard[move].piece.type_ != "king"
        ):
            if not is_check_caused(chessboard, pawn, move, team):
                chessboard[move].eat_move = True

    enpassant_field_pairs = []
    generate_moves_pawn(chessboard, pawn, enpassant=enpassant_field_pairs)
    for enpassant in enpassant_field_pairs:
        if (
                is_square_within_board(enpassant[0]) and
                chessboard[enpassant[0]].piece is None and
                is_square_within_board(enpassant[1]) and
                chessboard[enpassant[1]].piece is not None and
                chessboard[enpassant[1]].piece.type_ == "pawn" and
                not is_same_team(chessboard, pawn, enpassant[1]) and
                chessboard[enpassant[1]].piece.double_move
        ):
            if not is_check_caused(chessboard, pawn, enpassant[0], team):
                chessboard[enpassant[0]].special_move = True
                chessboard[enpassant[0]].enpassant_move = True


def highlight_potential_moves(chessboard, source, team):
    """
    Chooses what piece needs its move highlighted and executes the highlighting.
    :param chessboard: Dict
    :param source: Tuple
    :param team: String
    :return: None
    """
    if chessboard[source].piece is not None:
        if chessboard[source].piece.team == team:
            chessboard[source].selected_piece = True
            exec("highlight_moves_" + chessboard[source].piece.type_ + "(chessboard, clicked_square, team)")


def do_regular_move(chessboard, source, destination, check=False):
    """
    Executes a regular move.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    if check:
        chessboard[source].piece_cache = chessboard[source].piece
        chessboard[source].check_in_progress = True
        chessboard[destination].check_in_progress = True

    chessboard[destination].piece = chessboard[source].piece
    chessboard[source].piece = None

    if not check:
        for square in chessboard:
            if chessboard[square].former_move:
                chessboard[square].former_move = False

        chessboard[source].former_move = True
        chessboard[destination].former_move = True

        if chessboard[destination].piece.type_ in ["rook", "king"]:
            chessboard[destination].piece.moved = True


def do_eat_move(chessboard, source, destination, check=False):
    """
    Executes an eat move.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    if check:
        chessboard[destination].piece_cache = chessboard[destination].piece
    chessboard[destination].piece = None
    do_regular_move(chessboard, source, destination, check)


def do_double_move(chessboard, source, destination, check=False):
    """
    Executes a double move.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    do_regular_move(chessboard, source, destination, check)
    if not check:
        chessboard[destination].piece.double_move = True


def do_castle_move(chessboard, source, destination, check=False):
    """
    Executes a castle move.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    if chessboard[source].piece.type_ == "king":
        king = source
        rook = destination
    else:
        rook = source
        king = destination

    if check:
        chessboard[king].piece.moved = True
        chessboard[rook].piece.moved = True

    if rook[0] == 0:
        do_regular_move(chessboard, king, (2, king[1]), check)
        do_regular_move(chessboard, rook, (3, rook[1]), check)
    if rook[0] == 7:
        do_regular_move(chessboard, king, (6, king[1]), check)
        do_regular_move(chessboard, rook, (5, rook[1]), check)


def do_enpassant_move(chessboard, source, destination, check=False):
    """
    Executes an enpassant move.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    do_regular_move(chessboard, source, destination, check)
    offset = [1, -1]
    for offset_val in offset:
        enpassant = (destination[0], destination[1] + offset_val)
        if (
                chessboard[enpassant].piece is not None and
                chessboard[enpassant].piece.type_ == "pawn" and
                chessboard[enpassant].piece.double_move
        ):
            if check:
                chessboard[enpassant].piece_cache = chessboard[enpassant].piece
                chessboard[enpassant].check_in_progress = True
            chessboard[enpassant].piece = None


def do_promotion_move(chessboard, source, destination, check=False):
    """
    Executes the first half of the promotion move. Executes pawn movement and gui generation.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    do_regular_move(chessboard, source, destination, check)
    if not check:
        gui.set_promotion_display(chessboard, destination)


def do_promotion_resolve(chessboard, clicked_square):
    """
    Executes the second half of the promotion move. Executes piece swap after choice and gui reset.
    :param chessboard: Dict
    :param clicked_square: Tuple
    :return: None
    """
    if clicked_square[1] <= 4:
        promotion_field = (clicked_square[0], 0)
    else:
        promotion_field = (clicked_square[0], 7)

    chessboard[promotion_field].piece_cache = chessboard[clicked_square].piece
    gui.reset_promotion_display(chessboard, promotion_field)

    if chessboard[promotion_field].piece.type_ == "rook":
        chessboard[promotion_field].piece.moved = True


def do_move(chessboard, source, destination, check=False):
    """
    Executes the available move on the selected square.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param check: Bool
    :return: None
    """
    moves = ["regular_move", "eat_move"]
    if chessboard[source].piece.type_ == "pawn":
        moves.extend(["double_move", "promotion_move", "enpassant_move"])
    if chessboard[source].piece.type_ in ["king", "rook"]:
        moves.extend(["castle_move"])

    for move in moves:
        if eval("chessboard[clicked_square]." + move):
            if check:
                exec("do_" + move + "(chessboard, selected_piece, clicked_square, check)")
            else:
                exec("do_" + move + "(chessboard, selected_piece, clicked_square)")

    if not check:
        for square in chessboard:
            if (
                    chessboard[square].piece is not None and
                    chessboard[square].piece.team != chessboard[source].piece.team and
                    chessboard[square].piece.type_ == "pawn"
            ):
                chessboard[square].piece.double_move = False


def is_king_under_check(chessboard, team):
    """
    Tests if the king of the current team is currently under check.
    :param chessboard: Dict
    :param team: String
    :return: Bool
    """
    check = False
    for square in chessboard:
        if (
                chessboard[square].piece is not None and
                chessboard[square].piece.type_ == "king"
        ):
            if chessboard[square].piece.team == team:
                king = square
                break

    threats = ["king", "queen", "bishop", "knight", "rook", "pawn"]
    for threat in threats:
        attacks = []
        if threat == "pawn":
            generate_moves_pawn(chessboard, king, eat=attacks)
        else:
            exec("generate_moves_" + threat + "(attacks, king)")

        if threat in ["king", "knight", "pawn"]:
            for attack in attacks:
                if is_square_within_board(attack):
                    if (
                            chessboard[attack].piece is not None and
                            chessboard[attack].piece.type_ == threat
                    ):
                        if chessboard[attack].piece.team != team:
                            check = True
                            break

        if threat in ["queen", "bishop", "rook"]:
            for direction in attacks:
                for attack in direction:
                    if is_square_within_board(attack):
                        if (
                                chessboard[attack].piece is not None and
                                chessboard[attack].piece.type_ == threat
                        ):
                            if chessboard[attack].piece.team != team:
                                check = True
                                break
                    if is_direction_finished(chessboard, king, attack):
                        break

    return check


def is_check_caused(chessboard, source, destination, team):
    """
    Tests if the king of the current team is under check after a potential move would be executed.
    :param chessboard: Dict
    :param source: Tuple
    :param destination: Tuple
    :param team: String
    :return: Bool
    """
    do_move(chessboard, source, destination, check=True)
    king_state = is_king_under_check(chessboard, team)
    clear_cached_move(chessboard)
    return king_state


def is_valid_move_left(chessboard, team):
    """
    Tests if the current team has any valid moves left.
    :param chessboard: Dict
    :param team: String
    :return: Bool
    """
    any_moves_left = False
    for square in chessboard:
        if (
                chessboard[square].piece is not None and
                chessboard[square].piece.team == team
        ):
            highlight_potential_moves(chessboard, square, team)

        for square_ in chessboard:
            if (
                    chessboard[square_].regular_move or
                    chessboard[square_].eat_move or
                    chessboard[square_].special_move
            ):
                any_moves_left = True

        if any_moves_left:
            break

    clear_selection_highlight(chessboard)
    return any_moves_left


def is_checkmate_stalemate(chessboard, team):
    """
    Tests if a checkmate or a stalemate has occured for the current team.
    :param chessboard: Dict
    :param team: String
    :return: String or False
    """
    if not is_valid_move_left(chessboard, team):
        if not is_king_under_check(chessboard, team):
            return "stalemate"
        else:
            return team
    return False
