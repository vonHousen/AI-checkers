from abc import abstractmethod, abstractproperty
from enum import Enum
from collections import namedtuple


class Color(Enum):
    WHITE = 0
    BLACK = 1


def is_allowed_cell_on_board(row, column):
    """
    We are playing only on black cells in checkers.
    This function return true if the cell is black and  0=< row,column <= 7

    :param row:
    :param column:
    :return:
    """
    if (row + column) % 2 is not 1:
        return False
    if row < 0 or row > 7:
        return False
    if column < 0 or column > 7:
        return False
    return True


class Piece:

    def can_move_anywhere(self):
        if self.list_possible_moves():
            return True
        return False

    def can_attack_anywhere(self):
        if self.list_possible_attacks():
            return True
        return False

    def _is_different_color_than(self, piece):
        if self.color != piece.color:
            return True
        return False

    @abstractproperty
    def color(self):
        pass

    @abstractmethod
    def list_possible_moves(self):
        pass

    @abstractmethod
    def list_possible_attacks(self):
        pass


class Man(Piece):
    def __init__(self, row, column, board):
        if not is_allowed_cell_on_board(row, column):
            raise ValueError("Not allowed board cell")
        self.row = row
        self.column = column
        self.board = board

    def list_possible_moves(self):
        """
        :return: list of all possible moves ( example: [(0,1), (0,3)] )
        """

        directions = self._possible_move_directions()
        return [(row, col) for row, col in directions if self._can_move_to(row, col)]

    def list_possible_attacks(self):
        """
        Note that function returns new positions of attacking piece not positions of piece being attacked!
        :return: list of all possible attacks ( example: [(0,1), (0,3)] )
        """

        directions = self._possible_attack_direction()
        return [(row, col) for row, col in directions if self._can_attack_to(row, col)]

    def _can_move_to(self, row_desired, column_desired):
        """
        The function calling this should take care about moving the piece in allowed direction
        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false
        """
        if abs(row_desired - self.row) != 1 or abs(column_desired - self.column) != 1:
            raise ValueError("Piece can be moved only diagonally")

        if not is_allowed_cell_on_board(row_desired, column_desired):
            return False

        if not self.board.is_empty(row_desired, column_desired):
            return False
        return True

    def _can_attack_to(self, row_desired, column_desired):
        """
        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false
        """

        if not is_allowed_cell_on_board(row_desired, column_desired):
            return False
        if not self.board.is_empty(row_desired, column_desired):
            return False

        row_attacked = (self.row + row_desired) // 2
        column_attacked = (self.column + column_desired) // 2

        piece_attacked = self.board.get_piece_at(row_attacked, column_attacked)

        if not piece_attacked:
            return False

        if not self._is_different_color_than(piece_attacked):
            return False

        return True

    @abstractmethod
    def _possible_move_directions(self):
        """Can't implement it here, because white can only move up, and black can only move down"""
        pass

    def _possible_attack_direction(self):
        Directions = namedtuple("Man_attack_directions", ["up_left", "up_right", "down_left", "down_right"])
        return Directions((self.row - 2, self.column - 2), (self.row - 2, self.column + 2),
                          (self.row + 2, self.column - 2), (self.row + 2, self.column + 2))


class BlackMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @property
    def color(self):
        return Color.BLACK

    def __str__(self):
        return "b"

    def _possible_move_directions(self):
        """Black are moving toward ascending row numbers"""
        Directions = namedtuple("Black_man_move_directions", ["down_left", "down_right"])
        return Directions((self.row + 1, self.column - 1), (self.row + 1, self.column + 1))


class WhiteMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @property
    def color(self):
        return Color.WHITE

    def __str__(self):
        return "w"

    def _possible_move_directions(self):
        """Black are moving toward ascending row numbers"""
        Directions = namedtuple("White_man_move_directions", ["up_left", "up_right"])
        return Directions((self.row - 1, self.column - 1), (self.row - 1, self.column + 1))


class King(Piece):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def can_move_to(self, row_desired, column_desired):
        """

        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false: can it move to desired location?
        """
        can_move_to = False  # TODO implement, decide if necessary

        return can_move_to

    def can_attack_to(self, row_attacked, column_attacked):
        """

        :param row_attacked: destination to attack
        :param column_attacked: destination to attack
        :return: true/false: can it attack it?
        """
        can_attack_it = False  # TODO implement, decide if necessary

        return can_attack_it


class WhiteKing(King):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "W"

    @property
    def color(self):
        return Color.WHITE


class BlackKing(King):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "B"

    @property
    def color(self):
        return Color.BLACK
