from abc import ABC, abstractmethod
from enum import Enum


class Turn(Enum):
    WHITE = 0
    BLACK = 1

# TODO create new Enum for colours and refactor code


class Piece(ABC):

    @staticmethod
    @abstractmethod
    def get_colour():
        """

        :return: piece's colour
        """
        pass


class Man(Piece):
    def __init__(self, row, column, board):
        # if (row + column) % 2 is not 1:
        #     raise ValueError("Not allowed board cell")
        self.row = row
        self.column = column
        self.board = board

    def can_move(self):
        """

        :return: true/false: can it move at all?
        """
        can_move = False        # TODO implement, decide if necessary

        return can_move

    def can_attack(self):
        """

        :return: true/false: can it attack at all?
        """
        can_attack = False      # TODO implement - used as interface

        return can_attack

    def possible_attacks(self):
        """

        :return: count of possible attacks to be done by given piece
        """
        attack_count = 0        # TODO implement, decide if necessary

        return attack_count

    def possible_moves(self):
        """

        :return: count of possible moves to be done by given piece
        """
        moves_count = 0     # TODO implement, decide if necessary

        return moves_count

    def can_move_to(self, row_desired, column_desired):
        """

        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false: can it move to desired location?
        """
        can_move_to = False     # TODO implement, decide if necessary

        return can_move_to

    def can_attack_it(self, row_attacked, column_attacked):
        """

        :param row_attacked: destination to attack
        :param column_attacked: destination to attack
        :return: true/false: can it attack it?
        """
        can_attack_it = False    # TODO implement, decide if necessary

        return can_attack_it

    @staticmethod
    @abstractmethod
    def get_colour():
        pass

    @abstractmethod
    def list_possible_moves(self):
        """

        :return: list of all possible moves ( example: [[0,1], [0,3]] )
        """
        pass

    def list_possible_attacks(self):
        """

        :return: list of all possible attacks ( example: [[0,1], [0,3]] )
        """
        list_of_attacks = []

        if self.can_attack_it(self.row + 1, self.column - 1):
            list_of_attacks.append([self.row + 1, self.column - 1])

        if self.can_attack_it(self.row + 1, self.column + 1):
            list_of_attacks.append([self.row + 1, self.column + 1])

        # attacking backwards allowed
        if self.can_attack_it(self.row - 1, self.column - 1):
            list_of_attacks.append([self.row - 1, self.column - 1])

        if self.can_attack_it(self.row - 1, self.column + 1):
            list_of_attacks.append([self.row - 1, self.column + 1])

        return list_of_attacks


class BlackMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @staticmethod
    def get_colour():
        return Turn.BLACK

    def __str__(self):
        return "b"

    def list_possible_moves(self):
        """

        :return: list of all possible moves ( example: [[0,1], [0,3]] )
        """
        list_of_moves = []

        if self.can_move_to(self.row + 1, self.column - 1):
            list_of_moves.append([self.row + 1, self.column - 1])

        if self.can_move_to(self.row + 1, self.column + 1):
            list_of_moves.append([self.row + 1, self.column + 1])

        return list_of_moves


class WhiteMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    @staticmethod
    def get_colour():
        return Turn.WHITE

    def __str__(self):
        return "w"

    def list_possible_moves(self):
        """

        :return: list of all possible moves ( example: [[0,1], [0,3]] )
        """
        list_of_moves = []

        if self.can_attack_it(self.row - 1, self.column - 1):
            list_of_moves.append([self.row - 1, self.column - 1])

        if self.can_attack_it(self.row - 1, self.column + 1):
            list_of_moves.append([self.row - 1, self.column + 1])

        return list_of_moves


class King(Piece):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def can_move(self):
        """

        :return: true/false: can it move at all?
        """
        can_move = False        # TODO implement, decide if necessary

        return can_move

    def can_attack(self):
        """

        :return: true/false: can it attack at all?
        """
        can_attack = False      # TODO implement - used as interface

        return can_attack

    def possible_attacks(self):
        """

        :return: count of possible attacks to be done by given piece
        """
        attack_count = 0        # TODO implement, decide if necessary

        return attack_count

    def possible_moves(self):
        """

        :return: count of possible moves to be done by given piece
        """
        moves_count = 0     # TODO implement, decide if necessary

        return moves_count

    def can_move_to(self, row_desired, column_desired):
        """

        :param row_desired: destination to move
        :param column_desired: destination to move
        :return: true/false: can it move to desired location?
        """
        can_move_to = False     # TODO implement, decide if necessary

        return can_move_to

    def can_attack_it(self, row_attacked, column_attacked):
        """

        :param row_attacked: destination to attack
        :param column_attacked: destination to attack
        :return: true/false: can it attack it?
        """
        can_attack_it = False    # TODO implement, decide if necessary

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

    @staticmethod
    def get_colour():
        return Turn.WHITE


class BlackKing(King):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "B"

    @staticmethod
    def get_colour():
        return Turn.BLACK

