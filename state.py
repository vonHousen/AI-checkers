from board import *


class State:

    def __init__(self, board):
        self.turn = board.turn
        # 8 not allowed or empty
        # 2 white man
        # 3 white king
        # a black man
        # b black king
        # self.board_repr = board.board_repr
        self.level = board.level
        self.is_terminal = board.did_game_end()
        self._cached_board = board

        self.next_move = None
        self._value = None

    def hash(self):
        result = ""
        board_repr = self._cached_board.board_repr
        for rowNumber, row in enumerate(board_repr):
            mask = 0xF0000000
            for columnNumber in range(8):
                piece = row & mask
                if piece == 0x80000000:  # empty or not allowed
                    result += "e"
                elif piece == 0x20000000:  # white man
                    result += "a"
                elif piece == 0xa0000000:  # black man
                    result += "b"
                elif piece == 0x30000000:  # white king
                    result += "c"
                elif piece == 0xb0000000:  # black king
                    result += "d"
                row = row << 4

        if self.turn is Color.WHITE:
            result += "a"
        else:
            result += "b"

        result += str(self.level)

        return result

    def reset_level(self):
        self.level = 0
        if self._cached_board is not None:
            self._cached_board.level = 0

    @property
    def next_states(self):
        boards = self._board.get_next_boards()
        result = []
        for board in boards:
            new_state = State(board)
            result.append(new_state)
        return result

    @property
    def balance(self):
        if self.is_terminal:
            if self.turn is Color.WHITE:  # black wins
                return -1000
            else:  # white wins
                return 1000

        if self._value is None:
            self._value = self._board.balance
        return self._value

    @property
    def _board(self):
        """
        Cache new Board object (using stored representation) if it doesn't exist
        :return: Cached or just created Board object
        """
        return self._cached_board
        # if self._cached_board is None:
        #     self._cached_board = Board(self.board_repr, self.turn)
        # return self._cached_board

    def clean_cached_board(self):
        self._cached_board = None

    def __str__(self):
        printout = ""
        printout += "Turn = " + f'{self.turn}'
        printout += "   Balance = " + f'{self._board.balance}'
        if self._board.balance < 0:
            printout += "(black is winning)"
        elif self._board.balance > 0:
            printout += "(white is winning)"
        printout += "   Depth_level = " + f'{self.level}' + "\n"
        printout += self._board.__str__()

        return printout
