from board import *
import copy


class State:

    def __init__(self, next_turn=Turn.WHITE, board_repr=(0x8a8a8a8a,
                                                         0xa8a8a8a8,
                                                         0x8a8a8a8a,
                                                         0x88888888,
                                                         0x88888888,
                                                         0x28282828,
                                                         0x82828282,
                                                         0x28282828
                                                         )):
        self.turn = next_turn
        # 8 not allowed or empty
        # 2 white man
        # 3 white king
        # a black man
        # b black king
        self.board_repr = board_repr
        self._cached_board = None

    @property
    def board(self):
        """
        Cache new Board object (using stored representation) if it doesn't exist
        :return: Cached or just created Board object
        """
        if self._cached_board is None:
            self._cached_board = Board(self.board_repr)
        return self._cached_board

    def clean_cached_board(self):
        self._cached_board = None

    # TODO: implement storage of previous states ? (tree structure)
    # TODO: implement storage of next states ? (tree structure)

    def move_to(self, row_current, column_current, row_desired, column_desired):
        """
        Universal method to move one piece from curr loc to desired. It's not validating movements for generalization!
        :param row_current: current location of a piece to move
        :param column_current: current location of a piece to move
        :param row_desired: desired destination to move to
        :param column_desired: desired destination to move to
        :return: new state (deepcopy) generated due to the movement
        """

        # copy self.state and change it's copy
        changed_state = copy.deepcopy(self.board)

        if changed_state.board[row_desired][column_desired] is None \
                and changed_state.board[row_current][column_current] is not None \
                and 8 > row_desired >= 0 \
                and 8 > column_desired >= 0:

            # change piece's location
            changed_state.board[row_current][column_current].column = column_desired
            changed_state.board[row_current][column_current].row = row_desired

            # edit board
            changed_state.board[row_desired][column_desired] = changed_state.board[row_current][column_current]
            changed_state.board[row_current][column_current] = None

        return changed_state

    def attack_it(self, row_current, column_current, row_attacked, column_attacked):
        """

        :param row_current: current location of a piece to move
        :param column_current: current location of a piece to move
        :param row_attacked: destination to attack
        :param column_attacked: destination to attack
        :return: new state (deep copy) generated due to the attack
        """

        changed_state = copy.deepcopy(self.board)   # possibly unnecessary

        if changed_state.board[row_current][column_current] is Man:
            dx = row_attacked - row_current         # -1 / +1
            dy = column_attacked - column_current   # -1 / +1

            changed_state = self.move_to(row_current, column_current, row_current + 2*dx, column_current + 2*dy)
            changed_state.board[row_attacked][column_attacked] = None

        elif changed_state.board[row_current][column_current] is King:
            pass     # TODO implement!

        return changed_state

    def __str__(self):
        return self.board.__str__()


def test_attack_board():
    board_r = (0x8a8a8a8a,
               0xa8a8a8a8,
               0x888a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828
               )
    state = State(Turn.WHITE, board_r)
    print(state.board)
    print(state.attack_it(5, 2, 4, 1))
    print(state.board)  # should be the first board itself (unchanged)
    state.clean_cached_board()


if __name__ == '__main__':
    test_attack_board()
