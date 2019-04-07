from abc import abstractmethod, ABC
from enum import Enum


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


class Piece(ABC):
    def __init__(self, row, column, board):
        if not is_allowed_cell_on_board(row, column):
            raise ValueError("Not allowed board cell")
        self.row = row
        self.column = column
        self.board = board

    def can_move_anywhere(self):
        if self.possible_moves:
            return True
        return False

    def can_attack_anywhere(self):
        if self.possible_attacks:
            return True
        return False

    @property
    @abstractmethod
    def color(self):
        pass

    @property
    def possible_moves(self):
        """
        :return: list of all possible moves ( example: [(0,1), (0,3)] ) - moves are tuples (row,column)
        """
        potential = self._potential_moves()
        return [(row, col) for row, col in potential if self._can_move_to(row, col)]

    @property
    def possible_attacks(self):
        """
        Note that function returns positions of piece after performing an attack!
        :return: list of all possible attacks ( example: [(0,1), (0,3)] ) - attacks are tuples (row,column)
        """
        potential = self._potential_attacks()
        return [(row, col) for row, col in potential if self._can_attack_to(row, col)]

    def move_to(self, row_desired, column_desired):
        if not self._can_move_to(row_desired, column_desired):
            raise ValueError("Movement not allowed")
        self._move_unsafely_to(row_desired, column_desired)

    def attack_to(self, row_desired, column_desired):
        if not self._can_attack_to(row_desired, column_desired):
            raise ValueError("Attack not allowed")

        between_cells = self._get_cells_on_the_way_to(row_desired, column_desired)

        piece = None
        for row, column in between_cells:
            if self.board.is_there_piece_at(row, column):
                piece = self.board.get_piece_at(row, column)

        if piece is None:
            raise RuntimeError("Redundancy check: this should never happen")  # it was already checked by _can_attack_to
        row_attacked = piece.row
        column_attacked = piece.column

        self._move_unsafely_to(row_desired, column_desired)
        self.board.delete_piece_at(row_attacked, column_attacked)

    def _move_unsafely_to(self, row_desired, column_desired):

        self.board.delete_piece_at(self.row, self.column)
        self.board.set_piece_at(row_desired, column_desired, self)

        self.row = row_desired
        self.column = column_desired

    def _is_different_color_than(self, piece):
        if self.color != piece.color:
            return True
        return False

    def _can_move_to(self, row_desired, column_desired):
        """
                Checks if man can move to desired place, it checks if its allowed move and if the place is on the board
                :param row_desired: destination to move
                :param column_desired: destination to move
                :return: true/false
                """
        if (row_desired, column_desired) not in self._potential_moves():
            raise ValueError("This piece can't be moved in this direction")

        if not is_allowed_cell_on_board(row_desired, column_desired):
            return False

        if self.board.is_there_piece_at(row_desired, column_desired):
            return False

        between_cells = self._get_cells_on_the_way_to(row_desired, column_desired)

        for row, column in between_cells:
            if self.board.is_there_piece_at(row, column):
                return False
        return True

    def _can_attack_to(self, row_desired, column_desired):
        """
        :param row_desired: location after an attack
        :param column_desired: location after an attack
        :return: true/false
        """
        if (row_desired, column_desired) not in self._potential_attacks():
            raise ValueError("This piece can't be attack in this direction")

        if not is_allowed_cell_on_board(row_desired, column_desired):
            return False

        if self.board.is_there_piece_at(row_desired, column_desired):
            return False

        between_cells = self._get_cells_on_the_way_to(row_desired, column_desired)

        piece = None
        for row, column in between_cells:
            if self.board.is_there_piece_at(row, column):
                if piece is not None:  # more than one piece between
                    return False
                piece = self.board.get_piece_at(row, column)
                if not self._is_different_color_than(piece):  # if is the same color
                    return False
        if piece is None:  # there isn't any piece to attack
            return False
        return True

    def _get_cells_on_the_way_to(self, row_desired, column_desired):
        if self.row < row_desired:
            delta_row = 1
        else:
            delta_row = -1
        if self.column < column_desired:
            delta_column = 1
        else:
            delta_column = -1

        result = []

        row = self.row + delta_row
        column = self.column + delta_column

        while row != row_desired:
            result.append((row, column))
            column += delta_column
            row += delta_row

        return result

    @abstractmethod
    def _potential_moves(self):
        pass

    @abstractmethod
    def _potential_attacks(self):
        pass


class Man(Piece, ABC):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @abstractmethod
    def can_be_replaced_with_king(self):
        pass

    def replace_with_king(self):
        board = self.board
        row = self.row
        column = self.column
        board.delete_piece_at(row, column)
        if isinstance(self, WhiteMan):
            king = WhiteKing(row, column, board)
        elif isinstance(self, BlackMan):
            king = BlackKing(row, column, board)
        else:
            raise RuntimeError("What: Replacing not Man object with King?")
        board.set_piece_at(row, column, king)
        pass

    @abstractmethod
    def _potential_moves(self):
        """Can't implement it here, because white can only move up, and black can only move down"""
        pass

    def _potential_attacks(self):
        return [(self.row - 2, self.column - 2), (self.row - 2, self.column + 2),
                (self.row + 2, self.column - 2), (self.row + 2, self.column + 2)]


class BlackMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "b"

    @property
    def color(self):
        return Color.BLACK

    def can_be_replaced_with_king(self):
        if self.row is 7:
            return True
        return False

    def _potential_moves(self):
        """Black are moving toward ascending row numbers"""
        return [(self.row + 1, self.column - 1), (self.row + 1, self.column + 1)]


class WhiteMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "w"

    @property
    def color(self):
        return Color.WHITE

    def can_be_replaced_with_king(self):
        if self.row is 0:
            return True
        return False

    def _potential_moves(self):
        """Black are moving toward ascending row numbers"""
        return [(self.row - 1, self.column - 1), (self.row - 1, self.column + 1)]


class King(Piece, ABC):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def _potential_attacks(self):
        result = []
        for i in (2, 3, 4, 5, 6, 7):
            for row, col in [(i, i), (i, -i), (-i, i), (-i, -i)]:
                result.append((self.row + row, self.column + col))
        return result

    def _potential_moves(self):
        result = []
        for i in (1, 2, 3, 4, 5, 6, 7):
            for row, col in [(i, i), (i, -i), (-i, i), (-i, -i)]:
                result.append((self.row + row, self.column + col))
        return result


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
