from board import *
import copy


class State:

    def __init__(self, next_turn=Color.WHITE, board_repr=(0x8a8a8a8a,
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

    def get_state_after_movement(self, row_current, column_current, row_desired, column_desired):
        """
        Universal method to move one piece from curr loc to desired. It's not validating movements!
        :param row_current: current location of a piece to move
        :param column_current: current location of a piece to move
        :param row_desired: desired destination to move to
        :param column_desired: desired destination to move to
        :return: new state (deepcopy) generated due to the movement
        """

        # copy self.state and change it's copy
        changed_state = copy.deepcopy(self)
        changed_board = changed_state.board

        if changed_board.is_there_piece_at(row_current, column_current):
            moved_piece = changed_board.get_piece_at(row_current, column_current)
            moved_piece.move_to(row_desired, column_desired)

        else:
            raise RuntimeError("Moving piece do not exist")

        return changed_state

    def get_state_after_attack(self, row_current, column_current, row_after_attack, column_after_attack):
        """

        :param row_current: current location of a piece to move
        :param column_current: current location of a piece to move
        :param row_after_attack: location after attack
        :param column_after_attack: location after attack
        :return: new state (deep copy) generated due to the attack
        """

        # copy self.state and change it's copy
        changed_state = copy.deepcopy(self)
        changed_board = changed_state.board

        if changed_board.is_there_piece_at(row_current, column_current):
            attacking_piece = changed_board.get_piece_at(row_current, column_current)
            attacking_piece.attack_to(row_after_attack, column_after_attack)

        else:
            raise RuntimeError("Attacking piece do not exist")

        return changed_state

    def __str__(self):
        return self.board.__str__()

    # TODO adjust functions below after moving from game.py
    # def print_set(self, no_set_of_states):
    #     """

    #     :param no_set_of_states: number of the set of states to be printed
    #     :return: -
    #     """

    #     # TODO move to states
    #     if self.states.__len__() > no_set_of_states >= 0:
    #         for no, state in enumerate(self.states[no_set_of_states]):
    #             print("set_of_states: " + f'{no_set_of_states}' + " | state no: " + f'{no}')
    #             print(state)

    # def generate_next_states(self, turn):
    #     """
    #     Generates all possible states generated from the last one (appends to self.states)
    #     :param turn: decides what turn (what color) it is for generating new states
    #     :return: -
    #     """
    #     # TODO move to State
    #
    #     last_state = self.states[-1][0]  # it should be parent in the tree structure
    #     self.states.append([])  # new set_of_states
    #
    #     for piece in last_state.board.get_pieces_of_color(turn):
    #
    #         if piece.can_attack():
    #             for destination in piece.list_possible_attacks:
    #                 attacker_row = piece.row
    #                 attacker_col = piece.column
    #
    #                 self.states[-1].append(
    #                     last_state.get_state_after_attack(attacker_row, attacker_col, destination[0], destination[1]))
    #
    #                 # TODO if just appended state result in multiple-attack: append new states, delete prev.
    #                 # TODO make it recursive (no one knows how many multiple-attacks a piece can perform
    #
    #         elif piece.can_move():
    #             for destination in piece.list_possible_moves:
    #                 self.states[-1].append(
    #                     last_state.get_state_after_movement(piece.row, piece.column, destination[0], destination[1]))
    #
    #     if self.states[-1] == []:  # delete set_of_state if empty
    #    del self.states[-1]
    #


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
    state = State(Color.WHITE, board_r)
    print(state.board)
    print(state.get_state_after_attack(5, 2, 3, 0))
    print(state.board)  # should be the first board itself (unchanged)
    state.clean_cached_board()


def test_man_attacks():
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
        possible_attacks_list = piece.possible_attacks()
        if possible_attacks_list:
            print(possible_attacks_list)


if __name__ == '__main__':
    test_attack_board()
