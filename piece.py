from abc import abstractmethod
from enum import Enum
from collections import namedtuple


class Color(Enum):
    WHITE = 0
    BLACK = 1


def is_allowed_cell_on_board(row, column):
    """
    We are playing only on black cells in checkers.
    This function return true if the cell is black and  0< row,column <= 8

    :param row:
    :param column:
    :return:
    """
    if (row + column) % 2 is not 1:
        return False
    if row < 0 or row > 8:
        return False
    if column < 0 or column > 8:
        return False
    return True


class Piece:

    def can_move_anywhere(self):
        if self.possible_moves():
            return True
        return False

    def can_attack_anywhere(self):
        if self.possible_attacks():
            return True
        return False

    def is_different_color_than(self, piece):
        if self.color != piece.color:
            pass

    @abstractmethod
    def possible_attacks(self):
        pass

    @abstractmethod
    def possible_moves(self):
        pass

    @abstractmethod
    @property
    def color(self):
        pass


class Man(Piece):
    def __init__(self, row, column, board):
        if not is_allowed_cell_on_board(row, column):
            raise ValueError("Not allowed board cell")
        self.row = row
        self.column = column
        self.board = board

    def __can_move_to(self, row_desired, column_desired):
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

    def __can_attack_to(self, row_desired, column_desired):
        """
        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false
        """

        if not self.board.is_empty(row_desired, column_desired):
            return False

        if not is_allowed_cell_on_board(row_desired, column_desired):
            return False

        row_attacked = (self.row + row_desired) / 2
        column_attacked = (self.column + column_desired) / 2

        piece_attacked = self.board.get_piece_at(row_attacked, column_attacked)

        if not piece_attacked:
            return False

        if not self.is_different_color_than(piece_attacked):
            return False

        return True

    def list_possible_moves(self):
        """
        :return: list of all possible moves ( example: [(0,1), (0,3)] )
        """

        directions = self.possible_move_directions()
        return [(row, col) for row, col in directions if self.__can_move_to(col, row)]

    def list_possible_attacks(self):
        """
        Note that function returns new positions of attacking piece not positions of piece being attacked!
        :return: list of all possible attacks ( example: [(0,1), (0,3)] )
        """

        directions = self.possible_move_directions()
        return [(row, col) for row, col in directions if self.__can_attack_to(col, row)]

    @abstractmethod
    def possible_move_directions(self):
        pass

    def possible_attack_direction(self):
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

    def possible_move_directions(self):
        """Black are moving toward ascending row numbers"""
        Directions = namedtuple("Black man move directions", ["down_left", "down_right"])
        return Directions((self.row + 1, self.column - 1), (self.row + 1, self.column + 1))


class WhiteMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @property
    def color(self):
        return Color.WHITE

    def __str__(self):
        return "w"

    def possible_move_directions(self):
        """Black are moving toward ascending row numbers"""
        Directions = namedtuple("White man move directions", ["up_left", "up_right"])
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

    @staticmethod
    @abstractmethod
    def get_colour():
        pass


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
