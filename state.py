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
                                                          ), level=0):
        self.turn = next_turn
        # 8 not allowed or empty
        # 2 white man
        # 3 white king
        # a black man
        # b black king
        self.board_repr = board_repr
        self.level = level
        self._cached_board = None
        self._next_states = []

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

    def _get_state_after_movement(self, row_current, column_current, row_desired, column_desired):
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

    def _get_state_after_attack(self, row_current, column_current, row_after_attack, column_after_attack):
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

    @property
    def get_next_states(self):
        """

        :return: set of next states
        """

        return self._next_states

    def print_next_states(self):
        if self._next_states:
            for next_state in self._next_states:
                print("Balance = " + f'{next_state.board.balance}' +
                "   Turn = " + f'{next_state.turn}' +
                "   Level = " + f'{next_state.level}')
                print(next_state)
        else:
            print("<There are no next states available>\n")

    def generate_next_states(self):
        """
        Generates all possible states generated from the current one (appends to self._next_states)
        :return: -
        """
        set_of_new_states = []

        for piece in self.board.get_pieces_of_color(self.turn):
            if piece.possible_attacks:

                set_of_new_sub_states = self._generate_next_states_during_attack(piece)
                for new_sub_state in set_of_new_sub_states:
                    new_sub_state._next_level()
                    new_sub_state._next_turn()
                    set_of_new_states.append(new_sub_state)

            else:
                for after_move_loc in piece.possible_moves:
                    new_state_moved = self._get_state_after_movement(piece.row, piece.column, after_move_loc[0], after_move_loc[1])
                    new_state_moved._next_level()
                    new_state_moved._next_turn()
                    self._next_states.append(new_state_moved)

        for new_state in set_of_new_states:
            self._next_states.append(new_state)

    def _generate_next_states_during_attack(self, piece):
        """
        Generates all possible states generated from the current one for given piece
        Used only during multiple-attack
        :return: set of new states
        """
        set_of_new_states = []

        for after_attack_loc in piece.possible_attacks:

            new_state = \
                self._get_state_after_attack(piece.row, piece.column, after_attack_loc[0], after_attack_loc[1])
            set_of_new_states.append(new_state)

            # if just appended state result in multiple-attack: append new states, delete prev.
            attacking_piece = new_state.board.get_piece_at(after_attack_loc[0], after_attack_loc[1])
            if attacking_piece.possible_attacks:

                set_of_new_states.pop()
                set_of_new_sub_states = new_state._generate_next_states_during_attack(attacking_piece)
                for new_sub_state in set_of_new_sub_states:
                    set_of_new_states.append(new_sub_state)

        return set_of_new_states

    def _next_turn(self):
        """
        Changes turn of current state
        :return: -
        """
        if self.turn == Color.BLACK:
            self.turn = Color.WHITE
        else:
            self.turn = Color.BLACK

    def _next_level(self):
        """
        Changes deepness level in tree structure
        :return:
        """
        self.level += 1

def test_simple_attack():
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
    print(state._get_state_after_attack(5, 2, 3, 0))
    print(state.board)  # should be the first board itself (unchanged)
    state.clean_cached_board()


def test_generating_attacks():
    board_r = (0x8a8a8a8a,
               0xa888a8a8,
               0x8a8a8a8a,
               0x88888888,
               0x8a888888,
               0x28282828,
               0x82828282,
               0x28282828
               )
    state = State(Color.WHITE, board_r)
    print(state.board)

    for attack in state.board.get_piece_at(0, 1).possible_attacks:
        print(attack)

    state.print_next_states()
    state.generate_next_states()
    state.print_next_states()


if __name__ == '__main__':
    test_generating_attacks()

