from abc import abstractmethod
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
        if self.possible_moves():
            return True
        return False

    def can_attack_anywhere(self):
        if self.possible_attacks():
            return True
        return False

    @property
    @abstractmethod
    def color(self):
        pass

    @abstractmethod
    def possible_moves(self):
        """
        :return: list of all possible moves ( example: [(0,1), (0,3)] ) - moves are tuples (row,column)
        """
        pass

    @abstractmethod
    def possible_attacks(self):
        """
        Note that function returns positions of piece after performing an attack!
        :return: list of all possible attacks ( example: [(0,1), (0,3)] ) - attacks are tuples (row,column)
        """
        pass

    @abstractmethod
    def move_to(self, row_desired, column_desired):
        pass

    @abstractmethod
    def attack_to(self, row_after_attack, column_after_attack):
        pass

    def _is_different_color_than(self, piece):
        if self.color != piece.color:
            return True
        return False


class Man(Piece):
    def __init__(self, row, column, board):
        if not is_allowed_cell_on_board(row, column):
            raise ValueError("Not allowed board cell")
        self.row = row
        self.column = column
        self.board = board

    def possible_moves(self):

        directions = self._potential_moves()
        return [(row, col) for row, col in directions if self._can_move_to(row, col)]

    def possible_attacks(self):

        directions = self._potential_attacks()
        return [(row, col) for row, col in directions if self._can_attack_to(row, col)]

    def move_to(self, row_desired, column_desired):

        if not self._can_move_to(row_desired, column_desired):
            raise RuntimeError("Movement not allowed")

        else:
            self.board.delete_piece_at(self.row, self.column)
            self.board.set_piece_at(row_desired, column_desired, self)

            self.row = row_desired
            self.column = column_desired

    def _move_unsafely_to(self, row_desired, column_desired):

        if not is_allowed_cell_on_board(row_desired, column_desired) \
                or self.board.is_there_piece_at(row_desired, column_desired):
            raise RuntimeError("Movement during an attack not allowed")

        else:
            self.board.delete_piece_at(self.row, self.column)
            self.board.set_piece_at(row_desired, column_desired, self)

            self.row = row_desired
            self.column = column_desired

    def attack_to(self, row_after_attack, column_after_attack):

        row_attacked = (row_after_attack + self.row) // 2
        column_attacked = (column_after_attack + self.column) // 2

        if not self._can_attack_to(row_after_attack, column_after_attack):
            raise RuntimeError("Attack not allowed")

        else:
            self._move_unsafely_to(row_after_attack, column_after_attack)
            self.board.delete_piece_at(row_attacked, column_attacked)

    def _can_move_to(self, row_desired, column_desired):
        """
        Checks if man can move to desired place, it checks if its allowed move and if the place is on the board
        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false
        """
        if abs(row_desired - self.row) != 1 or abs(column_desired - self.column) != 1:
            raise ValueError("Piece can be moved only diagonally by 1 cell")

        if (row_desired, column_desired) not in self._potential_moves():
            raise ValueError("This piece can't be moved in this direction")

        if not is_allowed_cell_on_board(row_desired, column_desired):
            return False

        if not self.board.is_there_piece_at(row_desired, column_desired):
            return False
        return True

    def _can_attack_to(self, row_after_attack, column_after_attack):
        """
        :param row_after_attack: location after an attack
        :param column_after_attack: location after an attack
        :return: true/false
        """

        if not is_allowed_cell_on_board(row_after_attack, column_after_attack):
            return False
        if self.board.is_there_piece_at(row_after_attack, column_after_attack):
            return False

        row_attacked = (row_after_attack + self.row) // 2
        column_attacked = (column_after_attack + self.column) // 2

        piece_we_attack = self.board.get_piece_at(row_attacked, column_attacked)

        if not piece_we_attack:
            return False

        if not self._is_different_color_than(piece_we_attack):
            return False

        return True

    @abstractmethod
    def _potential_moves(self):
        """Can't implement it here, because white can only move up, and black can only move down"""
        pass

    def _potential_attacks(self):
        Potential_attacks = namedtuple("Man_potential_attacks", ["up_left", "up_right", "down_left", "down_right"])
        return Potential_attacks((self.row - 2, self.column - 2), (self.row - 2, self.column + 2),
                                 (self.row + 2, self.column - 2), (self.row + 2, self.column + 2))


class BlackMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @property
    def color(self):
        return Color.BLACK

    def __str__(self):
        return "b"

    def _potential_moves(self):
        """Black are moving toward ascending row numbers"""
        Moves = namedtuple("Black_man_potential_moves", ["down_left", "down_right"])
        return Moves((self.row + 1, self.column - 1), (self.row + 1, self.column + 1))


class WhiteMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @property
    def color(self):
        return Color.WHITE

    def __str__(self):
        return "w"

    def _potential_moves(self):
        """Black are moving toward ascending row numbers"""
        Potential_moves = namedtuple("White_man_potential_moves", ["up_left", "up_right"])
        return Potential_moves((self.row - 1, self.column - 1), (self.row - 1, self.column + 1))


class King(Piece):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def _can_move_to(self, row_desired, column_desired):
        """
        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false: can it move to desired location?
        """
        can_move_to = False  # TODO implement, decide if necessary

        return can_move_to

    def _can_attack_it(self, row_attacked, column_attacked):
        """
        :param row_attacked: destination to attack
        :param column_attacked: destination to attack
        :return: true/false: can it attack to?
        """
        can_attack_it = False  # TODO implement, decide if necessary

        return can_attack_it

    def possible_attacks(self):
        pass

    def possible_moves(self):
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
