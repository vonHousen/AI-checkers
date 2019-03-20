class Piece:
    pass


class Man(Piece):
    def __init__(self, row, column, board):
        if (row + column) % 2 is not 1:
            raise ValueError("Not allowed board cell")
        self.row = row
        self.column = column
        self.board = board


class BlackMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "b"


class WhiteMan(Man):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "w"


class King(Piece):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)


class WhiteKing(King):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "W"


class BlackKing(King):
    def __init__(self, row, column, board):
        super().__init__(row, column, board)

    def __str__(self):
        return "B"
