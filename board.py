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
                                   )):
        """
        :type board_repr: Memory optimized representation of board
        """
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
            if piece.get_representation() == 0x0000000a:        # isinstance(piece, BlackMan):
                result -= 1.0
            elif piece.get_representation() == 0x0000000b:      # isinstance(piece, BlackKing):
                result -= 1.6
            elif piece.get_representation() == 0x00000002:      # isinstance(piece, WhiteMan):
                result += 1.0
            elif piece.get_representation() == 0x00000003:      # isinstance(piece, WhiteKing):
                result += 1.6
        return result

    def is_there_piece_at(self, row, column):
        if self.__board[row][column] is None:
            return False
        return True

    def get_piece_at(self, row, column):
        return self.__board[row][column]

    def delete_piece_at(self, row, column):
        (self.__board[row][column]) = None

    def set_piece_at(self, row, column, piece):
        (self.__board[row][column]) = piece

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
