from piece import *


class Board:

    def __init__(self, board_repr):
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
                if isinstance(piece, WhiteMan):
                    board[rowNumber] |= 0x00000002
                elif isinstance(piece, WhiteKing):
                    board[rowNumber] |= 0x00000003
                elif isinstance(piece, BlackMan):
                    board[rowNumber] |= 0x0000000a
                elif isinstance(piece, BlackKing):
                    board[rowNumber] |= 0x0000000b
                else:
                    board[rowNumber] |= 0x00000008
                if columnNumber != 7:
                    board[rowNumber] = board[rowNumber] << 4
        return tuple(board)

    @property
    def pieces(self):
        """
        :return: List of pieces on the board
        """
        return [piece for row in self.__board for piece in row if piece is not None]

    def get_pieces_of_colour(self, colour):
        """
        :return: List of pieces on the board of specific colour
        """
        return [piece for row in self.__board for piece in row if (piece is not None and piece.colour == colour)]

    @property
    def balance(self):
        """
        :return: Positive balance means white is winning
        """
        result = 0
        for piece in self.pieces:
            if isinstance(piece, BlackMan):
                result -= 1
            elif isinstance(piece, BlackKing):
                result -= 1.6
            elif isinstance(piece, WhiteMan):
                result += 1
            elif isinstance(piece, WhiteKing):
                result += 1.6
        return result

    def is_empty(self, row, column):
        if self.__board[row][column] is None:
            return True
        return False

    def get_piece_at(self, row, column):
        return self.__board[row][column]

    def __str__(self):
        result = ""
        for row in self.__board:

            result += "| "
            for piece in row:
                if piece is None:
                    result += "." + " "
                else:
                    result += f'{piece}' + " "
            result += "|" + "\n"
        return result


def test_repr_gen():
    board_repr = (0x8a8a8a8a,
                  0xa8a8a8a8,
                  0x8a8a8a8a,
                  0x88888888,
                  0x88888888,
                  0x28282828,
                  0x82828282,
                  0x28282828
                  )
    board = Board(board_repr)
    print(board)
    for row_repr in board.board_repr:
        print(hex(row_repr))
    print()
    board2 = Board(board.board_repr)
    print(board2)


if __name__ == '__main__':
    test_repr_gen()
