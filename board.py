from piece import *


class Board:
    def __init__(self):
        self.board = ["halo"]
        self.board = [[None, BlackMan(1, 2, self), None, BlackMan(1, 4, self), None, BlackMan(1, 6, self), None,
                       BlackMan(1, 8, self)],
                      [BlackMan(2, 1, self), None, BlackMan(2, 3, self), None, BlackMan(2, 5, self), None,
                       BlackMan(2, 7, self), None],
                      [None, BlackMan(3, 2, self), None, BlackMan(3, 4, self), None, BlackMan(3, 6, self), None,
                       BlackMan(3, 8, self)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [WhiteMan(6, 1, self), None, WhiteMan(6, 3, self), None, WhiteMan(6, 5, self), None,
                       WhiteMan(6, 7, self), None],
                      [None, WhiteMan(7, 2, self), None, WhiteMan(7, 4, self), None, WhiteMan(7, 6, self), None,
                       WhiteMan(7, 8, self)],
                      [WhiteMan(8, 1, self), None, WhiteMan(8, 3, self), None, WhiteMan(8, 5, self), None,
                       WhiteMan(8, 7, self), None]
                      ]

    @property
    def pieces(self):
        # ta linia robi to co 6 wykomentowanych linii na dole, witamy w pythonie
        return [piece for row in self.board for piece in row if piece is not None]

        # pieces = []
        # for row in self.board:
        #     for piece in row:
        #         if piece is not None:
        #             pieces.append(piece)
        # return pieces

    @property
    def balance(self):
        result = 0
        for piece in self.pieces:
            if isinstance(piece, BlackMan):
                result += 1
            if isinstance(piece, BlackKing):
                result += 1.6
            if isinstance(piece, WhiteMan):
                result -= 1
            if isinstance(piece, WhiteKing):
                result -= 1.6
        return result

    def __str__(self):
        result = ""
        for row in self.board:
            for piece in row:
                if piece is None:
                    result += "-"
                else:
                    result += f'{piece}'
            result += "\n"
        return result


def main():
    board = Board()
    print(board)


if __name__ == '__main__':
    main()
