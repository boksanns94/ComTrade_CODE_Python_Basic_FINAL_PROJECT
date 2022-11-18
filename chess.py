"""
Main game file.
"""


import sys
import pygame
import graphics as gui
import gameplay as gpl
import globals as glb


def chess():
    """
    Main game thread.
    :return: None
    """
    WIN = pygame.display.set_mode((glb.BOARDWIDTH, glb.BOARDWIDTH))
    pygame.display.set_caption("CHESS")

    game = True
    team = "w"
    end = ""
    promotion_in_progress = False
    chessboard = {}
    gpl.populate_chessboard(chessboard)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_square = gui.get_clicked_square()
                if promotion_in_progress:
                    if chessboard[clicked_square].promotion_in_progress:
                        gpl.do_promotion_resolve(chessboard, clicked_square)
                        promotion_in_progress = False
                        team = gpl.switch_active_team(team)
                        end = gpl.is_checkmate_stalemate(chessboard, team)
                        if end:
                            game = False
                else:
                    if gpl.is_any_piece_selected(chessboard):
                        if (
                                chessboard[clicked_square].regular_move or
                                chessboard[clicked_square].eat_move or
                                chessboard[clicked_square].special_move
                        ):
                            gpl.do_move(chessboard, selected_piece, clicked_square)
                            gpl.clear_selection_highlight(chessboard)
                            if chessboard[clicked_square].promotion_in_progress:
                                promotion_in_progress = True
                            else:
                                team = gpl.switch_active_team(team)
                                end = gpl.is_checkmate_stalemate(chessboard, team)
                                if end:
                                    game = False
                        else:
                            gpl.clear_selection_highlight(chessboard)
                            if chessboard[clicked_square].piece is not None:
                                selected_piece = clicked_square
                                gpl.highlight_potential_moves(chessboard, clicked_square, team)
                    else:
                        if chessboard[clicked_square].piece is not None:
                            selected_piece = clicked_square
                            gpl.highlight_potential_moves(chessboard, clicked_square, team)
        gui.draw_chessboard(WIN, chessboard)

    gui.draw_chessboard(WIN, chessboard)
    gui.draw_end_prompt(WIN, end)

    while not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)


if __name__ == '__main__':
    chess()
