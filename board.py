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

    def get_pieces_of_color(self, color):
        """
        :return: List of pieces on the board of specific color
        """
        return [piece for row in self.__board for piece in row if (piece is not None and piece.color == color)]

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


def test_repr_gen():
    print("Test board repr generation:")
    board = Board()
    print(board)
    for row_repr in board.board_repr:
        print(hex(row_repr))
    print()
    board2 = Board(board.board_repr)
    print(board2)


def test_man_moves():
    print("Test man moves:")
    board = Board()
    print(board)
    for piece in board.pieces:
        moves = piece.possible_moves
        if moves:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(moves)


def test_man_attacks():
    print("Test man attacks")
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
        possible_attacks_list = piece.possible_attacks
        if possible_attacks_list:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(possible_attacks_list)


def test_king_moves():
    print("Test king moves")
    board_repr = (0x88888888,
                  0x88888888,
                  0x88888888,
                  0x8888b888,
                  0x88838888,
                  0x88888888,
                  0x88888888,
                  0x88888888
                  )
    board = Board(board_repr)
    print(board)

    for piece in board.pieces:
        possible_moves_list = piece.possible_moves
        if possible_moves_list:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(possible_moves_list)
            # for row, col in possible_moves_list:
            #     piece.board.set_piece_at(row, col, "x")
    piece = board.pieces[0]
    row, col = piece.possible_moves[0]
    piece.move_to(row , col)
    print(board)


def test_king_attacks():
    print("Test king attacks")
    board_repr = (0x88888888,
                  0x88888888,
                  0x88888888,
                  0x8888b888,
                  0x88838888,
                  0x88888838,
                  0x82888888,
                  0x88888888
                  )
    board = Board(board_repr)
    print(board)

    for piece in board.pieces:
        possible_moves_list = piece.possible_attacks
        if possible_moves_list:
            print(f"{piece}({piece.row},{piece.column}) -> ", end="")
            print(possible_moves_list)
    piece = board.pieces[0]
    row, col = piece.possible_attacks[0]
    piece.attack_to(row, col)
    print(board)


def test_replace_with_king():
    print("Test replace with king")
    board_repr = (0x82828a8a,
                  0xa8a8a8a8,
                  0x8a8a8a8a,
                  0x88288888,
                  0x88888a88,
                  0x28282828,
                  0x82828282,
                  0x28a828a8
                  )
    board = Board(board_repr)
    print(board)
    for piece in board.pieces:
        if piece.can_be_replaced_with_king():
            piece.replace_with_king()

    print(board)


if __name__ == '__main__':
    test_repr_gen()
    test_man_moves()
    test_man_attacks()
    test_king_moves()
    test_king_attacks()
    test_replace_with_king()
