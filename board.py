from typing import List, Any, Union

from piece import *


class Board:

    def __init__(self, board_repr=(0x8a8a8a8a,
                                   0xa8a8a8a8,
                                   0x8a8a8a8a,
                                   0x88888888,
                                   0x88888888,
                                   0x28282828,
                                   0x82828282,
                                   0x28282828
                                   ), next_turn=Color.WHITE, level=0):
        """
        :type board_repr: Memory optimized representation of board
        """
        self.turn = next_turn
        self.level = level
        # 8 not allowed or empty
        # 2 white man
        # 3 white king
        # a black man
        # b black king
        self.__board = [[], [], [], [], [], [], [], []]
        for rowNumber, row in enumerate(board_repr):
            mask = 0xF0000000
            for columnNumber in range(8):
                piece = row & mask
                if piece == 0x20000000:  # white man
                    self.__board[rowNumber].append(WhiteMan(rowNumber, columnNumber, self))
                elif piece == 0x30000000:  # white king
                    self.__board[rowNumber].append(WhiteKing(rowNumber, columnNumber, self))
                elif piece == 0xa0000000:  # black man
                    self.__board[rowNumber].append(BlackMan(rowNumber, columnNumber, self))
                elif piece == 0xb0000000:  # black king
                    self.__board[rowNumber].append(BlackKing(rowNumber, columnNumber, self))
                else:  # empty or not allowed
                    self.__board[rowNumber].append(None)
                row = row << 4

    @property
    def board_repr(self):
        """
        :return: Memory optimized representation of that board.
        """
        board = [0, 0, 0, 0, 0, 0, 0, 0]
        for rowNumber, row in enumerate(self.__board):
            for columnNumber, piece in enumerate(row):
                if piece is None:
                    board[rowNumber] |= 0x00000008
                else:
                    board[rowNumber] |= piece.get_representation()
                if columnNumber != 7:
                    board[rowNumber] = board[rowNumber] << 4
        return tuple(board)

    @property
    def pieces(self):
        """
        :return: List of pieces on the board
        """
        return [piece for row in self.__board for piece in row if piece is not None]

    def get_pieces_of_color(self, color):
        """
        :return: List of pieces on the board of specific color
        """
        return [piece for row in self.__board for piece in row if (piece is not None and piece.color == color)]

    def get_attacking_pieces_of_color(self, color):
        """
        :return: List of pieces on the board of specific color, only if they can attack
        """
        return [piece for row in self.__board for piece in row if
                (piece is not None
                 and piece.color == color
                 and piece.can_attack_anywhere())]

    def get_moving_pieces_of_color(self, color):
        """
        :return: List of pieces on the board of specific color, only if they can move and not attack
        """
        return [piece for row in self.__board for piece in row if
                (piece is not None
                 and piece.color == color
                 and not piece.can_attack_anywhere()
                 and piece.can_move_anywhere())]

    @property
    def balance(self):
        """
        :return: Positive balance means white is winning
        """
        result = 0.0
        for piece in self.pieces:
            if piece.get_representation() == 0x0000000a:  # isinstance(piece, BlackMan):
                result -= 1.0
            elif piece.get_representation() == 0x0000000b:  # isinstance(piece, BlackKing):
                result -= 1.6
            elif piece.get_representation() == 0x00000002:  # isinstance(piece, WhiteMan):
                result += 1.0
            elif piece.get_representation() == 0x00000003:  # isinstance(piece, WhiteKing):
                result += 1.6
        return result

    def is_there_piece_at(self, row, column):
        if self.__board[row][column] is None:
            return False
        return True

    def get_piece_at(self, row, column) -> Union[BlackMan, WhiteMan, BlackKing, WhiteKing]:
        # there's bug with pycharm correcly identyfing type when using double indexing
        # noinspection PyTypeChecker
        return self.__board[row][column]

    def delete_piece_at(self, row, column):
        (self.__board[row][column]) = None

    def set_piece_at(self, row, column, piece):
        (self.__board[row][column]) = piece

    def get_next_boards(self):
        """
        Generates all possible states generated from the current one (appends to self._next_states)
        :return: -
        """
        set_of_new_boards = []

        if self._does_any_piece_can_attack():
            for piece in self.get_attacking_pieces_of_color(self.turn):

                set_of_new_sub_boards = self._generate_next_boards_during_attack(piece)
                for new_sub_board, after_attack_row, after_attack_col in set_of_new_sub_boards:

                    # if attacking piece after finished attack is a man and can become a king - do so
                    moved_piece = new_sub_board.get_piece_at(after_attack_row, after_attack_col)
                    # if isinstance(piece, WhiteMan) or isinstance(piece, BlackMan)
                    if moved_piece.get_representation() == 0x0000000a or moved_piece.get_representation() == 0x00000002:
                        if moved_piece.can_be_replaced_with_king():
                            moved_piece.replace_with_king()

                    new_sub_board.next_level()
                    new_sub_board.next_turn()
                    set_of_new_boards.append(new_sub_board)

        else:
            for piece in self.get_moving_pieces_of_color(self.turn):

                for after_move_row, after_move_col in piece.possible_moves:
                    new_board_moved = self._get_board_after_movement(piece.row,
                                                                     piece.column,
                                                                     after_move_row,
                                                                     after_move_col)

                    # if moved_piece is a man and can become a king - do so
                    moved_piece = new_board_moved.get_piece_at(after_move_row, after_move_col)
                    # if isinstance(piece, WhiteMan) or isinstance(piece, BlackMan)
                    if moved_piece.get_representation() == 0x0000000a or moved_piece.get_representation() == 0x00000002:
                        if moved_piece.can_be_replaced_with_king():
                            moved_piece.replace_with_king()

                    new_board_moved.next_level()
                    new_board_moved.next_turn()
                    set_of_new_boards.append(new_board_moved)

        return set_of_new_boards

    def _generate_next_boards_during_attack(self, piece):
        """
        Generates all possible states generated from the current one for given piece
        Used only during multiple-attack
        :return: set of new states
        """
        set_of_new_boards = []

        for after_attack_row, after_attack_col in piece.possible_attacks:

            new_board = \
                self._get_board_after_attack(piece.row, piece.column, after_attack_row, after_attack_col)
            set_of_new_boards.append(tuple((new_board, after_attack_row, after_attack_col)))

            # if just appended state result in multiple-attack: append new states, delete prev.
            attacking_piece: Piece = new_board.get_piece_at(after_attack_row, after_attack_col)
            if attacking_piece.possible_attacks:

                set_of_new_boards.pop()
                set_of_new_sub_states = new_board._generate_next_boards_during_attack(attacking_piece)
                for new_sub_state, after_sub_attack_row, after_sub_attack_col in set_of_new_sub_states:
                    set_of_new_boards.append(tuple((new_sub_state, after_sub_attack_row, after_sub_attack_col)))

        return set_of_new_boards

    def _get_board_after_movement(self, row_current, column_current, row_desired, column_desired):
        """
        Universal method to move one piece from curr loc to desired. It's not validating movements!
        :param row_current: current location of a piece to move
        :param column_current: current location of a piece to move
        :param row_desired: desired destination to move to
        :param column_desired: desired destination to move to
        :return: new state (deepcopy) generated due to the movement
        """

        # copy board and change it's copy
        changed_board = Board(self.board_repr, self.turn, self.level)

        if changed_board.is_there_piece_at(row_current, column_current):
            moved_piece = changed_board.get_piece_at(row_current, column_current)
            moved_piece.move_to(row_desired, column_desired)

        else:
            raise RuntimeError("Moving piece do not exist")

        return changed_board

    def _get_board_after_attack(self, row_current, column_current, row_after_attack, column_after_attack):
        """

        :param row_current: current location of a piece to move
        :param column_current: current location of a piece to move
        :param row_after_attack: location after attack
        :param column_after_attack: location after attack
        :return: new state (deep copy) generated due to the attack
        """

        # copy board and change it's copy
        changed_board = Board(self.board_repr, self.turn, self.level)

        if changed_board.is_there_piece_at(row_current, column_current):
            piece = changed_board.get_piece_at(row_current, column_current)
            piece.attack_to(row_after_attack, column_after_attack)

        else:
            raise RuntimeError("Attacking piece do not exist")

        return changed_board

    def _does_any_piece_can_attack(self):
        """
        Defines if any piece can attack
        :return: true/false
        """
        for piece in self.get_pieces_of_color(self.turn):
            if piece.can_attack_anywhere():
                return True
        return False

    def next_level(self):
        """
        Changes deepness level in tree structure
        :return:
        """
        self.level += 1

    def next_turn(self):
        """
        Changes turn of current state
        :return: -
        """
        if self.turn == Color.BLACK:
            self.turn = Color.WHITE
        else:
            self.turn = Color.BLACK

    def __str__(self):
        result = "   "
        for i in range(8):
            result += f"{i} "
        result += "\n"

        row_count = 0
        for row in self.__board:
            result += f"{row_count}| "
            for piece in row:
                if piece is None:
                    result += "." + " "
                else:
                    result += f'{piece}' + " "
            result += "|" + "\n"
            row_count += 1
        return result
