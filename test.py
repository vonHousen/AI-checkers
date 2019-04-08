from game import *


def print_next_states(state):
    """
    Used only for testing
    :return:
    """
    if state.next_states:
        for next_state in state.next_states:
            print(next_state)
    else:
        print("<There are no next states available>\n")


def print_final_decision_chain(state):
    """
    Used only for testing
    Prints recursively final chain of moves resulting in best game outcome
    :return: -
    """
    print(state)
    if state.next_move:
        print_final_decision_chain(state.next_move)


def test_repr_gen():
    print("test_repr_gen")
    board = Board()
    print(board)
    for row_repr in board.board_repr:
        print(hex(row_repr))
    print()
    board2 = Board(board.board_repr)
    print(board2)


def test_man_moves():
    print("test_man_moves")
    board = Board()
    print(board)
    for piece in board.pieces:
        moves = piece.possible_moves
        if moves:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(moves)


def test_man_attacks():
    print("test_man_attacks")
    board_repr = (0x8a8a8a8a,
                  0xa8a8a8a8,
                  0x8a8a8a8a,
                  0x88288888,
                  0x88888a88,
                  0x28282828,
                  0x82828282,
                  0x28282828
                  )
    board = Board(board_repr)
    print(board)

    for piece in board.pieces:
        possible_attacks_list = piece.possible_attacks
        if possible_attacks_list:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(possible_attacks_list)


def test_king_moves():
    print("test_king_moves")
    board_repr = (0x88888888,
                  0x88888888,
                  0x88888888,
                  0x8888b888,
                  0x88838888,
                  0x88888888,
                  0x88888888,
                  0x88888888
                  )
    board = Board(board_repr)
    print(board)

    for piece in board.pieces:
        possible_moves_list = piece.possible_moves
        if possible_moves_list:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(possible_moves_list)
            # for row, col in possible_moves_list:
            #     piece.board.set_piece_at(row, col, "x")
    piece = board.pieces[0]
    row, col = piece.possible_moves[0]
    piece.move_to(row, col)
    print(board)


def test_king_attacks():
    print("test_king_attacks")
    board_repr = (0x88888888,
                  0x88888888,
                  0x88888888,
                  0x8888b888,
                  0x88838888,
                  0x88888838,
                  0x82888888,
                  0x88888888
                  )
    board = Board(board_repr)
    print(board)

    for piece in board.pieces:
        possible_moves_list = piece.possible_attacks
        if possible_moves_list:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(possible_moves_list)
    piece = board.pieces[0]
    row, col = piece.possible_attacks[0]
    piece.attack_to(row, col)
    print(board)


def test_replace_with_king():
    print("test_replace_with_king")
    board_repr = (0x82828a8a,
                  0xa8a8a8a8,
                  0x8a8a8a8a,
                  0x88288888,
                  0x88888a88,
                  0x28282828,
                  0x82828282,
                  0x28a828a8
                  )
    board = Board(board_repr)
    print(board)
    for piece in board.pieces:
        if piece.can_be_replaced_with_king():
            piece.replace_with_king()

    print(board)


def test_simple_attack_generating():
    print("test_simple_attack_generating")
    board_r = (0x8a8a8a8a,
               0xa8a8a8a8,
               0x888a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828
               )
    state = State(Board(board_r))
    print(state)

    # noinspection PyProtectedMember
    print(state._board._get_board_after_attack(5, 2, 3, 0))
    print(state)  # should be the first board itself (unchanged)
    state.clean_cached_board()


def test_generating_attacks():
    print("test_generating_attacks")
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828
               )
    state = State(Board(board_r))
    print(state)
    print_next_states(state)


def test_alpha_beta():
    print("test_alpha_beta")
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828)
    state = State(Board(board_r))
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    SearchAlgorithm().alpha_beta(state, 6)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    print_final_decision_chain(state)
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


def test_kings():
    print("test_kings")
    board_r = (0x88838888,
               0x88888888,
               0x88888888,
               0x88888888,
               0x888a8888,
               0x88888888,
               0x88888288,
               0x88888888)
    state = State(Board(board_r))
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    SearchAlgorithm().alpha_beta(state, 3)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    print_final_decision_chain(state)
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


def test_becoming_kings():
    print("test_becoming_kings")
    board_r = (0x88888888,
               0x28888888,
               0x88888888,
               0x88888888,
               0x88888888,
               0x8888a888,
               0x88888288,
               0x88888888)
    state = State(Board(board_r, Color.BLACK))
    print(40 * "-")
    print("Root state:")
    print(state)
    print(40 * "-")
    start_time = time.time()

    SearchAlgorithm().alpha_beta(state, 6)

    end_time = time.time()
    print(40 * "-")
    print("Final sequence:")
    print_final_decision_chain(state)
    print()
    print(40 * "-")
    print("alpha_beta time [s]: " + f'{end_time - start_time}')


if __name__ == '__main__':
    # test_repr_gen()
    # test_man_moves()
    # test_man_attacks()
    # test_king_moves()
    # test_king_attacks()
    # test_replace_with_king()
    # test_simple_attack_generating()
    # test_generating_attacks()
    # test_alpha_beta()
    # test_kings()
    test_becoming_kings()
